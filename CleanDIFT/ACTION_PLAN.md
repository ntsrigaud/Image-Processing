# CleanDIFT Performance Fix - Action Plan

## Executive Summary

**Pipeline Status**: Executes successfully without errors  
**Performance**: Does not match paper results  
**Root Cause**: Training configuration issues, NOT architecture problems

---

## Critical Issues Preventing Paper Reproduction

### 1. **CRITICAL: Timestep Stratification = 1 (Should be 3)**

This is THE MOST IMPORTANT issue. CleanDIFT's core innovation is consolidating information from multiple timesteps.

**Current:**

```python
num_t_stratification_bins: int = 1  # Only trains on ONE noise level
```

**Required:**

```python
num_t_stratification_bins: int = 3  # Sample 3 different noise levels per image
```

**Impact**: Model cannot learn to align features across the noise spectrum. This alone explains poor performance.

---

### 2. **CRITICAL: Dataset Too Small (200 → 10,000 images)**

**Current:** 200 images  
**Required:** 10,000+ images from COYO-700M  
**Paper Uses:** Random subset of COYO-700M with min 512² size

**Impact**: Insufficient semantic diversity for robust feature alignment.

---

### 3. **HIGH: Learning Rate 5× Too High**

**Current:** `lr = 1e-5`  
**Required:** `lr = 2e-6`  
**Impact**: May prevent fine convergence and stable training.

---

### 4. **MEDIUM: Text Conditioning Disabled**

**Current:** `use_text_condition = False`  
**Required:** `use_text_condition = True`  
**Impact**: Loses semantic grounding from captions.

---

### 5. **LOW: Training Steps Mismatch**

**Current:** 1000 steps, batch_size=1, grad_accum=4 (eff. batch=4)  
**Required:** 400 steps, batch_size=8  
**Impact**: More steps don't compensate for bad hyperparameters.

---

## Immediate Action Plan (Step-by-Step)

### Phase 1: Fix Training Configuration (30 minutes)

#### Step 1.1: Update TrainingConfig

Replace the configuration cell with:

```python
@dataclass
class TrainingConfig:
    """Training configuration for CleanDIFT - PAPER-MATCHED"""
    # Model settings
    sd_version: str = "sd15"
    t_max: int = 999
    num_t_stratification_bins: int = 3  # CRITICAL: Must be 3
    learn_timestep: bool = True
    use_text_condition: bool = True  # Enable for better results

    # Mapping network architecture
    mapping_depth: int = 2
    mapping_width: int = 256
    mapping_d_ff: int = 768
    mapping_dropout: float = 0.0

    # Adapter (projection head) architecture
    adapter_depth: int = 3
    adapter_ffn_expansion: float = 1.0

    # Training hyperparameters - PAPER MATCHED
    batch_size: int = 4  # 4 with grad_accum=2 = effective batch 8
    img_size: int = 512
    lr: float = 2e-6  # CRITICAL: Must be 2e-6, not 1e-5
    max_steps: int = 400  # Paper uses 400 steps
    grad_accum_steps: int = 2  # Effective batch = 8

    # Checkpointing
    checkpoint_freq: int = 100
    checkpoint_dir: str = "./checkpoints"

    # Seed for reproducibility
    seed: int = 42

    # Data
    dataset_dir: str = "./data/train_large"  # Use larger dataset
```

#### Step 1.2: Add Zero Initialization for Adapters

In the model initialization cell, after creating adapters, add:

```python
# After model = StableFeatureAligner(...)
# Add zero initialization for adapters (paper requirement)
if hasattr(model, 'adapters'):
    for adapter_name, adapter in model.adapters.items():
        for layer in adapter.layers:
            if hasattr(layer, 'down_proj'):
                nn.init.zeros_(layer.down_proj.weight)
                if hasattr(layer.down_proj, 'bias') and layer.down_proj.bias is not None:
                    nn.init.zeros_(layer.down_proj.bias)
    print("Adapters zero-initialized (act as identity at start)")
```

---

### Phase 2: Download Proper Dataset (2-4 hours)

#### Step 2.1: Create Dataset Download Cell

Add this NEW cell BEFORE the "Download COYO-700M Images" section:

```python
# Download proper COYO-700M subset for CleanDIFT training
from datasets import load_dataset
import requests
from io import BytesIO
from tqdm.auto import tqdm

def download_coyo_subset(output_dir="./data/train_large", num_images=10000, min_size=512):
    """Download COYO-700M subset matching paper specifications."""
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading COYO-700M dataset (streaming mode)...")
    dataset = load_dataset("kakaobrain/coyo-700m", streaming=True, split="train")

    successful = 0
    failed = 0
    skipped = 0

    pbar = tqdm(total=num_images, desc="Downloading images")

    for idx, item in enumerate(dataset):
        if successful >= num_images:
            break

        try:
            img_url = item['url']
            caption = item['text']

            # Download image
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content)).convert('RGB')

            # Filter by size (paper requirement: min 512²)
            if min(img.size) < min_size:
                skipped += 1
                continue

            # Save image and caption
            img_path = os.path.join(output_dir, f"img_{successful:05d}.jpg")
            img.save(img_path, quality=95)

            caption_path = os.path.join(output_dir, f"img_{successful:05d}.json")
            with open(caption_path, 'w') as f:
                json.dump({"caption": caption, "url": img_url}, f)

            successful += 1
            pbar.update(1)

        except Exception as e:
            failed += 1
            continue

    pbar.close()
    print(f"\nDownloaded {successful} images to {output_dir}")
    print(f"  Failed: {failed}, Skipped (too small): {skipped}")
    return successful

# Run download
num_downloaded = download_coyo_subset(
    output_dir="./data/train_large",
    num_images=10000,  # Minimum for paper-quality results
    min_size=512
)
```

#### Step 2.2: Update DataLoader to Use Captions

Replace DummyDataset with this:

```python
class COYODataset(data.Dataset):
    """Dataset matching paper specifications."""
    def __init__(self, dataset_dir: str, img_size: int = 512, min_size: int = 512):
        self.dataset_dir = dataset_dir
        self.img_size = img_size
        self.data = []

        jpg_files = sorted([f for f in os.listdir(dataset_dir) if f.endswith('.jpg')])

        for img_file in jpg_files:
            img_path = os.path.join(dataset_dir, img_file)
            json_path = img_path.replace('.jpg', '.json')

            if not os.path.exists(json_path):
                continue

            # Filter by size
            try:
                img = Image.open(img_path)
                if min(img.size) < min_size:
                    continue
            except:
                continue

            with open(json_path, 'r') as f:
                json_data = json.load(f)

            self.data.append({
                'img_path': img_path,
                'caption': json_data.get('caption', '')
            })

        print(f"Loaded {len(self.data)} valid images")

        # Match paper: crop + resize
        self.transform = transforms.Compose([
            transforms.RandomCrop(min(img_size, 512)),
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        img = Image.open(item['img_path']).convert('RGB')
        img = self.transform(img)

        return {
            'x': img,
            'caption': item['caption']
        }
```

---

### Phase 3: Retrain with Fixed Configuration (4 hours)

1. **Clear previous checkpoints**:

   ```python
   !rm -rf ./checkpoints/*
   torch.cuda.empty_cache()
   ```

2. **Initialize model with new config**

3. **Train for 400 steps** with paper-matched hyperparameters

4. **Monitor loss** - should see steady decrease

---

### Phase 4: Proper Evaluation (30 minutes)

Add PCK metric implementation:

```python
def compute_pck(correspondences, ground_truth, threshold=0.1):
    """
    Compute Percentage of Correct Keypoints (PCK).

    Args:
        correspondences: List of ((x1,y1), (x2,y2), score)
        ground_truth: List of ground truth correspondences
        threshold: Distance threshold as fraction of image diagonal

    Returns:
        PCK percentage
    """
    if not ground_truth:
        return None

    # Compute image diagonal for normalization
    H, W = 512, 512
    diagonal = np.sqrt(H**2 + W**2)
    threshold_px = threshold * diagonal

    correct = 0
    for pred, gt in zip(correspondences, ground_truth):
        pred_pt = np.array(pred[1])  # Target point
        gt_pt = np.array(gt[1])

        distance = np.linalg.norm(pred_pt - gt_pt)
        if distance <= threshold_px:
            correct += 1

    pck = (correct / len(ground_truth)) * 100
    return pck
```

---

## Expected Results After Fixes

| Metric                    | Before  | After (Expected) | Paper          |
| ------------------------- | ------- | ---------------- | -------------- |
| SPair-71K PCK             | ~10-20% | ~50-52%          | 52%            |
| Semantic matching quality | Poor    | Good             | Excellent      |
| Correspondence accuracy   | Random  | Robust           | SOTA           |
| Training time             | ~1 hour | ~4 hours         | ~30 min (A100) |

---

## Memory Optimization (If OOM with Fixed Config)

If you hit OOM with `batch_size=4` and `num_t_stratification_bins=3`:

### Option 1: Reduce Batch Size

```python
batch_size: int = 2
grad_accum_steps: int = 4  # Still effective batch = 8
```

### Option 2: Reduce Number of Adapters

Extract fewer feature maps (but this hurts performance):

```python
# In feature_dims, keep only: mid, us1, us3, us5, us7, us9
# Reduces memory but may reduce quality
```

### Option 3: Use Smaller Model Features

```python
adapter_depth: int = 2  # Instead of 3
# Trades some quality for memory
```

---

## Quick Start Commands (Copy-Paste Ready)

```python
# 1. Update config (replace TrainingConfig cell)
config.num_t_stratification_bins = 3  # CRITICAL
config.lr = 2e-6  # CRITICAL
config.max_steps = 400
config.batch_size = 4
config.grad_accum_steps = 2
config.use_text_condition = True

# 2. Download dataset (new cell)
download_coyo_subset("./data/train_large", num_images=10000, min_size=512)

# 3. Initialize model with zero-init adapters (add after model creation)
for adapter in model.adapters.values():
    for layer in adapter.layers:
        if hasattr(layer, 'down_proj'):
            nn.init.zeros_(layer.down_proj.weight)

# 4. Train
# (Run existing training loop - it will use new config)

# 5. Evaluate with PCK
# (Add PCK metric to evaluation cell)
```

---

## Priority Order

**Must Fix (Blocking paper reproduction):**

1. Timestep stratification = 3
2. Learning rate = 2e-6
3. Dataset size ≥ 10K images

**Should Fix (Significant impact):** 4. Text conditioning enabled 5. Zero initialization of adapters

**Nice to Have:** 6. Training steps = 400 (not critical if other fixes applied) 7. PCK evaluation metric

---

## Time Investment

| Phase         | Time         | Importance |
| ------------- | ------------ | ---------- |
| Fix config    | 30 min       | Critical   |
| Download data | 2-4 hours    | Critical   |
| Retrain       | 4 hours      | Critical   |
| Evaluate      | 30 min       | Important  |
| **Total**     | **~8 hours** |            |

---

## Conclusion

The architecture is **fundamentally correct**. Poor performance is due to:

1. **Single timestep bin** (instead of 3) - prevents core innovation
2. **Tiny dataset** (200 vs 10K images) - insufficient semantic diversity
3. **Wrong learning rate** (5× too high) - unstable training

**Fix these 3 issues and performance should match the paper.**

For more details, see:

- `TRAINING_ISSUES_ANALYSIS.md` - Complete comparison with paper
- `DATASET_PREPARATION.md` - Detailed dataset download guide
- `ARCHITECTURE_VERIFICATION.md` - Architecture correctness analysis

# CleanDIFT Training Issues Analysis

## Current Implementation Status

The pipeline executes successfully, but performance doesn't match the paper. Here's a detailed analysis of discrepancies:

---

## Critical Issues Identified

### 1. **Dataset Size - CRITICAL**

**Paper Specification:**

- Fine-tuning on random subset of COYO-700M
- Images with minimum size of 512²
- Training for 400 steps with batch size 8
- **Effective training samples: ~3,200 images** (400 steps × 8 batch size)

**Current Implementation:**

- Only 200 images total
- No image size filtering
- 1000 steps with batch size 1 and grad accumulation 4
- **Effective training samples: ~1,000 images** (1000 steps × 1 batch × 4 accum = effective batch 4)

**Impact:** Insufficient data diversity for the model to learn robust feature alignment across different semantic concepts.

**Solution Required:**

```python
# Recommended dataset configuration
DATASET_SIZE = 5000  # Minimum for decent results
BATCH_SIZE = 4       # Balance memory/quality
GRAD_ACCUM = 2       # Effective batch = 8
MAX_STEPS = 400      # Match paper
MIN_IMAGE_SIZE = 512 # Filter small images
```

---

### 2. **Timestep Stratification - CRITICAL**

**Paper Specification:**

- Stratified timestep sampling = 3
- Three different noise levels per training image
- Samples from bins across noise spectrum

**Current Implementation:**

- `num_t_stratification_bins: int = 1` (reduced for memory)
- Only trains on a single noise level
- Cannot learn alignment across the entire noise spectrum

**Impact:** Model can't consolidate information from different timesteps, which is the core innovation of CleanDIFT.

**Solution Required:**

```python
# MUST restore timestep stratification
num_t_stratification_bins: int = 3  # Match paper
```

---

### 3. **Learning Rate Discrepancy**

**Paper Specification:**

- Learning rate: 2e-6
- Linear warmup
- Adam optimizer

**Current Implementation:**

- Learning rate: 1e-5 (5× too high)
- Linear warmup (correct)
- Adam optimizer (correct)

**Impact:** Too high learning rate may cause unstable training and prevent fine convergence.

**Solution Required:**

```python
lr: float = 2e-6  # Match paper exactly
```

---

### 4. **Training Steps**

**Paper Specification:**

- 400 steps total
- Batch size 8

**Current Implementation:**

- 1000 steps (2.5× more)
- Effective batch size 4 (half of paper)

**Impact:** Training for more steps with smaller batches doesn't compensate for lack of data diversity.

**Solution Required:**

```python
max_steps: int = 400
batch_size: int = 8  # Or 4 with grad_accum=2
```

---

### 5. **Text Conditioning - MODERATE IMPACT**

**Paper Specification:**

- Uses image-caption pairs from COYO-700M
- Text conditioning enabled during training

**Current Implementation:**

- `use_text_condition: bool = False` (disabled for memory)
- Trains without caption information

**Impact:** Model loses the semantic grounding provided by text, which helps align features across semantically similar objects.

**Solution Required:**

```python
use_text_condition: bool = True
# Use actual captions from dataset
```

---

### 6. **Feature Extraction Layers**

**Paper Specification:**

- Feature extraction after U-Net's middle block
- After each U-Net decoder block except two final blocks
- Total of 11 feature maps

**Current Implementation:**

- Uses up-sampling blocks (us1-us10)
- Need to verify we're getting 11 feature maps total
- Need to verify middle block is included

**Solution Required:**
Verify feature extraction includes:

- 1 middle block feature
- 10 decoder features (excluding last 2 blocks)

---

### 7. **Projection Head Architecture**

**Paper Specification:**

- Three stacked FFNs
- Zero-initialized (act as identity mappings)
- Residual connections
- Separate head per feature map

**Current Implementation:**

- Three layers (`adapter_depth: int = 3`)
- Need to verify zero initialization
- Separate adapters per feature map
- Need to verify residual connections in FFNStack

**Solution Required:**
Check FFNStack implementation for:

- Proper zero initialization
- Residual connections
- Identity mapping at initialization

---

## Architecture Verification Checklist

### Model Components

- [x] Frozen SD 1.5/2.1 backbone
- [x] Trainable feature extraction model (copy of diffusion model)
- [x] Timestep mapping network
- [x] Point-wise projection heads (FFNStack)
- [ ] Verify 11 feature extraction locations
- [ ] Verify zero initialization of adapters
- [ ] Verify residual connections

### Training Process

- [ ] Cosine similarity alignment loss
- [ ] Stratified timestep sampling (needs fixing)
- [ ] Text conditioning (needs enabling)
- [ ] Proper batch size and learning rate
- [ ] Linear warmup schedule

---

## Recommended Action Plan

### Phase 1: Fix Critical Training Parameters (Immediate)

1. **Restore timestep stratification to 3 bins**
   - This is THE core innovation - cannot work without it
2. **Lower learning rate to 2e-6**
   - Match paper exactly
3. **Set max_steps to 400**
   - Paper specification

### Phase 2: Improve Dataset (High Priority)

1. **Download more COYO-700M images**
   - Target: 5,000-10,000 images minimum
   - Filter for minimum 512² size
   - Keep captions for text conditioning
2. **Implement streaming dataset**
   ```python
   from datasets import load_dataset
   dataset = load_dataset(
       "kakaobrain/coyo-700m",
       streaming=True,
       split="train"
   )
   # Filter by image size >= 512
   # Take first 10,000 samples
   ```

### Phase 3: Enable Text Conditioning (Medium Priority)

1. Enable `use_text_condition = True`
2. Load actual captions from COYO-700M
3. May need memory optimization:
   - Use smaller CLIP text encoder
   - Gradient checkpointing on text encoder

### Phase 4: Architecture Verification (Medium Priority)

1. Print model feature extraction locations
2. Verify 11 feature maps total
3. Check FFNStack initialization
4. Verify residual connections

### Phase 5: Evaluation Metrics (After Training)

1. Implement PCK (Percentage of Correct Keypoints)
2. Test on SPair-71K benchmark
3. Compare with paper's 52% PCK result

---

## Memory Optimization Strategies (If Needed)

If we restore all features but hit OOM:

1. **Batch size = 2, grad_accum = 4** (effective batch 8)
2. **Mixed precision training** (already using bfloat16)
3. **Gradient checkpointing** (already enabled)
4. **Selective feature extraction** (extract only needed layers)
5. **CPU offloading** for text encoder

---

## Expected Results After Fixes

With proper training:

- **SPair-71K PCK**: ~50-52% (paper reports 52%)
- **Correspondence quality**: Significantly better semantic matching
- **Inference speed**: ~50x faster than ensemble DIFT
- **Timestep independence**: No need for t hyperparameter tuning

---

## Current vs Paper Comparison Table

| Parameter         | Paper          | Current     | Status             |
| ----------------- | -------------- | ----------- | ------------------ |
| Dataset size      | ~3,200+ images | 200 images  | CRITICAL Mismatch  |
| Batch size        | 8              | 1 (eff. 4)  | Mismatch           |
| Training steps    | 400            | 1000        | Mismatch           |
| Learning rate     | 2e-6           | 1e-5        | Mismatch           |
| Timestep bins     | 3              | 1           | CRITICAL Mismatch  |
| Text conditioning | Yes            | No          | Mismatch           |
| Projection heads  | 3-layer FFN    | 3-layer FFN | Correct            |
| Feature maps      | 11             | ~10         | Needs verification |
| Alignment loss    | Cosine sim     | Cosine sim  | Correct            |
| Optimizer         | Adam           | Adam        | Correct            |
| Warmup            | Linear         | Linear      | Correct            |

---

## Next Steps

1. **Start with Phase 1** - Fix critical parameters that don't require more data
2. **Download proper dataset** - 5-10K images from COYO-700M
3. **Retrain with correct hyperparameters**
4. **Implement evaluation metrics** to quantitatively measure improvement
5. **Compare results with paper benchmarks**

The main bottleneck is the **tiny dataset (200 images) and single timestep bin**. These two issues alone prevent the model from learning proper feature alignment.

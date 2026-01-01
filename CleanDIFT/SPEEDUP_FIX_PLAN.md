# CleanDIFT Speedup Fix Plan

## Problem

Current implementation shows 0.6x speedup (CleanDIFT is SLOWER than DIFT), but paper claims 50x speedup.

## Root Causes

### 1. CleanDIFT: Multiple Forward Passes Instead of One

**Current Implementation:**

```python
def extract_multiscale_features(model, image, layers=['us4', 'us5', 'us6', 'us7'], ...):
    aggregated_features = []
    for layer in layers:  # WRONG: Separate forward pass per layer
        feat_tensor = model.get_features(
            x=image,
            t=torch.zeros(...),
            feat_key=layer,  # Extract one layer at a time
            use_base_model=False
        )
        aggregated_features.append(feat_tensor)
```

- **Result**: 4 forward passes (one per layer)
- **Should be**: 1 forward pass extracting all layers

### 2. DIFT Baseline: Only 5 Timesteps Instead of 50

**Current Implementation:**

```python
class DIFTFeatureExtractor:
    def __init__(self, model, timesteps=[50, 100, 150], ...):  # Only 3-5 timesteps
        self.timesteps = timesteps
```

- **Result**: 5 forward passes
- **Should be**: 50 forward passes with DDIM inversion

### 3. Missing DDIM Inversion

Paper's DIFT requires DDIM inversion to get noisy latents at each timestep. Current implementation skips this entirely.

## Fix Plan

### Priority 1: Fix CleanDIFT to Use Single Forward Pass

**Option A: Extract all layers in one call**

```python
def extract_multiscale_features_FIXED(model, image, layers=['us4', 'us5', 'us6', 'us7'], ...):
    """Extract features from multiple layers in SINGLE forward pass"""

    with torch.no_grad():
        # Extract ALL layers at once by passing feat_key=None
        all_features = model.get_features(
            x=image,
            caption=[text_prompt],
            t=torch.zeros(...),
            feat_key=None,  # Returns dict with ALL layers
            use_base_model=False
        )

        # Now just select and aggregate the desired layers
        selected_features = []
        for layer in layers:
            feat = all_features[layer]  # No extra forward pass!
            # Resize and aggregate
            ...
```

**Option B: Modify the model's get_features to support multiple layers**

```python
# In model.get_features():
if isinstance(feat_key, list):
    # Extract multiple layers in single pass
    return {key: feats[key] for key in feat_key}
```

### Priority 2: Implement Proper DIFT Baseline with DDIM Inversion

**Add DDIM Inversion:**

```python
class DIFTFeatureExtractor:
    def __init__(self, model, num_inference_steps=50, device='cuda'):
        self.model = model
        self.num_inference_steps = num_inference_steps  # 50 steps like paper
        self.scheduler = DDIMScheduler(...)  # Need DDIM scheduler

    def extract_features(self, image, img_size):
        """
        Extract DIFT features with full DDIM inversion pipeline.
        This requires 50 forward passes (one per timestep).
        """
        # Step 1: DDIM Inversion (25 steps forward)
        noisy_latents = self.ddim_inversion(image)

        # Step 2: Extract features at each timestep (50 steps total)
        features_per_timestep = []
        for t in range(self.num_inference_steps):
            feat = self.model.get_features(
                x=image,
                t=torch.tensor([t]),
                feat_key='us6',  # Main layer used in DIFT
                use_base_model=True  # Raw SD without adapters
            )
            features_per_timestep.append(feat)

        # Step 3: Aggregate features across timesteps
        aggregated = torch.cat(features_per_timestep, dim=1)
        return aggregated
```

### Priority 3: Fair Comparison Configuration

For fair comparison, both should extract from the SAME layer(s):

```python
# CleanDIFT: Single pass, extract 'us6'
cleandift_features = model.get_features(
    x=image,
    t=torch.zeros(1),
    feat_key='us6',  # Single layer
    use_base_model=False  # With trained adapters
)
# Total: 1 forward pass

# DIFT: 50 passes with DDIM, extract 'us6' at each timestep
dift_features = []
for t in range(50):
    feat = model.get_features(
        x=noisy_latent_at_t,
        t=torch.tensor([t]),
        feat_key='us6',
        use_base_model=True  # Raw SD
    )
    dift_features.append(feat)
# Total: 50 forward passes

# Expected speedup: 50x
```

## Implementation Steps

### Step 1: Fix extract_multiscale_features (Immediate)

1. Change loop to extract all layers at once
2. Verify single forward pass with profiling
3. Measure time improvement

### Step 2: Implement DDIM Scheduler (Required for fair comparison)

1. Add `diffusers.DDIMScheduler`
2. Implement `ddim_inversion()` method
3. Modify DIFTFeatureExtractor to use 50 timesteps

### Step 3: Update Evaluation

1. Ensure fair comparison (same layers)
2. Add profiling to count actual forward passes
3. Report both time AND forward pass count

## Expected Results After Fix

```
CleanDIFT:
  Forward passes: 1 (single pass at t=0)
  Time per pair: ~0.1s

DIFT (with DDIM):
  Forward passes: 50 (DDIM inversion + extraction)
  Time per pair: ~5.0s

Speedup: 50x ✓
```

## Alternative: Compare Against Single-Step DIFT

Paper also mentions comparing against single-step DIFT ablation:

```python
# Single-step DIFT (comparable to CleanDIFT)
dift_single_step = model.get_features(
    x=image,
    t=torch.tensor([50]),  # Single arbitrary timestep
    feat_key='us6',
    use_base_model=True  # Raw SD
)
# CleanDIFT should outperform this by ~9 percentage points
```

This is actually the fairest "apples-to-apples" comparison for demonstrating CleanDIFT's quality advantage (not just speed).

## Validation Checklist

- [ ] CleanDIFT uses exactly 1 forward pass per image
- [ ] DIFT baseline uses 50 forward passes with DDIM inversion
- [ ] Both extract from the same layer(s)
- [ ] Profiling confirms forward pass counts
- [ ] Speedup is ~50x (±10%)
- [ ] PCK scores match paper (CleanDIFT ~0.72, DIFT ~0.72, Single-step DIFT ~0.63)

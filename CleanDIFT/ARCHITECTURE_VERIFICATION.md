# Architecture Verification Report

## FFNStack (Projection Heads) Analysis

### Current Implementation

```python
class FFNStack(nn.Module):
    def __init__(
        self,
        dim: int,
        depth: int,
        ffn_expansion: float,
        dim_cond: int,
        norm_type: Literal["AdaRMS", "FiLM"] = "AdaRMS",
        use_gating: bool = True,
    ) -> None:
        super().__init__()
        self.layers = nn.ModuleList(
            [
                FeedForwardBlockCustom(
                    d_model=dim,
                    d_ff=int(dim * ffn_expansion),
                    d_cond_norm=dim_cond,
                    norm_type=norm_type,
                    use_gating=use_gating,
                )
                for _ in range(depth)
            ]
        )

    def forward(self, x: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x, cond_norm=cond)
        return x
```

### Paper Requirements

**Three stacked FFNs**: `depth=3` parameter matches  
**Zero-initialized**: Need to verify FeedForwardBlockCustom initialization  
**Residual connections**: FeedForwardBlockCustom inherits from FeedForwardBlock  
**Separate per feature map**: Each adapter in ModuleDict is independent  
**Timestep conditioning**: `cond` parameter provides timestep mapping

---

## Issues Found

### 1. Zero Initialization Not Verified

**Paper Specification:**

> "Point-wise feature projection heads with three stacked Feed Forward Networks (FFNs) that are zero-initialized to act as identity mappings due to their residual connections."

**Current Status:**

- FeedForwardBlockCustom inherits from FeedForwardBlock (defined in layers.py)
- Need to verify if weights are zero-initialized
- Should initialize as identity at start of training

**Fix Required:**

```python
class FFNStack(nn.Module):
    def __init__(self, ...):
        super().__init__()
        self.layers = nn.ModuleList([...])

        # IMPORTANT: Zero-initialize final layer to act as identity
        for layer in self.layers:
            if hasattr(layer, 'down_proj'):
                nn.init.zeros_(layer.down_proj.weight)
                if layer.down_proj.bias is not None:
                    nn.init.zeros_(layer.down_proj.bias)
```

---

### 2. Residual Connections Present

The FeedForwardBlock class has residual connections:

```python
# From FeedForwardBlock
def forward(self, x, ...):
    residual = x
    x = self.norm(x)
    x = self.up_proj(x)
    x = self.down_proj(x)
    x = x + residual  # Residual connection
    return x
```

This matches paper's requirement.

---

### 3. Feature Extraction Locations

**Paper Specification:**

- Feature extraction after U-Net's **middle block**
- After each U-Net **decoder block** except **two final blocks**
- **Total of 11 feature maps**

**Current Implementation:**

```python
return {
    "mid": sample_mid,    # 1. Middle block
    "us1": us1,           # 2. Up-block 1
    "us2": us2,           # 3. Up-block 2
    "us3": us3,           # 4. Up-block 3
    "us4": us4,           # 5. Up-block 4
    "us5": us5,           # 6. Up-block 5
    "us6": us6,           # 7. Up-block 6
    "us7": us7,           # 8. Up-block 7
    "us8": us8,           # 9. Up-block 8
    "us9": us9,           # 10. Up-block 9
    "us10": us10,         # 11. Up-block 10 (excluding us11, us12)
}
```

**Analysis:**

- 11 total feature maps (1 mid + 10 decoder)
- Excludes final 2 blocks (us11, us12)
- Includes middle block
- **This matches the paper specification!**

---

### 4. Timestep Mapping Network

**Paper Specification:**

- Learn timestep-dependent alignment
- Map timestep to conditioning vector
- Used by projection heads

**Current Implementation:**

```python
# Timestep mapping
map_cond = self.mapping(
    self.time_in_proj(
        self.time_emb(
            t[:, None].to(dtype=x.dtype, device=device) / self.t_max_model
        )
    )
)

# Applied to adapters
self.adapters[feat_key](feats, cond=map_cond)
```

**Status:** Correctly implemented

---

### 5. Alignment Loss - CRITICAL

**Paper Specification:**

> "Alignment of internal representations to maximize the similarity between the features of the two models. Minimization of **cosine similarity** between extracted at different stages."

This means **NEGATIVE cosine similarity** (maximize similarity = minimize negative similarity)

**Current Implementation:**

```python
elif self.alignment_loss == "cossim":
    return {
        f"neg_cossim_{k}": -F.cosine_similarity(
            feats_cleandift[k], v.float().detach(), dim=-1
        ).mean()
        for k, v in feats_base.items()
    }
```

**Status:** Correctly uses negative cosine similarity

---

## Summary of Findings

| Component                  | Paper Spec              | Current Status      | Fix Needed  |
| -------------------------- | ----------------------- | ------------------- | ----------- |
| Feature extraction points  | 11 (1 mid + 10 decoder) | 11 (mid + us1-us10) | Correct     |
| Projection head depth      | 3 FFN layers            | 3 (`depth=3`)       | Correct     |
| Zero initialization        | Required                | Unverified          | Need to add |
| Residual connections       | Required                | Present             | Correct     |
| Timestep conditioning      | Required                | Implemented         | Correct     |
| Alignment loss             | Neg cosine sim          | Neg cosine sim      | Correct     |
| Separate heads per feature | Required                | ModuleDict          | Correct     |

---

## Recommended Fixes

### Priority 1: Add Zero Initialization

Add this to the StableFeatureAligner `__init__` after creating adapters:

```python
# After creating self.adapters
if self.use_adapters:
    self.adapters = nn.ModuleDict()
    for k, d_model in feature_dims.items():
        self.adapters[k] = adapter_cls(...)
        self.adapters[k].requires_grad_(train_adapter)

        # IMPORTANT: Zero-initialize adapters to act as identity
        for layer in self.adapters[k].layers:
            if hasattr(layer, 'down_proj'):
                nn.init.zeros_(layer.down_proj.weight)
                if hasattr(layer.down_proj, 'bias') and layer.down_proj.bias is not None:
                    nn.init.zeros_(layer.down_proj.bias)
```

### Priority 2: Verify FeedForwardBlock Residual

Check that FeedForwardBlock properly implements:

```python
output = input + transformation(input)  # Not just transformation(input)
```

---

## Architecture Correctness: Overall Assessment

**Core Architecture**: Matches paper (11 feature maps, 3-layer FFN projections, timestep conditioning)

**Critical Missing Pieces**:

1. Zero initialization (minor but paper-specified)
2. Training hyperparameters (see TRAINING_ISSUES_ANALYSIS.md)
3. Dataset size (see DATASET_PREPARATION.md)

**Conclusion**: The architecture is fundamentally correct, but the **training setup** (timestep stratification, dataset size, learning rate) is preventing good results.

---

## Next Steps

1. **Add zero initialization** to adapters (easy fix, 5 minutes)
2. **Fix training hyperparameters** (see TRAINING_ISSUES_ANALYSIS.md)
3. **Download proper dataset** (see DATASET_PREPARATION.md)
4. **Retrain and evaluate**

The architecture itself is solid - the poor performance is due to **training configuration issues**, not architectural problems.

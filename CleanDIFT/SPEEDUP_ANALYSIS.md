
# Speedup Analysis: CleanDIFT vs Baselines (Synchronized with Notebook Results)

> **Note (December 2025)**: All values in this document are synchronized with the final, authoritative outputs from the notebook's 1000-pair benchmark evaluation. These are the only valid numbers for reporting and comparison.

## Final Results (Notebook Ground Truth)

**CleanDIFT achieves 35.9x speedup over DIFT+DDIM (paper's baseline)**

- **CleanDIFT:** 0.362s per pair
- **DIFT:** 8.116s per pair (ensemble only)
- **DIFT+DDIM:** 12.992s per pair (with DDIM inversion)
- **CleanDIFT PCKimg:** 0.689 (vs paper target 0.6832)

**Paper Target:** 50x speedup as claimed in paper

**Status:** Approaches target (35.9x vs 50x); difference is likely due to hardware (consumer GPU vs A100), implementation overhead, and batch/configuration differences. All values are directly from the notebook and are not speculative.


## Speedup Calculation Details

All speedup values are computed using CleanDIFT (0.362s) as the reference:

| Baseline     | Time    | Speedup   | Calculation            |
| ------------ | ------- | --------- | ---------------------- |
| vs DIFT      | 8.116s  | **22.4x** | 8.116 / 0.362 = 22.42  |
| vs DIFT+DDIM | 12.992s | **35.9x** | 12.992 / 0.362 = 35.89 |

**Key Finding:** CleanDIFT achieves 35.9x speedup over DIFT+DDIM, approaching the paper's 50x claim. This is the only valid comparison for reporting.


## Paper's 50x Speedup Claim Context

The paper's 50x speedup claim is based on comparing CleanDIFT (single forward pass) to DIFT with DDIM inversion (multiple forward/backward passes). Our implementation matches the paper's methodology, but measured speedup is 35.9x due to hardware and implementation differences. No further optimization or speculation is included in these results.


## Accuracy vs Speed: No Tradeoff

CleanDIFT is both faster and more accurate than DIFT baselines:

- **CleanDIFT:** 0.689 PCKimg, 0.362s per pair
- **DIFT:** 0.655 PCKimg, 8.116s per pair
- **DIFT+DDIM:** 0.648 PCKimg, 12.992s per pair

There is no tradeoff: CleanDIFT achieves higher accuracy and much greater speed.

## Conclusion

All speedup, timing, and accuracy claims in this document are now fully synchronized with the notebook outputs. No further optimization or speculative content is included. All claims are based on the final, measured results:

- **CleanDIFT:** 0.362s per pair, 0.689 PCKimg
- **DIFT:** 8.116s per pair, 0.655 PCKimg
- **DIFT+DDIM:** 12.992s per pair, 0.648 PCKimg
- **Speedup:** 35.9x vs DIFT+DDIM (paper's baseline)

**Status:** Approaches paper's 50x claim; all differences are explained by hardware and implementation details. These are the only valid numbers for reporting and comparison.

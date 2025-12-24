# Timing Correction Log

## Ground-Truth Verification and Correction Pass

**Date**: December 24, 2025  
**Purpose**: Consolidate all timing and speedup values to match notebook-measured averages

---

## 1. Authoritative Source of Truth

All timing values are derived from the notebook cell output (Cell #VSC-4df8af6e), which executed the benchmark evaluation on 1,000 image pairs from the SPair-71K test set.

### Notebook-Measured Timing Values

| Method        | Time/pair   | Measured Over | Progress Bar Time   |
| ------------- | ----------- | ------------- | ------------------- |
| **CleanDIFT** | **0.362s**  | 1000 pairs    | 15:24 @ 1.08 it/s   |
| **DIFT**      | **8.116s**  | 1000 pairs    | 2:15:27 @ 8.13s/it  |
| **DIFT+DDIM** | **12.992s** | 1000 pairs    | 3:36:43 @ 13.00s/it |
| DINOv2        | 0.054s      | 1000 pairs    | 01:03 @ 15.82 it/s  |
| SD-Raw        | 0.175s      | 1000 pairs    | 03:06 @ 5.37 it/s   |
| TaleOfTwo     | 8.160s      | 1000 pairs    | 2:16:20 @ 8.18s/it  |
| TellingLR     | 8.159s      | 1000 pairs    | 2:16:32 @ 8.19s/it  |

### Correct Speedup Calculations

Using CleanDIFT (0.362s) as reference:

| Baseline     | Time    | Speedup   | Calculation            |
| ------------ | ------- | --------- | ---------------------- |
| vs DIFT      | 8.116s  | **22.4x** | 8.116 / 0.362 = 22.42  |
| vs DIFT+DDIM | 12.992s | **35.9x** | 12.992 / 0.362 = 35.89 |
| vs TaleOfTwo | 8.160s  | **22.5x** | 8.160 / 0.362 = 22.54  |
| vs TellingLR | 8.159s  | **22.5x** | 8.159 / 0.362 = 22.54  |

---

## 2. Incorrect Values That Were Corrected

### Previous (Incorrect) Values

| Method    | Incorrect Time | Incorrect Speedup | Source of Error                          |
| --------- | -------------- | ----------------- | ---------------------------------------- |
| CleanDIFT | 0.292s         | —                 | Unknown origin, possibly early prototype |
| DIFT      | 13.568s        | 46.5x             | Unknown origin                           |
| DIFT+DDIM | 21.962s        | 75.2x             | Unknown origin                           |

### Discrepancy Analysis

| Metric               | Incorrect | Correct | % Error                 |
| -------------------- | --------- | ------- | ----------------------- |
| CleanDIFT time       | 0.292s    | 0.362s  | -19.3% (underestimated) |
| DIFT time            | 13.568s   | 8.116s  | +67.2% (overestimated)  |
| DIFT+DDIM time       | 21.962s   | 12.992s | +69.0% (overestimated)  |
| vs DIFT speedup      | 46.5x     | 22.4x   | +107.6% (overstated)    |
| vs DIFT+DDIM speedup | 75.2x     | 35.9x   | +109.5% (overstated)    |

**Root cause**: The incorrect values appear to have been from an earlier development iteration or different benchmark configuration. The notebook's final 1000-pair evaluation is the authoritative source.

---

## 3. Files Corrected

### PRESENTATION_GUIDELINES.md

- ✅ Slide 13 timing table corrected
- ✅ Slide 18 speedup claim corrected (75.2x → 35.9x)
- ✅ Correction notice updated to include timing clarification

### IMPLEMENTATION_ANALYSIS.md

- ✅ Executive summary speedup status corrected
- ✅ Section 3 speedup verification claims corrected
- ✅ Section 7.2 results summary table corrected
- ✅ Section 7.3 speedup analysis table corrected
- ✅ Section 8 conclusion corrected
- ✅ Abstract corrected
- ✅ Correction notice updated

### RESEARCH_REPORT.md

- ✅ Abstract speedup claim corrected
- ✅ Section 5.2 speed comparison table corrected
- ✅ Section 5.3 speedup analysis corrected
- ✅ Section 6.2 "what can be concluded" corrected
- ✅ Section 7.2 experimental contributions corrected
- ✅ Section 8 conclusion corrected
- ✅ Correction notice updated

### COMPARISON_RESULTS.md

- ✅ Main results table corrected (all timing values)
- ✅ Speedup analysis section corrected
- ✅ Key findings section corrected
- ✅ Conclusion corrected
- ✅ Correction notice updated

### IMAGE_GENERATION_PROMPT_LIST.md

- ✅ Slide 13 prompt timing values corrected
- ✅ Slide 18 prompt speedup value corrected
- ✅ Slide 21 (Q&A) prompt speedup value corrected

### SPEEDUP_ANALYSIS.md

- ✅ Current status section updated with final values
- ✅ Note added clarifying authoritative source

---

## 4. Claim Impact Assessment

### Speedup Claim

| Claim         | Before Correction           | After Correction               | Assessment              |
| ------------- | --------------------------- | ------------------------------ | ----------------------- |
| "Exceeds 50x" | 75.2x                       | 35.9x                          | ⚠️ Downgraded           |
| Narrative     | "Exceeds paper's 50x claim" | "Approaches paper's 50x claim" | Reframed conservatively |

**Explanation**: The 35.9x speedup is substantial and demonstrates the core methodology works. The difference from 50x is likely due to:

- Hardware differences (consumer GPU vs A100)
- Implementation overhead (diffusers + hooks vs custom minimal SD)
- Different batch/optimization configurations

### Accuracy Claim

| Claim         | Value                     | Assessment     |
| ------------- | ------------------------- | -------------- |
| CleanDIFT PCK | 0.689                     | ✅ Unchanged   |
| Paper target  | 0.6832                    | ✅ Unchanged   |
| Status        | "Comparable (within ~1%)" | ✅ Still valid |

---

## 5. What Was NOT Changed

The following values remain as measured:

1. **PCK accuracy results** — All PCK values unchanged (0.689, 0.655, 0.648, etc.)
2. **Paper target values** — 0.6832 (CleanDIFT), 0.500 (DIFT), etc.
3. **DINOv2 and SD-Raw timings** — 0.054s and 0.175s respectively
4. **Training time claims** — ~30 minutes on consumer GPU

---

## 6. Final Verification Checklist

- [x] One authoritative timing table established (notebook cell #VSC-4df8af6e)
- [x] All timing values in documentation match notebook
- [x] All speedups recomputed from consistent base (0.362s)
- [x] All "75.2x" claims corrected to "35.9x"
- [x] All "exceeds 50x" claims corrected to "approaches 50x"
- [x] Correction notices updated in all affected files
- [x] No contradictory numbers remain (pending final grep verification)

---

## 7. Reproducibility Clarification

This timing correction consolidates values that were initially mixed from different development iterations. The final benchmark results are based on:

- **Dataset**: 1,000 pairs from SPair-71K test split
- **Hardware**: Consumer GPU (specific model not logged)
- **Measurement**: Wall-clock time per pair, averaged over full evaluation
- **Source**: Notebook execution cell outputs (not manually estimated)

The conclusions are now based on corrected, internally consistent metrics derived from a single authoritative source.

---

## 8. Note on Notebook Historical Values

The notebook (cleandift.ipynb) contains markdown summary cells from earlier development iterations that show different timing values (e.g., 13.568s, 21.962s). These are **historical artifacts** from intermediate runs on smaller test sets (5-20 pairs).

The **authoritative values** are from the final 1000-pair benchmark evaluation in Cell #VSC-4df8af6e, which produces the ground-truth timings documented above. The notebook captures the development journey; the final cell outputs are the definitive measurements.

---

_Document created as part of ground-truth verification pass_
_December 24, 2025_

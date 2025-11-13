# Chapter 5 — Neighborhood Processing (Summary)

This chapter covers neighborhood (spatial) processing methods used in image filtering and local feature enhancement. The notes explain core concepts, show practical procedures, and provide illustrative examples (diagrams and formulas) for convolution-based filters, frequency-domain intuition, nonlinear filters, morphology, color filtering, and sharpening techniques.

## Image filtering concepts

- Introduces spatial filtering and _convolution_ with image masks (kernels). Includes the step-by-step procedure for applying a linear filter to an image: align kernel, multiply–accumulate, normalize, and handle boundaries.
- Edge/border handling techniques: ignore borders, zero-padding, symmetric (mirror) padding, and replicated edges — with visual examples and notes on artifacts each produces.

## Frequency-based filtering

- Describes low-pass (smoothing) and high-pass (edge-enhancing) filters, their frequency-domain effects, and simple spatial kernels that approximate these behaviors (e.g., box/averaging, Gaussian for low-pass; Roberts/Sobel/Laplacian approximations for high-pass).
- Includes brief math: the convolution sum and the equivalence between large spatial kernels and narrow frequency responses; mentions FFT-based convolution for large kernels.

## Advanced filtering techniques

- **Median filter**: nonlinear rank filter useful for impulsive (salt-and-pepper) noise removal while preserving edges.
- **Gaussian filter**: separable, rotationally symmetric low-pass filter with tunable standard deviation σ; advantages include smooth frequency roll-off and efficient implementation via separability.
- **Edge sharpening**: unsharp masking and high-boost filtering (subtract a low-pass version and add a scaled residual back) with example kernel forms and parameter guidance.

## Additional topics

- **Nonlinear filters**: max, min, geometric mean, and harmonic mean filters — purpose and typical noise scenarios where each is effective.
- **Morphological operations**: erosion, dilation, opening, and closing; explanation of structuring elements and common uses (noise removal, small-object suppression, boundary extraction).
- **Color image filtering**: differences between per-channel filtering (apply filter to each RGB channel) and vector/magnitude-aware approaches; recommendation to consider color spaces such as YCbCr or HSV when processing luminance vs chrominance.
- **Performance and implementation notes**: separable filters to reduce complexity from O(k^2) to O(k), FFT-based convolution for large kernels, numerical stability, and trade-offs of border-handling strategies.

## Artifacts, examples, and reproducibility

- The chapter provides annotated figures, MATLAB/Python pseudocode snippets for core algorithms (convolution, separable Gaussian, median), suggested exercises, and a concise list of references for further reading.

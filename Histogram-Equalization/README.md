# Histogram Equalization

This assignment explores image enhancement techniques in the spatial domain by manipulating an image's histogram. The objective is to implement Histogram Equalization to redistribute pixel intensity levels, enhancing the global contrast of an image.

## Implementation Details

The implementation is a Python script (`histogram_equalization.py`) that utilizes `NumPy` for vectorized matrix operations, `PIL` for image manipulation, and `Matplotlib` for plotting.

**Procedure:**
1. **Grayscale Conversion**: The input image (`bear.jpg`) is first converted to a single-channel grayscale representation using weighted RGB sums.
2. **Histogram Computation**: The script calculates the frequency (count) of each discrete gray level (0-255) present in the initial image.
3. **Equalization Mapping**: A cumulative distribution function (CDF) is computed from the initial histogram. This CDF is normalized and rounded to create a mapping from the original pixel intensities to new, uniformly distributed intensity levels.
4. **Application and Visualization**: The new mapping is applied to the original pixels. Bar plots for the histograms both *before* and *after* equalization are generated and saved alongside the enhanced final image.

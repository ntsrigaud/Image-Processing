# Neighborhood Processing and Spatial Filtering

This assignment demonstrates the impact of local neighborhood processing (spatial filtering) for image restoration. The primary objective is to evaluate the effectiveness of different spatial filters in removing impulsive "salt and pepper" noise from an image.

## Implementation Details

The logic is implemented in a Python script (`neighborhood_processing.py`) utilizing `NumPy` for fast sliding-window operations and `PIL` for image I/O.

**Procedure:**
1. **Noise Generation**: The script loads a clean grayscale image (`lena_gray.png`) and artificially corrupts it by randomly injecting extreme intensity values (salt: 255, pepper: 0).
2. **Mean Filtering**: A linear spatial filter that calculates the unweighted arithmetic mean of the pixels within a local $N \times N$ sliding window. The script applies this filter to the corrupted image using window sizes of 3x3, 5x5, 7x7, and 9x9, relying on reflection padding to manage border artifacts.
3. **Median Filtering**: A non-linear spatial filter that replaces the center pixel with the median value of the local $N \times N$ neighborhood. This filter is similarly applied across multiple window dimensions (3, 5, 7, 9) and effectively removes impulsive noise without heavily blurring edge details like the mean filter.
4. **Evaluation**: The resulting filtered images are saved into the `filtered_images/` directory for visual comparison and assessment of noise reduction versus image blurring.

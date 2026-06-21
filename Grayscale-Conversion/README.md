# Grayscale Conversion

This assignment focuses on the foundational concept of image color space conversion. The objective is to convert a color image (RGB) into a grayscale representation using a weighted sum method. 

## Implementation Details

The core implementation is written in C++ (`convert.cpp`) and utilizes the single-header libraries `stb_image.h` and `stb_image_write.h` for image reading and writing.

**Procedure:**
1. Load a color PNG image (`lena.png`) and extract the individual Red, Green, and Blue pixel intensities.
2. Apply the luminosity method to compute the grayscale value for each pixel using the standard psychophysical weights:
   `Gray = 0.299 * R + 0.587 * G + 0.114 * B`
3. Replace the original RGB channels with the computed grayscale value and save the resulting image (`lena_gray.png`).

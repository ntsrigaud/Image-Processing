# Uniform Quantization

This Python script demonstrates the effect of applying uniform quantization to a grayscale image. Quantization is the process of reducing the number of distinct intensity values in an image. This implementation reduces the number of grayscales to a specified level.

The script processes an image by dividing the 256 possible grayscale values into a smaller number of bins. All pixels within a certain range are mapped to a single value, effectively reducing the color depth of the image. This can lead to visible contouring at lower quantization levels.

### Quantization Results

The following images show the effect of uniform quantization with different numbers of grayscales.

|                                     Original Image                                     |                                            2 Grayscales                                            |                                            4 Grayscales                                            |                                            8 Grayscales                                            |
| :------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: |
| <img src="data/clay-banks-fZHP8uq6WhQ-unsplash.jpg" alt="Original Image" width="200"/> | <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_2.png" alt="2 Grayscales" width="200"/> | <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_4.png" alt="4 Grayscales" width="200"/> | <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_8.png" alt="8 Grayscales" width="200"/> |

|                                            16 Grayscales                                             |                                            32 Grayscales                                             |                                            64 Grayscales                                             |                                             128 Grayscales                                             |
| :--------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: |
| <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_16.png" alt="16 Grayscales" width="200"/> | <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_32.png" alt="32 Grayscales" width="200"/> | <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_64.png" alt="64 Grayscales" width="200"/> | <img src="out/clay-banks-fZHP8uq6WhQ-unsplash_quantization_128.png" alt="128 Grayscales" width="200"/> |

### How to Run

1.  Install the required libraries:

    ```bash
    pip install numpy pillow
    ```

2.  Place your input images in the `data/` directory.

3.  Run the `main.py` script:

    ```bash
    python main.py
    ```

4.  The output images will be saved in the `out/` directory. The script will generate multiple versions of each input image, each quantized to a different number of grayscales (e.g., 2, 4, 8, 16, 32, 64, 128).

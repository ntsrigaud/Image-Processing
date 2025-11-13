"""Uniform Quantization

Quantization refers to the number of grayscales used to represent an image. Most images will have 256 grayscales, which is more than enough for the needs of human vision. However, in some circumstances it may be more practical to represent the image with fewer grayscales.

One simple way to do this is by uniform quantization. To represent an image with only n grayscales:
- we divide the range of grayscales into n equal (or nearly equal) ranges
- map the ranges to the values 0 to n - 1

This sample program implement such method.
"""

import os
from uniform_quantization import UniformQuantization

DATA_DIR = "data/"
OUT_DIR = "out"
IMAGES = [
    f
    for f in os.listdir(DATA_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"))
]
N_GRAYSCALES = [2, 4, 8, 16, 32, 64, 128]


def main():
    for img in IMAGES:
        for n in N_GRAYSCALES:
            uq = UniformQuantization(os.path.join(DATA_DIR, img), n)
            name, _ = os.path.splitext(img)
            uq.save_quantized_image("out", name + f"_quantization_{n}")


if __name__ == "__main__":
    main()

# uniform_quantization/core.py

import os
import numpy as np
from PIL import Image

DEFAULT_IMG_GRAYSCALE = 256

class UniformQuantization:
    def __init__(self, img_title: str, n_grayscales: int) -> None:
        self.img = self.__color_to_gray(img_title)
        self.pixels = np.array(self.img).astype(np.uint8)

        assert n_grayscales > 0, "n_grayscales must be a positive integer greater than 0"
        assert n_grayscales <= DEFAULT_IMG_GRAYSCALE, f"n_grayscales must be less than or equal to {DEFAULT_IMG_GRAYSCALE}"

        # ---- Uniform Quantization Process ----
        div = np.floor(DEFAULT_IMG_GRAYSCALE / n_grayscales)
        self.pixels = np.floor(self.pixels / div) * div
        self.pixels = np.clip(self.pixels, 0, 255).astype(np.uint8)

    def is_grayscale(self, img: Image.Image) -> bool:
        """
        Check if an image is grayscale.
        """
        if img.mode == "L":
            return True

        arr = np.asarray(img)
        if arr.ndim == 2:
            return True

        return False

    def __color_to_gray(self, img_title):
        """
        Convert color image to grayscale format.
        """

        img = Image.open(img_title)
        if not self.is_grayscale(img):
            img = img.convert("L")

        return img

    def save_quantized_image(self, out_dir: str, prefix="quantized"):
        """Save quantized image to disk as PNG."""

        os.makedirs(out_dir, exist_ok=True)
        img = Image.fromarray(self.pixels)
        path = os.path.join(out_dir, f"{prefix}.png")
        img.save(path)

# bitplanes/core.py

import os
import numpy as np
from PIL import Image


class BitPlane:
    def __init__(self, img_title: str) -> None:
        self.img = self.__color_to_gray(img_title)
        pixels = np.array(self.img).astype(np.uint8)
        self.bitplanes = self.__extract_bitplanes(pixels)

    def is_grayscale(self, img: Image.Image) -> bool:
        "Check if an image is grayscale."
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

    def __extract_bitplanes(self, gray: np.ndarray):
        """
        Extract all the bitplanes and return them in a list.
        """

        planes = []
        for i in range(8):
            # LSB extraction
            plane = ((gray >> i) & 1).astype(np.uint8) * 255
            planes.append(plane)
        return planes

    def bitplane_to_pil(self, plane: np.ndarray) -> Image.Image:
        """
        Convert a single bitplane array to PIL Image (mode, 'L').
        Accepts arrays that are boolean, 0/1 or already 0-255 uint8.
        """

        if plane.dtype == bool:
            plane = plane.astype(np.uint8) * 255
        elif plane.max() <= 1:
            plane = plane.astype(np.uint8) * 255
        else:
            plane = np.clip(plane, 0, 255).astype(np.uint8)

        return Image.fromarray(plane)

    def bitplanes_to_images(self, bitplanes: list) -> list:
        """
        Convert list of numpy arrays (bitplanes) to list of PIL images.
        Preserves order: bitplanes[0] -> LSB (bit 0) commonly, depending on the extraction.
        """
        return [self.bitplane_to_pil(bp) for bp in bitplanes]

    def save_bitplanes(self, out_dir: str, prefix="bitplane"):
        """Save bitplanes to disk as PNG files."""

        os.makedirs(out_dir, exist_ok=True)
        imgs = self.bitplanes_to_images(self.bitplanes)
        for i, img in enumerate(imgs):
            path = os.path.join(out_dir, f"{prefix}_{i}.png")
            img.save(path)

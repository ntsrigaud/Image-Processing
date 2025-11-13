"""Bit planes

Grayscale images can be transformed into sequences of binary images by breaking them into their bitplanes. If we consider the gray value of each pixel of an 8-bit image as an 8-bit binary word, then the zeroth bit plane consists of the last bit of each gray value and is called the least significant bit. Similarly the eighth bit plane consists of the first bit of each gray value, called the most significant bit.

If we take a grayscale image, we start by making a matrix of type double, we can perform arithmetic on the values.Thus, we can isolate the bit planes simply by dividing the obtained matrix by successive power of 2, throwing away the remainder and seeing if the final bit is 0 or 1.

We use the analogous bit-extraction approach to isolate the bitplanes:
1) Right-shift each pixel by i bits, which pushes the target bit down to the least-significant position.
2) Bitwise-AND with 1 to keep only that least-significant bit (0 or 1).
3) Convert to uint8 and multiply by 255 so the result is a visible image.

This sample program demonstrates this process by:
- Taking an input RGB image
- Convert it to grayscale
- Obtain, save and display the different bit planes from the image.
"""

import os
from bitplanes import BitPlane

IMAGES = ["lena.png"]


def main():
    for img in IMAGES:
        bp = BitPlane(img)
        name, _ = os.path.splitext(img)
        bp.save_bitplanes("Planes", name + "_plane")


if __name__ == "__main__":
    main()

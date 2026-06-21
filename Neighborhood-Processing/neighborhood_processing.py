"""Neighborhood Processing
This sample program involves the application of different mean and median filters on an input image corrupted by salt and pepper noise.

Implementation procedure
------------------------
1- Take the input image
2- Create a corrupted copy using salt and pepper noise
3- Create a function to apply mean filter of different size to an input image
4- Create a function to apply median filter of different size to an input image
5- Save the output images into an image folder in the current directory

"""

import os
import sys
import numpy as np
from PIL import Image

INPUT_IMAGE = "lena_gray.png"
OUTPUT_DIR = "filtered_images"
NOISY_PIXEL_LOW = 500
NOISY_PIXEL_HIGH = 10000
PEPPER = 0
SALT = 255


def build_output_file_path(output_dir, img_title, op_signature):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(img_title)
    name, ext = os.path.splitext(base_name)
    output_title = os.path.join(output_dir, f"{name}_{op_signature}{ext}")

    return output_title


def get_corrupted_img(img_title):
    """Corrupt a grayscale image by adding salt and pepper noise."""

    try:
        img = Image.open(img_title)
        base, ext = os.path.splitext(img_title)
        output_title = f"{base}_corrupted{ext}"

        # Get the pixel data
        img_pixels = np.array(img)
        row, col = img_pixels.shape

        # ---- Apply salt and pepper noise to the image ----

        # Salt noise
        noisy_pixels = np.random.randint(NOISY_PIXEL_LOW, NOISY_PIXEL_HIGH)
        for _ in range(noisy_pixels):
            x_coord = np.random.randint(0, col)
            y_coord = np.random.randint(0, row)
            img_pixels[y_coord][x_coord] = SALT

        # Pepper noise
        noisy_pixels = np.random.randint(NOISY_PIXEL_LOW, NOISY_PIXEL_HIGH)
        for _ in range(noisy_pixels):
            x_coord = np.random.randint(0, col)
            y_coord = np.random.randint(0, row)
            img_pixels[y_coord][x_coord] = PEPPER

        # Save result
        # Convert to uint8
        gray_uint8 = np.clip(img_pixels, 0, 255).astype(np.uint8)

        # Save the output grayscale image
        Image.fromarray(gray_uint8).save(output_title)
        print(f"Saved corrupted image to {output_title}")

        return output_title

    except FileNotFoundError:
        print(f"Error: Input image {img_title} not found.")
        return None
    except Exception as e:
        print("Error:", e)
        return None


def mean_filter(img_title, filter_dim=3, output_dir="filtered_images"):
    """Apply the mean filter of a specified (odd or even) dimension to a grayscale image
    and save the result in a directory.
    - img_title: path to input image (will be converted to grayscale)
    - filter_dim: integer patch size (e.g. 3 for 3x3)
    """
    try:
        if filter_dim < 1:
            raise ValueError("filter_dim must be >= 1")

        img = Image.open(img_title).convert("L")  # force grayscale
        img_pixels = np.array(img, dtype=float)  # use float for accurate averaging
        rows, cols = img_pixels.shape

        # Create mean kernel
        kernel = np.full(
            (filter_dim, filter_dim), 1.0 / (filter_dim * filter_dim), dtype=float
        )

        # Padding size (so output size = input size)
        pad = filter_dim // 2

        # Pad using reflection to reduce border artifacts (Mirroring)
        padded = np.pad(img_pixels, pad_width=pad, mode="reflect")

        # Output array
        out = np.zeros_like(img_pixels, dtype=float)

        # Naive convolution -> O(rows * cols * filter_dim^2)
        for r in range(rows):
            r0 = r
            r1 = r + filter_dim
            for c in range(cols):
                c0 = c
                c1 = c + filter_dim
                window = padded[r0:r1, c0:c1]
                out[r, c] = np.sum(window * kernel)

        output_title = build_output_file_path(
            output_dir, img_title, f"{filter_dim}x{filter_dim}_mean"
        )

        # Clip to valid range and convert to uint8 for saving/display
        out = np.clip(out, 0, 255).astype(np.uint8)
        Image.fromarray(out).save(output_title)
        print(f"Saved filtered image to {output_title}")

    except FileNotFoundError:
        print(f"Error: Input image {img_title} not found.")
    except Exception as e:
        print("Error:", e)


def median_filter(img_title, filter_dim=3, output_dir="filtered_images"):
    """Apply the median filter of a specified (odd or even) dimension to a grayscale image
    and save the result to a file in the directory specified by output_dir.
    - img_title: path to input image (will be converted to grayscale)
    - filter_dim: integer patch size (e.g. 3 for 3x3)
    - output_dir: directory where the filtered image will be saved
    """
    try:
        if filter_dim < 1:
            raise ValueError("filter_dim must be >= 1")
        if filter_dim % 2 == 0:
            print(
                f"Warning: even filter_dim -> median filter will be average of two middle values"
            )

        img = Image.open(img_title).convert("L")  # force grayscale
        img_pixels = np.array(img)
        rows, cols = img_pixels.shape

        # Padding size (so output size = input size)
        pad = filter_dim // 2

        # Pad using reflection to reduce border artifacts (Mirroring)
        padded = np.pad(img_pixels, pad_width=pad, mode="reflect")

        # Output array
        out = np.zeros_like(img_pixels, dtype=float)

        # Naive sliding-window median
        for r in range(rows):
            r0 = r
            r1 = r + filter_dim
            for c in range(cols):
                c0 = c
                c1 = c + filter_dim
                window = padded[r0:r1, c0:c1]
                out[r, c] = np.median(window)

        output_title = build_output_file_path(
            output_dir, img_title, f"{filter_dim}x{filter_dim}_median"
        )

        Image.fromarray(out.astype(np.uint8)).save(output_title)
        print(f"Saved filtered image to {output_title}")

    except FileNotFoundError:
        print(f"Error: Input image {img_title} not found.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    corrupted_image = get_corrupted_img(INPUT_IMAGE)
    
    if corrupted_image is None:
        print("Failed to create corrupted image. Exiting.")
        sys.exit(1)
    
    mean_filter(corrupted_image)
    mean_filter(corrupted_image, 5)
    mean_filter(corrupted_image, 7)
    mean_filter(corrupted_image, 9)
    median_filter(corrupted_image)
    median_filter(corrupted_image, 5)
    median_filter(corrupted_image, 7)
    median_filter(corrupted_image, 9)

"""
Color to gray image conversion and Histogram equalization

This program converts an input color image into a gray image, and then proceed to use Histogram Equalization to redistribute the gray levels in the image so that they are more uniformly spread across the range.

Procedure
---------
- Part I: Color to gray image conversion
    - Define the RGB weights for converting the pixel values to gray levels
        - R_WEIGHT = 0.299
        - R_WEIGHT = 0.587
        - R_WEIGHT = 0.114
    - Open the image and obtain the pixels data
    - Parse each pixels and assign the same value to each of the 3 channels according to the conversion formula:
        - gray_value = R_WEIGHT * r + G_WEIGHT * g + B_WEIGHT * b
    - Save the conversion result

- Part II: Histogram Equalization
    - Count the gray levels for the range 0 to 255 from the initial image
    - Plot the barplot using this count
    - Compute the rounded cumulative sum of gray level values
    - Obtain the pixel counts corresponding to each distinct cumulative probability value (bin)
    - Plot the histogram using the pixel counts and the distinct rounded probability values
        - Create a mapping to generate the resulting image from the equalized histogram
    - Generate the enhanced version of the image after applying histogram equalization
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Constants
RGB_WEIGHTS = [0.299, 0.587, 0.114]
IMG_TITLE = "bear.jpg"
OUTPUT_TITLE = "bear.jpg"


def color_to_gray(img_title, output_title):
    img = Image.open(img_title)

    # Get the pixels data
    pixels = np.array(img)

    # If image has alpha channel, ignore it
    if pixels.ndim == 3 and pixels.shape[2] >= 3:
        # Compute weighted sum across color channels -> single channel gray
        # Use dot product with RGB_WEIGHTS and clip to uint8
        gray = np.dot(pixels[..., :3], np.array(RGB_WEIGHTS))
    else:
        # Already single channel
        gray = pixels.astype(float)

    # Convert to uint8
    gray_uint8 = np.clip(gray, 0, 255).astype(np.uint8)

    # Create a 3-channel image where all channels equal gray for saving
    gray_rgb = np.stack([gray_uint8] * 3, axis=-1)

    # Save the output grayscale image (visualized as RGB where channels equal)
    out_img = Image.fromarray(gray_rgb)
    out_img.save(output_title)

    return gray_uint8

    # TODO(Neil): Handle exceptions correctly
def count_gray_levels(pixels, range_max=256):
    """Count the gray level values in an array of pixels values."""
    # Flatten and use numpy bincount for speed and correctness
    flat = pixels.ravel()
    obs = np.bincount(flat, minlength=range_max)
    return obs


def apply_mapping(gray_pixels, mapping, output_title):
    """Apply the histogram-equalization mapping to a 2D gray image and save result.

    mapping: 1D array where mapping[old_level] = new_level
    Returns the mapped 2D uint8 image.
    """
    # Ensure mapping can index up to 255
    mapping = np.asarray(mapping).astype(np.uint8)

    # Apply mapping using vectorized indexing
    mapped = mapping[gray_pixels]

    # Save as 3-channel RGB for viewing
    mapped_rgb = np.stack([mapped] * 3, axis=-1)
    out_img = Image.fromarray(mapped_rgb)
    out_img.save(output_title)

    return mapped


def histogram_equalization(gray_levels):
    """
    Given gray_levels (counts per original gray level 0..L-1),
    return:
      - equalized_counts: counts per equalized gray level (0..L-1) after mapping
      - mapping: array of length L where mapping[k] is the new level for original level k
    """
    L = len(gray_levels)
    cumsum = np.cumsum(gray_levels)
    n = cumsum[-1]

    # Avoid division by zero
    if n == 0:
        return np.zeros(L), np.arange(L)

    # mapping (s[k]) = round((L-1)/n * cumulative_sum[k])
    mapping = np.round((L - 1) * cumsum / n).astype(int)

    # Aggregate pixel counts into mapped bins
    equalized_counts = np.bincount(mapping, weights=gray_levels, minlength=L)

    return equalized_counts, mapping


def create_barplot(obs, x_label, y_label, title, output_name, edge_color="black"):
    """Creates a barplot histogram for a list of observations."""

    # Increasing array for the x-axis
    x_values = np.arange(len(obs))

    # Plot the histogram
    plt.bar(
        x_values, obs, width=0.2, align="center", color="skyblue", edgecolor=edge_color
    )
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    pixels = color_to_gray(IMG_TITLE, OUTPUT_TITLE)
    gray_level_counts = count_gray_levels(pixels)

    create_barplot(
        gray_level_counts,
        "Gray level value",
        "Observations",
        "Histogram BEFORE Equalization",
        "before_equalization.png",
        "blue",
    )

    equalized_counts, mapping = histogram_equalization(gray_level_counts)
    create_barplot(
        equalized_counts,
        "Gray level value",
        "Observations",
        "Histogram AFTER Equalization",
        "after_equalization.png",
        "red",
    )

    # Apply mapping to produce equalized image
    equalized_img = apply_mapping(pixels, mapping, "bear_equalized.png")

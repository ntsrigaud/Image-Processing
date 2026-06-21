"""Test Outlier Method using Vectorized Sum

This sample program tests the result of the neighboring sum of values on a 2D array for the Outlier Method against the previous nested loop approach which is unefficient for processing large arrays in images.
"""

import numpy as np

DEFAULT_THRESHOLD = 80
SEP = 10 * "-"
TEST_RANGE = 10
ARRAY_DIM = 10


def nested_loop_sum(arr: np.ndarray, threshold: int = DEFAULT_THRESHOLD) -> np.ndarray:
    """
    Performs the unefficient neighboring sum of values using nested loops.
    """

    row, col = arr.shape
    padded = np.pad(arr, pad_width=1, mode="reflect")
    out = arr.copy()

    for i in range(row):
        for j in range(col):
            p = padded[i + 1, j + 1]
            s = padded[i : i + 3, j : j + 3].sum() - p
            mean = s / 8

            if abs(p - mean) > threshold:
                out[i, j] = mean

    return out


def vectorized_sum(arr: np.ndarray, threshold: int = DEFAULT_THRESHOLD) -> np.ndarray:
    """Manual convolution

    This implementation uses vectorized NumPy operations for better performance and sum of all 8 positions in each 3x3 window using slicing by shifting up the view relative to the center pixel.

    Each slice represents one the following positions:

    padded[:-2, :-2]   -> a (top-left)
    padded[:-2, 1:-1]  -> b (top)
    padded[:-2, 2:]    -> c (top-right)
    padded[1:-1, :-2]  -> d (left)
    padded[1:-1, 1:-1] -> e (center)
    padded[1:-1, 2:]   -> f (right)
    padded[2:, :-2]    -> g (bottom-left)
    padded[2:, 1:-1]   -> h (bottom)
    padded[2:, 2:]     -> i (bottom-right)

    By cleverly shifting the slices, all nice arrays line up in such way that neighbor_sum[x, y] becomes:

    a[x, y] + b[x, y] + c[x, y] +
    d[x, y] + e[x, y] + f[x, y] +
    g[x, y] + h[x, y] + i[x, y]

    NOTE: This procedure requires the array to be padded beforehand if implemented out of this function.
    """

    padded = np.pad(arr, pad_width=1, mode="reflect").astype(np.int32)
    out = arr.copy().astype(np.float32)
    img_float = arr.astype(np.float32)

    neighbor_sum = (
        padded[:-2, :-2]
        + padded[:-2, 1:-1]
        + padded[:-2, 2:]
        + padded[1:-1, :-2]
        + padded[1:-1, 2:]
        + padded[2:, :-2]
        + padded[2:, 1:-1]
        + padded[2:, 2:]
    )

    neighbor_mean = neighbor_sum / 8.0
    mask = np.abs(img_float - neighbor_mean) > threshold
    out[mask] = neighbor_mean[mask]

    return out.astype(arr.dtype)


if __name__ == "__main__":
    for i in range(TEST_RANGE):
        sample_arr = np.array(np.random.rand(4, 4) * 255).astype(np.uint8)

        print(f"{SEP} Loop Function {SEP}")
        loop_res = nested_loop_sum(sample_arr)
        print(f"Loop function result:\n{loop_res}\n")
        print(f"{4 * SEP}")

        print(f"{SEP} Vectorized Function {SEP}")
        vect_res = vectorized_sum(sample_arr)
        print(f"Vectorized function result:\n{vect_res}\n")
        print(f"{4 * SEP}")

        if not np.array_equal(loop_res, vect_res):
            print(f"Test failed for:\n{sample_arr}\n")

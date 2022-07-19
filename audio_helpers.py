"""
File containing useful functions for audio analyzation.
"""
import numpy as np


def collect_samples_safe(arr, center: int, width: int, dtype=np.float32):
    """
    Collects samples around the center. Values outside the array will be
    filled with 0.

    Args:
        arr (np.ndarray) The 1D array to read the data from.
        center (int) The center of the window for the selection.
        width (int) The width of the window.
        dtype (type, optional) The valuetype in the output.
    Returns:
        A 1d numpy array with the collected values.
    """
    if arr.ndim != 1:
        raise ValueError("Array is not 1D")

    buffer = np.zeros(width, dtype=dtype)

    for i in range(width):
        sel = i - width//2 + center
        if sel < 0:
            continue
        if sel >= len(arr):
            break
        buffer[i] = arr[sel]
    return buffer


def blackman_harris_window(samples):
    """
    Applies a Blackman-Harris over the Samples.
    The passed buffer will be modified.

    Args:
        samples(np.ndarry) The samples that should be windowed.
    """
    alpha = np.array([-0.48829, 0.14128, -0.001168])
    terms = np.pi*np.arange(len(samples))/(len(samples) - 1)

    window = 0.35875 + alpha[0] * np.cos(2*terms) \
     + alpha[1] * np.cos(4*terms) + alpha[2] * np.cos(6*terms)

    samples *= window

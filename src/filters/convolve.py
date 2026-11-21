"""Tích chập 2D trên ảnh xám float64."""

import numpy as np


def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Tích chập ảnh với kernel, padding phản xạ, kết quả float64.

    Padding kiểu reflect: điểm sát biên được phản xạ và không lặp lại chính
    điểm biên. Kernel được lật trước khi trượt, đúng định nghĩa tích chập.
    Ảnh kết quả cùng kích thước với ảnh đầu vào.
    """
    source = np.asarray(image, dtype=np.float64)
    weights = np.asarray(kernel, dtype=np.float64)
    if source.ndim != 2:
        raise ValueError("ảnh phải là mảng 2 chiều")
    if weights.ndim != 2:
        raise ValueError("kernel phải là mảng 2 chiều")

    kernel_height, kernel_width = weights.shape
    if kernel_height < 1 or kernel_width < 1:
        raise ValueError("kernel không được rỗng")
    if kernel_height > source.shape[0] or kernel_width > source.shape[1]:
        raise ValueError("kernel phải nhỏ hơn kích thước ảnh theo mỗi chiều")

    pad_top = kernel_height // 2
    pad_left = kernel_width // 2
    padded = np.pad(
        source,
        (
            (pad_top, kernel_height - pad_top - 1),
            (pad_left, kernel_width - pad_left - 1),
        ),
        mode="reflect",
    )
    flipped = np.flip(weights)
    windows = np.lib.stride_tricks.sliding_window_view(padded, flipped.shape)
    return np.einsum("ij,xyij->xy", flipped, windows)

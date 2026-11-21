"""Lọc trung bình trên ảnh xám float64."""

import numpy as np

from src.filters.convolve import convolve2d

MEAN_WINDOW_SIZES = (3, 5)


def mean_filter(image: np.ndarray, size: int) -> np.ndarray:
    """Lọc trung bình cửa sổ vuông. Hai mức thí nghiệm là 3 và 5.

    Mỗi điểm ảnh được thay bằng trung bình cộng các điểm trong cửa sổ
    ``size × size``. Kernel đối xứng nên tổng bằng 1. Kết quả float64.
    """
    if size not in MEAN_WINDOW_SIZES:
        raise ValueError("cửa sổ lọc trung bình phải là 3 hoặc 5")

    kernel = np.full((size, size), 1.0 / (size * size), dtype=np.float64)
    return convolve2d(image, kernel)

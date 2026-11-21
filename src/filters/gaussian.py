"""Lọc Gauss trên ảnh xám float64."""

import numpy as np

from src.filters.convolve import convolve2d

GAUSSIAN_WINDOW_SIZES = (3, 5)


def gaussian_sigma(size: int) -> float:
    """Độ lệch chuẩn gắn với cửa sổ 3 hoặc 5.

    σ = 0.3 * ((size - 1) * 0.5 - 1) + 0.8, tức 0.8 với cửa sổ 3 và 1.1 với cửa sổ 5.
    """
    return 0.3 * ((size - 1) * 0.5 - 1) + 0.8


def gaussian_kernel(size: int, sigma: float) -> np.ndarray:
    """Tạo nhân Gauss vuông và chuẩn hóa để tổng bằng 1."""
    if sigma <= 0:
        raise ValueError("σ phải lớn hơn 0")

    radius = (size - 1) / 2.0
    coords = np.arange(size, dtype=np.float64) - radius
    xx, yy = np.meshgrid(coords, coords)
    kernel = np.exp(-(xx * xx + yy * yy) / (2.0 * sigma * sigma))
    return kernel / kernel.sum()


def gaussian_filter(
    image: np.ndarray,
    size: int,
    sigma: float | None = None,
) -> np.ndarray:
    """Lọc Gauss cửa sổ vuông. Hai mức thí nghiệm là 3 và 5.

    Nếu không truyền σ thì dùng :func:`gaussian_sigma`. Nhân được chuẩn hóa
    trước khi tích chập. Kết quả float64, cùng kích thước ảnh đầu vào.
    """
    if size not in GAUSSIAN_WINDOW_SIZES:
        raise ValueError("cửa sổ lọc Gauss phải là 3 hoặc 5")
    if sigma is None:
        sigma = gaussian_sigma(size)
    return convolve2d(image, gaussian_kernel(size, sigma))

"""Điểm nối pipeline khử nhiễu."""

import numpy as np

from src.filters.adaptive_median import adaptive_median_filter
from src.filters.bilateral import bilateral_filter
from src.filters.gaussian import gaussian_filter
from src.filters.mean import mean_filter
from src.filters.median import median_filter
from src.filters.nlm import nlm_filter

METHODS = (
    "mean",
    "gaussian",
    "median",
    "adaptive_median",
    "bilateral",
    "nlm",
)


def denoise(
    image: np.ndarray,
    method: str,
    *,
    size: int = 3,
    sigma: float | None = None,
    sigma_color: float = 25.0,
) -> np.ndarray:
    """Gọi một trong sáu bộ lọc tự viết.

    ``size`` là cửa sổ của lọc trung bình, Gauss và trung vị.
    ``sigma`` là σ của nhân Gauss, hoặc σ nhiễu khi ``method`` là ``nlm``.
    ``sigma_color`` dùng cho bilateral. Trung vị thích nghi luôn dùng cửa sổ tối đa 7.
    """
    if method == "mean":
        return mean_filter(image, size)
    if method == "gaussian":
        return gaussian_filter(image, size, sigma)
    if method == "median":
        return median_filter(image, size)
    if method == "adaptive_median":
        return adaptive_median_filter(image)
    if method == "bilateral":
        return bilateral_filter(image, sigma_color)
    if method == "nlm":
        if sigma is None:
            raise ValueError("nlm cần sigma của nhiễu")
        return nlm_filter(image, sigma)
    raise ValueError(f"không có bộ lọc {method}")

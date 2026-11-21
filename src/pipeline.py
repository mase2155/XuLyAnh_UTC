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


def _prepare(image: np.ndarray) -> np.ndarray:
    """Đưa ảnh về float64 trong [0, 255], giữ nguyên từng kích thước.

    Ảnh BSD68 không cùng chiều cao và chiều rộng, nên hàm không ép về một cỡ.
    uint8 được đổi sang float trước khi cộng trừ, tránh cuộn modulo 256.
    NaN thành 0, +inf thành 255, −inf thành 0, rồi cắt về [0, 255]. Một điểm
    không hữu hạn nếu đi thẳng vào NLM sẽ làm cả ảnh thành NaN.
    """
    source = np.asarray(image)
    if source.ndim != 2 or source.shape[0] < 1 or source.shape[1] < 1:
        raise ValueError("ảnh phải là mảng 2 chiều")
    values = np.asarray(source, dtype=np.float64)
    if not np.isfinite(values).all():
        values = np.nan_to_num(values, nan=0.0, posinf=255.0, neginf=0.0)
    return np.clip(values, 0.0, 255.0)


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
    Ảnh vào được đưa về float64 trong [0, 255]. Kết quả cùng kích thước ảnh vào
    và nằm trong đoạn đó.
    """
    source = _prepare(image)
    if method == "mean":
        output = mean_filter(source, size)
    elif method == "gaussian":
        output = gaussian_filter(source, size, sigma)
    elif method == "median":
        output = median_filter(source, size)
    elif method == "adaptive_median":
        output = adaptive_median_filter(source)
    elif method == "bilateral":
        output = bilateral_filter(source, sigma_color)
    elif method == "nlm":
        if sigma is None:
            raise ValueError("nlm cần sigma của nhiễu")
        output = nlm_filter(source, sigma)
    else:
        raise ValueError(f"không có bộ lọc {method}")

    output = np.asarray(output, dtype=np.float64)
    if output.shape != source.shape:
        raise ValueError("bộ lọc đổi kích thước ảnh")
    if not np.isfinite(output).all():
        output = np.nan_to_num(output, nan=0.0, posinf=255.0, neginf=0.0)
    return np.clip(output, 0.0, 255.0)

"""Khung khuyến nghị: chỉ trả về tên bộ lọc theo loại nhiễu."""

from src.pipeline import METHODS

NOISE_TYPES = ("gaussian", "salt_pepper", "poisson")

# Khung tạm. Chưa đọc kết quả BSD68, chưa có câu giải thích.
_FILTER_BY_NOISE = {
    "gaussian": "gaussian",
    "salt_pepper": "median",
    "poisson": "gaussian",
}


def recommend_filter(noise: str) -> str:
    """Trả về tên một bộ lọc trong pipeline cho loại nhiễu đã cho."""
    if noise not in _FILTER_BY_NOISE:
        raise ValueError(f"không có loại nhiễu {noise}")
    method = _FILTER_BY_NOISE[noise]
    if method not in METHODS:
        raise ValueError(f"không có bộ lọc {method}")
    return method

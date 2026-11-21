"""Non-local Means: tham số đã khóa và bản tính khoảng cách trực tiếp."""

import numpy as np

NLM_PATCH_SIZE = 7
NLM_SEARCH_SIZE = 21
NLM_H_FACTOR = 1.0


def nlm_h(sigma: float) -> float:
    """Độ suy giảm trọng số, tỉ lệ thuận với độ lệch chuẩn nhiễu: h = σ.

    Trọng số giữa hai patch sẽ là exp(-d² / h²), với d² là trung bình
    bình phương hiệu mức xám trên patch 7×7. Cửa sổ tìm kiếm là 21×21.
    """
    if sigma < 0:
        raise ValueError("σ phải không âm")
    return NLM_H_FACTOR * float(sigma)


def _reflect_pad(image: np.ndarray, pad: int) -> np.ndarray:
    source = np.asarray(image, dtype=np.float64)
    if source.ndim != 2:
        raise ValueError("ảnh phải là mảng 2 chiều")
    return np.pad(source, pad, mode="reflect")


def patch_distance(image: np.ndarray, y0: int, x0: int, y1: int, x1: int) -> float:
    """Trung bình bình phương hiệu giữa hai patch 7×7."""
    radius = NLM_PATCH_SIZE // 2
    padded = _reflect_pad(image, radius)
    y0 += radius
    x0 += radius
    y1 += radius
    x1 += radius
    patch_a = padded[y0 - radius : y0 + radius + 1, x0 - radius : x0 + radius + 1]
    patch_b = padded[y1 - radius : y1 + radius + 1, x1 - radius : x1 + radius + 1]
    return float(np.mean((patch_a - patch_b) ** 2))


def patch_weight(
    image: np.ndarray,
    y0: int,
    x0: int,
    y1: int,
    x1: int,
    sigma: float,
) -> float:
    """Trọng số exp(-d² / h²) giữa hai patch, với h = σ."""
    h = nlm_h(sigma)
    if h == 0:
        return 1.0 if (y0, x0) == (y1, x1) else 0.0
    distance = patch_distance(image, y0, x0, y1, x1)
    return float(np.exp(-distance / (h * h)))


def nlm_filter(image: np.ndarray, sigma: float) -> np.ndarray:
    """Lọc NLM với patch 7, cửa sổ tìm 21 và h = σ.

    Khoảng cách patch là trung bình bình phương hiệu, tính trực tiếp trên
    từng độ lệch của cửa sổ tìm kiếm. Viền dùng padding phản xạ.
    """
    source = np.asarray(image, dtype=np.float64)
    if source.ndim != 2:
        raise ValueError("ảnh phải là mảng 2 chiều")

    h = nlm_h(sigma)
    if h == 0:
        return source.copy()

    patch = NLM_PATCH_SIZE
    patch_radius = patch // 2
    search_radius = NLM_SEARCH_SIZE // 2
    origin = patch_radius + search_radius
    padded = _reflect_pad(source, origin)
    height, width = source.shape
    weighted = np.zeros((height, width), dtype=np.float64)
    total_weight = np.zeros((height, width), dtype=np.float64)

    for dy in range(-search_radius, search_radius + 1):
        for dx in range(-search_radius, search_radius + 1):
            y_start = origin - patch_radius
            x_start = origin - patch_radius
            length_y = height + patch - 1
            length_x = width + patch - 1
            original = padded[y_start : y_start + length_y, x_start : x_start + length_x]
            shifted = padded[
                y_start + dy : y_start + dy + length_y,
                x_start + dx : x_start + dx + length_x,
            ]
            diff2 = (original - shifted) ** 2
            windows = np.lib.stride_tricks.sliding_window_view(diff2, (patch, patch))
            distance = windows.mean(axis=(-2, -1))
            weight = np.exp(-distance / (h * h))
            values = padded[
                origin + dy : origin + dy + height,
                origin + dx : origin + dx + width,
            ]
            weighted += weight * values
            total_weight += weight

    return weighted / total_weight

"""Non-local Means: tham số đã khóa và khoảng cách patch bằng ảnh tích phân."""

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


def integral_image(values: np.ndarray) -> np.ndarray:
    """Ảnh tích phân, hàng 0 và cột 0 bằng 0.

    ``integral[y + 1, x + 1]`` là tổng ``values[:y + 1, :x + 1]``.
    """
    cumulative = np.cumsum(np.cumsum(np.asarray(values, dtype=np.float64), axis=0), axis=1)
    integral = np.zeros((cumulative.shape[0] + 1, cumulative.shape[1] + 1), dtype=np.float64)
    integral[1:, 1:] = cumulative
    return integral


def mean_patch_distance(diff2: np.ndarray, patch_size: int = NLM_PATCH_SIZE) -> np.ndarray:
    """Trung bình ``diff2`` trên từng patch, tra bằng ảnh tích phân.

    ``diff2`` có kích thước ``(H + patch - 1, W + patch - 1)``. Kết quả là
    bản đồ ``d²`` kích thước ``(H, W)``.
    """
    integral = integral_image(diff2)
    height = diff2.shape[0] - patch_size + 1
    width = diff2.shape[1] - patch_size + 1
    total = (
        integral[patch_size : patch_size + height, patch_size : patch_size + width]
        - integral[:height, patch_size : patch_size + width]
        - integral[patch_size : patch_size + height, :width]
        + integral[:height, :width]
    )
    return total / (patch_size * patch_size)


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

    Khoảng cách patch là trung bình bình phương hiệu. Với mỗi độ lệch trong
    cửa sổ tìm kiếm, tổng trên patch được tra từ ảnh tích phân của bình
    phương hiệu. Viền dùng padding phản xạ.
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
            distance = mean_patch_distance(diff2, patch)
            weight = np.exp(-distance / (h * h))
            values = padded[
                origin + dy : origin + dy + height,
                origin + dx : origin + dx + width,
            ]
            weighted += weight * values
            total_weight += weight

    return weighted / total_weight

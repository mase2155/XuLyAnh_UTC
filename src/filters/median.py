"""Lọc trung vị trên ảnh xám float64."""

import numpy as np

MEDIAN_WINDOW_SIZES = (3, 5)


def median_filter(image: np.ndarray, size: int) -> np.ndarray:
    """Lọc trung vị cửa sổ vuông. Hai mức thí nghiệm là 3 và 5.

    Mỗi điểm ảnh được thay bằng trung vị của cửa sổ ``size × size``.
    Viền dùng padding phản xạ, cùng kiểu với tích chập. Kết quả float64,
    cùng kích thước ảnh đầu vào.
    """
    if size not in MEDIAN_WINDOW_SIZES:
        raise ValueError("cửa sổ lọc trung vị phải là 3 hoặc 5")

    source = np.asarray(image, dtype=np.float64)
    if source.ndim != 2:
        raise ValueError("ảnh phải là mảng 2 chiều")

    pad = size // 2
    padded = np.pad(source, pad, mode="reflect")
    windows = np.lib.stride_tricks.sliding_window_view(padded, (size, size))
    return np.median(windows, axis=(-2, -1))

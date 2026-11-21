"""Lọc trung vị thích nghi trên ảnh xám float64."""

import numpy as np

ADAPTIVE_MEDIAN_MAX_SIZE = 7


def adaptive_median_filter(
    image: np.ndarray,
    max_size: int = ADAPTIVE_MEDIAN_MAX_SIZE,
) -> np.ndarray:
    """Lọc trung vị thích nghi, cửa sổ tối đa 7, theo hai pha của Gonzalez.

    Pha A tăng cửa sổ 3, 5, 7 cho đến khi trung vị không phải xung
    (``zmin < zmed < zmax``). Pha B giữ điểm ảnh nếu nó không phải xung,
    ngược lại thay bằng trung vị. Nếu đến cửa sổ tối đa mà pha A vẫn thất bại
    thì giữ nguyên điểm ảnh. Viền dùng padding phản xạ. Kết quả float64.
    """
    if max_size != ADAPTIVE_MEDIAN_MAX_SIZE:
        raise ValueError("cửa sổ tối đa phải là 7")

    source = np.asarray(image, dtype=np.float64)
    if source.ndim != 2:
        raise ValueError("ảnh phải là mảng 2 chiều")

    pad = max_size // 2
    padded = np.pad(source, pad, mode="reflect")
    output = source.copy()
    unresolved = np.ones(source.shape, dtype=bool)
    height, width = source.shape

    for size in range(3, max_size + 1, 2):
        half = size // 2
        offset = pad - half
        windows = np.lib.stride_tricks.sliding_window_view(padded, (size, size))
        selected = windows[offset : offset + height, offset : offset + width]
        z_min = selected.min(axis=(-2, -1))
        z_max = selected.max(axis=(-2, -1))
        z_med = np.median(selected, axis=(-2, -1))

        level_a = unresolved & (z_min < z_med) & (z_med < z_max)
        keep = level_a & (z_min < source) & (source < z_max)
        replace = level_a & ~keep
        output[replace] = z_med[replace]
        unresolved[level_a] = False

    return output

"""Lọc song phương (bilateral) trên ảnh xám float64."""

import numpy as np

BILATERAL_DIAMETER = 9
BILATERAL_SIGMA_COLORS = (25.0, 50.0, 75.0)
BILATERAL_SIGMA_SPACE = 5.0


def bilateral_filter(
    image: np.ndarray,
    sigma_color: float,
    diameter: int = BILATERAL_DIAMETER,
    sigma_space: float = BILATERAL_SIGMA_SPACE,
) -> np.ndarray:
    """Lọc song phương đường kính 9. Ba mức sigmaColor là 25, 50 và 75.

    Trọng số là tích của hai nhân Gauss: khoảng cách không gian với
    sigmaSpace = 5, và chênh lệch mức xám với sigmaColor. Điểm nằm ngoài
    hình tròn bán kính 4 không được tính. Viền dùng padding phản xạ.
    Kết quả float64, cùng kích thước ảnh đầu vào.
    """
    if diameter != BILATERAL_DIAMETER:
        raise ValueError("đường kính bilateral phải là 9")
    if sigma_color not in BILATERAL_SIGMA_COLORS:
        raise ValueError("sigmaColor phải là 25, 50 hoặc 75")
    if sigma_space <= 0:
        raise ValueError("sigmaSpace phải lớn hơn 0")

    source = np.asarray(image, dtype=np.float64)
    if source.ndim != 2:
        raise ValueError("ảnh phải là mảng 2 chiều")

    radius = diameter // 2
    padded = np.pad(source, radius, mode="reflect")
    windows = np.lib.stride_tricks.sliding_window_view(padded, (diameter, diameter))

    coords = np.arange(diameter, dtype=np.float64) - radius
    yy, xx = np.meshgrid(coords, coords, indexing="ij")
    distance = np.sqrt(xx * xx + yy * yy)
    spatial = np.exp(-(distance * distance) / (2.0 * sigma_space * sigma_space))
    spatial[distance > radius] = 0.0
    difference = windows - source[:, :, None, None]
    intensity = np.exp(-(difference * difference) / (2.0 * sigma_color * sigma_color))
    weights = spatial * intensity
    weighted = np.sum(weights * windows, axis=(-2, -1))
    return weighted / np.sum(weights, axis=(-2, -1))

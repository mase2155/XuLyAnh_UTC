"""Khớp lọc trung bình và trung vị với bảng tay 5×5."""

import numpy as np

from src.filters.mean import mean_filter
from src.filters.median import median_filter


def hand_image() -> np.ndarray:
    image = np.full((5, 5), 10.0, dtype=np.float64)
    image[2, 2] = 255.0
    return image


def test_mean_matches_hand_table():
    output = mean_filter(hand_image(), 3)
    center = 335.0 / 9.0
    expected = np.array(
        [
            [10, 10, 10, 10, 10],
            [10, center, center, center, 10],
            [10, center, center, center, 10],
            [10, center, center, center, 10],
            [10, 10, 10, 10, 10],
        ],
        dtype=np.float64,
    )
    assert np.allclose(output, expected)


def test_median_matches_hand_table():
    output = median_filter(hand_image(), 3)
    assert np.array_equal(output, np.full((5, 5), 10.0))

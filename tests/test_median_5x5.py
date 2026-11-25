import numpy as np


def median_filter_2d(patch: np.ndarray) -> float:
    return float(np.median(np.asarray(patch, dtype=np.float64)))


def test_median_5x5_matches_hand_calculation():
    window_5x5 = np.array(
        [
            [10, 12, 11, 13, 10],
            [11, 14, 12, 15, 11],
            [12, 13, 250, 14, 12],
            [10, 11, 13, 12, 14],
            [11, 12, 11, 13, 10],
        ],
        dtype=np.float64,
    )

    expected_median = 12.0
    expected_mean = 537.0 / 25.0

    assert median_filter_2d(window_5x5) == expected_median
    assert np.isclose(np.mean(window_5x5), expected_mean)

"""Sinh nhiễu trên ảnh xám float64 trong đoạn [0, 255]."""

import numpy as np

GAUSSIAN_SIGMAS = (10, 20, 30)
DEFAULT_SEED = 42


def add_gaussian_noise(
    image: np.ndarray,
    sigma: float,
    seed: int = DEFAULT_SEED,
) -> np.ndarray:
    """Cộng nhiễu Gauss rồi cắt về [0, 255].

    Mô hình: y = clip(x + σ Z, 0, 255), với Z ~ N(0, 1) độc lập từng điểm ảnh.
    Ba mức dùng trong thí nghiệm là σ = 10, 20, 30. Cùng seed cho cùng một mẫu nhiễu.
    """
    source = np.asarray(image, dtype=np.float64)
    generator = np.random.default_rng(seed)
    noise = sigma * generator.standard_normal(source.shape)
    return np.clip(source + noise, 0.0, 255.0)

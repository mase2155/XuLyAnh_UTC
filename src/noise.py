"""Sinh nhiễu trên ảnh xám float64 trong đoạn [0, 255]."""

import numpy as np

GAUSSIAN_SIGMAS = (10, 20, 30)
SALT_PEPPER_AMOUNTS = (0.05, 0.10, 0.20)
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


def add_salt_pepper_noise(
    image: np.ndarray,
    amount: float,
    seed: int = DEFAULT_SEED,
) -> np.ndarray:
    """Thay một phần điểm ảnh bằng muối (255) và tiêu (0).

    ``amount`` là tỉ lệ điểm ảnh bị hỏng, ba mức thí nghiệm là 5%, 10% và 20%.
    Số điểm hỏng được chia đều: một nửa muối, một nửa tiêu. Nếu số điểm lẻ thì
    tiêu nhận thêm một điểm. Cùng seed cho cùng một mẫu nhiễu.
    """
    source = np.asarray(image, dtype=np.float64).copy()
    corrupted = int(round(amount * source.size))
    if corrupted <= 0:
        return source
    corrupted = min(corrupted, source.size)

    salt_count = corrupted // 2
    pepper_count = corrupted - salt_count
    generator = np.random.default_rng(seed)
    chosen = generator.choice(source.size, size=corrupted, replace=False)

    flat = source.reshape(-1)
    flat[chosen[:salt_count]] = 255.0
    flat[chosen[salt_count : salt_count + pepper_count]] = 0.0
    return flat.reshape(source.shape)

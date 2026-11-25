"""PSNR và SSIM, data_range mặc định là 255."""

import cv2
import numpy as np


def mse(clean: np.ndarray, restored: np.ndarray) -> float:
    """Sai số bình phương trung bình trên toàn ảnh."""
    difference = np.asarray(clean, dtype=np.float64) - np.asarray(restored, dtype=np.float64)
    return float(np.mean(difference * difference))


def psnr(
    clean: np.ndarray,
    restored: np.ndarray,
    data_range: float = 255.0,
) -> float:
    """PSNR với miền giá trị ``data_range``. Ảnh giống hệt thì trả về inf."""
    error = mse(clean, restored)
    if error == 0.0:
        return float("inf")
    return float(10.0 * np.log10((float(data_range) ** 2) / error))


def ssim(
    clean: np.ndarray,
    restored: np.ndarray,
    data_range: float = 255.0,
) -> float:
    """SSIM cửa sổ đều 7×7, hiệp phương sai mẫu.

    K1 = 0,01 và K2 = 0,03. Cửa sổ không dùng trọng số Gauss.
    """
    window = 7
    source = np.asarray(clean, dtype=np.float64)
    estimate = np.asarray(restored, dtype=np.float64)
    kernel = (window, window)
    mu_source = cv2.blur(source, kernel)
    mu_estimate = cv2.blur(estimate, kernel)
    sample = (window * window) / (window * window - 1.0)
    var_source = sample * (cv2.blur(source * source, kernel) - mu_source * mu_source)
    var_estimate = sample * (
        cv2.blur(estimate * estimate, kernel) - mu_estimate * mu_estimate
    )
    covariance = sample * (
        cv2.blur(source * estimate, kernel) - mu_source * mu_estimate
    )
    c1 = (0.01 * float(data_range)) ** 2
    c2 = (0.03 * float(data_range)) ** 2
    numerator = (2.0 * mu_source * mu_estimate + c1) * (2.0 * covariance + c2)
    denominator = (
        (mu_source ** 2 + mu_estimate ** 2 + c1) * (var_source + var_estimate + c2)
    )
    return float(np.mean(numerator / denominator))

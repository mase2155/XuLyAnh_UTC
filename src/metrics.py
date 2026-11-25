import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def _validate_images(img_true: np.ndarray, img_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    arr_true = np.asarray(img_true, dtype=np.float64)
    arr_test = np.asarray(img_test, dtype=np.float64)
    if arr_true.shape != arr_test.shape:
        raise ValueError(f"Kích thước hai ảnh không khớp: {arr_true.shape} vs {arr_test.shape}")
    return arr_true, arr_test


def compute_psnr(img_true: np.ndarray, img_test: np.ndarray, data_range: float = 255.0) -> float:
    """Tính PSNR (dB) giữa ảnh gốc và ảnh kiểm tra với data_range = 255."""
    arr_true, arr_test = _validate_images(img_true, img_test)
    return float(peak_signal_noise_ratio(arr_true, arr_test, data_range=data_range))


def compute_ssim(img_true: np.ndarray, img_test: np.ndarray, data_range: float = 255.0) -> float:
    """Tính SSIM giữa ảnh gốc và ảnh kiểm tra với data_range = 255."""
    arr_true, arr_test = _validate_images(img_true, img_test)
    win_size = min(7, arr_true.shape[0], arr_true.shape[1])
    if win_size % 2 == 0:
        win_size -= 1
    if arr_true.ndim == 3 and arr_true.shape[-1] in (3, 4):
        return float(
            structural_similarity(
                arr_true,
                arr_test,
                data_range=data_range,
                channel_axis=-1,
                win_size=win_size,
            )
        )
    return float(structural_similarity(arr_true, arr_test, data_range=data_range, win_size=win_size))
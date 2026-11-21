"""Đọc ảnh đầu vào cho pipeline khử nhiễu."""

from pathlib import Path

import cv2
import numpy as np


def load_grayscale(path: str | Path) -> np.ndarray:
    """Đọc một ảnh và trả về mảng xám float64 trong đoạn [0, 255].

    Ảnh màu được chuyển sang xám. Ảnh float đã nằm trong [0, 1] được nhân 255.
    """
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(path)

    if image.ndim == 2:
        gray = image
    elif image.shape[2] == 4:
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    values = gray.astype(np.float64)
    if np.issubdtype(gray.dtype, np.floating) and values.size and float(values.max()) <= 1.0:
        values *= 255.0
    return np.clip(values, 0.0, 255.0)

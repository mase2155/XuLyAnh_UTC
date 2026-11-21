"""Hệ số đã khóa. h của NLM chỉ được tính từ file này."""

from src.noise import GAUSSIAN_SIGMAS

# h = NLM_H_FACTOR * σ. Giữ đúng 1.0, không chỉnh để khớp OpenCV.
NLM_H_FACTOR = 1.0


def nlm_h(sigma: float) -> float:
    """Độ suy giảm trọng số NLM: h = hệ số đã khóa nhân σ.

    Trọng số giữa hai patch là exp(-d² / h²). Ba mức Gauss 10, 20, 30
    cho h = 10, 20, 30.
    """
    if sigma < 0:
        raise ValueError("σ phải không âm")
    return NLM_H_FACTOR * float(sigma)


NLM_H_BY_SIGMA = {float(sigma): nlm_h(sigma) for sigma in GAUSSIAN_SIGMAS}

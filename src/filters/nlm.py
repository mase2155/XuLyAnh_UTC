"""Tham số Non-local Means đã khóa. Thuật toán gắn ở task sau."""

import numpy as np

NLM_PATCH_SIZE = 7
NLM_SEARCH_SIZE = 21
NLM_H_FACTOR = 1.0


def nlm_h(sigma: float) -> float:
    """Độ suy giảm trọng số, tỉ lệ thuận với độ lệch chuẩn nhiễu: h = σ.

    Trọng số giữa hai patch sẽ là exp(-d² / h²), với d² là trung bình
    bình phương hiệu mức xám trên patch 7×7. Cửa sổ tìm kiếm là 21×21.
    """
    if sigma < 0:
        raise ValueError("σ phải không âm")
    return NLM_H_FACTOR * float(sigma)

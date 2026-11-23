"""Demo: hai cột ảnh, crop biên, PSNR, SSIM và thời gian lọc."""

import sys
import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.filters.gaussian import gaussian_sigma
from src.io import load_grayscale
from src.noise import (
    DEFAULT_SEED,
    GAUSSIAN_SIGMAS,
    POISSON_PEAK,
    SALT_PEPPER_AMOUNTS,
    add_gaussian_noise,
    add_poisson_noise,
    add_salt_pepper_noise,
)
from src.params import nlm_h
from src.pipeline import METHODS, denoise
from src.recommend import recommendation_line

SAMPLE = ROOT / "data" / "set12" / "01.png"

NOISE_LABELS = {
    "gaussian": "Gauss",
    "salt_pepper": "Muối tiêu",
    "poisson": "Poisson",
}
FILTER_LABELS = {
    "mean": "Trung bình",
    "gaussian": "Gauss",
    "median": "Trung vị",
    "adaptive_median": "Trung vị thích nghi",
    "bilateral": "Song phương",
    "nlm": "NLM",
}


def load_upload(data: bytes, name: str):
    suffix = Path(name).suffix or ".png"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(data)
        path = Path(tmp.name)
    try:
        return load_grayscale(path)
    finally:
        path.unlink(missing_ok=True)


def add_noise(image, noise: str, level: float):
    if noise == "gaussian":
        return add_gaussian_noise(image, level, DEFAULT_SEED)
    if noise == "salt_pepper":
        return add_salt_pepper_noise(image, level, DEFAULT_SEED)
    return add_poisson_noise(image, POISSON_PEAK, DEFAULT_SEED)


def border_crop(image: np.ndarray, size: int = 100) -> np.ndarray:
    """Góc trên trái, sát biên ảnh. Cùng kích thước cho hai cột."""
    height, width = image.shape
    return image[: min(size, height), : min(size, width)]


def _psnr(clean: np.ndarray, restored: np.ndarray) -> float:
    mse = float(np.mean((clean - restored) ** 2))
    if mse == 0:
        return float("inf")
    return float(10.0 * np.log10((255.0 * 255.0) / mse))


def _ssim(clean: np.ndarray, restored: np.ndarray) -> float:
    """SSIM cửa sổ đều 7×7, data_range = 255."""
    window = 7
    clean = np.asarray(clean, dtype=np.float64)
    restored = np.asarray(restored, dtype=np.float64)
    kernel = (window, window)
    mu_clean = cv2.blur(clean, kernel)
    mu_restored = cv2.blur(restored, kernel)
    cov_norm = (window * window) / (window * window - 1.0)
    var_clean = cov_norm * (cv2.blur(clean * clean, kernel) - mu_clean * mu_clean)
    var_restored = cov_norm * (
        cv2.blur(restored * restored, kernel) - mu_restored * mu_restored
    )
    cov = cov_norm * (cv2.blur(clean * restored, kernel) - mu_clean * mu_restored)
    c1 = (0.01 * 255.0) ** 2
    c2 = (0.03 * 255.0) ** 2
    numerator = (2.0 * mu_clean * mu_restored + c1) * (2.0 * cov + c2)
    denominator = (mu_clean ** 2 + mu_restored ** 2 + c1) * (var_clean + var_restored + c2)
    return float(np.mean(numerator / denominator))


def image_scores(clean: np.ndarray, restored: np.ndarray) -> tuple[float, float]:
    """Dùng src.metrics khi có. Chưa có thì tính tại demo, data_range = 255."""
    try:
        from src.metrics import psnr, ssim
    except ImportError:
        return _psnr(clean, restored), _ssim(clean, restored)
    return float(psnr(clean, restored)), float(ssim(clean, restored))


def main() -> None:
    st.set_page_config(page_title="Khử nhiễu", layout="wide")
    st.title("Khử nhiễu ảnh")
    st.caption(f"Seed nhiễu cố định: {DEFAULT_SEED}.")

    source_mode = st.radio("Nguồn ảnh", ["Ảnh mẫu", "Tải ảnh"], horizontal=True)
    uploaded = None
    if source_mode == "Tải ảnh":
        uploaded = st.file_uploader(
            "Chọn ảnh",
            type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"],
        )

    noise = st.selectbox(
        "Loại nhiễu",
        list(NOISE_LABELS),
        format_func=lambda key: NOISE_LABELS[key],
    )
    if noise == "gaussian":
        level = float(st.select_slider("σ nhiễu", options=list(GAUSSIAN_SIGMAS), value=20))
    elif noise == "salt_pepper":
        level = float(
            st.select_slider(
                "Tỉ lệ muối tiêu",
                options=list(SALT_PEPPER_AMOUNTS),
                value=0.10,
                format_func=lambda value: f"{int(round(value * 100))}%",
            )
        )
    else:
        level = float(POISSON_PEAK)
        st.caption(f"Poisson peak = {POISSON_PEAK:g}.")

    method = st.selectbox(
        "Bộ lọc",
        list(METHODS),
        format_func=lambda key: FILTER_LABELS[key],
    )
    size = 3
    sigma = None
    sigma_color = 25.0
    if method in ("mean", "gaussian", "median"):
        size = int(st.select_slider("Cửa sổ", options=[3, 5], value=3))
    if method == "gaussian":
        st.caption(f"σ của nhân = {gaussian_sigma(size):g}.")
    elif method == "bilateral":
        sigma_color = float(
            st.select_slider("sigmaColor", options=[25.0, 50.0, 75.0], value=25.0)
        )
        st.caption("Đường kính 9. sigmaSpace = 5.")
    elif method == "adaptive_median":
        st.caption("Cửa sổ tối đa 7.")
    elif method == "nlm":
        if noise == "gaussian":
            sigma = level
        else:
            sigma = float(st.select_slider("σ để tính h", options=list(GAUSSIAN_SIGMAS), value=20))
        st.caption(f"h = {nlm_h(sigma):g}. Patch 7, search 21.")

    if source_mode == "Ảnh mẫu":
        if not SAMPLE.is_file():
            st.error("Chưa có ảnh mẫu data/set12/01.png.")
            st.stop()
        image = load_grayscale(SAMPLE)
        source_name = "Set12 01.png"
    elif uploaded is None:
        st.info("Hãy tải một ảnh.")
        st.stop()
    else:
        image = load_upload(uploaded.getvalue(), uploaded.name)
        source_name = uploaded.name

    noisy = add_noise(image, noise, level)
    started = time.perf_counter()
    with st.spinner("Đang lọc..."):
        output = denoise(
            noisy,
            method,
            size=size,
            sigma=sigma,
            sigma_color=sigma_color,
        )
    elapsed = time.perf_counter() - started
    psnr_db, ssim_value = image_scores(image, output)

    height, width = output.shape
    noisy_view = noisy.astype(np.uint8)
    output_view = output.astype(np.uint8)
    noisy_edge = border_crop(noisy_view)
    output_edge = border_crop(output_view)
    psnr_text = "∞" if psnr_db == float("inf") else f"{psnr_db:.2f}"

    st.caption(
        f"{source_name}: {width}×{height}. "
        f"PSNR {psnr_text} dB. SSIM {ssim_value:.4f}. Thời gian {elapsed:.3f} s."
    )
    st.caption(recommendation_line(noise, level))
    full_left, full_right = st.columns(2)
    full_left.image(noisy_view, caption="Ảnh nhiễu")
    full_right.image(output_view, caption="Sau lọc")
    st.caption(f"Crop biên, góc trên trái, {noisy_edge.shape[1]}×{noisy_edge.shape[0]}.")
    crop_left, crop_right = st.columns(2)
    crop_left.image(noisy_edge, caption="Biên, ảnh nhiễu")
    crop_right.image(output_edge, caption="Biên, sau lọc")


if __name__ == "__main__":
    main()

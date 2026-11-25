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
PHONE_DIR = ROOT / "data" / "phone"
PHONE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

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


def list_phone_images() -> list[Path]:
    if not PHONE_DIR.is_dir():
        return []
    return sorted(
        path
        for path in PHONE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in PHONE_SUFFIXES
    )


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


def image_scores(clean: np.ndarray, restored: np.ndarray) -> tuple[float, float]:
    """PSNR và SSIM từ src.metrics, data_range = 255."""
    from src.metrics import psnr, ssim

    return float(psnr(clean, restored)), float(ssim(clean, restored))


def main() -> None:
    st.set_page_config(page_title="Khử nhiễu", layout="wide")
    st.title("Khử nhiễu ảnh")

    source_mode = st.radio(
        "Nguồn ảnh",
        ["Ảnh mẫu", "Tải ảnh", "Ảnh điện thoại"],
        horizontal=True,
    )
    has_reference = source_mode != "Ảnh điện thoại"
    uploaded = None
    phone_path = None
    if source_mode == "Tải ảnh":
        uploaded = st.file_uploader(
            "Chọn ảnh",
            type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"],
        )
    elif source_mode == "Ảnh điện thoại":
        phone_paths = list_phone_images()
        if not phone_paths:
            st.info(
                "Hãy để 8–15 ảnh điện thoại vào data/phone. "
                "Những ảnh này không có ảnh sạch và không được tính PSNR."
            )
            st.stop()
        phone_path = st.selectbox(
            "Ảnh điện thoại",
            phone_paths,
            format_func=lambda path: path.name,
        )
        st.caption(f"{len(phone_paths)} ảnh trong data/phone. Không tính PSNR.")

    noise = None
    level = None
    if has_reference:
        st.caption(f"Seed nhiễu cố định: {DEFAULT_SEED}.")
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
    elif source_mode == "Tải ảnh":
        if uploaded is None:
            st.info("Hãy tải một ảnh.")
            st.stop()
        image = load_upload(uploaded.getvalue(), uploaded.name)
        source_name = uploaded.name
    else:
        image = load_grayscale(phone_path)
        source_name = phone_path.name

    source_for_filter = add_noise(image, noise, level) if has_reference else image
    started = time.perf_counter()
    with st.spinner("Đang lọc..."):
        output = denoise(
            source_for_filter,
            method,
            size=size,
            sigma=sigma,
            sigma_color=sigma_color,
        )
    elapsed = time.perf_counter() - started

    height, width = output.shape
    input_view = source_for_filter.astype(np.uint8)
    output_view = output.astype(np.uint8)
    input_edge = border_crop(input_view)
    output_edge = border_crop(output_view)
    if has_reference:
        psnr_db, ssim_value = image_scores(image, output)
        psnr_text = "∞" if psnr_db == float("inf") else f"{psnr_db:.2f}"
        st.caption(
            f"{source_name}: {width}×{height}. "
            f"PSNR {psnr_text} dB. SSIM {ssim_value:.4f}. Thời gian {elapsed:.3f} s."
        )
        st.caption(recommendation_line(noise, level))
        input_caption = "Ảnh nhiễu"
        edge_caption = "Biên, ảnh nhiễu"
    else:
        st.caption(
            f"{source_name}: {width}×{height}. "
            f"Không có ảnh sạch. Không tính PSNR, SSIM. Thời gian {elapsed:.3f} s."
        )
        input_caption = "Ảnh điện thoại"
        edge_caption = "Biên, ảnh điện thoại"
    full_left, full_right = st.columns(2)
    full_left.image(input_view, caption=input_caption)
    full_right.image(output_view, caption="Sau lọc")
    st.caption(f"Crop biên, góc trên trái, {input_edge.shape[1]}×{input_edge.shape[0]}.")
    crop_left, crop_right = st.columns(2)
    crop_left.image(input_edge, caption=edge_caption)
    crop_right.image(output_edge, caption="Biên, sau lọc")


if __name__ == "__main__":
    main()

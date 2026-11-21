"""Demo: tải ảnh, chọn nhiễu, chọn bộ lọc, kéo thanh trượt."""

import sys
import tempfile
from pathlib import Path

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


def main() -> None:
    st.set_page_config(page_title="Khử nhiễu", layout="centered")
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
    with st.spinner("Đang lọc..."):
        output = denoise(
            noisy,
            method,
            size=size,
            sigma=sigma,
            sigma_color=sigma_color,
        )

    height, width = output.shape
    st.caption(f"{source_name}: {width}×{height}. Đã thêm nhiễu và đã lọc.")
    st.image(output.astype("uint8"), clamp=True)


if __name__ == "__main__":
    main()
else:
    main()

"""Một lệnh ghi bảng chương 4 vào results/bsd68_summary.csv."""

import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.io import load_grayscale
from src.noise import (
    DEFAULT_SEED,
    POISSON_PEAK,
    add_gaussian_noise,
    add_poisson_noise,
    add_salt_pepper_noise,
)
from src.pipeline import METHODS, denoise

DATA_DIR = ROOT / "data" / "bsd68"
OUTPUT = ROOT / "results" / "bsd68_summary.csv"
CHOSEN = ROOT / "results" / "chosen_params.csv"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

NOISE_LEVELS = (
    ("gaussian", 10.0),
    ("gaussian", 20.0),
    ("gaussian", 30.0),
    ("salt_pepper", 0.05),
    ("salt_pepper", 0.10),
    ("salt_pepper", 0.20),
    ("poisson", POISSON_PEAK),
)


def list_images(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )


def add_noise(image: np.ndarray, noise: str, level: float) -> np.ndarray:
    if noise == "gaussian":
        return add_gaussian_noise(image, level, DEFAULT_SEED)
    if noise == "salt_pepper":
        return add_salt_pepper_noise(image, level, DEFAULT_SEED)
    return add_poisson_noise(image, level, DEFAULT_SEED)


def load_chosen(path: Path = CHOSEN) -> dict[tuple[str, str, str], dict]:
    """Tham số đã chọn trên Set12. Khóa là nhiễu, mức, phương pháp."""
    if not path.is_file():
        return {}
    chosen = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            chosen[(row["noise"], f"{float(row['level']):g}", row["method"])] = json.loads(row["params"])
    return chosen


def filter_kwargs(method: str, noise: str, level: float, chosen: dict | None = None) -> dict:
    if chosen:
        params = chosen.get((noise, f"{float(level):g}", method))
        if params is not None:
            return params
    if method in ("mean", "median"):
        return {"size": 5}
    if method == "gaussian":
        return {"size": 5, "sigma": 1.1}
    if method == "bilateral":
        return {"sigma_color": 25.0}
    if method == "nlm":
        sigma = level if noise == "gaussian" else 20.0
        return {"sigma": sigma}
    return {}


def image_scores(clean: np.ndarray, restored: np.ndarray) -> tuple[float, float]:
    from src.metrics import psnr, ssim

    return float(psnr(clean, restored)), float(ssim(clean, restored))


def summarize(scores: dict[tuple[str, float, str], list[float]]) -> list[dict[str, str]]:
    rows = []
    for noise, level in NOISE_LEVELS:
        for method in METHODS:
            values = scores.get((noise, level, method), [])
            if not values:
                continue
            mean = sum(values) / len(values)
            if len(values) > 1:
                variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
                spread = variance ** 0.5
                spread_text = f"{spread:.4f}"
            else:
                spread_text = ""
            rows.append(
                {
                    "noise": noise,
                    "level": f"{level:g}",
                    "method": method,
                    "psnr_mean": f"{mean:.4f}",
                    "psnr_std": spread_text,
                }
            )
    return rows


def write_table(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("noise", "level", "method", "psnr_mean", "psnr_std"),
        )
        writer.writeheader()
        writer.writerows(rows)


def evaluate(paths: list[Path]) -> list[dict[str, str]]:
    chosen = load_chosen()
    scores: dict[tuple[str, float, str], list[float]] = {}
    for path in paths:
        clean = load_grayscale(path)
        for noise, level in NOISE_LEVELS:
            noisy = add_noise(clean, noise, level)
            for method in METHODS:
                restored = denoise(noisy, method, filter_kwargs(method, noise, level, chosen))
                psnr_db, _ssim_value = image_scores(clean, restored)
                scores.setdefault((noise, level, method), []).append(psnr_db)
    return summarize(scores)


def main() -> int:
    paths = list_images(DATA_DIR)
    if not paths:
        print(
            "Chưa có ảnh trong data/bsd68. Bảng chương 4 cần bộ BSD68.",
            file=sys.stderr,
        )
        return 1
    rows = evaluate(paths)
    write_table(rows, OUTPUT)
    print(f"Đã ghi {OUTPUT.relative_to(ROOT)} từ {len(paths)} ảnh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

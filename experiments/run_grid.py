"""Chạy lưới khử nhiễu và ghi CSV từng ảnh.

Cột: image, noise, level, method, params, psnr, ssim, ms.
Seed nhiễu là 42.
"""

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.io import load_grayscale
from src.metrics import psnr, ssim
from src.noise import (
    DEFAULT_SEED,
    POISSON_PEAK,
    add_gaussian_noise,
    add_poisson_noise,
    add_salt_pepper_noise,
)
from src.pipeline import denoise

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
COLUMNS = ("image", "noise", "level", "method", "params", "psnr", "ssim", "ms")

TUNING_CONFIGS = (
    ("mean", {"size": 3}),
    ("mean", {"size": 5}),
    ("gaussian", {"size": 3, "sigma": 0.8}),
    ("gaussian", {"size": 5, "sigma": 1.1}),
    ("median", {"size": 3}),
    ("median", {"size": 5}),
    ("adaptive_median", {}),
    ("bilateral", {"sigma_color": 25.0}),
    ("bilateral", {"sigma_color": 50.0}),
    ("bilateral", {"sigma_color": 75.0}),
    ("nlm", {"sigma": 10.0}),
    ("nlm", {"sigma": 20.0}),
    ("nlm", {"sigma": 30.0}),
)

ALL_LEVELS = (
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
    if noise == "poisson":
        return add_poisson_noise(image, level, DEFAULT_SEED)
    raise ValueError(f"không có nhiễu {noise}")


def params_text(params: dict) -> str:
    return json.dumps(params, sort_keys=True, separators=(",", ":"))


def load_configs(path: Path | None) -> tuple[tuple[str, dict], ...]:
    if path is None:
        return TUNING_CONFIGS
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    configs = []
    for row in rows:
        configs.append((row["method"], json.loads(row["params"] or "{}")))
    return tuple(configs)


def iter_rows(paths: list[Path], levels, configs):
    for path in paths:
        clean = load_grayscale(path)
        for noise, level in levels:
            noisy = add_noise(clean, noise, level)
            for method, params in configs:
                started = time.perf_counter()
                restored = denoise(noisy, method, params)
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                yield {
                    "image": path.name,
                    "noise": noise,
                    "level": f"{level:g}",
                    "method": method,
                    "params": params_text(params),
                    "psnr": f"{psnr(clean, restored):.6f}",
                    "ssim": f"{ssim(clean, restored):.6f}",
                    "ms": f"{elapsed_ms:.3f}",
                }


def write_rows(rows, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--configs", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--noises", default="")
    parser.add_argument("--levels", default="")
    parser.add_argument("--methods", default="")
    args = parser.parse_args()

    paths = list_images(args.data)
    if args.limit:
        paths = paths[: args.limit]
    if not paths:
        print(f"Chưa có ảnh trong {args.data}.", file=sys.stderr)
        return 1

    levels = list(ALL_LEVELS)
    if args.noises:
        allowed = set(args.noises.split(","))
        levels = [item for item in levels if item[0] in allowed]
    if args.levels:
        allowed_levels = {float(item) for item in args.levels.split(",")}
        levels = [item for item in levels if item[1] in allowed_levels]
    configs = load_configs(args.configs)
    if args.methods:
        allowed_methods = set(args.methods.split(","))
        configs = tuple(item for item in configs if item[0] in allowed_methods)

    rows = list(iter_rows(paths, levels, configs))
    write_rows(rows, args.output)
    print(f"Đã ghi {len(rows)} dòng vào {args.output}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

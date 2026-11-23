"""Sinh ảnh mẫu rồi ghi results/sample_summary.csv.

Ảnh do script này vẽ, không phải BSD68, Set12 hay ảnh điện thoại.
Bảng chương 4 vẫn chỉ đọc data/bsd68. Khi thư mục đó có ảnh,
dùng experiments/run_chapter4.py.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.run_chapter4 import evaluate, write_table

SAMPLE_DIR = ROOT / "data" / "samples"
OUTPUT = ROOT / "results" / "sample_summary.csv"


def _save(name: str, image: np.ndarray) -> Path:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    path = SAMPLE_DIR / name
    gray = np.rint(np.clip(image, 0.0, 255.0)).astype(np.uint8)
    if not cv2.imwrite(str(path), gray):
        raise RuntimeError(f"không ghi được {path}")
    return path


def make_samples() -> list[Path]:
    """Bốn ảnh xám cố định, có cả kích thước chẵn và lẻ."""
    height = np.linspace(0.0, 255.0, 80, dtype=np.float64)[:, None]
    width = np.linspace(0.0, 40.0, 120, dtype=np.float64)[None, :]
    ramp = np.clip(height * 0.7 + width, 0.0, 255.0)

    edge = np.full((81, 121), 25.0, dtype=np.float64)
    edge[:, 60:] = 210.0
    edge[28:52, 60:96] = 70.0

    stripes = np.full((64, 64), 20.0, dtype=np.float64)
    stripes[:, 4::8] = 230.0
    stripes[:, 5::8] = 230.0
    stripes[24:40, :] = 110.0

    yy, xx = np.mgrid[0:48, 0:47]
    blob = 255.0 * np.exp(-((yy - 24.0) ** 2 + (xx - 20.0) ** 2) / 90.0)

    return [
        _save("ramp_80x120.png", ramp),
        _save("edge_81x121.png", edge),
        _save("stripes_64x64.png", stripes),
        _save("blob_48x47.png", blob),
    ]


def main() -> int:
    paths = make_samples()
    rows = evaluate(paths)
    write_table(rows, OUTPUT)
    print(f"Đã ghi {len(paths)} ảnh mẫu vào {SAMPLE_DIR.relative_to(ROOT)}.")
    print(f"Đã ghi {OUTPUT.relative_to(ROOT)}. Đây không phải bảng BSD68.")
    print(f"{len(rows)} dòng. Cột giống bảng chương 4: noise, level, method, psnr_mean, psnr_std.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

import csv
from pathlib import Path
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from src.metrics import compute_psnr, compute_ssim

INPUT_DIR = Path("D:/xử lý ảnh")
OUTPUT_CSV = Path("results/verify_metrics.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

rows = []
for img_path in sorted(INPUT_DIR.glob("*.png"))[:10]:
    img = np.asarray(Image.open(img_path), dtype=np.float64)
    noisy = np.clip(img + np.random.default_rng(42).normal(0, 15, size=img.shape), 0, 255)

    psnr_custom = compute_psnr(img, noisy, data_range=255.0)
    psnr_ref = float(peak_signal_noise_ratio(img, noisy, data_range=255.0))

    if img.ndim == 3 and img.shape[-1] in (3, 4):
        ssim_custom = compute_ssim(img, noisy, data_range=255.0)
        ssim_ref = float(structural_similarity(img, noisy, data_range=255.0, channel_axis=-1))
    else:
        ssim_custom = compute_ssim(img, noisy, data_range=255.0)
        ssim_ref = float(structural_similarity(img, noisy, data_range=255.0))

    rows.append({
        "filename": img_path.name,
        "psnr_custom": round(psnr_custom, 6),
        "psnr_skimage": round(psnr_ref, 6),
        "psnr_diff": abs(psnr_custom - psnr_ref),
        "ssim_custom": round(ssim_custom, 6),
        "ssim_skimage": round(ssim_ref, 6),
        "ssim_diff": abs(ssim_custom - ssim_ref),
    })

with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["filename", "psnr_custom", "psnr_skimage", "psnr_diff", "ssim_custom", "ssim_skimage", "ssim_diff"],
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Đã ghi kết quả đối chiếu vào {OUTPUT_CSV}")
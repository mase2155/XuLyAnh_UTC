import csv
from pathlib import Path
from PIL import Image

# Chỉnh lại đường dẫn thư mục chứa ảnh của bạn nếu cần (ví dụ: D:/xử lý ảnh hoặc thư mục trong repo)
IMAGE_DIRS = [
    Path("D:/xử lý ảnh"),
]
OUTPUT_CSV = Path("data/manifest.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

rows = []
for folder in IMAGE_DIRS:
    if not folder.exists():
        continue
    for img_path in sorted(folder.rglob("*")):
        if img_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
            with Image.open(img_path) as im:
                width, height = im.size
            # Xác định tên tập dữ liệu dựa trên tên thư mục hoặc tên file
            dataset_name = folder.name
            rows.append({
                "filename": img_path.name,
                "width": width,
                "height": height,
                "dataset": dataset_name,
            })

with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "width", "height", "dataset"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Đã ghi {len(rows)} dòng vào {OUTPUT_CSV}")
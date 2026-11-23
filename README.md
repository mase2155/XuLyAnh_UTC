# XuLyAnh_UTC

Môn học Xử Lý Ảnh được giảng dạy tại Đại Học Giao Thông Vận Tải.

Bảng chương 4 chạy lại bằng một lệnh, từ thư mục gốc của repo:

```
.\.venv\Scripts\python.exe experiments/run_chapter4.py
```

Lệnh đọc ảnh trong `data/bsd68`, sinh nhiễu với seed 42, chạy sáu bộ lọc đã khóa, rồi ghi `results/bsd68_summary.csv`. Các cột là `noise`, `level`, `method`, `psnr_mean`, `psnr_std`.

Ảnh mẫu để chạy thử khung, trước khi có BSD68:

```
.\.venv\Scripts\python.exe experiments/run_samples.py
```

Lệnh này tự vẽ bốn ảnh xám trong `data/samples` và ghi `results/sample_summary.csv`. File đó không phải bảng chương 4.

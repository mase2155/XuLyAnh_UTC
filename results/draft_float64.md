# Vì sao pipeline tính trên float64

Ảnh đọc từ file thường là uint8, mỗi điểm là số nguyên 0 đến 255. Phép trừ trên uint8 bị cuộn theo modulo 256. Ví dụ \(10 - 20\) không ra \(-10\) mà ra 246. PSNR tính trên số đã cuộn sẽ sai.

`denoise` trong `src/pipeline.py` đổi ảnh sang float64 trước khi lọc. NaN thành 0, +inf thành 255, −inf thành 0, rồi cắt về [0, 255]. Một điểm không hữu hạn nếu đi vào NLM sẽ làm ảnh tích phân thành NaN và kéo cả ảnh thành NaN.

Ảnh ra cũng là float64, cùng kích thước ảnh vào, và được cắt lại về [0, 255]. Không ép mọi ảnh về một cỡ vì BSD68 có cả 481×321 và 321×481.

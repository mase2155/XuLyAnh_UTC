Cùng crop 64×64, nhiễu Gauss σ = 20, patch 7, search 21, và cùng số h = 20.

| | Sai tuyệt đối lớn nhất | Sai tuyệt đối trung bình |
|---|---|---|
| So với `cv2.fastNlMeansDenoising` | 7.940 | 0.285 |

Điểm (32, 32): bộ lọc tự viết ra 84.549, OpenCV ra 84.

Công thức tự viết là `w = exp(-d² / h²)`, với `d²` là trung bình bình phương hiệu đúng trên patch và `h = σ`.

OpenCV 5.1 cũng viết `w = exp(-dist / h²)` cho ảnh xám, nhưng `dist` không phải `d²` đúng. Tổng bình phương trên patch 7×7 (49 điểm) được dịch bit sang lũy thừa 2 gần nhất, là 64, rồi mới đưa về trung bình. Trọng số nhỏ hơn 0.001 bị đặt bằng 0. Ảnh vào và ảnh ra là `uint8`, phép chia có làm tròn.

Vì vậy cùng một số h không cho cùng một ảnh. Không chỉnh `h` của nhóm để ép trùng OpenCV.

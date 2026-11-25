# Nháp: BM3D là mốc thư viện

Sáu bộ lọc tự viết là đối tượng cần so sánh. BM3D không được viết lại. Nó là mốc thư viện, cùng vai trò với các hàm OpenCV đã dùng để kiểm tra từng lọc, nhưng ở mức cả thuật toán khử nhiễu.

BM3D do Dabov, Foi, Katkovnik và Egiazarian công bố năm 2007. Ý chính là gom các khối ảnh giống nhau, biến đổi, rồi lọc chung trong miền biến đổi trước khi trả khối về chỗ cũ. Vì dùng sự giống nhau không chỉ ở lân cận liền kề, BM3D thường giữ chi tiết tốt hơn lọc trung bình và lọc Gauss.

Trong repo, lời gọi là `bm3d.bm3d` từ gói `bm3d` 4.0.3. Ảnh thử là `data/set12/01.png`, nhiễu Gauss σ = 20, seed 42. PSNR của ảnh nhiễu là 22,43 dB. PSNR sau BM3D là 30,43 dB. Số này là một lần chạy trên một ảnh, chưa phải trung bình BSD68.

BM3D không vào bảng khuyến nghị nếu bảng đó chỉ xếp sáu lọc tự viết. Khi chương 4 có đủ BSD68, BM3D được ghi thêm một cột mốc để thấy sáu lọc tự viết còn cách mốc thư viện bao nhiêu, không phải để chỉnh tham số cho trùng BM3D.

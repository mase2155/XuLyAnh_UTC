# Nháp công thức PSNR, MSE, SSIM cho chương 2

Ảnh sạch là \(x\), ảnh sau lọc là \(\hat x\). Cả hai là ảnh xám float64, \(N\) điểm, data_range = 255. Hàm nằm trong `src/metrics.py`.

## MSE

\[
\mathrm{MSE} = \frac{1}{N}\sum_{i=1}^{N}(x_i - \hat x_i)^2
\]

MSE bằng 0 khi hai ảnh trùng nhau. MSE càng nhỏ thì hai ảnh càng gần nhau.

## PSNR

\[
\mathrm{PSNR} = 10\log_{10}\frac{255^2}{\mathrm{MSE}}
\]

Đơn vị là dB. PSNR càng lớn càng tốt. Nếu MSE = 0 thì hàm trả về vô cực, vì không còn sai số để lấy log.

## SSIM

Cửa sổ đều 7×7, không dùng trọng số Gauss. \(\mu\) là trung bình cửa sổ, \(\sigma^2\) là phương sai mẫu, \(\sigma_{x\hat x}\) là hiệp phương sai mẫu. Hệ số mẫu là \(49/48\).

\[
\mathrm{SSIM} = \frac{(2\mu_x\mu_{\hat x}+C_1)(2\sigma_{x\hat x}+C_2)}{(\mu_x^2+\mu_{\hat x}^2+C_1)(\sigma_x^2+\sigma_{\hat x}^2+C_2)}
\]

\(C_1 = (0{,}01 \times 255)^2\), \(C_2 = (0{,}03 \times 255)^2\). Chỉ số báo cáo là trung bình SSIM trên toàn ảnh. Giá trị càng lớn càng giống về cấu trúc. Công thức này là bản cửa sổ đều, sẽ đối chiếu với scikit-image trong `results/verify_metrics.csv`.

# Phân cảnh video demo, khoảng 6 phút

Đây là kịch bản để quay. Repo không chứa file video.

1. Mở demo bằng `.\.venv\Scripts\python.exe -m streamlit run app/demo.py`. Chọn nguồn Ảnh mẫu. Nói đây là Set12 `01.png`, ảnh xám. (30 giây)
2. Chọn nhiễu Gauss σ = 20. Để lọc trung bình, cửa sổ 5, rồi đổi sang Gauss cửa sổ 5, sigma 1,1. Chỉ PSNR và SSIM trên ảnh. (70 giây)
3. Đổi nhiễu muối tiêu 10%. Chọn lọc trung vị cửa sổ 5, rồi trung vị thích nghi. Nói cửa sổ thích nghi dừng ở 7 và giữ điểm nếu pha A thất bại. (70 giây)
4. Đổi lại Gauss σ = 20. Chọn song phương, sigma_color 25, rồi NLM. Nói patch 7, search 21, h bằng σ. (70 giây)
5. Nếu `results/bsd68_summary.csv` đã có, đọc dòng khuyến nghị trên màn hình và nói số đó lấy từ trung bình BSD68, không lấy từ ảnh đang mở. (40 giây)
6. Chọn nguồn Ảnh điện thoại. Nếu `data/phone` trống, dừng ở câu thông báo thư mục trống. Nói chế độ này không sinh nhiễu và không hiện PSNR. (40 giây)
7. Chỉ file `experiments/run_chapter4.py` và `results/bsd68_summary.csv` trong thư mục, rồi kết. (30 giây)

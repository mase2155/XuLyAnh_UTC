# Nhận xét nháp hai đường cong tham số trên Set12

Hai hình chỉ vẽ nhiễu Gauss. Mỗi điểm là PSNR trung bình 12 ảnh. h của NLM bằng tham số sigma đưa vào hàm, vì NLM_H_FACTOR = 1.

## NLM, results/sweep_nlm.png

Đỉnh của mỗi đường nằm đúng tại h bằng σ của nhiễu.

- Gauss σ = 10: h = 10 cho 32,43 dB, h = 20 cho 29,66 dB, h = 30 cho 26,80 dB.
- Gauss σ = 20: h = 20 cho 28,99 dB. h = 10 tụt xuống 22,88 dB, h = 30 còn 26,86 dB.
- Gauss σ = 30: h = 30 cho 26,72 dB, cao hơn h = 20 (24,23 dB) và h = 10 (18,82 dB).

h nhỏ hơn σ thì lọc chưa đủ. h lớn hơn σ thì lọc mạnh hơn mức nhiễu và PSNR giảm.

## Song phương, results/sweep_bilateral.png

sigma_color được chọn tăng theo σ.

- Gauss σ = 10: sigma_color 25 cho 31,82 dB, rồi 29,13 dB và 27,19 dB khi sigma_color lên 50 và 75.
- Gauss σ = 20: đỉnh ở sigma_color 50, 28,10 dB. Hai đầu 25 và 75 đều khoảng 26,9 dB.
- Gauss σ = 30: sigma_color 75 cho 25,98 dB, nhích hơn 50 (25,51 dB). sigma_color 25 chỉ còn 21,93 dB.

## Muối tiêu không nằm trên hai hình

Trên muối tiêu, bộ sigma_color cao nhất trong ba mức vẫn thua trung vị thích nghi. Ví dụ muối tiêu 10%: song phương sigma_color 75 đạt 19,58 dB, trong khi trung vị thích nghi đạt 32,51 dB. Đường cong song phương vì thế chỉ dùng để chọn sigma_color, không phải để chọn lọc cho xung.

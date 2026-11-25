# Tham số đã chọn trên Set12

Mỗi ô là một bộ (nhiễu, mức, phương pháp). Tham số được chọn là bộ có PSNR trung bình cao nhất trên 12 ảnh Set12.
Nếu hai bộ bằng nhau đến số đã tính thì giữ bộ đứng trước trong TUNING_CONFIGS của experiments/run_grid.py.
BSD68 không tham gia lần chọn này. Seed nhiễu là 42.

## gaussian 10

- mean {"size":3}: 27.9268 ± 2.4256 dB
- gaussian {"sigma":0.8,"size":3}: 29.6974 ± 2.0842 dB
- median {"size":3}: 28.4048 ± 2.5480 dB
- adaptive_median {}: 28.7171 ± 1.2480 dB
- bilateral {"sigma_color":25.0}: 31.8231 ± 0.8650 dB
- nlm {"sigma":10.0}: 32.4319 ± 1.0118 dB ← cao nhất trong ô nhiễu

## gaussian 20

- mean {"size":3}: 26.5903 ± 1.7780 dB
- gaussian {"sigma":0.8,"size":3}: 27.4188 ± 1.2339 dB
- median {"size":3}: 26.1907 ± 1.5771 dB
- adaptive_median {}: 24.3173 ± 0.4898 dB
- bilateral {"sigma_color":50.0}: 28.1049 ± 1.0304 dB
- nlm {"sigma":20.0}: 28.9898 ± 1.2456 dB ← cao nhất trong ô nhiễu

## gaussian 30

- mean {"size":3}: 25.0962 ± 1.2679 dB
- gaussian {"sigma":1.1,"size":5}: 25.6463 ± 1.5214 dB
- median {"size":5}: 24.4146 ± 1.7021 dB
- adaptive_median {}: 21.3845 ± 0.2529 dB
- bilateral {"sigma_color":75.0}: 25.9821 ± 1.0966 dB
- nlm {"sigma":30.0}: 26.7162 ± 1.2497 dB ← cao nhất trong ô nhiễu

## salt_pepper 0.05

- mean {"size":3}: 24.6781 ± 1.2890 dB
- gaussian {"sigma":1.1,"size":5}: 25.2385 ± 1.5074 dB
- median {"size":3}: 29.3517 ± 3.2299 dB
- adaptive_median {}: 33.2930 ± 3.8402 dB ← cao nhất trong ô nhiễu
- bilateral {"sigma_color":75.0}: 22.6844 ± 1.2450 dB
- nlm {"sigma":30.0}: 25.3713 ± 1.4063 dB

## salt_pepper 0.1

- mean {"size":5}: 22.9743 ± 1.5704 dB
- gaussian {"sigma":1.1,"size":5}: 23.4578 ± 1.1427 dB
- median {"size":3}: 28.6298 ± 2.9899 dB
- adaptive_median {}: 32.5108 ± 3.6077 dB ← cao nhất trong ô nhiễu
- bilateral {"sigma_color":75.0}: 19.5768 ± 1.1003 dB
- nlm {"sigma":30.0}: 21.0552 ± 1.3581 dB

## salt_pepper 0.2

- mean {"size":5}: 21.1211 ± 1.2566 dB
- gaussian {"sigma":1.1,"size":5}: 20.9141 ± 0.9052 dB
- median {"size":3}: 26.0015 ± 2.0499 dB
- adaptive_median {}: 30.6522 ± 3.1710 dB ← cao nhất trong ô nhiễu
- bilateral {"sigma_color":75.0}: 15.6172 ± 0.8726 dB
- nlm {"sigma":30.0}: 13.5827 ± 0.4952 dB

## poisson 255

- mean {"size":3}: 27.8048 ± 2.3515 dB
- gaussian {"sigma":0.8,"size":3}: 29.4663 ± 1.9761 dB
- median {"size":3}: 28.1788 ± 2.4177 dB
- adaptive_median {}: 28.0490 ± 1.4808 dB
- bilateral {"sigma_color":25.0}: 31.2905 ± 0.8160 dB ← cao nhất trong ô nhiễu
- nlm {"sigma":10.0}: 31.2839 ± 1.2104 dB

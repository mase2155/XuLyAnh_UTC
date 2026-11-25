# Đối chiếu tên tham số chương 2 với mã

Đã đọc lại chương 2 trong `Bao cao De 2.docx` và đối với từng tên trong mã. Các tên dưới đây khớp.

| Trong chương 2 | Trong mã |
| --- | --- |
| size 3 hoặc 5 | `size` của mean, gaussian, median |
| sigma 0,8 khi size 3; sigma 1,1 khi size 5 | `gaussian_sigma` trong `src/filters/gaussian.py` |
| reflect, cùng nghĩa BORDER_REFLECT_101 | `np.pad(..., mode="reflect")` |
| σ Gauss 10, 20, 30 | `GAUSSIAN_SIGMAS` |
| muối tiêu 0,05, 0,10, 0,20 | `SALT_PEPPER_AMOUNTS` |
| peak 255 | `POISSON_PEAK` |
| seed 42 | `DEFAULT_SEED` |
| cửa sổ thích nghi tối đa 7, thất bại thì giữ zxy | `ADAPTIVE_MEDIAN_MAX_SIZE = 7` |
| đường kính 9, bán kính 4, sigmaSpace 5 | `BILATERAL_DIAMETER`, `BILATERAL_SIGMA_SPACE` |
| sigma_color 25, 50, 75 | `BILATERAL_SIGMA_COLORS` |
| patch 7, search 21 | `NLM_PATCH_SIZE`, `NLM_SEARCH_SIZE` |
| h = 1,0 × sigma | `NLM_H_FACTOR` trong `src/params.py` |
| data_range 255 | đối số mặc định của `psnr` và `ssim` |
| cửa sổ SSIM 7×7, hệ số mẫu 49/48, K1 = 0,01, K2 = 0,03 | `src/metrics.py` |

Không thấy tên trong chương 2 chỉ một tham số khác với mã. `sigma` của NLM là độ lệch chuẩn đưa vào `nlm_h`, không phải sigma của nhân Gauss.

# Dữ liệu khử nhiễu

Ảnh trong thư mục này không được đưa lên git. File này chỉ ghi nguồn, số lượng, kích thước và điều kiện dùng.

## BSD68

- Số ảnh trong `data/bsd68`: 68 ảnh xám.
- Kích thước đo trên file: 53 ảnh 481×321, 15 ảnh 321×481.
- Nguồn file: testsets/BSD68 của FFDNet, https://github.com/cszn/FFDNet/tree/master/testsets/BSD68
- Bộ gốc: Berkeley Segmentation Dataset, https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/
- 68 ảnh là tập kiểm tra mà Roth và Black dùng trong bài Fields of Experts (CVPR 2005).
- Điều kiện dùng của trang Berkeley: được tải cho nghiên cứu và giáo dục phi thương mại. Bài dùng bộ này cần trích Martin, Fowlkes, Tal, Malik, ICCV 2001.

## Set12

- Số ảnh trong `data/set12`: 12 ảnh xám.
- Kích thước đo trên file: 7 ảnh 256×256 (`01.png` đến `07.png`), 5 ảnh 512×512 (`08.png` đến `12.png`).
- Nguồn file: testsets/Set12 của FFDNet, https://github.com/cszn/FFDNet/tree/master/testsets/Set12
- Bộ này là 12 ảnh kiểm tra dùng trong các bài khử nhiễu của Zhang, Zuo, Zhang (FFDNet, IEEE TIP 2018, DOI 10.1109/TIP.2018.2839891).
- Không có một giấy phép SPDX chung cho cả 12 ảnh. Đây là ảnh kiểm tra chuẩn được các bài khử nhiễu phát lại kèm mã nguồn.

`data/phone` để ảnh điện thoại của nhóm. `data/samples` là ảnh do `experiments/run_samples.py` tự vẽ, không thuộc BSD68 hay Set12.

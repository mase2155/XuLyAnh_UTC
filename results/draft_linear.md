# Nháp lý thuyết lọc trung bình và lọc Gauss

Cả hai lọc thay một điểm bằng tổng có trọng số của lân cận. Ảnh tính bằng float64. Biên dùng padding phản xạ, NumPy `reflect`, cùng nghĩa OpenCV `BORDER_REFLECT_101`.

## Lọc trung bình

Cửa sổ \(s \in \{3, 5\}\). Mọi hệ số bằng \(1/s^2\), tổng hệ số bằng 1.

\[
\hat x(i,j) = \frac{1}{s^2}\sum_{u=0}^{s-1}\sum_{v=0}^{s-1} x(i+u-r, j+v-r), \quad r = \lfloor s/2 \rfloor
\]

Lọc này giảm nhiễu Gauss vì lấy trung bình nhiều điểm độc lập, nhưng cộng cả điểm cạnh vào điểm nền nên làm mờ cạnh. Muối tiêu có giá trị 0 hoặc 255, một điểm như vậy kéo cả cửa sổ lệch đi.

## Lọc Gauss

Cùng hai cửa sổ. Nếu không truyền \(\sigma\) thì

\[
\sigma = 0{,}3\left((s-1)\times 0{,}5 - 1\right) + 0{,}8
\]

tức \(\sigma = 0{,}8\) khi \(s = 3\) và \(\sigma = 1{,}1\) khi \(s = 5\). Nhân trước khi chuẩn hóa là

\[
g(u,v) = \exp\left(-\frac{u^2+v^2}{2\sigma^2}\right)
\]

rồi chia cho tổng nhân để tổng hệ số bằng 1. Điểm gần tâm được tính nặng hơn lọc trung bình, nhưng lọc vẫn tuyến tính nên vẫn mờ cạnh và vẫn không xóa được xung. Không dùng \(\sigma = 0\) của OpenCV, vì giá trị đó được OpenCV hiểu là nhân nhị thức.

# Nháp lý thuyết song phương: hai sigma và muối tiêu

Lọc song phương trong `src/filters/bilateral.py` có đường kính 9. Chỉ các điểm nằm trong hình tròn bán kính 4 được tính. Biên dùng padding phản xạ.

Trọng số là tích của hai nhân Gauss.

\[
w = \exp\left(-\frac{d^2}{2\sigma_s^2}\right)\exp\left(-\frac{(I-I_0)^2}{2\sigma_c^2}\right)
\]

\(\sigma_s\) là sigmaSpace, khóa bằng 5. Nó giảm trọng số khi điểm nằm xa tâm. \(\sigma_c\) là sigmaColor, ba mức 25, 50 và 75. Nó giảm trọng số khi mức xám khác điểm đang lọc. Ảnh ra là tổng trọng số nhân mức xám, chia cho tổng trọng số.

sigmaColor nhỏ thì chỉ những điểm có mức xám gần nhau được cộng vào, nên cạnh giữa hai vùng khác mức xám được giữ. sigmaColor lớn thì nhánh mức xám gần như luôn bằng 1, lọc tiến về lọc Gauss và cạnh bị mờ hơn.

Muối tiêu không hợp với lọc này. Một điểm muối có mức xám 255. Nếu điểm đang lọc là nền, hiệu mức xám rất lớn, sigmaColor làm trọng số của chính điểm muối nhỏ, nên muối bị giảm. Nhưng khi điểm đang lọc chính là hạt muối, các điểm muối lân cận có cùng mức 255 được trọng số cao, còn nền bị loại. Hạt muối vì thế được giữ hoặc chỉ bị làm yếu, không bị thay bằng trung vị của nền. Trung vị mới là lọc phù hợp với xung.

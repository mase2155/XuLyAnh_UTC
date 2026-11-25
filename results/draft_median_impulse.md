# Trung vị với nhiễu xung dưới 50%

Muối tiêu thay một phần điểm bằng 0 hoặc 255. Trong một cửa sổ, trung vị là điểm đứng giữa sau khi sắp xếp.

Gọi tỉ lệ điểm hỏng trong cửa sổ là \(p\). Nếu \(p < 0{,}5\) thì quá nửa số điểm vẫn là điểm sạch. Điểm đứng giữa của cửa sổ lẻ phải nằm trong nửa sạch đó, nên trung vị không lấy muối và không lấy tiêu.

Cửa sổ 3×3 có 9 điểm. Muối tiêu dưới 50% nghĩa là không quá 4 điểm hỏng. Năm điểm còn lại sạch, nên điểm thứ 5 sau khi sắp xếp là điểm sạch.

Điều này không còn đúng khi một cửa sổ có từ 5 điểm hỏng trở lên. Với muối tiêu 20% trên cả ảnh, hầu hết cửa sổ 3×3 vẫn dưới 50%, nhưng một số cửa sổ rơi vào cụm xung và trung vị giữ lại xung. Cửa sổ 5×5 có 25 điểm, cần nhiều xung hơn mới vượt 50%, nên hết xung dễ hơn nhưng lấy thêm điểm nền và làm mờ chi tiết.

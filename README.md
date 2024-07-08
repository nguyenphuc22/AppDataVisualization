# AppDataVisualization

## Cài đặt môi trường
- Python 3.10.14
## Chạy sử dụng CLI
- streamlit run main.py

## Ghi Chú
- Đã cập nhật thêm phần giả thuyết cho từng người. Mọi người xem và bổ sung thêm vào nhé. Phần nào có từ "TODO + Tên ai thì người đó làm nhé" là phần cần bổ sung.
- Phần ChatBot em sẽ nghiên cứu và cập nhật lên sau

## Kế hoạch
Kế hoạch thực hiện ứng dụng "Data Visualization" cho dự án cuối kỳ môn học "Xử lý dữ liệu thông minh" của nhóm 5 người.

1. Thu thập dữ liệu tự động ( Cái này làm sau cũng được, không gấp)
   - Tạo script Python để tự động thu thập dữ liệu sản phẩm và đánh giá mới từ Lazada theo lịch định kỳ (hàng ngày/giờ).
   - Lưu trữ dữ liệu mới vào cơ sở dữ liệu CSV.

2. Tiền xử lý và làm sạch dữ liệu
   - Viết các hàm Python để thực hiện các bước tiền xử lý và làm sạch dữ liệu tương tự như báo cáo giữa kỳ.
     - ProductManager - ReviewManager có hàm xử lý tự động gọi rồi nha mấy ný, viết trong đó thôi, đừng đổi khung ở ngoài nếu không cần thiết.
   - Quá trình này sẽ được thực hiện khi người dùng nhấn nút "Cập nhật dữ liệu" trên giao diện. (Hiện tại chưa làm cái này)

3. Phân tích và trực quan hóa dữ liệu sản phẩm
   - Xây dựng các hàm để tính toán và trực quan hóa các chỉ số như phân phối sản phẩm theo địa điểm, thương hiệu, đánh giá, giá bán, giảm giá, số lượng bán, v.v.
   - Tạo các biểu đồ tương tác sử dụng Plotly hoặc Altair để người dùng có thể thay đổi tham số và xem kết quả trực quan.
   - Quá trình này sẽ được thực hiện khi người dùng truy cập vào trang "Sản phẩm -> Trực quan hoá", "Đánh giá -> Tự làm flow nhé" -> người dùng tương tác với các điều khiển lọc và chọn dữ liệu trên giao diện.

4.1 Phân tích dùng OLS
   - Mấy bạn làm phần này tự viết vào nhé

4.2 Phân tích cảm xúc từ dữ liệu đánh giá
   - Mấy bạn làm phần này tự viết vào nhé
   
5. Xây dựng ứng dụng Streamlit
   - Thiết kế giao diện ứng dụng với Streamlit, tạo các trang (pages) cho từng chức năng chính.
   - Trang chủ: Giới thiệu về ứng dụng, hướng dẫn sử dụng, và liên kết đến các trang khác.
   - Trang "Sản phẩm": Hiển thị kết quả phân tích và trực quan hóa dữ liệu sản phẩm.
     - Sử dụng các widget của Streamlit như selectbox, slider, checkbox để người dùng lựa chọn và lọc dữ liệu theo các tiêu chí khác nhau.
     - Hiển thị các biểu đồ tương tác, bảng dữ liệu, và các chỉ số thống kê quan trọng.
   - Trang "Đánh giá": Hiển thị kết quả phân tích cảm xúc từ dữ liệu đánh giá.
     - Sử dụng các widget để người dùng lựa chọn thương hiệu, sản phẩm, khoảng thời gian đánh giá.
     - Hiển thị biểu đồ tỷ lệ cảm xúc, wordcloud từ khóa, và các ví dụ đánh giá điển hình.

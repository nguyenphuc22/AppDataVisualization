# AppDataVisualization

Dưới đây là bản kế hoạch hoàn chỉnh để phát triển ứng dụng phân tích dữ liệu sử dụng Streamlit, kèm theo sơ đồ mô tả quá trình thực hiện và cập nhật kết quả trên giao diện:

1. Thu thập dữ liệu tự động ( Cái này làm sau cũng được, không gấp)
   - Tạo script Python để tự động thu thập dữ liệu sản phẩm và đánh giá mới từ Lazada theo lịch định kỳ (hàng ngày/giờ).
   - Sử dụng các thư viện như requests, BeautifulSoup, Selenium để truy cập và lấy dữ liệu từ trang web.
   - Lưu trữ dữ liệu mới vào cơ sở dữ liệu CSV.

2. Tiền xử lý và làm sạch dữ liệu
   - Viết các hàm Python để thực hiện các bước tiền xử lý và làm sạch dữ liệu tương tự như báo cáo giữa kỳ.
   - Sử dụng các thư viện xử lý dữ liệu như Pandas, NumPy để thao tác và xử lý dữ liệu hiệu quả.
   - Áp dụng các kỹ thuật làm sạch dữ liệu như loại bỏ dữ liệu trùng lặp, xử lý giá trị thiếu, chuẩn hóa văn bản, v.v.
   - Quá trình này sẽ được thực hiện khi người dùng nhấn nút "Cập nhật dữ liệu" trên giao diện.

3. Phân tích và trực quan hóa dữ liệu sản phẩm
   - Sử dụng các thư viện phân tích dữ liệu như Pandas, Matplotlib, Seaborn để thực hiện các phân tích thống kê và trực quan hóa.
   - Xây dựng các hàm để tính toán và trực quan hóa các chỉ số như phân phối sản phẩm theo địa điểm, thương hiệu, đánh giá, giá bán, giảm giá, số lượng bán, v.v.
   - Tạo các biểu đồ tương tác sử dụng Plotly hoặc Altair để người dùng có thể thay đổi tham số và xem kết quả trực quan.
   - Quá trình này sẽ được thực hiện khi người dùng truy cập vào trang "Sản phẩm" hoặc khi người dùng tương tác với các điều khiển lọc và chọn dữ liệu trên giao diện.

4. Phân tích cảm xúc từ dữ liệu đánh giá
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
   - Trang "Nhận định & Đề xuất": Tổng hợp các nhận định, đề xuất dựa trên kết quả phân tích.
     - Sử dụng thẻ (tags), bảng, và văn bản để trình bày các nhận định và đề xuất một cách rõ ràng, dễ hiểu.
     - Cho phép người dùng lựa chọn và xem các nhận định, đề xuất theo chủ đề hoặc lĩnh vực cụ thể.
   - Kết quả từ quá trình 3 và 4 sẽ được cập nhật tự động lên các trang tương ứng khi có dữ liệu mới hoặc khi người dùng tương tác với các điều khiển lọc và chọn dữ liệu.

```mermaid
graph TD
    A[1. Thu thập dữ liệu tự động] -->|Định kỳ| B[2. Tiền xử lý và làm sạch dữ liệu]
    B -->|Khi truy cập trang hoặc tương tác| C[3. Phân tích và trực quan hóa dữ liệu sản phẩm]
    B -->|Khi truy cập trang hoặc tương tác| D[4. Phân tích cảm xúc từ dữ liệu đánh giá]
    C -->|Cập nhật kết quả| E[5. Hiển thị trên trang "Sản phẩm"]
    D -->|Cập nhật kết quả| F[5. Hiển thị trên trang "Đánh giá"]
    E -->|Tương tác với điều khiển lọc và chọn| C
    F -->|Tương tác với điều khiển lọc và chọn| D
    G[Người dùng] -->|Truy cập ứng dụng Streamlit| E
    G -->|Truy cập ứng dụng Streamlit| F
    G -->|Nhấn nút "Cập nhật dữ liệu"| B

```
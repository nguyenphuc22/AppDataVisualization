# AppDataVisualization

## Cài đặt môi trường
- Python 3.10.14
- `pip install -r ./requirements.txt`

## Chạy sử dụng CLI
- `streamlit run main.py`

## Về Chatbot Keys
- Để có thể sử dụng chức năng liên quan đến chatbot, xin hãy nhập `OPENAI_API_KEY` khi ở console khi khởi động lần đầu, hoặc có thể cập nhật `OPENAI_API_KEY` tại file `ChatBotUtils/privateInfo.py`.

## Kế hoạch
Kế hoạch thực hiện "Ứng dụng phân tích tự động tích hợp AI" cho dự án cuối kỳ môn học "Phân tích dữ liệu thông minh" của nhóm 5 người.

1. Tiền xử lý và làm sạch dữ liệu
   - Viết các hàm Python để thực hiện các bước tiền xử lý và làm sạch dữ liệu tương tự như báo cáo giữa kỳ trong thư mục `DataManager`.
   - Quá trình này sẽ được thực hiện khi người dùng nhấn nút "Cập nhật dữ liệu" trên giao diện. 

2. Phân tích và trực quan hóa dữ liệu sản phẩm
   - Xây dựng các hàm để tính toán và trực quan hóa các chỉ số như phân phối sản phẩm theo địa điểm, thương hiệu, đánh giá, giá bán, giảm giá, số lượng bán, v.v.
   - Tạo các biểu đồ tương tác sử dụng Plotly hoặc Altair để người dùng có thể thay đổi tham số và xem kết quả trực quan.
   - Quá trình này sẽ được thực hiện khi người dùng truy cập vào trang "Sản phẩm → Trực quan hoá", "Đánh giá → người dùng tương tác với các điều khiển lọc và chọn dữ liệu trên giao diện.

3. Thực hiện phân tích tự động
  - Phân tích dùng OLS
    - Sử dụng kỹ thuật ước lượng hồi quy tuyến tính OLS.
    - Đưa ra được phân tích phân phối sản phối theo giảm giá (discount).
    - Phân tích ảnh hưởng thương hiệu, địa điêm, mức giảm giá và điểm đánh giá lên số lượng sản phẩm bán ra.

  - Phân tích cảm xúc từ dữ liệu đánh giá
    - Sử dụng kỹ thuật NLP dựa trên thư viện underthesea để rút trích các từ, sau đó phân loại vào các cảm xúc.
    - Trực quan hóa các yếu tố ảnh hưởng đến cảm xúc của khách hàng.
    - Trích xuất các đặc trưng của sản phẩm, phân tích các yếu tố được khách hàng quan tâm nhiều.
   
4. Xây dựng ứng dụng Streamlit
   - Thiết kế giao diện ứng dụng với Streamlit, tạo các trang (pages) cho từng chức năng chính.
   - Trang chủ: Giới thiệu về ứng dụng, hướng dẫn sử dụng, và liên kết đến các trang khác.
   - Trang "Sản phẩm": Hiển thị kết quả phân tích và trực quan hóa dữ liệu sản phẩm.
     - Sử dụng các widget của Streamlit như selectbox, slider, checkbox để người dùng lựa chọn và lọc dữ liệu theo các tiêu chí khác nhau.
     - Hiển thị các biểu đồ tương tác, bảng dữ liệu, và các chỉ số thống kê quan trọng.
   - Trang "Đánh giá": Hiển thị kết quả phân tích cảm xúc từ dữ liệu đánh giá.
     - Sử dụng các widget để người dùng lựa chọn thương hiệu, sản phẩm, khoảng thời gian đánh giá.
     - Hiển thị biểu đồ tỷ lệ cảm xúc, wordcloud từ khóa, và các ví dụ đánh giá điển hình.

5. Tích hợp Chatbot từ OpenAI để phân tích dữ liệu tự động từ hình ảnh / kết quả mô hình OLS
   - Phương pháp thực hiện:
      - Xây dựng database chứa các hình ảnh trực quan, các kết quả phân tích dữ liệu của nhóm.
      - Thiết lập cơ chế truy vấn tăng cường (Retrieval-Augmented Generation) vào tệp database của nhóm khi nhận được câu hỏi từ người dùng.
      - Đưa các kết quả truy vấn bao gồm hình ảnh/kết quả phân tích dữ liệu của nhóm vào prompt của chatbot, kết hợp với câu hỏi từ người dùng để sinh ra câu trả lời từ chatbot.
   - Kết quả thực hiện:
      - Đối với các trang "Giả thuyết", một kết quả phân tích từ chatbot sẽ được khởi tạo sẵn bởi nhóm tại đầu mục "Kết luận".
      - Đối với tất cả các trang trong ứng dung, các hình ảnh được hiển thị tại trang đó có thể được Chatbot truy cập và giải thích, nhận xét thông qua câu hỏi được người dùng đặt ra tại thanh bên "Trợ lý".

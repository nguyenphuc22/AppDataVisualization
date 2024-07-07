class StringManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StringManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.strings = {
            "home_title": "Trang chủ",
            "product_title": "Sản phẩm",
            "review_title": "Đánh giá",
            "welcome_message": "Chào mừng đến với ứng dụng của chúng tôi!",
            "product_page_message": "Đây là trang sản phẩm của chúng tôi.",
            "review_page_message": "Đây là trang đánh giá của chúng tôi.",
            "data_visualization_title": "Trực quan hoá dữ liệu",
            "data_visualization_message": "Đây là trang trực quan hoá dữ liệu.",
            "hypothesis_title": "Giả thuyết",
            "hypothesis_message": "Đây là trang giả thuyết.",
            "menu_title": "Danh Mục",
            "menu_options": ["Trang chủ", "Sản phẩm", "Đánh giá"],
            "product_options": ["Trực quan hoá dữ liệu", "Giả thuyết"],
            "product_hypothesis_title": ["Giả thuyết Phúc", "Giả thuyết Thành", "Giả thuyết Bình"],
            "review_options": ["Trực quan hoá dữ liệu", "Giả thuyết"],
            "review_hypothesis_title": ["Giả thuyết Nhi", "Giả thuyết Viên"],
            "menu_icons": ["house", ["box", "chart_with_upwards_trend", "lightbulb"], "star"],
            "menu_icon": "cast",
            "update_button": "Cập nhật",
            "pick_file_button": "Chọn tệp",
            "file_uploader_title": "Chọn tệp CSV hoặc Excel",
            "File_uploaded" : "File đã được tải lên",
            "Not_files_uploaded" : "Chưa có file nào được tải lên.",
            "chatbot_title": "Trợ Lý",
            "you" : "Bạn",
            'bot' : 'Bot',
            "send" : "Gửi"
        }

    def get_string(self, key):
        return self.strings.get(key, "")

    def set_string(self, key, value):
        self.strings[key] = value

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
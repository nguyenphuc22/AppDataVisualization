

class AppContext():
    _instance = None
    def __init__(self):
        super().__init__()
        self.titlePage = "Trang chủ"
        self.content = "Chào mừng đến với ứng dụng của chúng tôi!"
        self.hyphothesisTitle = "Giả thuyết sử dụng OLS trên tập dữ liệu số lượng bản Lazada"
        self.hyphothesisContent = "Thông số OLS của mô hình là: 0.5, 0.6, 0.7, 0.8, 0.9"
        self.prompt = "Các thông số trên là giả định, không phải là thực tế. Hãy cho tôi biết nó nói lên điều gì ?"


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppContext, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
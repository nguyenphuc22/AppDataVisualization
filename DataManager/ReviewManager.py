from DataManager.DataManager import AbstractDataManager


class ReviewManager(AbstractDataManager):
    _instance = None
    def __init__(self):
        super().__init__()
        self.get_data = None  # or initialize it with some value

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ReviewManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def preprocess_data(self, data):
        # Code Tiền Sử Lý Chung Cho Review tại đây nhé
        return data

    def get_data(self):
        return self.data
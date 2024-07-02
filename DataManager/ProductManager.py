from DataManager.DataManager import AbstractDataManager

class ProductManager(AbstractDataManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProductManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()

    def preprocess_data(self, data):
        # Code Tiền Sử Lý Chung Cho Product tại đây nhé
        return data

    def get_data(self):
        return self.data
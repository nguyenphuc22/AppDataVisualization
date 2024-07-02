from DataManager.DataManager import AbstractDataManager


class ReviewManager(AbstractDataManager):
    def __init__(self):
        super().__init__()
        self.get_data = None  # or initialize it with some value

    def preprocess_data(self, data):
        # Code Tiền Sử Lý Chung Cho Review tại đây nhé
        return data
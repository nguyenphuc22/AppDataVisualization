from abc import ABC, abstractmethod
import pandas as pd

class AbstractDataManager(ABC):
    _instances = {}

    def __init__(self):
        self.file_path = None
        self.data = pd.DataFrame()

    @classmethod
    def get_instance(cls):
        if cls not in cls._instances:
            cls._instances[cls] = cls()
        return cls._instances[cls]

    def read_data(self, file_path):
        self.file_path = file_path
        data = pd.read_excel(file_path)
        self.data = self.preprocess_data(data)
        return self.data

    @abstractmethod
    def preprocess_data(self, data):
        # This method should return a pandas DataFrame
        pass

    def update_data(self, new_data):
        self.data = self.preprocess_data(new_data) # Replace old data with new data

def check_format(data):
    required_product_columns = ['itemId', 'name', 'priceShow', 'discount', 'ratingScore', 'review', 
                'location', 'sellerName', 'sellerId', 'brandName', 'brandId', 
                'price', 'category', 'originalPrice', 'itemSoldCntShow', 'options']
    required_review_columns = ['reviewRateId', 'boughtDate', 'reviewContent', 'reviewTime', 'rating', 
                        'likeCount', 'likeText', 'helpful', 'isPurchased', 'isGuest', 
                        'sellerId', 'sellerName', 'itemId', 'itemTitle', 'skuInfo', 
                        'skuId', 'upVotes', 'downVotes', 'isGoodReview']

    if all(col in data.columns for col in required_product_columns):
        return {'valid': True, 'type': 'product'}
    elif all(col in data.columns for col in required_review_columns):
        return {'valid': True, 'type': 'review'}
    else:
        return {'valid': False}
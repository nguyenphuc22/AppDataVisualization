from abc import ABC, abstractmethod
import pandas as pd

class AbstractDataManager(ABC):
    _instances = {}

    def __init__(self):
        self.file_path = None
        self.data = None

    @classmethod
    def get_instance(cls):
        if cls not in cls._instances:
            cls._instances[cls] = cls()
        return cls._instances[cls]

    def read_data(self, file_path, isNewFile = False):
        if self.data is None or isNewFile is True:
            self.file_path = file_path
            data = pd.read_excel(file_path)
            self.data = self.preprocess_data(data)
        return self.data

    @abstractmethod
    def preprocess_data(self, data):
        print("Preprocessing data entry Abstract")
        # This method should return a pandas DataFrame
        pass
    

    def update_data(self, new_data):
        new_data.to_excel(self.file_path, index=False)
        self.read_data(self.file_path, isNewFile=True)
        print("Data updated successfully.")

def check_format(data):
    # Convert column names in the DataFrame to lower case
    data_columns_lower = [col.lower() for col in data.columns]
    
    # Define required columns with their lower case equivalents
    required_product_columns = [
        'itemid', 'name', 'priceshow', 'discount', 'ratingscore', 'review', 
        'location', 'sellername', 'sellerid', 'brandname', 'brandid', 
        'price', 'category', 'originalprice', 'itemsoldcntshow', 'options'
    ]
    
    required_review_columns = [
        'reviewrateid', 'boughtdate', 'reviewcontent', 'reviewtime', 'rating', 
        'likecount', 'liketext', 'helpful', 'ispurchased', 'isguest', 
        'sellerid', 'sellername', 'itemid', 'itemtitle', 'skuinfo', 
        'skuid', 'upvotes', 'downvotes', 'isgoodreview'
    ]

    # Check if all required product columns are present (case-insensitive)
    if all(col in data_columns_lower for col in required_product_columns):
        return {'valid': True, 'type': 'product'}
    
    # Check if all required review columns are present (case-insensitive)
    elif all(col in data_columns_lower for col in required_review_columns):
        return {'valid': True, 'type': 'review'}
    
    # If neither condition is met, return invalid
    else:
        return {'valid': False}

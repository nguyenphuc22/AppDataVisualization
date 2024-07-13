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
        new_data.to_excel(self.file_path, index=False)
        print("Data updated successfully.")
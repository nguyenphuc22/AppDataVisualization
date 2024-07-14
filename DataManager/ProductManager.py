from DataManager.DataManager import AbstractDataManager
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import DBSCAN
import re

class ProductManager(AbstractDataManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProductManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()

    def preprocess_data(self, data):
        print("Preprocessing data entry Product")

        try:
            df_good_products = data.groupby('itemId').first().reset_index()
        except KeyError:
            raise ValueError("Required column 'itemId' is missing in the input data.")
        
        try:
            df_good_products = df_good_products[~df_good_products['location'].str.contains('overseas', case=False)]
        except KeyError:
            print("Column 'location' is missing. Skipping this step.")

        brand_replacements = {
            'xiao': 'Xiaomi',
            'OPPO': 'Oppo',
            'Vivotek': 'Vivo',
            'vsmart': 'Vsmart',
            'NaN': 'No Brand'
        }
        
        try:
            df_good_products['brandName'] = df_good_products['brandName'].replace(brand_replacements)
        except KeyError:
            print("Column 'brandName' is missing. Skipping this step.")
        
        brand_patterns = {
            'Realme': [r'realme'],
            'Nokia': [r'nokia'],
            'LG': [r'lg'],
            'Panasonic': [r'panasonic'],
            'Lenovo': [r'lenovo'],
            'Xiaomi': [r'xi ao mi', r'xiao.*'],
            'Google': [r'pixel', r'google'],
            'Huawei': [r'huawei'],
            'Vsmart': [r'vsmart'],
            'Sony': [r'sony', r'[xX][zZ]\d{1}'],
            'Microsoft': [r'microsoft', r'surface'],
            'Oppo': [r'oppo', r'reno.*', r'[afAF]\d{1}'],
            'Poco': [r'poco', r'x3pro'],
            'Vivo': [r'[yvYV]\d{2}'],
            'Apple': [r'apple', r'[il]\-?pad', r'iph[o0]ne', r'promax', r'\d[1]s?\s*plus|\d\s*s', r'[iI][pP]?\s*\d{1,2}', r'.*pro\s*max.*'],
            'Samsung': [r'j\d{1}', r'sam', r'galaxy', r'[sS]\d{2}'],
        }

        try:
            df_good_products['brandName'] = df_good_products.apply(
                lambda row: self.update_brand_name(row['name'], row['brandName'], brand_patterns), axis=1
            )
        except KeyError:
            print("Column 'name' or 'brandName' is missing. Skipping this step.")
        
        try:
            df_good_products = df_good_products[df_good_products['brandName'] != 'No Brand']
            df_good_products['brandName'] = df_good_products['brandName'].str.capitalize()
        except KeyError:
            print("Column 'brandName' is missing. Skipping this step.")
        
        try:
            bad_keywords = ['tablets', 'vitamin', 'pen']
            df_good_products = df_good_products[~df_good_products['name'].str.contains('|'.join(bad_keywords), case=False, na=False)]
        except KeyError:
            print("Column 'name' is missing. Skipping this step.")
        
        try:
            brand_counts = df_good_products['brandName'].value_counts()
            brands_to_remove = brand_counts[brand_counts <= 10].index.tolist()
            df_good_products = df_good_products[~df_good_products['brandName'].isin(brands_to_remove)]
        except KeyError:
            print("Column 'brandName' is missing. Skipping this step.")
        
        try:
            df_good_products['ratingScore'] = df_good_products['ratingScore'].fillna(0)
            df_good_products['ratingScore'] = df_good_products['ratingScore'].apply(lambda score: round(float(score), 3))
        except KeyError:
            print("Column 'ratingScore' is missing. Skipping this step.")
        
        try:
            df_good_products.loc[df_good_products['originalPrice'] < df_good_products['priceShow'], 'originalPrice'] = df_good_products['priceShow']
        except KeyError:
            print("Column 'originalPrice' or 'priceShow' is missing. Skipping this step.")
        
        try:
            df_good_products.drop(columns=['price'], inplace=True)
        except KeyError:
            print("Column 'price' is missing. Skipping this step.")
        

        columns_to_check = ['priceShow', 'discount', 'ratingScore', 'review', 'itemSoldCntShow', 'originalPrice']
        df_good_products = self.combined_outlier_removal(df_good_products, columns_to_check)
        
        # Reset index
        df_good_products.reset_index(drop=True, inplace=True)

        return df_good_products

    def get_data(self):
        return self.data

    def combined_outlier_removal(self,df, columns_to_check, eps=0.5, min_samples=5, iqr_factor=1.5):
        # Bước 1: Áp dụng DBSCAN
        scaler = RobustScaler()
        data_scaled = scaler.fit_transform(df[columns_to_check])

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(data_scaled)

        df_dbscan = df[clusters != -1].copy()

        # Bước 2: Áp dụng IQR trên kết quả của DBSCAN
        def remove_iqr_outliers(df, column, factor=1.5):
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - factor * IQR
            upper_bound = Q3 + factor * IQR
            return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

        df_combined = df_dbscan.copy()
        for col in columns_to_check:
            df_combined = remove_iqr_outliers(df_combined, col, factor=iqr_factor)

        return df_combined

    @staticmethod
    def update_brand_name(name, current_brand, brand_patterns):
        name_lower = name.lower()
        for brand, patterns in brand_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower, re.IGNORECASE):
                    return brand
        return current_brand
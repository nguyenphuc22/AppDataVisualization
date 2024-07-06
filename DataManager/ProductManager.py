from DataManager.DataManager import AbstractDataManager
import pandas as pd
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
        data = data.groupby('itemId').first().reset_index()
        df_good_products = data[~data['location'].str.contains('overseas', case=False)]

        brand_replacements = {
            'xiao': 'Xiaomi',
            'OPPO': 'Oppo',
            'Vivotek': 'Vivo',
            'vsmart': 'Vsmart',
            'NaN': 'No Brand'
        }
        df_good_products.loc[:, 'brandName'] = df_good_products['brandName'].replace(brand_replacements)

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

        df_good_products.loc[:, 'brandName'] = df_good_products.apply(
            lambda row: self.update_brand_name(row['name'], row['brandName'], brand_patterns), axis=1
        )

        df_good_products = df_good_products[df_good_products['brandName'] != 'No Brand']
        df_good_products.loc[:, 'brandName'] = df_good_products['brandName'].str.capitalize()

        bad_keywords = ['tablets', 'vitamin', 'pen']
        df_good_products = df_good_products[~df_good_products['name'].str.contains('|'.join(bad_keywords), case=False, na=False)]

        '''Remove brand that has devices <= 10'''
        brand_counts = df_good_products['brandName'].value_counts()
        brands_to_remove = brand_counts[brand_counts <= 10].index.tolist()
        df_good_products = df_good_products[~df_good_products['brandName'].isin(brands_to_remove)]

        '''Reformat the rating system to correct format and replace NaN value'''
        df_good_products['ratingScore'] = df_good_products['ratingScore'].fillna(0)

        '''Update originalPrice where originalPrice < priceShow'''
        df_good_products.loc[df_good_products['originalPrice'] < df_good_products['priceShow'], 'originalPrice'] = df_good_products['priceShow']

        '''Drop column price because they are similar to priceShow'''
        df_good_products.drop(columns=['price'], inplace=True)

        '''Reformat the rating system to correct format'''
        df_good_products['ratingScore'] = df_good_products['ratingScore'].apply(lambda score: round(float(score), 3))

        return df_good_products

    def get_data(self):
        return self.data

    @staticmethod
    def update_brand_name(name, current_brand, brand_patterns):
        name_lower = name.lower()
        for brand, patterns in brand_patterns.items():
            for pattern in patterns:
                if re.search(pattern, name_lower, re.IGNORECASE):
                    return brand
        return current_brand

import re
from underthesea import word_tokenize
from datetime import datetime
import pandas as pd
from DataManager import AbstractDataManager

class ReviewManager(AbstractDataManager):
    _instance = None

    def __init__(self):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ReviewManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def load_stopwords(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            stopwords = set(f.read().splitlines())
        return stopwords

    def load_compound_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            compound_words = set(line.strip() for line in file)
        return compound_words

    def remove_emojis(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"
                                   u"\U0001F300-\U0001F5FF"
                                   u"\U0001F680-\U0001F6FF"
                                   u"\U0001F1E0-\U0001F1FF"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def remove_punctuation(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def replace_star_icons(self, text):
        star_pattern = re.compile(r'[*★☆⭐🌟✨]')
        return star_pattern.sub(' sao', text)

    def combine_compound_words(self, words, compound_words):
        combined_words = []
        i = 0
        while i < len(words):
            if i < len(words) - 1:
                two_word_combo = words[i] + ' ' + words[i + 1]
                if two_word_combo in compound_words:
                    combined_words.append(two_word_combo.replace(' ', '_'))
                    i += 2
                    continue
            combined_words.append(words[i])
            i += 1
        return combined_words

    def replace_dots(self, text):
        text = re.sub(r'\.{2,}', ' ', text)
        return text

    def preprocessing(self, text, vietnamese_stopwords, compound_words):
        text = str(text).lower()
        text = self.replace_dots(text)
        text = self.replace_star_icons(text)
        text = self.remove_emojis(text)
        text = self.remove_punctuation(text)
        words = word_tokenize(text, format='text').split()
        words = [w for w in words if w not in vietnamese_stopwords]
        words = self.combine_compound_words(words, compound_words)
        words = [w.replace('_', ' ') for w in words]
        return words

    def preprocess_data(self, data):
        vietnamese_stopwords = self.load_stopwords('./Data/vietnamese-stopwords.txt')
        compound_words = self.load_compound_words('./Data/compound_words.txt')

        data['boughtDate'] = pd.to_datetime(data['boughtDate'].astype(int), format='%Y%m%d')
        data['year'] = data['boughtDate'].dt.year
        data['month'] = data['boughtDate'].dt.month
        data['day'] = data['boughtDate'].dt.day

        data_rating_5 = data[data['rating'] == 5]
        data_rating_5_unique = data_rating_5.drop_duplicates(subset=['reviewContent'])
        data_combined = pd.concat([data[data['rating'] != 5], data_rating_5_unique])
        data_combined.reset_index(drop=True, inplace=True)

        data_combined['cleanedContent'] = data_combined['reviewContent'].apply(self.preprocessing, args=(vietnamese_stopwords, compound_words))
        data_combined['cleanedItem'] = data_combined['itemTitle'].apply(self.preprocessing, args=(vietnamese_stopwords, compound_words))

        return data_combined

    def get_data(self):
        return self.data

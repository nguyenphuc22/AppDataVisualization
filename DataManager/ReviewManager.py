from DataManager.DataManager import AbstractDataManager

import pandas as pd
import re
from underthesea import word_tokenize
from datetime import datetime
import logging

class ReviewManager(AbstractDataManager):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ReviewManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        super().__init__()
        self.vietnamese_stopwords = self.load_stopwords('./Data/vietnamese-stopwords.txt')
        self.compound_words = self.load_compound_words('./Data/compound_words.txt')
        self.positive_words = [
            'nhanh chóng', 'hiệu quả', 'bền bỉ', 'đáp ứng', 'tốt', 'hợp lý', 'hài lòng', 'tin tưởng', 'an tâm', 'cảm ơn',
            'tuyệt vời', 'uy tín', 'tích cực', '5 sao', 'hàng đẹp', 'đẹp', 'mới', 'nhanh', 'mượt', 'pin tốt', 'mạnh', 'pin khỏe',
            'nhiệt tình', 'chất lượng', 'ưng ý', 'chu đáo', 'ủng hộ', 'chuẩn', 'bền', 'phù hợp', 'thú vị', 'rẻ', 'mong đợi',
            'yên tâm', 'ưng ý', 'hay', 'xuất sắc', 'đúng', 'bền', 'chuẩn', 'ổn định', 'cẩn thận', 'đầy đủ', 'xứng đáng', 'may mắn',
            'bổ rẻ', 'chuyên nghiệp', 'ưng ý', 'sang', 'đúng', 'ổn áp', 'êm ru', 'tot'
        ]
        self.negative_words = [
            'kém', 'gian', 'lận', 'gian lận','lùa đảo', 'lừa đảo', 'lừa gạt', 'mất đạo đức', 'xạo',
            'không đúng', 'không có', 'hu hong', 'mau hết', 'chán', '1 sao', 'lỗi', 'không mua', 'hàng dởm', 'máy lỗi',
            'nóng máu', 'mù', 'lừa', 'yếu', 'giởm', 'hàng cũ', 'ko đúng', 'kém', 'liệt pin', 'nhấp nháy', 'hư', 'treo đầu dê bán thịt chó',
            'chê', 'k đúng', 'lổi', 'cũ', 'thất vọng', 'phí tiền', 'cũ xước', 'hàng tệ', 'ko trung thực', 'rùa bò', 'chậm', 'không nhiệt tình',
            'không hoạt động', 'tráo hàng', 'hết pin', 'hết dung lượng', 'dỏm', 'rác', 'tê liệt', 'lãng phí', 'phí tiền', 'cố ý',
            'không trả lời', 'xau', 'giao sai', 'pin mau hết', 'lua dao', 'not working', 'poor quality', 'đơ', 'đểu', 'lừa lọc',
            'giả mạo', 'te', 'cham', 'it', 'bực mình', 'từ chối', 'chậm trễ', 'sơ sài', 'lưa', 'trầy', 'pin yếu', 'không phản hồi',
            'dổm', 'lưa đao', 'ko dung', 'sập', 'mất tiền', 'bực', 'mất', 'cảnh giác', 'lãng phí', 'lôi', 'giao sai', 'vỡ', 'yeu',
            'cham', 'kem', 'ko hài lòng', 'sai', '0', 'bẩn', 'thua', 'không tốt', 'hỏng', 'lác'
        ]
        self.neutral_words = [
            'bình thường', 'trung', 'bình', 'ổn', 'bình', 'dân', 'bt', 'thông thường', 'nan'
        ]
        self.brand_map = {
            'Apple': ['iphone', 'lphone', 'ip', 'khủng lphone', 'i', 'i15', 'i14', 'air', 'lpad', 'ipad', 'pro', 'iphơne', 'ip6', 'ip6g', 'padmini', 'pad4', 'pad', 'ipaad', 'iph0ne', 'pad4 bản'],
            'Samsung': ['galaxy', 'samsung', 'a57', 'ss', 's23', 'ultra' ,'thoạia71', 's22ultra', 'đồng s22ultra', 'tab3', 'tab'],
            'Google': ['pixel'],
            'Huawei': ['huawei', 'honor'],
            'Lenovo': ['lenovo'],
            'LG': ['lg'],
            'Nokia': ['nokia', 'e71'],
            'Nobard': ['nobard'],
            'MASSTEL': ['masstel'],
            'Oppo': ['oppo', 'a56', 'thoạia58', 'thoạia57', 'thoạia77', 'a95', 'reno', 'thoạia93', 'thoạia17', 'thoạia38', 'a58', 'thoạif11', 'a73', 'a93' ,'thoạia73', 'a18', 'a3s', 'thoạia74', 'a2x', 'a17'],
            'Realme': ['realme'],
            'Sony': ['sony'],
            'Vivo': ['vivo', 'thoạiy50', 'thoạiy17', 'thoạiy19', 'thoạiv20', 'thoạiy50', 'thoạiy55', 'thoạiy22s', 'v29', 'thoạiy11', 'thoạiy93', 'y56', 'y19', 'thoạiy16', 'thoạiy11', 'y93', 'y70s', 'y22s'],
            'Vsmart': ['vsmart'],
            'Xiaomi': ['xiaomi', 'redmi'],
            'Sharp': ['sharp'],
            'Gree': ['gree'],
            'Murah': ['murah']
        }
        # Thiết lập logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def load_stopwords(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())

    # Load dữ liệu compound words
    def load_compound_words(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(line.strip() for line in file)

    # Lọc các biểu cảm trong văn bản
    def remove_emojis(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    # Loại bỏ dấu câu
    def remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', '', text)

    # Thay thế icon sao bằng từ "sao"
    def replace_star_icons(self, text):
        star_pattern = re.compile(r'[*★☆⭐🌟✨]')
        return star_pattern.sub(' sao', text)
    
    # Thay thế dấu chấm nhiều lần bằng một dấu cách
    def replace_dots(self, text):
        return re.sub(r'\.{2,}', ' ', text)    

    # Kết hợp các từ ghép
    def combine_compound_words(self, words):
        combined_words = []
        i = 0
        while i < len(words):
            if i < len(words) - 1:
                two_word_combo = words[i] + ' ' + words[i + 1]
                if two_word_combo in self.compound_words:
                    combined_words.append(two_word_combo.replace(' ', '_'))
                    i += 2
                    continue
            combined_words.append(words[i])
            i += 1
        return combined_words

    # Tiền xử lý dữ liệu
    def preprocessing(self, text):
        text = str(text).lower()
        text = self.replace_dots(text)
        text = self.replace_star_icons(text)
        text = self.remove_emojis(text)
        text = self.remove_punctuation(text)
        words = word_tokenize(text, format='text').split()
        words = [w for w in words if w not in self.vietnamese_stopwords]
        words = self.combine_compound_words(words)
        words = [w.replace('_', ' ') for w in words]
        return words

    # Phân loại cảm xúc
    def classify_sentiment(self, keywords):
        positive_count = sum(1 for word in keywords if word in self.positive_words)
        negative_count = sum(1 for word in keywords if word in self.negative_words)
        neutral_count = sum(1 for word in keywords if word in self.neutral_words)

        if positive_count > negative_count and positive_count > neutral_count:
            return 'Positive'
        elif negative_count > positive_count and negative_count > neutral_count:
            return 'Negative'
        else:
            return 'Neutral'

    # Trích xuất thương hiệu
    def extract_brand(self, cleaned_item):
        for brand, keywords in self.brand_map.items():
            for keyword in keywords:
                if keyword in cleaned_item:
                    return brand
        return 'None'

    # Load dữ liệu
    def preprocess_data(self, data):
        print("Preprocessing data entry ReviewManager")

        # Định dạng lại ngày 
        data['boughtDate'] = pd.to_datetime(data['boughtDate'], format='%Y%m%d', errors='coerce')

        # Remove duplicates các đánh giá 5 sao (seeding)
        df_rating_5 = data[data['rating'] == 5]
        df_rating_5_unique = df_rating_5.drop_duplicates(subset=['reviewContent'])
        data = pd.concat([data[data['rating'] != 5], df_rating_5_unique])
        data.reset_index(drop=True, inplace=True)

        # Áp dụng hàm preprocessing
        data['cleanedContent'] = data['reviewContent'].apply(self.preprocessing)
        data['cleanedItem'] = data['itemTitle'].apply(self.preprocessing)

        # Phân loại cảm xúc
        data['Sentiment'] = data['cleanedContent'].apply(self.classify_sentiment)

        # Trích xuất thương hiệu
        data['brandName'] = data['cleanedItem'].apply(self.extract_brand)

        # Drop các cột không cần thiết
        data.drop(columns=['cleanedItem'], inplace=True)
        return data

    def get_data(self):
        """
        Trả về dữ liệu đã được xử lý.
        """
        if self.data is None:
            self.logger.warning("Data has not been loaded. Call load_data() first.")
        return self.data

    def get_data_summary(self):
        """
        Trả về tóm tắt về dữ liệu.
        """
        if self.data is None:
            return "Data has not been loaded."
        return f"Data shape: {self.data.shape}, Columns: {', '.join(self.data.columns)}"
    
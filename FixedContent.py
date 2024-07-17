
# Fixed content for chatbot
class FixedContent:
    _instance = None
    def __init__(self):
        self.products_multiAttributesImpact_olsResult = """"""
        self.products_priceImpact_olsResult = """"""
        self.reviews_sentiments_generalContent = """"""
        self.reviews_keywords_generalContent = """"""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FixedContent, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
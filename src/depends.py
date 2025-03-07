from src.etl_facade import EtlFacade
from src.extract.news_api import NewsApi


news_api = NewsApi()

etl_facade = EtlFacade(news_api)

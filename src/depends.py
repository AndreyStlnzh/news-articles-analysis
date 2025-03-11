from src.db.repositories.article_repo import ArticleRepo
from src.db.repositories.word_stat_repo import WordStatRepo
from src.etl_facade import EtlFacade
from src.extract.news_api import NewsApi
from src.extract.news_api import NewsApi
from src.services.article_service import ArticleService
from src.services.word_stat_service import WordStatService
from src.transform.most_common_words import MostCommonWords
from src.transform.sentiment_analysis import SentimentAnalysis
from src.transform.text_cleaner import TextCleaner
from src.db.db_connection import async_session_maker
news_api = NewsApi()

text_cleaner: TextCleaner = TextCleaner()
most_common_words: MostCommonWords = MostCommonWords()
sentiment_analysis: SentimentAnalysis = SentimentAnalysis()

article_repo: ArticleRepo = ArticleRepo(async_session_maker)
word_stat_repo: WordStatRepo = WordStatRepo(async_session_maker)

article_service: ArticleService = ArticleService(article_repo)
word_stat_service: WordStatService = WordStatService(word_stat_repo)

etl_facade = EtlFacade(news_api)

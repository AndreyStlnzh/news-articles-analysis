from src.db.repositories.article_repo import ArticleRepo
from src.db.repositories.word_stat_repo import WordStatRepo
from src.etl_facade import EtlFacade
from src.extract.news_api import NewsApi
from src.extract.news_api import NewsApi
from src.minio.minio_client import MinioClient
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

minio_client = MinioClient()

etl_facade = EtlFacade(
    news_api=news_api,
    text_cleaner=text_cleaner,
    most_common_words=most_common_words,
    sentiment_analysis=sentiment_analysis,
    article_service=article_service,
    word_stat_service=word_stat_service,
    minio_client=minio_client,
)

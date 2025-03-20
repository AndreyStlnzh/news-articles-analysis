from src.etl_facade import EtlFacade
from src.load import SaveToDB
from src.load import SaveToMinio
from src.db.repositories.article_repo import ArticleRepo
from src.db.repositories.word_stat_repo import WordStatRepo
from src.minio.minio_client import MinioClient
from src.services.article_service import ArticleService
from src.services.word_stat_service import WordStatService
from src.db.db_connection import async_session_maker


article_repo: ArticleRepo = ArticleRepo(async_session_maker)
word_stat_repo: WordStatRepo = WordStatRepo(async_session_maker)

article_service: ArticleService = ArticleService(article_repo)
word_stat_service: WordStatService = WordStatService(word_stat_repo)

minio_client = MinioClient()

save_to_db = SaveToDB(article_service, word_stat_service)
save_to_minio = SaveToMinio(minio_client)

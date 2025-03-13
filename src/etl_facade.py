import pandas as pd

from datetime import datetime, timedelta

from src.extract import NewsApi
from src.load.save_to_db import SaveToDB
from src.transform import MostCommonWords
from src.transform import SentimentAnalysis
from src.transform import TextCleaner
from src.load import SaveToMinio


class EtlFacade:
    def __init__(
        self,
        news_api: NewsApi,
        text_cleaner: TextCleaner,
        most_common_words: MostCommonWords,
        sentiment_analysis: SentimentAnalysis,
        save_to_db: SaveToDB,
        save_to_minio: SaveToMinio,
    ) -> None:
        self.news_api: NewsApi = news_api
        self.text_cleaner: TextCleaner = text_cleaner
        self.most_common_words: MostCommonWords = most_common_words
        self.sentiment_analysis: SentimentAnalysis = sentiment_analysis
        self.save_to_db: SaveToDB = save_to_db
        self.save_to_minio: SaveToMinio = save_to_minio


    async def run_ETL_news_for_last_n_days(
        self,
        keyword: str="apple",
        n: int=3
    ):
        date_from = (datetime.now() - timedelta(days=n)).date().isoformat()
        date_to = (datetime.now()).date().isoformat()

        # Extract
        data_df: pd.DataFrame = self.news_api.get_articles(keyword, date_from, date_to)
        print(f"Данные извлечены. Всего {len(data_df)} статей")

        # Transform
        self.text_cleaner.preprocess_data(data_df)
        words, count = self.most_common_words.find_most_common_words(data_df)
        data_df: pd.DataFrame = self.sentiment_analysis.process_sentiment_analysis(data_df)
        print("Данные успешно предобработаны")

        # Load
        await self.save_to_db.save_dataframe_to_db(data_df, words, count)
        print("Таблицы БД успешно пополнены")
        self.save_to_minio.save_csv_to_minio(data_df)
        print("CSV успешно загружен в MinIO")
        self.save_to_minio.save_dataframe_to_parquet(data_df)
        print("parquet успешно загружен в MinIO")

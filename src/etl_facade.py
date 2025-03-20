from typing import List, Tuple
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
        save_to_db: SaveToDB,
        save_to_minio: SaveToMinio,
    ) -> None:
        self.news_api: NewsApi = NewsApi()
        self.text_cleaner: TextCleaner = TextCleaner()
        self.most_common_words: MostCommonWords = MostCommonWords()
        self.sentiment_analysis: SentimentAnalysis = SentimentAnalysis()
        self.save_to_db: SaveToDB = save_to_db
        self.save_to_minio: SaveToMinio = save_to_minio


    def extract(
        self,
        keyword: str,
        date_from: datetime,
        date_to: datetime,
    ) -> pd.DataFrame:
        """Extraction"""
        data_df: pd.DataFrame = self.news_api.get_articles(keyword, date_from, date_to)
        print(f"Данные извлечены. Всего {len(data_df)} статей")
        return data_df


    def transform(
        self,
        data_df: pd.DataFrame,
    ) -> Tuple[pd.DataFrame, List[str], List[int]]:
        """Transformation"""
        self.text_cleaner.preprocess_data(data_df)
        words, counts = self.most_common_words.find_most_common_words(data_df)
        data_df: pd.DataFrame = self.sentiment_analysis.process_sentiment_analysis(data_df)
        print("Данные успешно предобработаны")
        return data_df, words, counts


    async def load(
        self,
        data_df: pd.DataFrame,
        words: List[str],
        counts: List[int],
    ) -> None:
        """Load"""
        await self.save_to_db.save_dataframe_to_db(data_df, words, counts)
        print("Таблицы БД успешно пополнены")
        self.save_to_minio.save_csv_to_minio(data_df)
        print("CSV успешно загружен в MinIO")
        self.save_to_minio.save_dataframe_to_parquet(data_df)
        print("parquet успешно загружен в MinIO")


    async def run_ETL_news_for_last_n_days(
        self,
        keyword: str="apple",
        n: int=3
    ):
        date_from = (datetime.now() - timedelta(days=n)).date().isoformat()
        date_to = (datetime.now()).date().isoformat()

        # Extract
        data_df = self.extract(keyword, date_from, date_to)
        
        # Transform
        data_df, words, counts = self.transform(data_df)

        # Load
        await self.load(data_df, words, counts)

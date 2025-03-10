from datetime import datetime, timedelta

import pandas as pd
from src.extract.news_api import NewsApi
from src.transform.most_common_words import MostCommonWords
from src.transform.sentiment_analysis import SentimentAnalysis
from src.transform.text_cleaner import TextCleaner


class EtlFacade:
    def __init__(
        self,
        news_api: NewsApi,
        text_cleaner: TextCleaner,
        most_common_words: MostCommonWords,
        sentiment_analysis: SentimentAnalysis,
    ) -> None:
        self.news_api: NewsApi = news_api
        self.text_cleaner: TextCleaner = text_cleaner
        self.most_common_words: MostCommonWords = most_common_words
        self.sentiment_analysis: SentimentAnalysis = sentiment_analysis

    def run_ETL_news_for_last_n_days(
        self,
        keyword: str="apple",
        n: int=3
    ):
        date_from = (datetime.now() - timedelta(days=n)).date().isoformat()
        date_to = (datetime.now()).date().isoformat()

        data_df: pd.DataFrame = self.news_api.get_articles(keyword, date_from, date_to)
        self.text_cleaner.preprocess_data(data_df)

        words, count = self.most_common_words.find_most_common_words(data_df)
        data_df: pd.DataFrame = self.sentiment_analysis.process_sentiment_analysis(data_df)


    def run_ETL(
        self,
        keyword: str,
        date_from: str,
        date_to: str,
    ) -> None:
        data_df: pd.DataFrame = self.news_api.get_articles(keyword, date_from, date_to)
        data_df: pd.DataFrame = self.text_cleaner.preprocess_data(data_df)
        
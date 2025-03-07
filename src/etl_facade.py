from datetime import datetime, timedelta

import pandas as pd
from src.extract.news_api import NewsApi


class EtlFacade:
    def __init__(
        self,
        news_api: NewsApi,
    ) -> None:
        self.news_api: NewsApi = news_api


    def run_ETL_news_for_last_n_days(
        self,
        keyword: str="apple",
        n: int=3
    ):
        
        date_from = (datetime.now() - timedelta(days=n)).date().isoformat()
        date_to = (datetime.now()).date().isoformat()

        data_df: pd.DataFrame = self.news_api.get_articles(keyword, date_from, date_to)
        data_df.to_csv(f"data_{keyword}.csv")


    def run_ETL(
        self,
        keyword: str,
        date_from: str,
        date_to: str,
    ) -> None:
        self.news_api.get_articles(keyword, date_from, date_to)

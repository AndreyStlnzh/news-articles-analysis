from datetime import datetime, timedelta
from typing import List

import pandas as pd
from src.dto import ArticleDTO, WordStatDTO
from src.extract.news_api import NewsApi
from src.services.article_service import ArticleService
from src.services.word_stat_service import WordStatService
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
        article_service: ArticleService,
        word_stat_service: WordStatService,
    ) -> None:
        self.news_api: NewsApi = news_api
        self.text_cleaner: TextCleaner = text_cleaner
        self.most_common_words: MostCommonWords = most_common_words
        self.sentiment_analysis: SentimentAnalysis = sentiment_analysis
        self.article_service: ArticleService = article_service
        self.word_stat_service: WordStatService = word_stat_service


    async def run_ETL_news_for_last_n_days(
        self,
        keyword: str="apple",
        n: int=3
    ):
        date_from = (datetime.now() - timedelta(days=n)).date().isoformat()
        date_to = (datetime.now()).date().isoformat()

        data_df: pd.DataFrame = self.news_api.get_articles(keyword, date_from, date_to)
        print("Данные извлечены")
        self.text_cleaner.preprocess_data(data_df)

        words, count = self.most_common_words.find_most_common_words(data_df)
        data_df: pd.DataFrame = self.sentiment_analysis.process_sentiment_analysis(data_df)
        print("Данные успешно предобработаны")

        article_dtos = self.convert_df_to_dto(data_df)
        word_stat_dtos = self.words_and_counts_to_dto(words, count)

        await self.article_service.save_articles(article_dtos)
        await self.word_stat_service.save_word_stats(word_stat_dtos)
        print("Таблицы БД успешно пополнены")

    def convert_df_to_dto(
        self,
        data: pd.DataFrame,
    ) -> List[ArticleDTO]:
        return [
            ArticleDTO(
                author=row.author,
                title=row.title,
                description=row.description,
                url=row.url,
                publishedAt=row.publishedAt,
                content=row.content,
                sentiment=row.sentiment,
            )
            for _, row in data.iterrows()
        ]
    
    def words_and_counts_to_dto(
        self,
        words: List[str],
        count: List[int],
    ) -> List[WordStatDTO]:
        return [
            WordStatDTO(
                word=words[i],
                count=count[i]
            )
            for i in range(len(words))
        ]

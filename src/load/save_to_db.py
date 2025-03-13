

from typing import List
import pandas as pd
from src.dto import ArticleDTO, WordStatDTO
from src.services.article_service import ArticleService
from src.services.word_stat_service import WordStatService


class SaveToDB:
    def __init__(
        self,
        article_service: ArticleService,
        word_stat_service: WordStatService,
    ):
        self.article_service: ArticleService = article_service
        self.word_stat_service: WordStatService = word_stat_service

    async def save_dataframe_to_db(
        self,
        data_df: pd.DataFrame,
        words: List[str],
        count: List[int],
    ):
        """
        Функция сохранения необходимых данных в БД

        Args:
            data_df (pd.DataFrame): DataFrame с данными
            words (List[str]): самые частые слова
            count (List[int]): частотность самых частых слов
        """
        article_dtos = self.convert_df_to_dto(data_df)
        word_stat_dtos = self.words_and_counts_to_dto(words, count)

        await self.article_service.save_articles(article_dtos)
        await self.word_stat_service.save_word_stats(word_stat_dtos)


    def convert_df_to_dto(
        self,
        data: pd.DataFrame,
    ) -> List[ArticleDTO]:
        """Конвертация датафрейма в дто для сохранения в БД"""
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
        """Функция конвертации частотности слов в дто для сохранения в БД"""
        return [
            WordStatDTO(
                word=words[i],
                count=count[i]
            )
            for i in range(len(words))
        ]

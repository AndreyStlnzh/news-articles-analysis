from typing import List
from src.db.repositories.word_stat_repo import WordStatRepo
from src.dto import WordStatDTO


class WordStatService:
    def __init__(
        self, 
        word_stat_repo: WordStatRepo
    ) -> None:
        self.word_stat_repo: WordStatRepo = word_stat_repo


    async def save_word_stats(
        self,
        word_stats: List[WordStatDTO],
    ) -> None:
        for word_stat in word_stats:
            await self.word_stat_repo.create_word_stat(word_stat)

        print("Статистика успешно сохранена")


    async def get_word_stat_by_id(
        self,
        word_stat_id: int,
    ) -> WordStatDTO | None:
        return await self.word_stat_repo.get_word_stat_by_id(word_stat_id)
    

    async def get_all_word_stats(
        self,
        limit: int=10,
        offset: int=0,
    ) -> List[WordStatDTO]:
        return await self.word_stat_repo.get_all_word_stats(limit, offset)

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.db.models.word_stat_model import WordStat
from src.dto import WordStatDTO


class WordStatRepo:

    def __init__(
        self,
        session_maker: async_sessionmaker,
    ) -> None:
        self.session_maker: async_sessionmaker = session_maker


    async def create_word_stat(
        self,
        word_stat_dto: WordStatDTO,
    ) -> int:
        """Создает новую статью в БД и возвращает её ID"""
        

        async with self.session_maker() as session:
            new_stat = WordStat(**word_stat_dto.model_dump())

            session.add(new_stat)
            await session.commit()
            await session.refresh(new_stat)

            return new_stat.id
    

    async def get_word_stat_by_id(
        self,
        stat_id: int,
    ) -> WordStatDTO | None:
        """Возвращает статью по ID, если она существует"""
        async with self.session_maker() as session:
            query = select(WordStat).where(WordStat.id == stat_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    

    async def get_all_word_stats(
        self,
        limit: int=10,
        offset: int=0,
    ) -> List[WordStatDTO]:
        """Возвращает список всех статей с пагинацией"""
        async with self.session_maker() as session:
            query = select(WordStat).limit(limit).offset(offset)
            result = await self.execute(query)
            stats = result.scalars().all()

            return [WordStatDTO.model_validate(stat) for stat in stats]

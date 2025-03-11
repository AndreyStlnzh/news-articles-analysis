from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.word_stat_model import WordStatModel
from src.dto import WordStatDTO


class WordStatRepo:

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session: AsyncSession = session


    async def create_word_stat(
        self,
        word_stat_dto: WordStatDTO,
    ) -> int:
        """Создает новую статью в БД и возвращает её ID"""

        new_stat = WordStatModel(**word_stat_dto.model_dump())

        self.session.add(new_stat)
        await self.session.commit()
        await self.session.refresh(new_stat)

        return new_stat.id
    

    async def get_word_stat_by_id(
        self,
        stat_id: int,
    ) -> WordStatDTO | None:
        """Возвращает статью по ID, если она существует"""
        query = select(WordStatModel).where(WordStatModel.id == stat_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    

    async def get_all_word_stats(
        self,
        limit: int=10,
        offset: int=0,
    ) -> List[WordStatDTO]:
        """Возвращает список всех статей с пагинацией"""
        query = select(WordStatModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        stats = result.scalars().all()

        return [WordStatDTO.model_validate(stat) for stat in stats]

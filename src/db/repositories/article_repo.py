from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.article_model import ArticleModel
from src.dto import ArticleDTO


class ArticleRepo:

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session: AsyncSession = session


    async def create_article(
        self,
        article_dto: ArticleDTO,
    ) -> int:
        """Создает новую статью в БД и возвращает её ID"""

        new_article = ArticleModel(**article_dto.model_dump())

        self.session.add(new_article)
        await self.session.commit()
        await self.session.refresh(new_article)

        return new_article.id
    

    async def get_article_by_id(
        self,
        article_id: int,
    ) -> ArticleDTO:
        """Возвращает статью по ID, если она существует"""
        query = select(ArticleModel).where(ArticleModel.id == article_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    

    async def get_all_articles(
        self,
        limit: int=10,
        offset: int=0,
    ) -> List[ArticleDTO]:
        """Возвращает список всех статей с пагинацией"""
        query = select(ArticleModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        articles = result.scalars().all()

        return [ArticleDTO.model_validate(article) for article in articles]

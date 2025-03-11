from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.db.models.article_model import Article
from src.dto import ArticleDTO


class ArticleRepo:

    def __init__(
        self,
        session_maker: async_sessionmaker,
    ) -> None:
        self.session_maker: async_sessionmaker = session_maker


    async def create_article(
        self,
        article_dto: ArticleDTO,
    ) -> int:
        """Создает новую статью в БД и возвращает её ID"""
        async with self.session_maker() as session:
            new_article = Article(**article_dto.model_dump())

            session.add(new_article)
            await session.commit()
            await session.refresh(new_article)

            return new_article.id

    async def get_article_by_id(
        self,
        article_id: int,
    ) -> ArticleDTO | None:
        """Возвращает статью по ID, если она существует"""
        async with self.session_maker() as session:
            query = select(Article).where(Article.id == article_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    

    async def get_all_articles(
        self,
        limit: int=10,
        offset: int=0,
    ) -> List[ArticleDTO]:
        """Возвращает список всех статей с пагинацией"""
        async with self.session_maker() as session:
            query = select(Article).limit(limit).offset(offset)
            result = await session.execute(query)
            articles = result.scalars().all()

            return [ArticleDTO.model_validate(article) for article in articles]

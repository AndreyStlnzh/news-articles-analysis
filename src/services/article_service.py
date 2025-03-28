from typing import List
from src.db.repositories.article_repo import ArticleRepo
from src.dto import ArticleDTO


class ArticleService:
    def __init__(
        self, 
        article_repo: ArticleRepo
    ) -> None:
        self.article_repo: ArticleRepo = article_repo


    async def save_articles(
        self,
        articles: List[ArticleDTO],
    ) -> None:
        for article in articles:
            article.publishedAt = article.publishedAt.to_pydatetime()
            article.publishedAt = article.publishedAt.replace(tzinfo=None)
            await self.article_repo.create_article(article)

        print("Статьи успешно сохранены")

    async def get_article_by_id(
        self,
        article_id: int,
    ) -> ArticleDTO | None:
        return await self.article_repo.get_article_by_id(article_id)
    

    async def get_all_articles(
        self,
        limit: int=10,
        offset: int=0,
    ) -> List[ArticleDTO]:
        return await self.article_repo.get_all_articles(limit, offset)

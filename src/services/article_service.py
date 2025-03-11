

from src.db.repositories.article_repo import ArticleRepo


class ArticleService:
    def __init__(
        self, 
        article_repo: ArticleRepo
    ) -> None:
        self.article_repo: ArticleRepo = article_repo

        
from datetime import datetime
from sqlalchemy import String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.db_connection import Base

class ArticleModel(Base):
    author: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    publishedAt: Mapped[datetime]
    content: Mapped[str]
    sentiment: Mapped[str]

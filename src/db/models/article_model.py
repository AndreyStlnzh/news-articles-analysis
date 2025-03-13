from datetime import datetime
from sqlalchemy.orm import Mapped

from src.db.db_connection import Base

class Article(Base):
    author: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]
    publishedAt: Mapped[datetime]
    content: Mapped[str]
    sentiment: Mapped[str]

from sqlalchemy.orm import Mapped

from src.db.db_connection import Base

class WordStat(Base):
    word: Mapped[str]
    count: Mapped[int]

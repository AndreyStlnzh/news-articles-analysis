from datetime import datetime
from sqlalchemy import String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.db_connection import Base

class WordStat(Base):
    word: Mapped[str]
    count: Mapped[int]

from datetime import datetime
from pydantic import BaseModel


class ArticleDTO(BaseModel):
    author: str
    title: str
    description: str
    url: str
    publishedAt: datetime
    content: str
    sentiment: str

class WordStatDTO(BaseModel):
    word: str
    count: str

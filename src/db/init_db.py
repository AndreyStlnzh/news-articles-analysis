import asyncio

from src.db.models.article_model import Article
from src.db.models.word_stat_model import WordStat
from src.db.db_connection import create_db_and_tables


async def main():
    await create_db_and_tables()

if __name__ == "__main__":
    asyncio.run(main())

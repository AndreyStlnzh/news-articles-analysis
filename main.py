import asyncio
from src.depends import etl_facade


async def main():
    await etl_facade.run_ETL_news_for_last_n_days(
        keyword="apple", 
        n=3
    )

if __name__ == "__main__":
    asyncio.run(main())


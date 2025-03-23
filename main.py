import asyncio
from src.db.db_connection import create_db_and_tables
from src.etl_facade import EtlFacade
from src.services.dependecies import (
    save_to_db,
    save_to_minio,
)

async def main():
    await create_db_and_tables()

    etl_facade = EtlFacade(
        save_to_db=save_to_db,
        save_to_minio=save_to_minio
    )

    await etl_facade.run_ETL_news_for_last_n_days(
        keyword="apple", 
        n=3
    )

if __name__ == "__main__":
    asyncio.run(main())



from src.depends import etl_facade


def main():
    etl_facade.run_ETL_news_for_last_n_days(
        keyword="apple", 
        n=3
    )

if __name__ == "__main__":
    main()

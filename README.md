# Analysis of news articles

ETL-pipeline implementation. <u>Fundamentals of Data Engineering</u>

## Task
Collect, process, and save data from news sites to analyze the most popular topics.

## ETL-pipeline

1) **Extract**
    - Using the API of the news aggregator;
    - Uploading articles on the specified topics (for example, "technology", "science", "apple").
2) **Transform**
    - Text preprocessing (stop words, extra characters);
    - Sentiment analysis;
    - Identifying the main topics (TF-IDF).
3) **Load**
    - Save data to PostgreSQL;
    - Save the processed data to a Minio in CSV and Parquet format.

## Technologies used

- SQLAlchemy (PostgreSQL)
- MinIO
- requests
- pandas, nltk
- pydantic
- parquet

## Next step
Next step is refine and adapt project to <u>Airflow</u> (automated data updates).

## Run
docker-compose up --build
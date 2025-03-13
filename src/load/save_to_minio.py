from datetime import datetime
from io import BytesIO
from typing import Tuple
import pandas as pd
from src.minio.minio_client import MinioClient


class SaveToMinio:
    def __init__(
        self,
        minio_client: MinioClient,
    ):
        self.minio_client: MinioClient = minio_client

    def save_csv_to_minio(
        self,
        data_df: pd.DataFrame,
    ) -> str:
        """
        Функция загрузки csv в minio

        Args:
            data_df (pd.DataFrame): DataFrame для загрузки

        Returns:
            str: путь до загруженного файла в бакете
        """
        csv_bytes = data_df.to_csv().encode("utf-8")
        csv_buffer = BytesIO(csv_bytes)
        minio_path = f"csv/data_{datetime.now().isoformat(timespec='seconds')}.csv"
        
        self.minio_client.upload_file(csv_buffer, minio_path, len(csv_bytes))
        return minio_path
    

    def download_csv_from_minio(
        self,
        minio_path: str,
    ) -> pd.DataFrame:
        """
        Функция скачивания csv файла с minio

        Args:
            minio_path (str): путь в бакете

        Returns:
            pd.DataFrame: скачанный DataFrame
        """
        bytes_file = self.minio_client.download_file(minio_path)
        buffer = BytesIO(bytes_file)
        data_df = pd.read_csv(buffer)
        return data_df


    def save_dataframe_to_parquet(
        self,
        data_df: pd.DataFrame
    ) -> str:
        parquet_bytes = data_df.to_parquet(engine="pyarrow")
        parquet_buffer = BytesIO(parquet_bytes)
        minio_path = f"parquet/data_{datetime.now().isoformat(timespec='seconds')}.parquet"
        self.minio_client.upload_file(parquet_buffer, minio_path, len(parquet_bytes))
        return minio_path

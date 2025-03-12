from datetime import datetime
from io import BytesIO
import os
import minio

from src.config import settings

class MinioClient:
    def __init__(self):
        self._minio_client = minio.Minio(
            **settings.get_minio_client_settings()
        )

        if not self._minio_client.bucket_exists(settings.MINIO_BUCKET):
            self._minio_client.make_bucket(settings.MINIO_BUCKET)

        self._bucket_name = settings.MINIO_BUCKET


    def upload_csv(
            self,
            buffer: BytesIO,
            len_csv_bytes: int
    ) -> str:
        """
        Функция сохранения CSV в MinIO

        Args:
            buffer (BytesIO): буффер, содержаший данные
            len_csv_bytes (int): длина csv данных в байтах

        Returns:
            str: путь к загруженному объекту в MinIO 
        """
        minio_path = f"csv/data_{datetime.now().isoformat(timespec='seconds')}.csv"
        self._minio_client.put_object(
            bucket_name=self._bucket_name,
            object_name=minio_path,
            data=buffer,
            length=len_csv_bytes,
            # content_type='application/csv',
        )

        return minio_path

    def download_file(
            self,
            object_name: str
    ):
        """
        Скачивает CSV-файл из MinIO и загружает его в DataFrame.

        Аргументы:
            object_name (str): Имя объекта (путь в бакете).

        Возвращает:
            pd.DataFrame: DataFrame с содержимым CSV-файла.
        """
        minio_path = f"csv/filename"
        response = self._minio_client.get_object(
            bucket_name=self._bucket_name,
            object_name=minio_path,
        )
        csv_data = response.read()
        return bytes
        # buffer = BytesIO(csv_data)

    def delete_file(
            self,
            filename: str
    ):
        self._minio_client.remove_object(
            bucket_name=self._bucket_name,
            object_name=filename
    )

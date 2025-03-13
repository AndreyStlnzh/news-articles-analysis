import minio

from io import BytesIO

from src.config import settings

class MinioClient:
    def __init__(self):
        self._minio_client = minio.Minio(
            **settings.get_minio_client_settings()
        )

        if not self._minio_client.bucket_exists(settings.MINIO_BUCKET):
            self._minio_client.make_bucket(settings.MINIO_BUCKET)

        self._bucket_name = settings.MINIO_BUCKET


    def upload_file(
            self,
            buffer: BytesIO,
            minio_path: str,
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
        self._minio_client.put_object(
            bucket_name=self._bucket_name,
            object_name=minio_path,
            data=buffer,
            length=len_csv_bytes,
        )


    def download_file(
            self,
            object_name: str
    ) -> bytes:
        """
        Скачивает файл из MinIO и возвращает как bytes.

        Аргументы:
            object_name (str): Имя объекта (путь в бакете).

        Возвращает:
            bytes: файл в виде байтов.
        """
        response = self._minio_client.get_object(
            bucket_name=self._bucket_name,
            object_name=object_name,
        )
        bytes_file = response.read()
        return bytes_file
        

    def delete_file(
            self,
            filename: str
    ):
        self._minio_client.remove_object(
            bucket_name=self._bucket_name,
            object_name=filename
    )

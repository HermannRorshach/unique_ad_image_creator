import boto3
from botocore.config import Config
from dotenv import load_dotenv
import os

# Загружаем данные из .env файла
load_dotenv()

# Получаем ключи из .env
aws_access_key_id = os.getenv('YANDEX_CLOUD_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('YANDEX_CLOUD_SECRET_ACCESS_KEY')

# Настройка клиента S3
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    config=Config(signature_version='s3v4')
)

import mimetypes

# Функция для загрузки файлов из папки
def upload_files_from_folder(folder_path, bucket_name):
    for root, _, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)  # Полный путь к файлу на локальной машине
            relative_path = os.path.relpath(local_path, folder_path)  # Относительный путь
            object_name = relative_path.replace("\\", "/")  # Преобразуем в формат S3

            # Определяем MIME-тип файла
            content_type, _ = mimetypes.guess_type(local_path)
            if not content_type:
                content_type = "application/octet-stream"  # Устанавливаем тип по умолчанию

            print(f"Загружаем файл: {local_path} -> {object_name} с MIME-типом: {content_type}")
            s3_client.upload_file(
                local_path,
                bucket_name,
                object_name,
                ExtraArgs={"ContentType": content_type}  # Передаём MIME-тип
            )
            print(f"Файл {object_name} успешно загружен!")


# Укажите локальную папку и имя бакета
folder_path = r"C:/Users/Павел/Documents/Work/folders_1"  # Замените на путь к вашей папке
bucket_name = "0001-small-test"

# Загружаем файлы
upload_files_from_folder(folder_path, bucket_name)

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

# Загрузка файла
bucket_name = 'adverts-bucket'
file_name = 'Screenshot_8.png'  # Исходное имя файла
object_name = f'uploads/{file_name}'  # Имя объекта в бакете совпадает с именем файла

s3_client.upload_file(file_name, bucket_name, object_name)

# Генерация публичной ссылки
public_url = f"https://storage.yandexcloud.net/{bucket_name}/{object_name}"
print(public_url)

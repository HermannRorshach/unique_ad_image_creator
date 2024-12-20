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

# Ввод названия бакета
bucket_name = input("Введите название бакета: ")

# Получение списка файлов
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        print("Список файлов в бакете:")
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print("Бакет пустой или не содержит объектов.")
except Exception as e:
    print(f"Ошибка при получении списка файлов: {e}")

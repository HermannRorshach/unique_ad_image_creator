import os
import re
import boto3
from botocore.config import Config
from dotenv import load_dotenv

# Загрузка данных из .env
load_dotenv()

# Получение ключей доступа
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

# Функция для безопасного имени папки
def sanitize_name(name):
    name = re.sub(r'[\\/:"*?<>|]+', '_', name).rstrip('.')
    if re.fullmatch(r'[a-zA-Z0-9]+', name):
        name = f"{name}"
    return name


# Основной блок программы
if __name__ == "__main__":
    bucket_name = "001test001" # input("Введите название бакета: ").strip()
    save_path = "c:/Users/Павел/Documents/Work/folders" # input("Введите путь к папке для сохранения файлов: ").strip()

    if not os.path.exists(save_path):
        print("Указанный путь для сохранения не существует.")
        exit()

    # Скачивание файлов из бакета
    print("Начинается скачивание файлов...")

    try:
        continuation_token = None
        total_files = 0

        while True:
            # Параметры для пагинации
            kwargs = {"Bucket": bucket_name}
            if continuation_token:
                kwargs["ContinuationToken"] = continuation_token

            # Получение объектов
            response = s3_client.list_objects_v2(**kwargs)
            objects = response.get('Contents', [])
            total_files += len(objects)

            # Обработка файлов
            for obj in objects:
                key = obj['Key']

                # Корректируем путь сохранения
                path_parts = [sanitize_name(part) for part in key.split('/')]
                file_save_path = os.path.join(save_path, *path_parts)

                # Создаём директории, если нужно
                os.makedirs(os.path.dirname(file_save_path), exist_ok=True)

                if not key.endswith('/'):  # Пропускаем "папки" S3
                    print(f"Скачивается файл: {key}...")
                    s3_client.download_file(bucket_name, key, file_save_path)
                    print(f"Файл сохранён: {file_save_path}")

            # Проверяем, есть ли следующая страница
            if response.get('IsTruncated'):  # Если есть ещё данные
                continuation_token = response['NextContinuationToken']
            else:
                break

        print(f"Скачивание завершено успешно! Всего файлов: {total_files}")
    except Exception as e:
        print(f"Ошибка при скачивании файлов: {e}")

import json
from io import BytesIO

import boto3
from botocore.config import Config
from PIL import Image


# Настройка клиента S3
s3_client = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    config=Config(signature_version='s3v4'),
)

MAX_SIZE = 307200  # Максимальный размер файла (300 КБ)

class Paths:
    def __init__(self):
        self.full_paths = []  # Полные пути
        self.relative_paths = []  # Относительные пути

    def add_full_path(self, full_path):
        self.full_paths.append(full_path)

    def extend_full_paths(self, full_paths_list):
        self.full_paths.extend(full_paths_list)

    def add_relative_path(self, relative_path):
        self.relative_paths.append(relative_path)

    def extend_relative_paths(self, relative_paths_list):
        self.relative_paths.extend(relative_paths_list)


def get_files(bucket_name):
    files = Paths()
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):  # Исключаем папки
                    filename = obj['Key']
                    files.add_relative_path(filename)
                    files.add_full_path(f"https://storage.yandexcloud.net/{bucket_name}/{filename}")
    except Exception as e:
        print(f"Ошибка при получении списка файлов: {e}")
    return files


def compress_image_to_size(image_data, max_size, resize_factor=0.9):
    """Сжимает изображение до заданного размера, уменьшая разрешение."""

    image = Image.open(BytesIO(image_data))
    image = image.convert('RGB')  # Конвертируем в RGB для JPEG

    buffer = BytesIO()
    width, height = image.size

    while True:
        # Сохраняем изображение в буфер
        image.save(buffer, format="JPEG", quality=95)
        # Проверяем размер
        if buffer.tell() <= max_size:
            break
        # Уменьшаем разрешение
        width = int(width * resize_factor)
        height = int(height * resize_factor)
        image = image.resize((width, height), Image.LANCZOS)
        buffer = BytesIO()  # Очищаем буфер

    buffer.seek(0)
    return buffer


def clear_image_metadata(bucket_name, file_key):
    try:
        # Скачиваем файл из бакета
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_data = response['Body'].read()

        # Проверяем размер файла
        if len(file_data) > MAX_SIZE:
            print(f"File '{file_key}' exceeds 300KB, compressing...")
            compressed_file = compress_image_to_size(file_data, MAX_SIZE)
            file_data = compressed_file.getvalue()

        # Загрузка файла обратно с очищенными мета-данными
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_data,
            Metadata={},  # Пустые мета-данные
        )

        return f"Metadata for file '{file_key}' cleaned and file compressed (if needed) successfully."
    except Exception as e:
        raise RuntimeError(f"Error processing file '{file_key}' in bucket '{bucket_name}': {e}")


def main(event, context):
    body = json.loads(event['body'])
    bucket_name = body.get('bucket_name')

    if not bucket_name:
        raise ValueError("Both 'bucket_name' and 'file_key' are required.")

    files = get_files(bucket_name)
    print(files.relative_paths[:4])

    # Синхронно обрабатываем файлы
    for file_path in files.relative_paths[:4]:
        clear_image_metadata(file_key=file_path, bucket_name=bucket_name)


    # Возврат успешного ответа
    return {
        "statusCode": 200,
        "body": json.dumps({
            "bucket_name": bucket_name,
            "status": "success"
        })
    }

# if __name__ == "__main__":
#     event = {
#         "body": json.dumps({
#             "bucket_name": "0001-small-test"
#         })
#     }
#     context = {}  # Пустой контекст, если он не используется
#     main(event, context)

    # except (json.JSONDecodeError, ValueError) as e:
    #     # Обработка ошибок валидации входных данных
    #     print(f"Ошибка обработки входных данных: {e}")
    #     return {
    #         "statusCode": 400,
    #         "body": json.dumps({
    #             "message": "Invalid input format",
    #             "error": str(e)
    #         })
    #     }
    # except RuntimeError as e:
    #     # Обработка ошибок из вспомогательных функций
    #     print(f"Ошибка при вызове вспомогательной функции: {e}")
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({
    #             "message": "Internal processing error",
    #             "error": str(e)
    #         })
    #     }
    # except Exception as e:
    #     # Общая обработка остальных ошибок
    #     print(f"Непредвиденная ошибка: {e}")
    #     return {
    #         "statusCode": 500,
    #         "body": json.dumps({
    #             "message": "Internal server error",
    #             "error": str(e)
    #         })
    #     }
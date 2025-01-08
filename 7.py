import os
import logging
from concurrent.futures import ThreadPoolExecutor
from botocore.config import Config
from dotenv import load_dotenv
import boto3
import requests

# Настроим логирование
log_file = "app.log"
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат вывода
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль
        logging.FileHandler(log_file, encoding='utf-8')  # Запись логов в файл
    ]
)
logger = logging.getLogger()

# Загрузка переменных окружения
load_dotenv()
YANDEX_ACCESS_KEY = os.getenv('YANDEX_CLOUD_ACCESS_KEY_ID')
YANDEX_SECRET_KEY = os.getenv('YANDEX_CLOUD_SECRET_ACCESS_KEY')
YANDEX_BUCKET_NAME = '001test001'  # Укажите ваш бакет
YANDEX_ENDPOINT_URL = 'https://storage.yandexcloud.net'

# Настройка клиента S3
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url=YANDEX_ENDPOINT_URL,
    aws_access_key_id=YANDEX_ACCESS_KEY,
    aws_secret_access_key=YANDEX_SECRET_KEY,
    config=Config(signature_version='s3v4', max_pool_connections=50)
)

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
        # Инициализируем переменную для токена пагинации
        continuation_token = None

        while True:
            # Выполняем запрос с возможным токеном продолжения
            if continuation_token:
                response = s3_client.list_objects_v2(
                    Bucket=bucket_name,
                    ContinuationToken=continuation_token
                )
            else:
                response = s3_client.list_objects_v2(Bucket=bucket_name)

            if 'Contents' in response:
                for obj in response['Contents']:
                    if not obj['Key'].endswith('/'):  # Исключаем папки
                        filename = obj['Key']
                        files.add_relative_path(filename)
                        files.add_full_path(f"{YANDEX_ENDPOINT_URL}/{bucket_name}/{filename}")

            # Если есть токен продолжения, запрашиваем следующую страницу
            if response.get('IsTruncated'):  # Если объекты не все, продолжаем с токеном
                continuation_token = response.get('NextContinuationToken')
            else:
                break  # Если объекты закончились, выходим из цикла

    except Exception as e:
        logger.error(f"Ошибка при получении списка файлов: {e}")

    logger.info(f"Длина списка файлов в бакете: {len(files.relative_paths)}")
    return files


def call_yandex_function(file_url, bucket_name):
    try:
        json = {
            "bucket_name": bucket_name,
            "file_key": file_url,
            'image_transform_option': 'second_phase'}
        logger.info(f"Вызов Яндекс функции с параметрами: {json}")
        response = requests.post(
            "https://functions.yandexcloud.net/d4eg8gpu7n7q7okqp839",
            json=json,
            timeout=180  # Увеличить при необходимости
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка вызова Яндекс Функции для {file_url}: {e}")
        return None


from collections import defaultdict


def check_unique_file_in_folders(bucket_name, condition=0):
    folders_with_multiple_files = []

    try:
        files = get_files(bucket_name)
        folder_dict = defaultdict(list)
        for file in files.relative_paths:
            folder = '/'.join(file.split('/')[:-1])
            folder_dict[folder].append(file)

        folders_with_multiple_files = (
            {folder: files for folder, files in folder_dict.items() if len(files) > 1},
            {folder: files for folder, files in folder_dict.items() if len(files) > 1 and len(files) != 144},
            {folder: files for folder, files in folder_dict.items() if len(files) != 144}
            )[condition]

    except Exception as e:
        logger.error(f"Ошибка при проверке папок: {e}")

    return folders_with_multiple_files

def delete_files_from_bucket(file_keys, bucket_name):
    for file_key in file_keys:
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        logger.info(f"Файл {file_key} удалён из бакета {bucket_name}.")


from concurrent.futures import ThreadPoolExecutor

def process_file(file_url, bucket_name):
    """Обработка одного файла, возвращаем True при успешной обработке, False при ошибке"""
    try:
        result = call_yandex_function(file_url, bucket_name)
        if result:
            logger.info(f"Успешная обработка файла {file_url}: {result}")
            return True  # Успешная обработка
        else:
            logger.error(f"Ошибка обработки файла {file_url}")
            return False  # Ошибка
    except Exception as e:
        logger.error(f"Ошибка при обработке файла {file_url}: {e}")
        return False  # Ошибка


def main(bucket_name):
    operation = input("Главное меню. Выберите операцию\n"
                      "1 - Запустить уникализацию файлов\n"
                      "2 - Запустить проверку на ошибки после выполненной уникализации\n"
                      "3 - Автоматически исправить ошибку с количеством файлов в папках\n"
                      "любая другая клавиша - выйти из программы\n")
    if operation not in ("123"):
        return operation
    if int(operation) == 2:
        wrong_folders = check_unique_file_in_folders(bucket_name, condition=2)
        logger.info(
            ("В папках ошибки не обнаружены",
             f"В следующих {len(list(wrong_folders))} папках находится неправильное количество файлов:\n\n")[bool(wrong_folders)])
        [logger.info(key) for key in list(wrong_folders.keys())]
        return

    for iteration in range(3):
        if int(operation) == 3 and iteration < 2:
            continue
        logger.info(
            ("Запускаем подготовительный этап проверки папок",
             "Переходим к этапу поиска и исправления ошибок")[bool(iteration)])

        folders = check_unique_file_in_folders(bucket_name, condition=iteration)

        if folders:
            if iteration == 2:
                logger.info(f"------------------\n\nВ следующих {len(list(folders))} папках находится неправильное количество файлов:\n\n")
                [logger.info(key) for key in list(folders.keys())]

            answer = 'y'
            if not iteration:
                logger.info(f"В следующих {len(list(folders))} папках находится более 1 файла,\n"
                            f"для продолжения работы потребуется удалить лишние файлы:")
                logger.info(folders.keys())
                answer = input("Удалить лишние файлы в этих папках? Y - да, N - нет. ")
            if answer.lower() == 'y':
                with ThreadPoolExecutor(max_workers=100) as executor:
                    for folder, files in list(folders.items()):
                        executor.submit(delete_files_from_bucket, files[1:], bucket_name)
            else:
                logger.info("Программа завершена")
                return
        else:
            logger.info(
                "Папок с лишними файлами не найдено" + (", переходим к уникализации изображений" if not iteration else "")
                )

            if iteration:
                break

        files = (get_files(bucket_name).relative_paths, [files[0] for files in folders.values()])[bool(iteration)]

        # Аинхронно обрабатываем файлы
        with ThreadPoolExecutor(max_workers=100) as executor:
            for file_path in files:
                logger.info(file_path)
                executor.submit(process_file, file_url=file_path, bucket_name=bucket_name)


    logger.info("Операция завершена.")







if __name__ == "__main__":
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    bucket_name = input("Введите имя бакета: ")
    while True:
        answer = main(bucket_name)
        if answer is not None:
            print("Программа завершена")
            break

import os
import logging
from concurrent.futures import ThreadPoolExecutor
from botocore.config import Config
from dotenv import load_dotenv
import boto3
from pprint import pprint
from random import shuffle


# Настроим логирование
log_file = "app.log"
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат вывода
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль
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


# Функция для получения списка папок
def get_folders(files):
    folders = Paths()
    try:
        for file in files.relative_paths:
            folder = '/'.join(file.split('/')[:-1])
            if not folder in folders.relative_paths:
                folders.add_relative_path(folder)

        for file in files.full_paths:
            folder = '/'.join(file.split('/')[:-1])
            if not folder in folders.full_paths:
                folders.add_full_path(folder)
    except Exception as e:
        print(f"Ошибка при получении списка папок: {e}")

    return folders

def get_products(files):
    products = Paths()
    try:
        for file in files.relative_paths:
            product = '/'.join(file.split('/')[:-2])
            if not product in products.relative_paths:
                products.add_relative_path(product)

        for file in files.full_paths:
            product = '/'.join(file.split('/')[:-2])
            if not product in products.full_paths:
                products.add_full_path(product)
    except Exception as e:
        print(f"Ошибка при получении списка папок: {e}")

    return products

import openpyxl

def update_excel_with_image_urls(file_name, sheet_name, image_urls):
    # Открытие Excel файла
    wb = openpyxl.load_workbook(file_name)

    # Открытие нужного листа
    sheet = wb[sheet_name]

    # Найдём индекс столбца с названием "ImageUrls"
    header_row = sheet[1]  # Предполагаем, что заголовки находятся в первой строке
    image_urls_column = None
    for col_idx, cell in enumerate(header_row, 1):
        if cell.value == "ImageUrls":
            image_urls_column = col_idx
            break

    if image_urls_column is None:
        raise ValueError("Столбец 'ImageUrls' не найден.")

    # Заполнение столбца "ImageUrls"
    row_idx = 2  # Начинаем с 2-й строки (после заголовка)
    for i, image_url in enumerate(image_urls):
        sheet.cell(row=row_idx, column=image_urls_column, value=image_url)
        row_idx += 1
        if i == 1:
            print("Печатаем", image_url)

    # Сохраняем изменения в файл
    wb.save(file_name)
    print(f"Файл {file_name} успешно обновлён.")

# Пример использования
file_name = "ggdevice.xlsx"
sheet_name = "2"  # Название листа



def main(bucket_name):
    files = get_files(bucket_name)
    folders = get_folders(files)
    print("Длина списка папок: ", len(folders.relative_paths))
    products = get_products(files)
    print("Длина списка товаров: ", len(products.relative_paths), products.full_paths[0])
    shuffle(files.relative_paths)
    print("Длина списка файлов: ", len(files.relative_paths), files.relative_paths[0])

    product_images = [
        [
            [
                f"{YANDEX_ENDPOINT_URL}/{bucket_name}/{file}" for file in files.relative_paths
                if file.startswith(folder + "/")
            ]
            for folder in folders.relative_paths
            if folder.startswith(product + "/")
        ]
        for product in products.relative_paths
    ]

    values_for_table = []
    for product in product_images:
        values_for_table.extend([" | ".join(items) for items in zip(*product)])
        values_for_table.append("")

    print(len(values_for_table))


    update_excel_with_image_urls(file_name, sheet_name, values_for_table)



if __name__ == "__main__":

    main("0001-small-test")
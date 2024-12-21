import math
import os
from io import BytesIO

import boto3
from botocore.config import Config
from dotenv import load_dotenv
from PIL import Image, ImageEnhance, ImageOps

load_dotenv()
YANDEX_ACCESS_KEY = os.getenv('YANDEX_CLOUD_ACCESS_KEY_ID')
YANDEX_SECRET_KEY = os.getenv('YANDEX_CLOUD_SECRET_ACCESS_KEY')
YANDEX_BUCKET_NAME = '001test001' # "adverts-bucket"
YANDEX_ENDPOINT_URL = 'https://storage.yandexcloud.net'

# Настройка клиента S3
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=YANDEX_ACCESS_KEY,
    aws_secret_access_key=YANDEX_SECRET_KEY,
    config=Config(signature_version='s3v4')
)


class Paths:
    def __init__(self):
        self.full_paths = []  # Список полных путей (с URL)
        self.relative_paths = []  # Список относительных путей (внутри бакета)

    def add_full_path(self, full_path):
        self.full_paths.append(full_path)

    def extend_full_paths(self, full_paths_list):
        self.full_paths.extend(full_paths_list)

    def add_relative_path(self, relative_path):
        self.relative_paths.append(relative_path)

    def extend_relative_paths(self, relative_paths_list):
        self.relative_paths.extend(relative_paths_list)


# Функция для получения списка папок
def get_folders(bucket_name):
    folders = Paths()
    try:
        files = get_files(bucket_name)

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

# Функция для получения списка файлов
def get_files(bucket_name):
    files = Paths()
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                # Проверяем, что объект не является папкой (папки заканчиваются на '/')
                if not obj['Key'].endswith('/'):
                    filename = obj['Key'].replace(' ', '%20')
                    files.add_relative_path(filename)
                    files.add_full_path(
                        f"{YANDEX_ENDPOINT_URL}/{YANDEX_BUCKET_NAME}/{filename}")
        else:
            print("Бакет пустой или не содержит объектов.")
    except Exception as e:
        print(f"Ошибка при получении списка файлов: {e}")
    return files  # Возвращаем список файлов


def download_and_clean_metadata(bucket_name, file_key):
    try:
        # Скачиваем файл из бакета
        file_name = file_key.split('/')[-1]  # Имя файла
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

        # Получаем содержимое файла
        file_data = response['Body'].read()

        # Загрузка файла обратно с минимальными мета-данными
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,  # Загружаем файл обратно в ту же директорию
            Body=file_data,
            Metadata={},  # Пустые мета-данные
        )

        print(f"Файл {file_key} был успешно загружен обратно с очищенными мета-данными.")
        return BytesIO(file_data)

    except Exception as e:
        print(f"Ошибка при скачивании и загрузке файла {file_key}: {e}")



def calculate_opposite(hypotenuse, angle_deg):
    angle_rad = math.radians(angle_deg)
    return hypotenuse * math.sin(angle_rad)

def rotate_image(image_path_or_file, direction='right', degrees=90):
    # Открываем изображение
    image = Image.open(image_path_or_file)

    # Проверяем направление и корректируем угол
    if direction == 'right':
        degrees = -degrees

    # Поворачиваем изображение
    rotated_image = image.rotate(degrees, expand=False)
    width, height = rotated_image.size
    print('После ротации')
    print('width =', width, 'height =', height)

    # Размеры исходного изображения
    width, height = image.size

    # Рассчитываем, сколько обрезать
    height_cut = calculate_opposite(width, abs(degrees))
    print('width =', width, 'Обрезаем сверху и снизу:', height_cut)
    # Вычисляем обрезку слева и справа
    width_cut = calculate_opposite(height, abs(degrees))
    print('height =', height, 'Обрезаем слева и справа:', width_cut)

    # Обрезаем новое изображение
    left = width_cut
    right = width - width_cut
    top = height_cut
    bottom = height - height_cut

    print('left, top, right, bottom :', left, top, right, bottom)
    cropped_image = rotated_image.crop((left, top, right, bottom))


    # Преобразуем в RGB, если требуется
    if cropped_image.mode == 'RGBA':
        cropped_image = cropped_image.convert('RGB')

    # Сохраняем результат в формате JPG в память
    output = BytesIO()
    cropped_image.save(output, format='JPEG')
    output.seek(0)  # Возвращаем указатель на начало файла
    return output


def upload_image(changed_file, file_name, bucket_name):
    try:
        # Загрузить изменённое изображение обратно в Yandex Cloud
        new_file_key = f"{file_name}"  # Путь в бакете
        s3_client.put_object(
            Bucket=bucket_name,
            Key=new_file_key,
            Body=changed_file.getvalue(),
            Metadata={}  # Пустые мета-данные
        )

        print(f"Файл {new_file_key} успешно загружен в Yandex Cloud с изменениями.")

    except Exception as e:
        print(f"Ошибка при обработке и загрузке файла {file_name}: {e}")


def add_suffix_to_filename(file_path, suffix):
    parts = file_path.rsplit('.', 1)
    return f"{parts[0]}_{suffix}.JPG" if len(parts) > 1 else f"{file_path}_{suffix}"


def adjust_contrast(file_obj, factor):
    # Функция для изменения контрастности
    image = Image.open(file_obj)
    # Применение ориентации из EXIF
    image = ImageOps.exif_transpose(image)
    enhancer = ImageEnhance.Contrast(image)
    adjusted_image = enhancer.enhance(factor)

    # Сохранение результата в BytesIO
    output = BytesIO()
    adjusted_image.save(output, format="JPEG")
    output.seek(0)
    return output

def adjust_brightness(file_obj, factor):
    # Функция для изменения яркости
    image = Image.open(file_obj)
    # Применение ориентации из EXIF
    image = ImageOps.exif_transpose(image)
    enhancer = ImageEnhance.Brightness(image)
    adjusted_image = enhancer.enhance(factor)

    # Сохранение результата в BytesIO
    output = BytesIO()
    adjusted_image.save(output, format="JPEG")
    output.seek(0)
    return output


def adjust_white_balance(file_obj, red_factor, green_factor, blue_factor):
    image = Image.open(file_obj)
    # Применение ориентации из EXIF
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")

    # Разделение изображения на каналы
    r, g, b = image.split()

    # Применение коэффициентов для каждого канала
    r = r.point(lambda i: i * red_factor)
    g = g.point(lambda i: i * green_factor)
    b = b.point(lambda i: i * blue_factor)

    # Объединение каналов обратно
    adjusted_image = Image.merge("RGB", (r, g, b))

    # Сохранение результата в BytesIO
    output = BytesIO()
    adjusted_image.save(output, format="JPEG")
    output.seek(0)
    return output


def process_and_save(file_path, edit_function, *args):
    print(file_path)
    print(edit_function)
    print(*args)
    # Открыть файл и передать в функцию редактирования
    with open(file_path, "rb") as file_obj:
        output = edit_function(file_obj, *args)

    # Определение нового имени файла
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = f"{base}_{counter}{ext}"

    while os.path.exists(new_file_path):
        counter += 1
        new_file_path = f"{base}_{counter}{ext}"

    # Сохранить результат
    with open(new_file_path, "wb") as output_file:
        output_file.write(output.getvalue())

    print(f"Файл сохранён как: {new_file_path}")
    return new_file_path

# Ввод названия бакета
bucket_name = YANDEX_BUCKET_NAME # input("Введите название бакета: ")


# def main():
    # # Получение списка папок
    # folders = get_folders(bucket_name)
    # # print("\nСписок относительных путей папок в бакете:")
    # # for folder in folders.relative_paths:
    # #     print(folder)
    # # print("\nСписок абсолютных путей папок в бакете:")
    # # for folder in folders.full_paths:
    # #     print(folder)

    # # Получение списка файлов
    # files = get_files(bucket_name)
    # print("\nСписок относительных путей файлов в бакете:")
    # print(list(zip(files.relative_paths, folders.relative_paths)))
    # for file in files.relative_paths:
    #     file = "01/noinf1/1/3.jpg"
    #     # file = "03/noinf1/1/2.jpg"
    #     file_data = download_and_clean_metadata(bucket_name, file)

    #     output = adjust_brightness(file_data, 0.7)
    #     new_name = add_suffix_to_filename(file, "brightness")
    #     upload_image(output, new_name, bucket_name)

    #     break


    #     # Создаём и загружаем изображение, повёрнутое на 1 градус вправо
    #     output = rotate_image(file_data, direction='right', degrees=1)
    #     new_name = add_suffix_to_filename(file, "right_rotated_1_degrees")
    #     upload_image(output, new_name, bucket_name)

    #     # Создаём и загружаем изображение, повёрнутое на 2 градус вправо
    #     output = rotate_image(file_data, direction='right', degrees=2)
    #     new_name = add_suffix_to_filename(file, "right_rotated_2_degrees")
    #     upload_image(output, new_name, bucket_name)

    #     # Создаём и загружаем изображение, повёрнутое на 1 градус влево
    #     output = rotate_image(file_data, direction='left', degrees=1)
    #     new_name = add_suffix_to_filename(file, "left_rotated_1_degrees")
    #     upload_image(output, new_name, bucket_name)

    #     # Создаём и загружаем изображение, повёрнутое на 2 градус влево
    #     output = rotate_image(file_data, direction='left', degrees=2)
    #     new_name = add_suffix_to_filename(file, "left_rotated_2_degrees")
    #     upload_image(output, new_name, bucket_name)


    #     break


    # print("\nСписок абсолютных путей файлов в бакете:")
    # for file in files.full_paths:
    #     print(file)

white_balance_factors = (
    (1.1, 1.0, 0.9),  # Лёгкий сдвиг в сторону тёплых тонов
    (0.9, 1.0, 1.1),  # Лёгкий сдвиг в сторону холодных тонов
    (1.0, 1.1, 0.9),  # Усиление зелёного с уменьшением синего
    (1.0, 0.9, 1.1),  # Ослабление зелёного, усиление синего
    (1.1, 0.9, 1.0),  # Лёгкий сдвиг в сторону красного
    (0.9, 1.1, 1.0),  # Усиление зелёного, ослабление красного
    (1.05, 1.0, 0.95),  # Едва заметное усиление красного
    (0.95, 1.0, 1.05),  # Едва заметное усиление синего
    (1.0, 1.05, 0.95),  # Лёгкое усиление зелёного
    (1.0, 0.95, 1.05),  # Лёгкое ослабление зелёного
    (1.1, 1.1, 0.9),  # Усиление красного и зелёного, ослабление синего
    (0.9, 1.1, 1.1),  # Усиление зелёного и синего, ослабление красного
    (1.05, 0.95, 1.0),  # Едва заметный сдвиг
    (0.95, 1.05, 1.0),  # Едва заметный сдвиг в обратную сторону
)


if __name__ == "__main__":
    for tpl in white_balance_factors:
        process_and_save("3.jpg", adjust_white_balance, *tpl)
    #main()
    # Пример использования:
    # Если хотите сохранить изображение в файл
    # rotated_img = rotate_image("Screenshot_28.png ", direction='right', degrees=45)
    # with open('rotated_image.jpg', 'wb') as f:
    #     f.write(rotated_img.getvalue())

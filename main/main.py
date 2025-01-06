import json
import math
import os
from io import BytesIO

import boto3
import cv2
import numpy as np
from botocore.config import Config
from PIL import Image, ImageEnhance, ImageOps

from patterns import patterns

# Настройка клиента S3
s3_client = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    config=Config(signature_version='s3v4')
    # aws_access_key_id='my_access_key_id',
    # aws_secret_access_key='my_secret_access_key'
)

MAX_SIZE = 307200  # Максимальный размер файла (300 КБ)

def calculate_opposite(hypotenuse, angle_deg):
    angle_rad = math.radians(angle_deg)
    return hypotenuse * math.sin(angle_rad)


def rotate_image(image_path_or_file, direction, degrees):
    if direction not in ['left', 'right']:
        raise ValueError("Direction must be 'left' or 'right'.")

    # Read image as a numpy array
    image = cv2.imdecode(np.frombuffer(image_path_or_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Get image dimensions
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Calculate rotation angle
    angle = -degrees if direction == 'right' else degrees

    # Compute the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    height_cut = calculate_opposite(w, abs(degrees))

    # Вычисляем обрезку слева и справа
    width_cut = calculate_opposite(h, abs(degrees))
    width = int(w - width_cut * 2)
    height = int(h - height_cut * 2)

    rotation_matrix[0, 2] -= (w - width) / 2
    rotation_matrix[1, 2] -= (h - height) / 2

    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    # Convert back to a file-like object
    is_success, buffer = cv2.imencode('.jpg', rotated_image)
    if not is_success:
        raise RuntimeError("Failed to encode rotated image.")

    return BytesIO(buffer.tobytes())


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


def add_suffix_to_filename(file_path, pattern_name, suffix, args):
    print("принт из add_suffix_to_filename", "file_path =", file_path, 'pattern_name =', pattern_name, 'suffix =', suffix, 'args =', args)
    parts = file_path.rsplit('.', 1)
    if not all(type(arg) in (int, float, str) for arg in args):
        args = [(float(arg), int(arg))[round(float(arg), 2) == int(arg)] for arg in args]
    if f"pattern_{pattern_name}" in file_path:
        pattern_name = ""
    else:
        pattern_name = f"_pattern_{pattern_name}"
    return f"{parts[0]}{pattern_name}_{suffix}_{args}.JPG" if len(parts) > 1 else f"{file_path}_{suffix}"


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


def resize_image(file_obj, width_percent):
    image = Image.open(file_obj)
    # Применение ориентации из EXIF
    image = ImageOps.exif_transpose(image)

    # Вычисление новых размеров
    new_width = int(image.width * (width_percent / 100))

    # Изменение размера изображения
    resized_image = image.resize((new_width, image.height))

    # Сохранение результата в BytesIO
    output = BytesIO()
    resized_image.save(output, format="JPEG")
    output.seek(0)
    return output


def crop_image(file_obj, left=0, top=0, right=0, bottom=0):
    image = Image.open(file_obj)
    # Применение ориентации из EXIF
    image = ImageOps.exif_transpose(image)

    # Вычисление новых границ
    width, height = image.size
    crop_box = (
        left,
        top,
        width - right,
        height - bottom
    )

    # Проверка границ на корректность
    if crop_box[0] < 0 or crop_box[1] < 0 or crop_box[2] > width or crop_box[3] > height:
        raise ValueError("Invalid crop dimensions: resulting size is out of bounds.")

    # Обрезка изображения
    cropped_image = image.crop(crop_box)

    # Сохранение результата в BytesIO
    output = BytesIO()
    cropped_image.save(output, format="JPEG")
    output.seek(0)
    return output


def crop_image_by_percentage(file_obj, left_pct=0, top_pct=0, right_pct=0, bottom_pct=0):
    image = Image.open(file_obj)
    # Применение ориентации из EXIF
    image = ImageOps.exif_transpose(image)

    # Получение размеров изображения
    width, height = image.size

    # Вычисление границ обрезки в пикселях на основе процентов
    left = int(width * left_pct / 100)
    top = int(height * top_pct / 100)
    right = int(width * right_pct / 100)
    bottom = int(height * bottom_pct / 100)

    # Вычисление новых границ
    crop_box = (
        left,
        top,
        width - right,
        height - bottom
    )

    # Проверка границ на корректность
    if crop_box[0] < 0 or crop_box[1] < 0 or crop_box[2] > width or crop_box[3] > height:
        raise ValueError("Invalid crop dimensions: resulting size is out of bounds.")

    # Обрезка изображения
    cropped_image = image.crop(crop_box)

    # Сохранение результата в BytesIO
    output = BytesIO()
    cropped_image.save(output, format="JPEG")
    output.seek(0)
    return output


def delete_files_from_bucket(file_keys, bucket_name):
    for file_key in file_keys:
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        print(f"Файл {file_key} удалён из бакета {bucket_name}.")



def list_files_in_folder(bucket_name, file_key):
    folder_path = "/".join(file_key.split("/")[:-1]) + "/"
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
    return [obj['Key'] for obj in response.get('Contents', [])]




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

def process_and_save(patterns, files, bucket_name):
    for name in files:
        for pattern_name, pattern in patterns.items():
            new_name = name
            response = s3_client.get_object(Bucket=bucket_name, Key=name)
            file_obj = BytesIO(response['Body'].read())

            for function in functions.keys():
                args = pattern.get(function.__name__)
                if args:
                    new_name = add_suffix_to_filename(new_name, pattern_name, functions[function], args)
                    file_obj = function(file_obj, *args)
            # Определение нового имени файла
            base, ext = os.path.splitext(new_name)
            new_name = f"{base}{ext}"
            s3_client.put_object(Body=file_obj.getvalue(), Bucket=bucket_name, Key=new_name)


functions = {
    adjust_white_balance: "wb",
    adjust_contrast: "contrast",
    adjust_brightness: "brightness",
    crop_image_by_percentage: "crop",
    resize_image: "resize",
    rotate_image: "rotate"
    }


def main(event, context):
    # try:
    # Десериализация тела запроса
    body = json.loads(event['body'])
    bucket_name = body.get('bucket_name')
    file_key = body.get('file_key')
    image_transform_option = body.get('image_transform_option')

    if not bucket_name or not file_key:
        raise ValueError("Both 'bucket_name' and 'file_key' are required.")

    # Вызов первой функции
    clear_image_metadata(bucket_name, file_key)

    first_phase = patterns["first_phase"]

    process_and_save(first_phase, [file_key], bucket_name)

    files = list_files_in_folder(bucket_name, file_key)

    second_phase = patterns[image_transform_option]
    process_and_save(second_phase, files, bucket_name)
    files = [f for f in list_files_in_folder(bucket_name, file_key) if f != file_key]
    third_phase = patterns["third_phase"]
    for count, (key, value) in enumerate(third_phase.items()):
        crop_settings = {key: value}
        files_to_crop = [files[count]]
        process_and_save(crop_settings, files_to_crop, bucket_name)
    delete_files_from_bucket(files, bucket_name)

    # Возврат успешного ответа
    return {
        "statusCode": 200,
        "body": json.dumps({
            "bucket_name": bucket_name,
            "file_key": file_key,
            "status": "success"
        })
    }

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

# if __name__ == "__main__":
#     event = {
#         "body": json.dumps({
#             "bucket_name": "0001-small-test",
#             "file_key": "04/noinf1/3/2023-05-11 13-27-08.JPG",
#             'image_transform_option': 'second_phase'
#         })
#     }
#     context = {}  # Пустой контекст, если он не используется
#     main(event, context)

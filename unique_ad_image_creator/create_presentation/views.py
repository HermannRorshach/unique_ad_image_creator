import os
import shutil
from io import BytesIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import render

from .main import extract_data, main, read_google_sheets


def remove_garbage(folder_path):
    # Удаление файлов по условиям
    for filename in os.listdir(folder_path):
        if filename.startswith(
            'Презентация') and filename.endswith(
                '.pdf') or filename == 'output.pdf':
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)  # Удаление файла

    # Удаление всех файлов в папке media
    media_folder_path = os.path.join(settings.MEDIA_ROOT)
    for media_filename in os.listdir(media_folder_path):
        media_file_path = os.path.join(media_folder_path, media_filename)
        # Проверяем, является ли это файлом
        if os.path.isfile(media_file_path):
            # Удаление файла
            os.remove(media_file_path)
        elif os.path.isdir(media_file_path):
            # Если это директория, удаляем ее и все содержимое
            shutil.rmtree(media_file_path)


def upload_files(request):
    remove_garbage(os.path.join(settings.BASE_DIR, "create_presentation"))

    if request.method == 'POST':
        images = request.FILES.getlist('images')

        # Проверяем, был ли загружен Excel-файл
        excel_file = request.FILES.get('excel_file')
        if excel_file:
            # Сохраняем Excel-файл
            fs = FileSystemStorage()
            excel_filename = fs.save(excel_file.name, excel_file)
            data_source = os.path.join(settings.MEDIA_ROOT, excel_filename)
        else:
            # Если файл не загружен, читаем данные из Google Sheets
            data_source = read_google_sheets()

        # Сохраняем изображения
        fs = FileSystemStorage()
        saved_image_filenames = [fs.save(image.name, image)
                                 for image in images]
        first_image, second_image = saved_image_filenames

        # Обрабатываем данные
        if excel_file:
            all_data = extract_data(data_source)
        else:
            all_data = data_source

        if isinstance(all_data, str):
            error_message = (f"Данные невалидны. Пожалуйста, проверьте файл."
                             f"<br>Ошибка: {all_data}")
            return render(request, 'create_presentation/upload_files.html',
                          {'error_message': error_message})

        pdf_file_path, filename = main(all_data, first_image, second_image)

        # Удаляем загруженные файлы
        if excel_file:
            fs.delete(excel_filename)
        fs.delete(first_image)
        fs.delete(second_image)

        # Создание выходного потока
        pdf_output_stream = BytesIO()

        # Открытие и копирование содержимого
        with open(pdf_file_path, 'rb') as existing_pdf_file:
            pdf_output_stream.write(existing_pdf_file.read())

            # Перемещаем указатель потока в начало
            pdf_output_stream.seek(0)
            return FileResponse(
                pdf_output_stream,
                as_attachment=True,
                filename=f"{filename}.pdf"
            )
    return render(request, 'create_presentation/upload_files.html')


def faq(request):
    return render(request, 'create_presentation/FAQ.html')


def contacts(request):
    return render(request, 'create_presentation/contacts.html')

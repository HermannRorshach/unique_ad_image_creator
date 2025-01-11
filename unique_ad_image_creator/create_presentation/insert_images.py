import os

import fitz  # PyMuPDF
from django.conf import settings
from PIL import Image


def insert_images(doc, contexts):

    def insert_repeated_image(
            page, image, rect, repeat_count=1,
            interval=0, direction='horizontal_asc'):
        # Вставляем картинку несколько раз с интервалом
        for i in range(repeat_count):
            if direction == 'horizontal_asc':
                offset_rect = rect + (i * interval, 0, i * interval, 0)
            elif direction == 'horizontal_desc':
                offset_rect = rect - (i * interval, 0, i * interval, 0)
            else:
                offset_rect = rect + (0, i * interval, 0, i * interval)
            page.insert_image(offset_rect, stream=image)

    # Открываем существующий PDF

    for context in contexts:

        img = Image.open(os.path.join(
            settings.BASE_DIR, f"{context['image_path']}"))
        img_width, img_height = img.size
        # Загружаем изображение
        image = open(os.path.join(settings.BASE_DIR,
                     f"{context['image_path']}"), "rb").read()
        # Выбираем страницу
        page = doc.load_page(context['page_num'])
        x, y = context['coordinates']
        # Определяем позицию для вставки
        rect = fitz.Rect(x, y, img_width *
                         context['coef'] + x,
                         img_height * context['coef'] + y)
        # Определяем количество раз,
        # которые нужно выполнить вставку изображения
        repeat_insertion = context.get('repeat_insertion', False)
        if repeat_insertion:
            repeat_count = repeat_insertion.get('repeat_count', 1)
            interval = repeat_insertion.get('interval', 0)
            direction = repeat_insertion.get('direction', 'horizontal')
            # Вставляем изображение
            insert_repeated_image(
                page, image, rect, repeat_count, interval, direction)
        else:
            insert_repeated_image(page, image, rect)

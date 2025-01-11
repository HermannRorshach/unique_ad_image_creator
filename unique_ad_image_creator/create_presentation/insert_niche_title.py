import os

import fitz
from django.conf import settings


def add_title(doc, context):

    # Загружаем первую страницу для редактирования
    page = doc.load_page(context['page_num'])
    font_path = os.path.join(
        settings.BASE_DIR, f"create_presentation/{context['font_path']}"
    )

    # Вставка кастомного шрифта на страницу
    fontname = 'CustomFont'
    # Загрузка кастомного шрифта
    page.insert_font(fontfile=font_path, fontname=fontname)

    # Устанавливаем начальные координаты для текста
    current_y = context['y_coordinate']

    # Параметры страницы
    page_width = page.rect.width
    margin = context['margin']

    # Прямоугольник для вставки текста
    text_rect = fitz.Rect(
        margin,
        current_y,
        page_width - margin,
        current_y + context['font_size'] * 10
    )

    # Вставляем текст с кастомным шрифтом
    page.insert_textbox(
        text_rect,
        context['text'],
        fontsize=context['font_size'],
        fontname='CustomFont',
        fill=context['color'],
        align=1
    )
    # current_y += 90

import os

import fitz
from django.conf import settings


def add_centered_text(doc, contexts):
    # Открываем существующий PDF

    for context in contexts:

        # Загружаем первую страницу для редактирования
        page = doc.load_page(context['page_num'])
        font_path = os.path.join(
            settings.BASE_DIR, f"create_presentation/{context['font_path']}")

        # Вставка кастомного шрифта на страницу
        fontname = 'CustomFont'
        page.insert_font(fontfile=font_path, fontname=fontname)

        # Параметры страницы и текста
        current_y = context['y_coordinate']
        text_x_center = context['x_center']
        text_width = context['text_width']

        # Прямоугольник для вставки текста с выравниванием
        # по заданной координате X
        left_x = text_x_center - (text_width / 2)
        right_x = text_x_center + (text_width / 2)
        text_rect = fitz.Rect(left_x, current_y, right_x,
                              current_y + context['font_size'] * 10)

        # Вставляем текст с кастомным шрифтом
        page.insert_textbox(text_rect, context['text'],
                            fontsize=context['font_size'],
                            fontname='CustomFont',
                            fill=context['color'],
                            align=1)

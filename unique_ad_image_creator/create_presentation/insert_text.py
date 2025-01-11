import os

from django.conf import settings


def insert_texts(doc, contexts):

    for context in contexts:

        # Выбор страницы, на которой нужно работать
        page = doc.load_page(context['page_num'])  # Первая страница (индекс 0)

        # Путь к кастомному шрифту
        font_path = os.path.join(
            settings.BASE_DIR, f"create_presentation/{context['font_path']}")

        # Вставка кастомного шрифта на страницу
        fontname = os.path.splitext(os.path.basename(context['font_path']))[0]
        page.insert_font(fontfile=font_path, fontname=fontname)

        # Настройка шрифта и текста
        text = context['text']
        text_position = context['coordinates']   # Позиция (x, y) для текста

        # Добавление текста на страницу с использованием кастомного шрифта
        page.insert_text(
            text_position,              # Позиция текста
            text,                       # Содержимое текста
            fontsize=context['font_size'],                # Размер шрифта
            fontname=fontname,          # Имя кастомного шрифта
            # Цвет текста (в диапазоне от 0 до 1)
            color=context['color']
        )

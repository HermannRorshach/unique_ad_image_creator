import copy as xerox
import os

from django.conf import settings
from PIL import Image, ImageFont

from .add_centered_text import add_centered_text
from .insert_images import insert_images
from .insert_text import insert_texts

context_scale_value = {
    'page_num': 7,
    'font_size': 30,
    'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
    'text': '0',
    'color': (1, 1, 1),
    'y_coordinate': 700,
    'x_center': 370,  # Центр текста по оси X
    'text_width': 180,  # Ширина текстового блока
    'margin': 10,
}

context_insert_images = [
    {
        'image_path': 'create_presentation/img/Line 1.png',
        'page_num': 7,
        'coordinates': (1114, 283),
        'repeat_insertion': {
            'repeat_count': 5,
            'interval': 186,
            'direction': 'horizontal_desc'
        },
        'coef': 1,
    },
    {
        'image_path': 'create_presentation/img/output_image_1.png',
        'page_num': 7,
        'coordinates': (376, 350),
        'coef': 1,
    },
    {
        'image_path': 'create_presentation/img/output_image_2.png',
        'page_num': 7,
        'coordinates': (376, 517),
        'coef': 1,
    }
]

contexts_for_values_in_side = [
    {
        'page_num': 7,
        'font_size': 30,
        'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
        'text': '',
        'color': (1, 1, 1),
        'coordinates': [390, 390],
    },
    {
        'page_num': 7,
        'font_size': 30,
        'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
        'text': '',
        'color': (1, 1, 1),
        'coordinates': [390, 560],
    }
]

context_values_in_rectangles = [
    {
        'page_num': 7,
        'font_size': 30,
        'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
        'text': '0',
        'color': (0, 0, 0),
        'y_coordinate': 367,
        'x_center': 500,  # Центр текста по оси X
        'text_width': 180,  # Ширина текстового блока
        'margin': 10,
    }
]


def create_color_rectanges(img_width, img_height, color, output_path):
    # Если ширина равна нулю, то задаем ширину 10px и
    # делаем прямоугольник прозрачным.
    # Почему ширина именно 10px? Просто так
    if img_width == 0:
        img_width = 10
        color = (0, 0, 0, 0)  # Прозрачный цвет (RGBA)

    # Создание нового изображения
    image = Image.new("RGBA", (img_width, img_height), color)

    # Сохранение изображения в формате PNG
    image.save(os.path.join(settings.BASE_DIR,
               f"create_presentation/{output_path}"))
    image.close()


coordinates_numbers_on_scale = (370, 556, 742, 928)


def calculate_scale_and_widths(value_1, value_2):
    max_value = max(value_1, value_2)

    step = 1
    max_scale_value = step * 5
    level = 0

    while max_scale_value < max_value:
        level += 1
        step = max_scale_value
        if (level % 3 == 0) or (level % 3 == 2):
            max_scale_value = step * 5
        elif level % 3 == 1:
            max_scale_value = step * 4

    img_1_width = int(value_1 / (step / 186))
    img_2_width = int(value_2 / (step / 186))

    scale_marks = [step * _ for _ in range(5)]

    return img_1_width, img_2_width, scale_marks


def is_text_fitting(value, font_path, img_width, context):
    # Корректное формирование абсолютного пути
    full_font_path = os.path.join(os.path.dirname(__file__), font_path)

    # Проверка, существует ли файл шрифта
    if not os.path.exists(full_font_path):
        raise FileNotFoundError(f"Шрифт не найден по пути: {full_font_path}")

    # Вычисляем ширину текста
    font = ImageFont.truetype(full_font_path, context['font_size'])
    bbox = font.getbbox(str(value))

    # Выводим ширину текста в консоль
    text_width_actual = bbox[2] - bbox[0]

    # Проверяем, поместится ли текст в указанный прямоугольник
    return text_width_actual + 40 <= img_width


def add_transparent_gap_to_line(input_image_path, output_image_path,
                                gap_start, gap_height):
    # Открываем исходное изображение
    image = Image.open(os.path.join(settings.BASE_DIR,
                       f"{input_image_path}")).convert("RGBA")

    # Получаем размеры исходного изображения
    width, height = image.size

    # Создаем новое изображение с таким же размером и поддержкой прозрачности
    new_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # Копируем часть изображения до разрыва
    new_image.paste(image.crop((0, 0, width, gap_start)), (0, 0))

    # Копируем часть изображения после разрыва
    new_image.paste(image.crop((0, gap_start + gap_height,
                    width, height)), (0, gap_start + gap_height))
    # Сохраняем новое изображение
    new_image.save(os.path.join(settings.BASE_DIR,
                   f"{output_image_path}"), "PNG")


def handle_text_overflow(
        doc, value_1, value_2, img_1_width, img_2_width, context,
        copy_contexts_for_values_in_side, copy_context_insert_images
):
    flag_1, flag_1_1, flag_2 = False, False, False
    interval = copy_context_insert_images[0]['repeat_insertion']['interval']
    if (not is_text_fitting(
        value_1, 'fonts/CodePro/Code-Pro-Bold.ttf',
        img_1_width, context) and not is_text_fitting(
            value_1, 'fonts/CodePro/Code-Pro-Bold.ttf', abs(
                interval - img_1_width),
            context)) or (not is_text_fitting(
                value_2, 'fonts/CodePro/Code-Pro-Bold.ttf', img_2_width,
                context) and not is_text_fitting(
                value_2, 'fonts/CodePro/Code-Pro-Bold.ttf',
                abs(interval - img_2_width), context)):
        copy_context_insert_images[0]['repeat_insertion']['repeat_count'] = 3
    if not is_text_fitting(value_1, 'fonts/CodePro/Code-Pro-Bold.ttf',
                           img_1_width, context):
        flag_1 = True
        if not is_text_fitting(value_1, 'fonts/CodePro/Code-Pro-Bold.ttf',
                               abs(interval - img_1_width), context):
            input_image_path = 'create_presentation/img/Line 1.png'
            output_image_path = 'create_presentation/img/line_with_gap.png'
            gap_start = 67  # Начало разрыва (в пикселях)
            gap_height = 60  # Высота разрыва (в пикселях)
            flag_1_1 = True
            add_transparent_gap_to_line(
                input_image_path, output_image_path, gap_start, gap_height)
        copy_contexts_for_values_in_side[0]['coordinates'][0] = (376
                                                                 + img_1_width
                                                                 + 30)
        copy_contexts_for_values_in_side[0]['text'] = str(value_1)
        insert_texts(doc, [copy_contexts_for_values_in_side[0]])

    if not is_text_fitting(value_2, 'fonts/CodePro/Code-Pro-Bold.ttf',
                           img_2_width, context):
        flag_2 = True
        if not is_text_fitting(
                value_2, 'fonts/CodePro/Code-Pro-Bold.ttf',
                abs(interval - img_2_width), context):
            if flag_1_1:
                input_image_path = 'create_presentation/img/line_with_gap.png'
            else:
                input_image_path = 'create_presentation/img/Line 1.png'
            output_image_path = 'create_presentation/img/line_with_gap.png'
            gap_start = 234  # Начало разрыва (в пикселях)
            gap_height = 60  # Высота разрыва (в пикселях)

            add_transparent_gap_to_line(
                input_image_path, output_image_path, gap_start, gap_height)

        copy_contexts_for_values_in_side[1]['coordinates'][0] = (376
                                                                 + img_2_width
                                                                 + 30)
        copy_contexts_for_values_in_side[1]['text'] = str(value_2)
        insert_texts(doc, [copy_contexts_for_values_in_side[1]])

    context_lines = [
        {
            'image_path': 'create_presentation/img/Line 1.png',
            'page_num': 7,
            'coordinates': (370, 283),
            'coef': 1,
        },
        {
            'image_path': 'create_presentation/img/line_with_gap.png',
            'page_num': 7,
            'coordinates': (556, 283),
            'coef': 1,
        }
    ]

    context_lines.extend(copy_context_insert_images)

    insert_images(doc, context_lines)

    return flag_1, flag_2


def replace_images_with_squares():
    image_paths = [
        'create_presentation/img/search_view_cost_1.png',
        'create_presentation/img/recommendation_view_cost_1.png',
        'create_presentation/img/search_view_cost_2.png',
        'create_presentation/img/recommendation_view_cost_2.png',
        'create_presentation/img/search_view_cost_3.png',
        'create_presentation/img/recommendation_view_cost_3.png',
        'create_presentation/img/output_image_1.png',
        'create_presentation/img/output_image_2.png'
    ]
    for img_path in image_paths:
        # Заменяем каждое изображение на прозрачный квадрат 1x1
        # Прозрачный квадрат
        square = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        square.save(img_path)  # Сохраняем с тем же именем


def create_diagram_page_8(doc, context):
    # Создаём независимые копии, чтобы изменять именно их
    copy_contexts_for_values_in_side = xerox.deepcopy(
        contexts_for_values_in_side)
    copy_context_values_in_rectangles = xerox.deepcopy(
        context_values_in_rectangles)
    copy_context_insert_images = xerox.deepcopy(context_insert_images)

    value_1 = context['value_1']
    value_2 = context['value_2']

    img_1_width, img_2_width, scale_marks = calculate_scale_and_widths(
        value_1, value_2)
    img_height = 60

    # Цвет (в формате RGB)
    color_1 = (255, 255, 255)  # Цвет B8FF00 в формате RGB
    color_2 = (184, 255, 0)

    create_color_rectanges(img_1_width, img_height,
                           color_1, "img/output_image_1.png")
    create_color_rectanges(img_2_width, img_height,
                           color_2, "img/output_image_2.png")

    copy_context_values_in_rectangles[0]['x_center'] = 370 + img_1_width / 2
    copy_context_values_in_rectangles[0]['text'] = str(value_1)
    copy = {key: value for key,
            value in copy_context_values_in_rectangles[0].items()}
    copy['x_center'] = 370 + img_2_width / 2
    copy['text'] = str(value_2)
    copy['y_coordinate'] = 536
    copy_context_values_in_rectangles.append(copy)

    if (is_text_fitting(
        value_1, 'fonts/CodePro/Code-Pro-Bold.ttf',
        img_1_width, context
    ) and is_text_fitting(
            value_2, 'fonts/CodePro/Code-Pro-Bold.ttf',
            img_2_width, context)
    ):
        insert_images(doc, copy_context_insert_images)
        add_centered_text(doc, copy_context_values_in_rectangles)
    else:
        flag_1, flag_2 = handle_text_overflow(
            doc, value_1, value_2, img_1_width, img_2_width,
            context, copy_contexts_for_values_in_side,
            copy_context_insert_images)
        if not flag_1:
            add_centered_text(doc, [copy_context_values_in_rectangles[0]])
        if not flag_2:
            add_centered_text(doc, [copy_context_values_in_rectangles[1]])

    context_text = []
    x_center = context_scale_value['x_center']
    for mark in scale_marks:
        copy = {key: value for key, value in context_scale_value.items()}
        copy['text'] = str(mark)
        copy['x_center'] = x_center
        context_text.append(copy)
        x_center += 186
    add_centered_text(doc, context_text)


context = {
    # 'value_1': 300100000,
    # 'value_2': 25000000,
    # 'value_1': 250000,
    # 'value_2': 5001000,
    # 'value_1': 5643,
    # 'value_2': 10745,
    # 'value_1': 5,
    # 'value_2': 1000,
    # 'value_1': 5000,
    # 'value_2': 100,
    'value_1': 10000,
    'value_2': 55000,
    'font_size': 30
}

# create_diagram_page_8(context)

contexts_page_10 = [
    {
        'page_num': 9,
        'font_size': 25,
        'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
        'text': 'ЦЕНА ПРОСМОТРА',
        'color': (1, 1, 1),
        'coordinates': (381, 300),
    },
    {
        'page_num': 9,
        'font_size': 25,
        'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
        'text': 'КОНВЕРСИЯ В КОНТАКТ',
        'color': (1, 1, 1),
        'coordinates': (691, 300),
    },
    {
        'page_num': 9,
        'font_size': 25,
        'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
        'text': 'ЦЕНА КОНТАКТА',
        'color': (1, 1, 1),
        'coordinates': (1071, 300),
    },
    {
        'page_num': 9,
        'font_size': 25,
        'font_path': 'fonts/CodePro/Code-Pro.ttf',
        'text': 'Значение поисковой выдачи',
        'color': (1, 1, 1),
        'coordinates': (1071, 300),
    },
    {
        'page_num': 9,
        'font_size': 25,
        'font_path': 'fonts/CodePro/Code-Pro.ttf',
        'text': 'Значение рекомендаций',
        'color': (1, 1, 1),
        'coordinates': (1071, 300),
    },
]

context_insert_images_page_10 = [
    {
        'image_path': 'create_presentation/img/Line 1.png',
        'page_num': 9,
        'coordinates': (370, 320),
        'coef': 1,
    },
    {
        'image_path': 'create_presentation/img/Line 1.png',
        'page_num': 9,
        'coordinates': (680, 320),
        'repeat_insertion': {
            'repeat_count': 2,
            'interval': 380,
            'direction': 'horizontal_asc'
        },
        'coef': 1,
    },
    {
        'image_path': 'create_presentation/img/search_view_cost_1.png',
        'page_num': 9,
        'coordinates': [376, 390],
        'coef': 1,
    },
    {
        'image_path': 'create_presentation/img/recommendation_view_cost_1.png',
        'page_num': 9,
        'coordinates': [376, 560],
        'coef': 1,
    }
]


def calculate_rectangle_widths(max_width, search_value, recommendation_value):
    # Находим максимальное значение
    max_value = max(search_value, recommendation_value)

    # Вычисляем процент меньшего значения
    if max_value == search_value:
        smaller_value = recommendation_value
        smaller_key = 'recommendation'
        larger_key = 'search'
    else:
        smaller_value = search_value
        smaller_key = 'search'
        larger_key = 'recommendation'

    # Вычисляем процент от максимального значения
    if max_value == 0:  # Предотвращение ZeroDivisionError
        smaller_value_percent = 0
        smaller_rect_width = 0
        max_width = 0
    else:
        smaller_value_percent = (smaller_value / max_value) * 100
        # Вычисляем ширину прямоугольника для меньшего значения
        smaller_rect_width = (max_width * smaller_value_percent) / 100

    # Возвращаем словарь с ширинами прямоугольников
    return {
        # Ширина для большего значения
        larger_key: max_width,
        # Ширина для меньшего значения
        smaller_key: int(smaller_rect_width)
    }


def create_diagram_page_10(doc, context):
    search_view_cost = context[
        'search_view_cost']
    search_contact_conversion_rate = context[
        'search_contact_conversion_rate']
    search_contact_cost = context[
        'search_contact_cost']

    recommendation_view_cost = context[
        'recommendation_view_cost']
    recommendation_contact_conversion_rate = context[
        'recommendation_contact_conversion_rate']
    recommendation_contact_cost = context[
        'recommendation_contact_cost']

    view_cost = calculate_rectangle_widths(200, float(
        search_view_cost), float(recommendation_view_cost))
    conversion_rate = calculate_rectangle_widths(
        200, float(search_contact_conversion_rate.split(
            '.')[0]),
        float(recommendation_contact_conversion_rate.split('.')[0]))
    contact_cost = calculate_rectangle_widths(
        200, float(search_contact_cost.split(
            '.')[0]), float(recommendation_contact_cost.split('.')[0]))

    # Создаём независимые копии, чтобы изменять именно их
    copy_contexts_page_10 = xerox.deepcopy(contexts_page_10)
    copy_context_insert_images_page_10 = xerox.deepcopy(
        context_insert_images_page_10)

    for index, dictionary in enumerate(
            (view_cost, conversion_rate, contact_cost), start=1):
        img_1_width = dictionary['search']
        img_2_width = dictionary['recommendation']
        img_height = 60
        color_1 = (255, 255, 255)
        color_2 = (184, 255, 0)
        output_path_1 = f"img/search_view_cost_{index}.png"
        output_path_2 = f"img/recommendation_view_cost_{index}.png"
        # Создаём цветные прямоугольники для диаграмм
        create_color_rectanges(img_1_width, img_height, color_1, output_path_1)
        create_color_rectanges(img_2_width, img_height, color_2, output_path_2)

    for tpl in (
        ('create_presentation/img/search_view_cost_1.png',
         'create_presentation/img/recommendation_view_cost_1.png', 376),
        ('create_presentation/img/search_view_cost_2.png',
         'create_presentation/img/recommendation_view_cost_2.png', 686),
        ('create_presentation/img/search_view_cost_3.png',
         'create_presentation/img/recommendation_view_cost_3.png', 1066)
    ):
        first_img = {key: value for key,
                     value in copy_context_insert_images_page_10[2].items()}
        second_img = {key: value for key,
                      value in copy_context_insert_images_page_10[3].items()}
        first_img['image_path'] = tpl[0]
        first_img['coordinates'] = [
            tpl[2], copy_context_insert_images_page_10[2]['coordinates'][1]]
        second_img['image_path'] = tpl[1]
        second_img['coordinates'] = [
            tpl[2], copy_context_insert_images_page_10[3]['coordinates'][1]]

        copy_context_insert_images_page_10.extend([first_img, second_img])

    del copy_context_insert_images_page_10[2:4]

    # Вставляем текст со значениями справа от диаграмм
    for index, tpl in enumerate((
        (search_view_cost, recommendation_view_cost, view_cost),
        (search_contact_conversion_rate,
         recommendation_contact_conversion_rate, conversion_rate),
        (search_contact_cost, recommendation_contact_cost, contact_cost)
    )):
        first_line = {key: value for key,
                      value in copy_contexts_page_10[3].items()}
        second_line = {key: value for key,
                       value in copy_contexts_page_10[4].items()}
        first_line['text'] = str(tpl[0])
        x = (copy_context_insert_images_page_10[2 + index *
                                                2]['coordinates'][0]
             + tpl[2]['search']
             + 30)
        y = (copy_context_insert_images_page_10[2 +
                                                index * 2][
            'coordinates'][1]
            + 40)

        first_line['coordinates'] = [x, y]
        second_line['text'] = str(tpl[1])
        x = (copy_context_insert_images_page_10[2 + index * 2 +
                                                1]['coordinates'][0]
             + tpl[2]['recommendation']
             + 30)
        y = copy_context_insert_images_page_10[2 +
                                               index * 2 + 1][
                                                   'coordinates'
        ][1] + 40
        second_line['coordinates'] = [x, y]

        copy_contexts_page_10.extend([first_line, second_line])
    del copy_contexts_page_10[3:5]

    insert_images(doc, copy_context_insert_images_page_10)

    insert_texts(doc, copy_contexts_page_10)

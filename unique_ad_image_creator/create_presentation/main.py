import os
from datetime import datetime

import fitz
import gspread
import pandas as pd
import pytz
from django.conf import settings

from .add_centered_text import add_centered_text
from .create_diagram import create_diagram_page_8, create_diagram_page_10
from .insert_images import insert_images
from .insert_niche_title import add_title
from .insert_text import insert_texts


def preparing_data(data):
    required_keys = [
        "Просмотры в поисковой выдаче",
        "Просмотры в рекомендациях",
        "Цена просмотра в поисковой выдаче",
        "Цена просмотра в рекомендациях",
        "Конверсия в контакт в поисковой выдаче",
        "Конверсия в контакт в рекомендациях",
        "Цена контакта в поисковой выдаче",
        "Цена контакта в рекомендациях",
        "Оптимальный рекламный бюджет",
        "Количество контактов",
        "Средняя стоимость контакта",
        "Публикация объявлений",
        "Продвижение объявлений",
        "Бюджет на просмотры/объявления",
        "Бюджет на услуги продвижения",
        "Бюджет на тариф авито",
        "Стоимость услуг агентства",
        "Название тарифа",
        "Суммарный рекламный бюджет",
        "Ниша"
    ]

    for key in required_keys:
        try:
            data[key] = data.loc[key].values[0]
        except KeyError:
            raise KeyError(f"Ключ '{key}' отсутствует в данных.")
    return {
        'views_search': (
            data.loc[
                "Просмотры в поисковой выдаче"
            ].values[0]
        ),
        'views_recommendations': (
            data.loc[
                "Просмотры в рекомендациях"
            ].values[0]
        ),
        'cost_per_view_search': (
            str(round(float(
                data.loc[
                    'Цена просмотра '
                    'в поисковой выдаче'
                ].values[0]), 1))
        ),
        'cost_per_view_recommendations': (
            str(round(float(
                data.loc[
                    'Цена просмотра '
                    'в рекомендациях'
                ].values[0]), 1))
        ),
        'conversion_rate_search': (
            str(round(float(
                data.loc[
                    'Конверсия в контакт '
                    'в поисковой выдаче'
                ].values[0]) * 100, 1)) + '%'
        ),

        'conversion_rate_recommendations': (
            str(round(float(
                data.loc[
                    'Конверсия в контакт '
                    'в рекомендациях'
                ].values[0]) * 100, 1)) + '%'
        ),
        'cost_per_contact_search': (
            str(round(float(
                data.loc[
                    'Цена контакта '
                    'в поисковой выдаче'
                ].values[0]))
                )
        ),
        'cost_per_contact_recommendations': (
            str(round(float(
                data.loc[
                    'Цена контакта '
                    'в рекомендациях'
                ].values[0]))
                )
        ),
        'optimal_ad_budget': (
            str(round(float(
                data.loc[
                    'Оптимальный '
                    'рекламный бюджет'
                ].values[0]))
                )
        ),
        'total_contacts': (
            str(round(float(
                data.loc[
                    'Количество '
                    'контактов'
                ].values[0]))
                )
        ),
        'average_contact_cost': (
            str(round(float(
                data.loc[
                    'Средняя стоимость '
                    'контакта'
                ].values[0]))
                )
        ),
        'all_ads_count': (
            data.loc[
                "Публикация объявлений"
            ].values[0]
        ),
        'ad_promotion_range': (
            data.loc[
                "Продвижение объявлений"
            ].values[0]
        ),
        'budget_views_ads': (
            str(round(float(
                data.loc[
                    'Бюджет на '
                    'просмотры/объявления'
                ].values[0]))
                )
        ),
        'budget_promotion_services': (
            str(round(float(
                data.loc[
                    'Бюджет на '
                    'услуги продвижения'
                ].values[0].replace(' ', '')))
                )
        ),
        'avito_tariff_budget': (
            str(round(float(
                data.loc[
                    'Бюджет на '
                    'тариф авито'
                ].values[0]))
                )
        ),
        'agency_service_cost': (
            str(round(float(data.loc[
                'Стоимость услуг агентства'].values[0])))),
        'tariff_name': data.loc[
            "Название тарифа"].values[0],
        'total_ad_budget': (
            str(round(float(data.loc['Суммарный рекламный бюджет'
                                     ].values[0])))),

        'niche': data.loc["Ниша"].values[0]
    }


def read_google_sheets():
    try:
        # Авторизация с использованием учетных данных
        gc = gspread.service_account(filename="client-api.json")
        spreadsheet = gc.open("Первичный анализ ниши 9-13 Для презентации ")

        if "Для разработчика" not in [
            sheet.title for sheet in spreadsheet.worksheets()
        ]:
            raise ValueError("Лист 'Для разработчика' отсутствует в таблице.")

        # Открытие Google таблицы
        wks = spreadsheet.worksheet("Для разработчика")

        # Получение всех данных из таблицы
        data = wks.get_all_values()

        # Удаление символов \xa0 из всех значений
        cleaned_data = [[cell.replace('\xa0', ' ')
                        for cell in row] for row in data]

        df = pd.DataFrame(cleaned_data, columns=[0, 1]).set_index(0)
        df.loc[df.index.isin(
            ['Конверсия в контакт в поисковой выдаче',
             'Конверсия в контакт в рекомендациях']), 1] = df.loc[
            df.index.isin(['Конверсия в контакт в поисковой выдаче',
                           'Конверсия в контакт в рекомендациях']), 1
        ].replace({'%': '', ',': '.'}, regex=True).astype(float) / 100
        # Вызов функции preparing_data с переданным DataFrame
        return preparing_data(df)
    except Exception as e:
        # Обработка ошибки и вывод сообщения
        return str(e)


def extract_data(file_path):
    try:
        # Контекстный менеджер закроет файл после использования
        with pd.ExcelFile(file_path) as xls:
            # Извлечение данных с листа "Для разработчика" без заголовков
            if "Для разработчика" not in xls.sheet_names:
                raise ValueError(
                    "Лист 'Для разработчика' отсутствует в файле.")
            presentation_data = pd.read_excel(
                xls, sheet_name="Для разработчика", header=None, dtype=str)

            # Устанавливаем первый столбец как индекс
            presentation_data.set_index(0, inplace=True)
            return preparing_data(presentation_data)

    except Exception as e:
        # Здесь вы можете обработать ошибку и вернуть сообщение пользователю
        return str(e)


def main(all_data, first_image, second_image):
    # Присвоение значений переменным
    views_search = all_data['views_search']
    views_recommendations = all_data['views_recommendations']
    cost_per_view_search = all_data['cost_per_view_search']
    cost_per_view_recommendations = all_data['cost_per_view_recommendations']
    conversion_rate_search = all_data['conversion_rate_search']
    conversion_rate_recommendations = (
        all_data['conversion_rate_recommendations'])
    cost_per_contact_search = all_data['cost_per_contact_search']
    cost_per_contact_recommendations = (
        all_data['cost_per_contact_recommendations'])
    optimal_ad_budget = all_data['optimal_ad_budget']
    total_contacts = all_data['total_contacts']
    average_contact_cost = all_data['average_contact_cost']
    all_ads_count = all_data['all_ads_count']
    ad_promotion_range = all_data['ad_promotion_range']
    budget_views_ads = all_data['budget_views_ads']
    budget_promotion_services = all_data['budget_promotion_services']
    avito_tariff_budget = all_data['avito_tariff_budget']
    agency_service_cost = all_data['agency_service_cost']
    tariff_name = all_data['tariff_name']
    total_ad_budget = all_data['total_ad_budget']
    niche = all_data['niche']

    doc = fitz.open(os.path.join(settings.BASE_DIR,
                    "create_presentation/без данных.pdf"))

    contexts = [
        {
            'file': doc,
            'page_num': 9,
            'font_size': 33,
            'font_path': 'fonts/CodePro/Code-Pro-Bold.ttf',
            'text': '',
            'color': (184 / 255, 1, 0),
            'coordinates': (390, 360),
        },
        {
            'file': doc,
            'page_num': 13,
            'font_size': 30,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': ad_promotion_range,
            'color': (184 / 255, 1, 0),
            'coordinates': (413, 560),
        },
        {
            'file': doc,
            'page_num': 13,
            'font_size': 30,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': all_ads_count,
            'color': (184 / 255, 1, 0),
            'coordinates': (710, 95),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{optimal_ad_budget}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (445, 297),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{budget_views_ads}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (120, 360),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{budget_promotion_services}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (120, 417),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{avito_tariff_budget}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (120, 480),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': total_contacts,
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (755, 365),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{average_contact_cost}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (755, 423),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{agency_service_cost}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (805, 652),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': tariff_name,
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (1060, 652),
        },
        {
            'file': doc,
            'page_num': 14,
            'font_size': 30,
            'font_path': 'fonts/Jost-Regular.ttf',
            'text': f"{total_ad_budget}₽",
            'color': (0.94901, 0.41569, 0.35686),
            'coordinates': (1170, 695),
        },
    ]

    insert_texts(doc, contexts)

    contexts = [
        {
            'file': doc,
            'page_num': 11,
            'font_size': 50,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': optimal_ad_budget,
            'color': (184 / 255, 1, 0),
            'coordinates': (750, 380),
            'y_coordinate': 350,
            'x_center': 820,
            'text_width': 300,
        },
        {
            'file': doc,
            'page_num': 11,
            'font_size': 50,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': total_contacts,
            'color': (184 / 255, 1, 0),
            'coordinates': (1180, 280),
            'y_coordinate': 250,
            'x_center': 1230,
            'text_width': 300,
        },
        {
            'file': doc,
            'page_num': 11,
            'font_size': 50,
            'font_path': 'fonts/CodePro/Code-Pro.ttf',
            'text': average_contact_cost,
            'color': (184 / 255, 1, 0),
            'coordinates': (1140, 680),
            'y_coordinate': 640,
            'x_center': 1180,
            'text_width': 300,
        },
    ]

    add_centered_text(doc, contexts)

    contexts = [
        {
            'image_path': f"media/{first_image}",
            'file': doc,
            'page_num': 8,
            'coordinates': (157, 283),
            'coef': 0.623,
        },
        {
            'image_path': f"media/{second_image}",
            'file': doc,
            'page_num': 10,
            'coordinates': (80, 287),
            'coef': 0.635,
        },
    ]

    insert_images(doc, contexts)

    context = {
        # 'file_name': 'output.pdf',
        'file': doc,
        'page_num': 6,
        'font_size': 92,
        'font_path': 'fonts/CodePro/Code-Pro.ttf',
        'text': niche,
        'color': (1, 1, 1),
        'y_coordinate': 430,
        'margin': 40
    }

    add_title(doc, context)

    context = {
        'value_1': int(views_search),
        'value_2': int(views_recommendations),
        'font_size': 30
    }

    create_diagram_page_8(doc, context)

    context_page_10 = {
        'search_view_cost': cost_per_view_search,
        'search_contact_conversion_rate': conversion_rate_search,
        'search_contact_cost': cost_per_contact_search,
        'recommendation_view_cost': cost_per_view_recommendations,
        'recommendation_contact_conversion_rate': (
            conversion_rate_recommendations
        ),
        'recommendation_contact_cost': cost_per_contact_recommendations
    }

    create_diagram_page_10(doc, context_page_10)

    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)

    filename = f"Презентация_{niche}_{moscow_time.strftime('%d%m%Y_%H%M')}.pdf"

    # Сохраняем изменения один раз в конце
    doc.save(os.path.join(settings.BASE_DIR,
             f"create_presentation/{filename}"
                          ), incremental=False, encryption=0)
    # Закрываем документ
    doc.close()
    return os.path.join(
        settings.BASE_DIR,
        f"create_presentation/{filename}"
    ), filename

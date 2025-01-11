import os
import sys

import django
from django.conf import settings

# Добавьте корневую директорию вашего проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'PresentationGenerator.settings'
    )

django.setup()


# Код ниже позволяет автоматизировать открытие файла pdf
pdf_file = os.path.join(
    settings.BASE_DIR, "create_presentation/без данных.pdf"
    )
page_number = 8
acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
# Команда для открытия PDF в Adobe Acrobat на нужной странице
os.system(f'start "" "{acrobat_path}" /A "page={page_number}" "{pdf_file}"')

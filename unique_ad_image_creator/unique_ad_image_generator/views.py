from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import AdvertForm
from .models import Advert


import zipfile
import os
import tempfile
import boto3
from botocore.config import Config
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View
from .models import Advert
from .forms import AdvertForm
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
YANDEX_ACCESS_KEY = os.getenv('YANDEX_CLOUD_ACCESS_KEY_ID')
YANDEX_SECRET_KEY = os.getenv('YANDEX_CLOUD_SECRET_ACCESS_KEY')
# YANDEX_BUCKET_NAME = 'adverts-bucket'
YANDEX_ENDPOINT_URL = 'https://storage.yandexcloud.net'

# Настройка клиента S3 для Яндекс Object Storage
s3_client = boto3.client(
    service_name='s3',
    endpoint_url=YANDEX_ENDPOINT_URL,
    aws_access_key_id=YANDEX_ACCESS_KEY,
    aws_secret_access_key=YANDEX_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

class ServicesView(View):
    template_name = "auth.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



class AdvertCreateView(CreateView):
    model = Advert
    form_class = AdvertForm
    template_name = 'unique_ad_image_generator/advert_form.html'
    success_url = reverse_lazy('image_generator:advert_list')

    def form_valid(self, form):
        # Получаем имя бакета, в который будем сохранять изображения
        backet_name = form.cleaned_data['backet_name']
        # Получаем объект архива из формы
        archive = self.request.FILES.get('images')
        if not archive:
            return super().form_invalid(form)

        # Создаём временную директорию для распаковки
        with tempfile.TemporaryDirectory() as tmpdir:

            # Распаковка архива
            if zipfile.is_zipfile(archive):
                with zipfile.ZipFile(archive, 'r') as zip_ref:
                    zip_ref.extractall(tmpdir)

                # Загрузка файлов на Яндекс Object Storage
                uploaded_files = []
                for root, _, files in os.walk(tmpdir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, tmpdir)  # Путь внутри архива
                        s3_key = relative_path.replace("\\", "/")  # Универсальный путь для S3

                        # Загружаем файл в бакет
                        s3_client.upload_file(file_path, backet_name, s3_key)
                        file_url = f"{YANDEX_ENDPOINT_URL}/{backet_name}/{s3_key}"
                        uploaded_files.append(file_url)

                # Сохраняем пути загруженных файлов в модель
                advert = form.save(commit=False)
                advert.images = "\n".join(uploaded_files)
                advert.save()
            else:
                form.add_error('images', 'Загруженный файл не является архивом в формате ZIP')
                return super().form_invalid(form)

        return super().form_valid(form)


class AdvertListView(ListView):
    model = Advert
    template_name = 'unique_ad_image_generator/advert_list.html'
    context_object_name = 'adverts'
    paginate_by = 10


class AdvertDetailView(DetailView):
    model = Advert
    template_name = 'unique_ad_image_generator/advert_detail.html'
    context_object_name = 'advert'

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views import View

@method_decorator(login_required, name='dispatch')
class CabinetView(View):
    template_name = 'unique_ad_image_generator/cabinet.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

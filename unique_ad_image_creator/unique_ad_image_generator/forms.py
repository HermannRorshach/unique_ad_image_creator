from django import forms
from .models import Advert

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['title', 'backet_name', 'category_id', 'description', 'images']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите описание объявления'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.zip'})
        }
        labels = {
            'title': 'Заголовок объявления',
            'backet_name': 'Имя бакета',
            'category_id': 'Категория',
            'description': 'Описание',
            'images': 'Ссылки на изображения',
        }
        help_texts = {
            'title': 'Введите заголовок вашего объявления.',
            'category_id': 'Введите ID категории.',
            'description': 'Опишите ваше объявление.',
            'images': 'Введите прямые ссылки на изображения, разделенные запятыми.',
        }
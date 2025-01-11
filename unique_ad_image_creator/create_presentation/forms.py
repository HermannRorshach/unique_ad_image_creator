from django import forms

from .models import IranPassport


class IranPassportForm(forms.ModelForm):
    class Meta:
        model = IranPassport
        fields = '__all__'
        widgets = {
            'lond_number': forms.Textarea(attrs={'cols': 60, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     instance = self.instance  # текущий экземпляр модели

    #     # Получаем название файла из метода __str__
    #     file_name = str(instance)

    #     # Добавляем название файла в cleaned_data
    #     cleaned_data['file_name'] = file_name

    #     return cleaned_data

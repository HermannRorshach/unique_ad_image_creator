import os

from django.core.exceptions import ValidationError
from django.db import models


def validate_zip_file(file):
    if not file.name.endswith('.zip'):
        raise ValidationError("Файл должен быть в формате ZIP.")

class Advert(models.Model):
    title = models.CharField(max_length=128, default='', null=False)
    backet_name = models.CharField(max_length=256, default='adverts-bucket', null=False)
    category_id = models.IntegerField(default=0, null=False)
    description = models.TextField(null=True)
    images = models.FileField(upload_to='adverts/zips/', validators=[validate_zip_file], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status_id = models.SmallIntegerField(default=1, null=False)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title



class SimilarAdvert(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name='similar_adverts')
    title = models.CharField(max_length=128, default='')
    category_id = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_id = models.SmallIntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

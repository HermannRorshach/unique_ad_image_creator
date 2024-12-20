from django.urls import path

from . import views

app_name = 'image_generator'

urlpatterns = [
    path('', views.AdvertCreateView.as_view(), name='advert_create'),
    path('advert_list/', views.AdvertListView.as_view(), name='advert_list'),
    path('adverts/<int:pk>/', views.AdvertDetailView.as_view(), name='advert_detail'),
]

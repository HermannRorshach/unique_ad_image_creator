from django.urls import path

from . import views

app_name = 'image_generator'

urlpatterns = [
    path('', views.ServicesView.as_view(), name='services'),
    path('huy', views.AdvertCreateView.as_view(), name='advert_create'),
    path('advert_list/', views.AdvertListView.as_view(), name='advert_list'),
    path('adverts/<int:pk>/', views.AdvertDetailView.as_view(), name='advert_detail'),
    path('cabinet', views.CabinetView.as_view(), name='cabinet'),

]

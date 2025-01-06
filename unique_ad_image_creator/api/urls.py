from django.urls import path
from . import views

urlpatterns = [
    path('authenticate/', views.AuthenticateUserView.as_view(), name='authenticate_user'),
]

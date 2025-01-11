from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import LunchParticipantViewSet, FeedbackViewSet, TaskViewSet, UserViewSet

router = DefaultRouter()
router.register(
    r'lunch/participants',
    LunchParticipantViewSet, basename='lunch_parcicipant')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')


app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]

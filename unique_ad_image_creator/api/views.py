from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.patterns import patterns


@method_decorator(csrf_exempt, name='dispatch')
class AuthenticateUserView(View):
    def post(self, request, *args, **kwargs):
        # Получаем данные из тела запроса
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        print(username, password)

        # Проверяем логин и пароль
        user = authenticate(username=username, password=password)
        if user is not None:
            # Если аутентификация успешна, возвращаем словарь
            return JsonResponse({"success": True, "patterns": patterns}, status=200)
        else:
            # Если логин или пароль неверны
            return JsonResponse({"success": False, "error": "Invalid credentials"}, status=401)

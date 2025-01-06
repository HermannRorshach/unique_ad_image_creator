import requests
import json


def main(bucket_name, patterns):
    print(patterns)

if __name__ == "__main__":
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    bucket_name = input("Введите имя бакета: ")
    # URL вашего эндпоинта для аутентификации
    url = "http://127.0.0.1:8000/authenticate/"  # Замените на правильный URL

    # Данные для запроса
    data = {
        "username": login,
        "password": password
    }

    # Отправка POST-запроса
    response = requests.post(url, data=data)

    if response.status_code == 200:
        # Если аутентификация успешна, получаем patterns из ответа
        response_data = response.json()
        patterns = response_data.get("patterns")

        if patterns:
            main(bucket_name, patterns)
        else:
            print("Ошибка: Не получены данные patterns")
    else:
        print(f"Ошибка аутентификации: {response.json().get('error')}")

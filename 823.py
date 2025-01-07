import gspread

# Авторизация с использованием учетных данных
gc = gspread.service_account(filename="client-api.json")

# Открытие Google таблицы
spreadsheet = gc.open("Первичный анализ ниши 9-13 Для презентации ")

# Получение листа по названию "Для разработчика"
wks = spreadsheet.worksheet("Для разработчика")

# Получение всех данных из таблицы
data = wks.get_all_values()

# Вывод данных в консоль
for row in data:
    print(row)


# Авторизация с использованием учетных данных
gc = gspread.service_account(filename="client-api.json")

# Открытие Google таблицы
wks = gc.open(
    "Первичный анализ ниши 9-13 Для презентации ").worksheet("Для разработчика")

# Получение всех данных из таблицы
data = wks.get_all_values()

# Удаление символов \xa0 из всех значений
cleaned_data = [[cell.replace('\xa0', ' ') for cell in row] for row in data]

# Вывод очищенных данных в консоль
for row in cleaned_data:
    print(row)

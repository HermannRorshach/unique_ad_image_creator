import fitz  # PyMuPDF

# Открываем PDF файл
pdf_path = "с данными.pdf"
doc = fitz.open(pdf_path)

# Указываем слово для поиска
search_word = "73840₽"

# Выбираем страницу для поиска (например, 8-я страница, индекс 7)
page = doc.load_page(14)

# Находим все вхождения слова на странице
text_instances = page.search_for(search_word)

# Выводим координаты каждого найденного вхождения
for instance in text_instances:
    x = round((instance[2] - instance[0]) / 2 + instance[0])
    y = round((instance[3] - instance[1]) / 2 + instance[1])
    print(
        f"Найдено слово '{search_word}' с приблизительными координатами:"
        f" {x}, {y}"
        )

# Закрываем документ
doc.close()

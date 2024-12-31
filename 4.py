from pprint import pprint

class ImageModifier(float):
    def __init__(self, value, name=None):
        self.value = value
        self.name = name

    def __repr__(self):
        # Если имя переменной передано, то выводим его в строковом представлении
        if self.name:
            return self.name
        return f"ImageModifier({self.value!r})"

    def __str__(self):
        # Для других случаев возвращаем значение как строку
        return str(self.value)



# Значения для увеличения контрастности
contrast_increase_high = 1.6 # Обычное использование переменной
contrast_increase_low = ImageModifier(1.2, name="contrast_increase_low") # Использование ООП

patterns = {
    1: {
        'adjust_contrast': (contrast_increase_high,),
    },
    2: {
        'adjust_contrast': (contrast_increase_high,),
    },
    3: {
        'adjust_contrast': (contrast_increase_low,),
    },
    4: {
        'adjust_contrast': (contrast_increase_low,),
    },
    5: {
        'adjust_contrast': (contrast_increase_low,),
    }
}

pprint(patterns, sort_dicts=False, compact=False)

print(contrast_increase_low)
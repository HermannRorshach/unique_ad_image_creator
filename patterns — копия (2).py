import itertools

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



# Значения для контрастности
contrast_normal = ImageModifier(1, name="contrast_normal")

# Значения для увеличения контрастности
contrast_increase_low = ImageModifier(1.2, name="contrast_increase_low")
contrast_increase_moderate = ImageModifier(1.4, name="contrast_increase_moderate")
contrast_increase_high = ImageModifier(1.6, name="contrast_increase_high")

# Значения для уменьшения контрастности
contrast_decrease_low = ImageModifier(0.9, name="contrast_decrease_low")
contrast_decrease_moderate = ImageModifier(0.8, name="contrast_decrease_moderate")
contrast_decrease_high = ImageModifier(0.7, name="contrast_decrease_high")

# Значения для яркости
brightness_normal = ImageModifier(1, name="brightness_normal")

# Значения для увеличения яркости
brightness_increase_low = ImageModifier(1.1, name="brightness_increase_low")
brightness_increase_moderate = ImageModifier(1.2, name="brightness_increase_moderate")
brightness_increase_high = ImageModifier(1.3, name="brightness_increase_high")

# Значения для уменьшения яркости
brightness_decrease_low = ImageModifier(0.93, name="brightness_decrease_low")
brightness_decrease_moderate = ImageModifier(0.87, name="brightness_decrease_moderate")
brightness_decrease_high = ImageModifier(0.8, name="brightness_decrease_high")

# Значения для обрезки
crop_normal = ImageModifier(0, name="crop_normal")
crop_increase_low = ImageModifier(2, name="crop_increase_low")
crop_increase_moderate = ImageModifier(4, name="crop_increase_moderate")
crop_increase_high = ImageModifier(6, name="crop_increase_high")


class AdjustContrast:
    def __init__(self):

        self.normal = 1

        # Значения для увеличения контрастности
        self.increase_low = 1.2
        self.increase_moderate = 1.4
        self.increase_high = 1.6

        # Значения для уменьшения контрастности
        self.decrease_low = 0.9
        self.decrease_moderate = 0.8
        self.decrease_high = 0.7

class AdjustBrightness:
    def __init__(self):

        self.normal = 1

        # Значения для увеличения яркости
        self.increase_low = 1.1
        self.increase_moderate = 1.2
        self.increase_high = 1.3

        # Значения для уменьшения яркости
        self.decrease_low = 0.93
        self.decrease_moderate = 0.87
        self.decrease_high = 0.8

class CropImage:
    def __init__(self):
        # Значения для обрезки
        self.normal = 0
        self.increase_low = 2
        self.increase_moderate = 4
        self.increase_high = 6

    def generate_combinations(self):
        # Возможные значения
        values = ['crop_image.normal', 'crop_image.increase_low', 'crop_image.increase_moderate', 'crop_image.increase_high']

        # Генерация всех возможных комбинаций длины 4
        all_combinations = itertools.product(values, repeat=4)

        # Отбор комбинаций, в которых не больше 2 значений `self.normal` (0)
        valid_combinations = [', '.join(combo) for combo in all_combinations if combo.count('crop_image.normal') <= 2]

        return valid_combinations

# Создаём экземпляр класса
crop_image = CropImage()

# Генерируем комбинации
combinations = crop_image.generate_combinations()
print(len(combinations))

# Печатаем первые три комбинации
for num, combo in enumerate(combinations[:1], 1):
    print(num, combo)


# Создаем экземпляры классов
contrast = AdjustContrast()
brightness = AdjustBrightness()
crop = CropImage()

# Списки значений контрастности и яркости
contrast_values = [
    'contrast.increase_low',
    'contrast.increase_moderate',
    'contrast.increase_high',
    'contrast.normal',
    'contrast.decrease_low',
    'contrast.decrease_moderate',
    'contrast.decrease_high'
]

brightness_values = [
    'brightness.increase_low',
    'brightness.increase_moderate',
    'brightness.increase_high',
    'brightness.normal',
    'brightness.decrease_low',
    'brightness.decrease_moderate',
    'brightness.decrease_high'
]

# Генерация уникальных комбинаций
combinations = []
for c in contrast_values:
    for b in brightness_values:
        combinations.append(f"'adjust_contrast': ({c},),\n        'adjust_brightness': ({b},),")

# Ограничиваем до 28 уникальных комбинаций
unique_combinations = combinations

# Вывод комбинаций
# for i, combo in enumerate(combinations, 1):
#     print(f"Комбинация {i}:\n{combo}")
#     print()

# Обновляем словарь patterns
patterns = {
    '1': {
        'adjust_white_balance': (1.1, 1.0, 0.9),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_increase_low,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_low, crop_increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '2': {
        'adjust_white_balance': (0.9, 1.0, 1.1),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_increase_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_low, crop_increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '3': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_increase_high,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_low, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '4': {
        'adjust_white_balance': (1.0, 0.9, 1.1),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_normal,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_moderate, crop_increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '5': {
        'adjust_white_balance': (1.1, 0.9, 1.0),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_decrease_low,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_moderate, crop_increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '6': {
        'adjust_white_balance': (0.9, 1.1, 1.0),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_decrease_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '7': {
        'adjust_white_balance': (1.05, 1.0, 0.95),
        'adjust_contrast': (contrast_increase_low,),
        'adjust_brightness': (brightness_decrease_high,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_high, crop_increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '8': {
        'adjust_white_balance': (0.95, 1.0, 1.05),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_increase_low,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_high, crop_increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '9': {
        'adjust_white_balance': (1.0, 1.05, 0.95),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_increase_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_normal, crop_increase_high, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '10': {
        'adjust_white_balance': (1.0, 0.95, 1.05),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_increase_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_normal, crop_increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '11': {
        'adjust_white_balance': (1.1, 1.1, 0.9),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_normal,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_normal, crop_increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '12': {
        'adjust_white_balance': (0.9, 1.1, 1.1),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_decrease_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_normal, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '13': {
        'adjust_white_balance': (1.05, 0.95, 1.0),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_decrease_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_low, crop_normal),
        'resize_image': (),
        'rotate_image': ()
    },
    '14': {
        'adjust_white_balance': (0.95, 1.05, 1.0),
        'adjust_contrast': (contrast_increase_moderate,),
        'adjust_brightness': (brightness_decrease_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_low, crop_increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '15': {
        'adjust_white_balance': (1.1, 1.0, 0.9),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_increase_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_low, crop_increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '16': {
        'adjust_white_balance': (0.9, 1.0, 1.1),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_increase_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_low, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '17': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_increase_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_normal),
        'resize_image': (),
        'rotate_image': ()
    },
    '18': {
        'adjust_white_balance': (1.0, 0.9, 1.1),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_normal,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '19': {
        'adjust_white_balance': (1.1, 0.9, 1.0),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_decrease_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '20': {
        'adjust_white_balance': (0.9, 1.1, 1.0),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_decrease_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '21': {
        'adjust_white_balance': (1.05, 1.0, 0.95),
        'adjust_contrast': (contrast_increase_high,),
        'adjust_brightness': (brightness_decrease_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '22': {
        'adjust_white_balance': (0.95, 1.0, 1.05),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_increase_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '23': {
        'adjust_white_balance': (1.0, 1.05, 0.95),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_increase_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '24': {
        'adjust_white_balance': (1.0, 0.95, 1.05),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_increase_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '25': {
        'adjust_white_balance': (1.1, 1.1, 0.9),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_normal,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '26': {
        'adjust_white_balance': (0.9, 1.1, 1.1),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_decrease_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '27': {
        'adjust_white_balance': (1.05, 0.95, 1.0),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_decrease_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '28': {
        'adjust_white_balance': (0.95, 1.05, 1.0),
        'adjust_contrast': (contrast_normal,),
        'adjust_brightness': (brightness_decrease_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '29': {
        'adjust_white_balance': (1.1, 1.0, 0.9),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_increase_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '30': {
        'adjust_white_balance': (0.9, 1.0, 1.1),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_increase_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '31': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_increase_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '32': {
        'adjust_white_balance': (1.0, 0.9, 1.1),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_normal,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '33': {
        'adjust_white_balance': (1.1, 0.9, 1.0),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_decrease_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '34': {
        'adjust_white_balance': (0.9, 1.1, 1.0),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_decrease_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '35': {
        'adjust_white_balance': (1.05, 1.0, 0.95),
        'adjust_contrast': (contrast_decrease_low,),
        'adjust_brightness': (brightness_decrease_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '36': {
        'adjust_white_balance': (0.95, 1.0, 1.05),
        'adjust_contrast': (contrast_decrease_moderate,),
        'adjust_brightness': (brightness_increase_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '37': {
        'adjust_white_balance': (1.0, 1.05, 0.95),
        'adjust_contrast': (contrast_decrease_moderate,),
        'adjust_brightness': (brightness_increase_moderate,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '38': {
        'adjust_white_balance': (1.0, 0.95, 1.05),
        'adjust_contrast': (contrast_decrease_moderate,),
        'adjust_brightness': (brightness_increase_high,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '39': {
        'adjust_white_balance': (1.1, 1.1, 0.9),
        'adjust_contrast': (contrast_decrease_moderate,),
        'adjust_brightness': (brightness_normal,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '40': {
        'adjust_white_balance': (0.9, 1.1, 1.1),
        'adjust_contrast': (contrast_decrease_moderate,),
        'adjust_brightness': (brightness_decrease_low,),
        'crop_image_by_percentage': (crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high),
        'resize_image': (),
        'rotate_image': ()
    }
}

white_balance_factors = (
    (1.1, 1.0, 0.9),  # Лёгкий сдвиг в сторону тёплых тонов
    (0.9, 1.0, 1.1),  # Лёгкий сдвиг в сторону холодных тонов
    (1.0, 1.1, 0.9),  # Усиление зелёного с уменьшением синего
    (1.0, 0.9, 1.1),  # Ослабление зелёного, усиление синего
    (1.1, 0.9, 1.0),  # Лёгкий сдвиг в сторону красного
    (0.9, 1.1, 1.0),  # Усиление зелёного, ослабление красного
    (1.05, 1.0, 0.95),  # Едва заметное усиление красного
    (0.95, 1.0, 1.05),  # Едва заметное усиление синего
    (1.0, 1.05, 0.95),  # Лёгкое усиление зелёного
    (1.0, 0.95, 1.05),  # Лёгкое ослабление зелёного
    (1.1, 1.1, 0.9),  # Усиление красного и зелёного, ослабление синего
    (0.9, 1.1, 1.1),  # Усиление зелёного и синего, ослабление красного
    (1.05, 0.95, 1.0),  # Едва заметный сдвиг
    (0.95, 1.05, 1.0),  # Едва заметный сдвиг в обратную сторону
)

num_factors = len(white_balance_factors)

def move_param_value(patterns, key, param_name):
    keys = list(patterns.keys())
    key_index = keys.index(key)

    # Перебираем все шаблоны после текущего
    for i in range(key_index + 1, len(keys)):
        current_key = keys[i]
        prev_key = keys[i - 1]

        # Переносим значение из текущего шаблона в предыдущий
        patterns[prev_key][param_name] = patterns[current_key][param_name]

    # Устанавливаем параметр в последнем шаблоне в None
    patterns[keys[-1]][param_name] = None
    print(patterns[keys[-1]][param_name])
    return patterns

pprint(move_param_value(patterns, "3", 'adjust_contrast'), sort_dicts=False, compact=False)
# print(move_param_value(patterns, "3", 'adjust_contrast'))

# Итерация через паттерны и замена значений 'adjust_white_balance'
# for i, (key, pattern) in enumerate(patterns.items()):
#     # Вычисляем индекс для white_balance_factors
#     factor_index = i % num_factors
#     pattern['adjust_white_balance'] = white_balance_factors[factor_index]

# Проверка результата
# for key, pattern in patterns.items():
#     print(f"{key}: {pattern}")

# if __name__ == "__main__":
#     for num, pattern in patterns.items():
#         print(num)
#         for key, value in pattern.items():
#             print('    ', key, value)
#         print()

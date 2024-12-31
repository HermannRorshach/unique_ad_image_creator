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
        values = [crop_normal, crop_increase_low, crop_increase_moderate, crop_increase_high]

        # Генерация всех возможных комбинаций длины 4
        all_combinations = itertools.product(values, repeat=4)

        # Отбор комбинаций, в которых не больше 2 значений `self.normal` (0)
        valid_combinations = [combo for combo in all_combinations if combo.count(crop_normal) <= 2]
        combinations = {num:value for num, value in enumerate(valid_combinations[:144], 1)}

        return combinations

    def check_combinations(self):
       # Возможные значения
       values = ['crop_normal', 'crop_increase_low', 'crop_increase_moderate', 'crop_increase_high']

       # Генерация всех возможных комбинаций длины 4
       all_combinations = itertools.product(values, repeat=4)

       # Отбор комбинаций, в которых не больше 2 значений `self.normal` (0)
       valid_combinations = [combo for combo in all_combinations if combo.count(crop_normal) <= 2]
       combinations = {num:value for num, value in enumerate(valid_combinations[:47], 1)}
       return combinations

# Создаём экземпляр класса
crop_image = CropImage()

# Генерируем комбинации
combinations = crop_image.generate_combinations()
# pprint(combinations)
# for key, value in combinations.items():
#     print(key, value)
# print(combinations)


# Печатаем первые три комбинации
# for num, combo in enumerate(combinations[:100], 1):
    # print(num, combo)


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
# combinations = []
# for c in contrast_values:
#     for b in brightness_values:
#         combinations.append(f"'adjust_contrast': ({c},),\n        'adjust_brightness': ({b},),")

# Ограничиваем до 28 уникальных комбинаций
unique_combinations = combinations

# Вывод комбинаций
# for i, combo in enumerate(combinations, 1):
#     print(f"Комбинация {i}:\n{combo}")
#     print()

# Обновляем словарь patterns
patterns = {'first_phase': {
                 1: {'adjust_contrast': (contrast_increase_low,),
                     'adjust_brightness': (brightness_increase_low,)},
                 2: {'adjust_contrast': (contrast_increase_low,),
                     'adjust_brightness': (brightness_increase_moderate,)},
                 3: {'adjust_contrast': (contrast_increase_low,),
                     'adjust_brightness': (brightness_normal,)},
                 4: {'adjust_contrast': (contrast_increase_low,),
                     'adjust_brightness': (brightness_decrease_low,)},
                 5: {'adjust_contrast': (contrast_increase_low,),
                     'adjust_brightness': (brightness_decrease_moderate,)},
                 6: {'adjust_contrast': (contrast_increase_low,),
                     'adjust_brightness': (brightness_decrease_high,)},
                 7: {'adjust_contrast': (contrast_increase_moderate,),
                     'adjust_brightness': (brightness_increase_low,)},
                 8: {'adjust_contrast': (contrast_increase_moderate,),
                     'adjust_brightness': (brightness_increase_moderate,)},
                 9: {'adjust_contrast': (contrast_increase_moderate,),
                     'adjust_brightness': (brightness_normal,)},
                 10: {'adjust_contrast': (contrast_increase_moderate,),
                      'adjust_brightness': (brightness_decrease_low,)},
                 11: {'adjust_contrast': (contrast_increase_moderate,),
                      'adjust_brightness': (brightness_decrease_moderate,)},
                 12: {'adjust_contrast': (contrast_increase_moderate,),
                      'adjust_brightness': (brightness_decrease_high,)},
                 13: {'adjust_contrast': (contrast_increase_high,),
                      'adjust_brightness': (brightness_increase_low,)},
                 14: {'adjust_contrast': (contrast_increase_high,),
                      'adjust_brightness': (brightness_normal,)},
                 15: {'adjust_contrast': (contrast_increase_high,),
                      'adjust_brightness': (brightness_decrease_low,)},
                 16: {'adjust_contrast': (contrast_increase_high,),
                      'adjust_brightness': (brightness_decrease_moderate,)},
                 17: {'adjust_contrast': (contrast_increase_high,),
                      'adjust_brightness': (brightness_decrease_high,)},
                 18: {'adjust_contrast': (contrast_normal,),
                      'adjust_brightness': (brightness_increase_low,)},
                 19: {'adjust_contrast': (contrast_normal,),
                      'adjust_brightness': (brightness_increase_moderate,)},
                 20: {'adjust_contrast': (contrast_normal,),
                      'adjust_brightness': (brightness_normal,)},
                 21: {'adjust_contrast': (contrast_normal,),
                      'adjust_brightness': (brightness_decrease_low,)},
                 22: {'adjust_contrast': (contrast_normal,),
                      'adjust_brightness': (brightness_decrease_moderate,)},
                 23: {'adjust_contrast': (contrast_normal,),
                      'adjust_brightness': (brightness_decrease_high,)},
                 24: {'adjust_contrast': (contrast_decrease_low,),
                      'adjust_brightness': (brightness_increase_low,)},
                 25: {'adjust_contrast': (contrast_decrease_low,),
                      'adjust_brightness': (brightness_increase_moderate,)},
                 26: {'adjust_contrast': (contrast_decrease_low,),
                      'adjust_brightness': (brightness_normal,)},
                 27: {'adjust_contrast': (contrast_decrease_low,),
                      'adjust_brightness': (brightness_decrease_low,)},
                 28: {'adjust_contrast': (contrast_decrease_low,),
                      'adjust_brightness': (brightness_decrease_moderate,)},
                 29: {'adjust_contrast': (contrast_decrease_low,),
                      'adjust_brightness': (brightness_decrease_high,)},
                 30: {'adjust_contrast': (contrast_decrease_moderate,),
                      'adjust_brightness': (brightness_increase_low,)},
                 31: {'adjust_contrast': (contrast_decrease_moderate,),
                      'adjust_brightness': (brightness_increase_moderate,)},
                 32: {'adjust_contrast': (contrast_decrease_moderate,),
                      'adjust_brightness': (brightness_normal,)},
                 33: {'adjust_contrast': (contrast_decrease_moderate,),
                      'adjust_brightness': (brightness_decrease_low,)},
                 34: {'adjust_white_balance': (1.1, 1.0, 0.9)},
                 35: {'adjust_white_balance': (0.9, 1.0, 1.1)},
                 36: {'adjust_white_balance': (1.0, 1.1, 0.9)},
                 37: {'adjust_white_balance': (1.0, 0.9, 1.1)},
                 38: {'adjust_white_balance': (1.1, 0.9, 1.0)},
                 39: {'adjust_white_balance': (0.9, 1.1, 1.0)},
                 40: {'adjust_white_balance': (1.05, 1.0, 0.95)},
                 41: {'adjust_white_balance': (0.95, 1.0, 1.05)},
                 42: {'adjust_white_balance': (1.0, 1.05, 0.95)},
                 43: {'adjust_white_balance': (1.0, 0.95, 1.05)},
                 44: {'adjust_white_balance': (1.1, 1.1, 0.9)},
                 45: {'adjust_white_balance': (0.9, 1.1, 1.1)},
                 46: {'adjust_white_balance': (1.05, 0.95, 1.0)},
                 47: {'adjust_white_balance': (0.95, 1.05, 1.0)}},
 'second_phase': {48: {'rotate_image': ('right', 1)},
                  49: {'rotate_image': ('left', 1)}},
 'third_phase': {50: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_low)},
                 51: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_moderate)},
                 52: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_high)},
                 53: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_low)},
                 54: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate)},
                 55: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_high)},
                 56: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_low)},
                 57: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_moderate)},
                 58: {'crop_image_by_percentage': (crop_normal,
                                                   crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_high)},
                 59: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_normal,
                                                   crop_increase_low)},
                 60: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_normal,
                                                   crop_increase_moderate)},
                 61: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_normal,
                                                   crop_increase_high)},
                 62: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_low,
                                                   crop_normal)},
                 63: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_low,
                                                   crop_increase_low)},
                 64: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_low,
                                                   crop_increase_moderate)},
                 65: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_low,
                                                   crop_increase_high)},
                 66: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_moderate,
                                                   crop_normal)},
                 67: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_moderate,
                                                   crop_increase_low)},
                 68: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate)},
                 69: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_moderate,
                                                   crop_increase_high)},
                 70: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_high,
                                                   crop_normal)},
                 71: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_high,
                                                   crop_increase_low)},
                 72: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_high,
                                                   crop_increase_moderate)},
                 73: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_low,
                                                   crop_increase_high,
                                                   crop_increase_high)},
                 74: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_normal,
                                                   crop_increase_low)},
                 75: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_normal,
                                                   crop_increase_moderate)},
                 76: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_normal,
                                                   crop_increase_high)},
                 77: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_low,
                                                   crop_normal)},
                 78: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_low,
                                                   crop_increase_low)},
                 79: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_low,
                                                   crop_increase_moderate)},
                 80: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_low,
                                                   crop_increase_high)},
                 81: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate,
                                                   crop_normal)},
                 82: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate,
                                                   crop_increase_low)},
                 83: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate)},
                 84: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate,
                                                   crop_increase_high)},
                 85: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_high,
                                                   crop_normal)},
                 86: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_high,
                                                   crop_increase_low)},
                 87: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_high,
                                                   crop_increase_moderate)},
                 88: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_moderate,
                                                   crop_increase_high,
                                                   crop_increase_high)},
                 89: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_normal,
                                                   crop_increase_low)},
                 90: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_normal,
                                                   crop_increase_moderate)},
                 91: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_normal,
                                                   crop_increase_high)},
                 92: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_low,
                                                   crop_normal)},
                 93: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_low,
                                                   crop_increase_low)},
                 94: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_low,
                                                   crop_increase_moderate)},
                 95: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_low,
                                                   crop_increase_high)},
                 96: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_moderate,
                                                   crop_normal)},
                 97: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_moderate,
                                                   crop_increase_low)},
                 98: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_moderate,
                                                   crop_increase_moderate)},
                 99: {'crop_image_by_percentage': (crop_normal,
                                                   crop_increase_high,
                                                   crop_increase_moderate,
                                                   crop_increase_high)},
                 100: {'crop_image_by_percentage': (crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_normal)},
                 101: {'crop_image_by_percentage': (crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_increase_low)},
                 102: {'crop_image_by_percentage': (crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_increase_moderate)},
                 103: {'crop_image_by_percentage': (crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_increase_high)},
                 104: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_normal,
                                                    crop_increase_low)},
                 105: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_normal,
                                                    crop_increase_moderate)},
                 106: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_normal,
                                                    crop_increase_high)},
                 107: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_normal)},
                 108: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_increase_low)},
                 109: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_increase_moderate)},
                 110: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_increase_high)},
                 111: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_normal)},
                 112: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_increase_low)},
                 113: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate)},
                 114: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_increase_high)},
                 115: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_normal)},
                 116: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_low)},
                 117: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_moderate)},
                 118: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_high)},
                 119: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_normal)},
                 120: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_low)},
                 121: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_moderate)},
                 122: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_high)},
                 123: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_normal)},
                 124: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_low)},
                 125: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_moderate)},
                 126: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_high)},
                 127: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_normal)},
                 128: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_low)},
                 129: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate)},
                 130: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_high)},
                 131: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_high,
                                                    crop_normal)},
                 132: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_low)},
                 133: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_moderate)},
                 134: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_high)},
                 135: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_normal,
                                                    crop_normal)},
                 136: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_low)},
                 137: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_moderate)},
                 138: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_high)},
                 139: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_normal)},
                 140: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_low)},
                 141: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_moderate)},
                 142: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_high)},
                 143: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate,
                                                    crop_normal)},
                 144: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate,
                                                    crop_increase_low)},
                 145: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate)},
                 146: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate,
                                                    crop_increase_high)},
                 147: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_high,
                                                    crop_normal)},
                 148: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_high,
                                                    crop_increase_low)},
                 149: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_high,
                                                    crop_increase_moderate)},
                 150: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_high,
                                                    crop_increase_high)},
                 151: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_normal,
                                                    crop_normal)},
                 152: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_normal,
                                                    crop_increase_low)},
                 153: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_normal,
                                                    crop_increase_moderate)},
                 154: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_normal,
                                                    crop_increase_high)},
                 155: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_low,
                                                    crop_normal)},
                 156: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_low,
                                                    crop_increase_low)},
                 157: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_low,
                                                    crop_increase_moderate)},
                 158: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_low,
                                                    crop_increase_high)},
                 159: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_moderate,
                                                    crop_normal)},
                 160: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_moderate,
                                                    crop_increase_low)},
                 161: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate)},
                 162: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_moderate,
                                                    crop_increase_high)},
                 163: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_normal)},
                 164: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_increase_low)},
                 165: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_increase_moderate)},
                 166: {'crop_image_by_percentage': (crop_increase_low,
                                                    crop_increase_high,
                                                    crop_increase_high,
                                                    crop_increase_high)},
                 167: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_normal,
                                                    crop_increase_low)},
                 168: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_normal,
                                                    crop_increase_moderate)},
                 169: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_normal,
                                                    crop_increase_high)},
                 170: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_normal)},
                 171: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_increase_low)},
                 172: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_increase_moderate)},
                 173: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_low,
                                                    crop_increase_high)},
                 174: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_normal)},
                 175: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_increase_low)},
                 176: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate)},
                 177: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_moderate,
                                                    crop_increase_high)},
                 178: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_normal)},
                 179: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_low)},
                 180: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_moderate)},
                 181: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_normal,
                                                    crop_increase_high,
                                                    crop_increase_high)},
                 182: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_normal)},
                 183: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_low)},
                 184: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_moderate)},
                 185: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_normal,
                                                    crop_increase_high)},
                 186: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_normal)},
                 187: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_low)},
                 188: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_moderate)},
                 189: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_low,
                                                    crop_increase_high)},
                 190: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_normal)},
                 191: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_low)},
                 192: {'crop_image_by_percentage': (crop_increase_moderate,
                                                    crop_increase_low,
                                                    crop_increase_moderate,
                                                    crop_increase_moderate)}
              #    193: {'crop_image_by_percentage': (crop_increase_moderate,
              #                                       crop_increase_low,
              #                                       crop_increase_moderate,
              #                                       crop_increase_high)}
              }
                                                    }

my_dick = {"crop_normal": crop_normal, "crop_increase_low": crop_increase_low,
"crop_increase_moderate": crop_increase_moderate, "crop_increase_high": crop_increase_high}

# for num in range(47, 101):
#     patterns[num] = {'adjust_white_balance': (),
#       'adjust_contrast': (),
#       'adjust_brightness': (),
#       'crop_image_by_percentage': (),
#       'resize_image': (),
#       'rotate_image': ()}



# errors = []
# for num, combination in combinations.items():
#     c = tuple(my_dick[key] for key in combination)
#     try:
#        if patterns[num]['crop_image_by_percentage'] != c:
#               # print(patterns[num]['crop_image_by_percentage'])
#               # print(c)

#               errors.append(num)
#               patterns[num]['crop_image_by_percentage'] = c


#     except KeyError:

#         break
# print(errors)
# pprint(patterns, sort_dicts=False, compact=False)

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
    patterns[keys[-1]][param_name] = tuple()
    print(patterns[keys[-1]][param_name])
    return patterns


# for phase in patterns.values():
#     for pattern in phase.values():
#         # Создаём список ключей, которые нужно удалить
#         keys_to_delete = [key for key, values in pattern.items() if not values]

#         # Удаляем их
#         for key in keys_to_delete:
#             del pattern[key]



#     # patterns = move_param_value(patterns, key, 'crop_image_by_percentage')
# #     index = key + 49
# #     # print(combinations[key])
# #     patterns[index] = {}
# #     patterns[index]['crop_image_by_percentage'] = combinations[key]
#     # pprint(patterns[50], sort_dicts=False, compact=False)





# pprint(patterns, sort_dicts=False, compact=False)
# print(len(patterns))

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

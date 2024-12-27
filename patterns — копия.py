import itertools


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
        combinations.append(f"'adjust_contrast': ({c},),\n'adjust_brightness': ({b},)")

# Ограничиваем до 28 уникальных комбинаций
unique_combinations = combinations

# Вывод комбинаций
for i, combo in enumerate(combinations, 1):
    print(f"Комбинация {i}:\n{combo}")
    print()

# Обновляем словарь patterns
patterns = {
    '1': {
        'adjust_white_balance': (1.1, 1.0, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_low, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '2': {
        'adjust_white_balance': (0.9, 1.0, 1.1),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_low, crop_image.increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '3': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_low, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '4': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_moderate, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '5': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_moderate, crop_image.increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '6': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_high,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '7': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_high,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_high, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '8': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_high,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_high, crop_image.increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '9': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_high, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '10': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_low,),
        'adjust_brightness': (brightness.decrease_high,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.normal, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '11': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.normal, crop_image.increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '12': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.increase_low,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.normal, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '13': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.increase_low,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_low, crop_image.normal),
        'resize_image': (),
        'rotate_image': ()
    },
    '14': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.increase_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_low, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '15': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.increase_low,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_low, crop_image.increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '16': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_low,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_low, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '17': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_low,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.normal),
        'resize_image': (),
        'rotate_image': ()
    },
    '18': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
    '19': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_low,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_moderate),
        'resize_image': (),
        'rotate_image': ()
    },
    '20': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '21': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '22': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '23': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '24': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '25': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '26': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.decrease_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '27': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_low,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '28': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_moderate,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '29': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '30': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '31': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '32': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '33': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '34': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '35': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '36': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '37': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '38': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '39': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
    '40': {
        'adjust_white_balance': (1.0, 1.1, 0.9),
        'adjust_contrast': (contrast.increase_high,),
        'adjust_brightness': (brightness.decrease_moderate,),
        'crop_image_by_percentage': (crop_image.normal, crop_image.increase_low, crop_image.increase_moderate, crop_image.increase_high),
        'resize_image': (),
        'rotate_image': ()
    },
}


# if __name__ == "__main__":
#     for num, pattern in patterns.items():
#         print(num)
#         for key, value in pattern.items():
#             print('    ', key, value)
#         print()

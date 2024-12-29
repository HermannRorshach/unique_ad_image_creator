from pprint import pprint

class ImageModifier:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ImageModifier({self.value!r})"


# Создаем экземпляры ImageModifier с соответствующими значениями

# Значения для контрастности
contrast_normal = ImageModifier(1)

# Значения для увеличения контрастности
contrast_increase_low = ImageModifier(1.2)
contrast_increase_moderate = ImageModifier(1.4)
contrast_increase_high = ImageModifier(1.6)

# Значения для уменьшения контрастности
contrast_decrease_low = ImageModifier(0.9)
contrast_decrease_moderate = ImageModifier(0.8)
contrast_decrease_high = ImageModifier(0.7)


# Значения для яркости
brightness_normal = ImageModifier(1)

# Значения для увеличения яркости
brightness_increase_low = ImageModifier(1.1)
brightness_increase_moderate = ImageModifier(1.2)
brightness_increase_high = ImageModifier(1.3)

# Значения для уменьшения яркости
brightness_decrease_low = ImageModifier(0.93)
brightness_decrease_moderate = ImageModifier(0.87)
brightness_decrease_high = ImageModifier(0.8)


# Значения для обрезки
crop_normal = ImageModifier(0)
crop_increase_low = ImageModifier(2)
crop_increase_moderate = ImageModifier(4)
crop_increase_high = ImageModifier(6)


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
    }
}

patterns = {'1': {'adjust_white_balance': (1.1, 1.0, 0.9),
       'adjust_contrast': (ImageModifier(1.2),),
       'adjust_brightness': (ImageModifier(1.1),),
       'crop_image_by_percentage': (ImageModifier(0),
                                    ImageModifier(0),
                                    ImageModifier(2),
                                    ImageModifier(2)),
       'resize_image': (),
       'rotate_image': ()},
 '2': {'adjust_white_balance': (0.9, 1.0, 1.1),
       'adjust_contrast': (ImageModifier(1.2),),
       'adjust_brightness': (ImageModifier(1.2),),
       'crop_image_by_percentage': (ImageModifier(0),
                                    ImageModifier(0),
                                    ImageModifier(2),
                                    ImageModifier(4)),
       'resize_image': (),
       'rotate_image': ()},
 '3': {'adjust_white_balance': (1.0, 1.1, 0.9),
       'adjust_contrast': (ImageModifier(1.2),),
       'adjust_brightness': (ImageModifier(1.3),),
       'crop_image_by_percentage': (ImageModifier(0),
                                    ImageModifier(0),
                                    ImageModifier(2),
                                    ImageModifier(6)),
       'resize_image': (),
       'rotate_image': ()},
 '4': {'adjust_white_balance': (1.0, 0.9, 1.1),
       'adjust_contrast': (ImageModifier(1.2),),
       'adjust_brightness': (ImageModifier(1),),
       'crop_image_by_percentage': (ImageModifier(0),
                                    ImageModifier(0),
                                    ImageModifier(4),
                                    ImageModifier(2)),
       'resize_image': (),
       'rotate_image': ()},
 '5': {'adjust_white_balance': (1.1, 0.9, 1.0),
       'adjust_contrast': (ImageModifier(1.2),),
       'adjust_brightness': (ImageModifier(0.93),),
       'crop_image_by_percentage': (ImageModifier(0),
                                    ImageModifier(0),
                                    ImageModifier(4),
                                    ImageModifier(4)),
       'resize_image': (),
       'rotate_image': ()}}
pprint(patterns, sort_dicts=False)

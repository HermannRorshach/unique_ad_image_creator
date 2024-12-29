class ContrastNormal:
    def __init__(self):
        self.value = 1

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return str(self.value)

a = ContrastNormal()

class AdjustContrast:
    def __init__(self):

        self.normal = repr(ContrastNormal())

        # Значения для увеличения контрастности
        self.increase_low = 1.2
        self.increase_moderate = 1.4
        self.increase_high = 1.6

        # Значения для уменьшения контрастности
        self.decrease_low = 0.9
        self.decrease_moderate = 0.8
        self.decrease_high = 0.7

contrast = AdjustContrast()

patterns = {
    '1': {
        'adjust_white_balance': (1.1, 1.0, 0.9),
        'adjust_contrast': (contrast.normal,),
        # 'adjust_brightness': (brightness.increase_low,),
        # 'crop_image_by_percentage': (crop_image.normal, crop_image.normal, crop_image.increase_low, crop_image.increase_low),
        'resize_image': (),
        'rotate_image': ()
    },
}
print(repr(a))
print(a)
print(patterns)
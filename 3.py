from pprint import pprint

patterns = {
    1: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    2: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    3: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    4: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    5: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    6: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    7: {
        'adjust_contrast': ('contrast_increase_low',),
    },
    8: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    9: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    10: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    11: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    12: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    13: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    14: {
        'adjust_contrast': ('contrast_increase_moderate',),
    },
    15: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    16: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    17: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    18: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    19: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    20: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    21: {
        'adjust_contrast': ('contrast_increase_high',),
    },
    22: {
        'adjust_contrast': ('contrast_normal',),
    },
    23: {
        'adjust_contrast': ('contrast_normal',),
    },
    24: {
        'adjust_contrast': ('contrast_normal',),
    },
    25: {
        'adjust_contrast': ('contrast_normal',),
    },
    26: {
        'adjust_contrast': ('contrast_normal',),
    },
    27: {
        'adjust_contrast': ('contrast_normal',),
    },
    28: {
        'adjust_contrast': ('contrast_normal',),
    },
    29: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    30: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    31: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    32: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    33: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    34: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    35: {
        'adjust_contrast': ('contrast_decrease_low',),
    },
    36: {
        'adjust_contrast': ('contrast_decrease_moderate',),
    },
    37: {
        'adjust_contrast': ('contrast_decrease_moderate',),
    },
    38: {
        'adjust_contrast': ('contrast_decrease_moderate',),
    },
    39: {
        'adjust_contrast': ('contrast_decrease_moderate',),
    },
    40: {
        'adjust_contrast': ('contrast_decrease_moderate',),}}


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
    return patterns

for key in (38, 31, 24, 17, 16, 10, 3):
    patterns = move_param_value(patterns, key, 'adjust_contrast')
    pprint(patterns, sort_dicts=False, compact=False)
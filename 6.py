import cv2
import numpy as np

def rotate_image(image, angle):
    # Получение размеров исходного изображения
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Создание матрицы поворота
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Вычисление новых границ изображения после поворота
    cos = abs(rotation_matrix[0, 0])
    sin = abs(rotation_matrix[0, 1])
    new_width = int((h * sin) + (w * cos))
    new_height = int((h * cos) + (w * sin))

    # Корректировка матрицы поворота
    rotation_matrix[0, 2] += (new_width / 2) - center[0]
    rotation_matrix[1, 2] += (new_height / 2) - center[1]

    # Применение поворота
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
    return rotated_image

# Пример использования
image = cv2.imread("input.jpg")
rotated = rotate_image(image, 15)  # Поворот на 45 градусов
cv2.imwrite("output.jpg", rotated)

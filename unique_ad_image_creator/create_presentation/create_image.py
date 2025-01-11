from PIL import Image, ImageDraw, ImageFont

# Размеры изображения
img_width = 250
img_height = 60

# Цвет (в формате RGB)
color = (184, 255, 0)  # Цвет B8FF00 в формате RGB

# Создание нового изображения
image = Image.new("RGB", (img_width, img_height), color)

# Сохранение изображения в формате PNG
image.save("output_image.png")
image.close()


im1 = Image.open('white_lines_big.png')
im2 = Image.open('output_image.png')

im1.paste(im2, (12, 200))
im1.save('fon_pillow_paste.png')


# Создаем объект со шрифтом
font = ImageFont.truetype('Code-Pro-Bold-LC.ttf', size=24)
draw_text = ImageDraw.Draw(im1)
draw_text.text(
    (100, 100),
    '10000',
    # Добавляем шрифт к изображению
    font=font,
    fill='#ffff')
im1.show()
im2.show()

im1.close()
im2.close()

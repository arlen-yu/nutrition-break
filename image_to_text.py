from parseIngredients import parseIngredient

try:
    import Image

except ImportError:
    from PIL import Image

import pytesseract

text_from_img = pytesseract.image_to_string(Image.open('test.jpg'))

print text_from_img

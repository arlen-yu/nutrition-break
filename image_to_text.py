from parseIngredients import parseIngredient
import pytesseract

def convert_to_text(path):
    try:
        import Image
    except ImportError:
        from PIL import Image

    text_from_img = pytesseract.image_to_string(Image.open(path))

    return parseIngredient (text_from_img)

print convert_to_text("images/a.png")

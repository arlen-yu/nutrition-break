import parseIngredients
import pytesseract

def convert_to_text(path):
    try:
        import Image
    except ImportError:
        from PIL import Image

    text_from_img = pytesseract.image_to_string(Image.open(path))

    return parseIngredients.parseIngredient(text_from_img)

def convert_to_text(path):

    from parseIngredients import parseIngredient

    try:
        import Image

    except ImportError:
        from PIL import Image

    import pytesseract

    text_from_img = pytesseract.image_to_string(Image.open(path))

    return parseIngredient (text_from_img)

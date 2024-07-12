from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

img = Image.open('text.jpeg')
text = tess.image_to_string(img)

print(text)


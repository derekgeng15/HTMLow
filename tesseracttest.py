import pytesseract
import cv2 as cv

pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

img = cv.imread('output\\1g.png')
rev = pytesseract.image_to_string(img, config="--psm 10")
print(rev)

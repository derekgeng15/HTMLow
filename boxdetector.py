import pytesseract
import cv2 as cv
import numpy as np
pytesseract.pytesseract.tesseract_cmd=r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

d = {"T" : "text", "B" : "button", "H":"header"}
class Widget():
    def __init__(self, x, y, width, height, box):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.b = box
        self.text = ""

def filterRed(img): #returns red bin mask
    min_mask = (100, 0, 100)
    max_mask = (180, 255, 255)
    b1 = cv.inRange(img, min_mask, max_mask)
    min_mask = (0, 0, 114)
    max_mask = (4, 255, 255)
    b2 = cv.inRange(img, min_mask, max_mask)
    return b1 | b2
def filterGreen(img): #returns green bin mask
    min_mask = (55, 0, 30)
    max_mask = (90, 255, 190)
    return cv.inRange(img, min_mask, max_mask)
def filterBlack(img): #returns black bin mask
    min_mask = (0, 0, 0)
    max_mask = (255, 255, 60)
    return cv.inRange(img, min_mask, max_mask)
def getWidgets(img):#returns a list of boxes
    frame_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    bin_mask = filterBlack(img)
    out = []
    contours, hierarchy = cv.findContours(bin_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    f_cnt = []
    ct = 1
    for c in contours:
        x, y, w, h = cv.boundingRect(c)
        area = w * h
        if area > 10000:
            oimg = img[y:(y+h), x:(x+w)]
            out.append(Widget(x, y, w, h, oimg))
            cv.imwrite(f'output\\{ct}.png', oimg)
            ct+=1
            f_cnt.append(c)
    return out
def createWebWidgets(img):
    fout = img
    out = []
    widgets = getWidgets(img)
    ct = 1
    custom_config = r'-c tessedit_char_whitelist=TBHtbh --psm 10'
    for w in widgets:
        frame_HSV = cv.cvtColor(w.b, cv.COLOR_BGR2HSV)
        cv.rectangle(fout, (w.x, w.y), (w.x + w.w, w.y + w.h), (0, 255, 0), 3)
        rbin_mask = filterRed(frame_HSV)
        rbin_mask = cv.erode(rbin_mask, kernel=np.ones((2, 2), np.uint8), iterations = 1)
        rbin_mask = cv.dilate(rbin_mask, kernel=np.ones((2, 2), np.uint8), iterations=1)
        rbin_mask = cv.bitwise_not(rbin_mask)
        text = pytesseract.image_to_string(rbin_mask)
        cv.imwrite(f'output\\{ct}r.png', rbin_mask)
        # print(text)
        gbin_mask = filterGreen(frame_HSV)    
        contours, hierarchy = cv.findContours(gbin_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        x, y, wi, h = cv.boundingRect(contours[0])
        letter = gbin_mask[y:(y+h), x:(x+wi)]
        letter = cv.dilate(letter, kernel=np.ones((4, 4), np.uint8))
        letter = cv.copyMakeBorder(letter, 20, 20, 20, 20, cv.BORDER_CONSTANT, None, value = 0)
        letter = cv.resize(letter, (60, 60))
        letter = cv.bitwise_not(letter)
        wtype = pytesseract.image_to_string(letter, config=custom_config)
        # print("type", wtype)
        if len(wtype) == 0:
            wtype = "B"
        cv.imwrite(f'output\\{ct}g.png', letter)
        ct+=1
        out.append([w.x, w.y, w.w, w.h, d[wtype[0]], text])
    print(out)
    cv.imwrite(f'output\\out.png', fout)
    return out
img = cv.imread('img\\demo.jpg', cv.COLOR_BGR2HSV)
w = createWebWidgets(img)
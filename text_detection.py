#!/usr/bin/env python3
import sys

sys.path.append(r"c:\python38\lib\site-packages")
sys.path.append(r"c:\users\pradyun\appdata\roaming\python\python38\site-packages")

import numpy as np
import cv2


def text_detection(filename: str) -> tuple:
    # returns:
    #   type box it is
    #   the text contained in the box
    image = open(filename)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(image,image, mask= mask)

    cv2.imshow('frame', image)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

if __name__ == "main":
    text_detection('test.jpg')


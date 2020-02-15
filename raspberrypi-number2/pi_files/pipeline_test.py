import cv2
import timeit
import numpy as np

best_low = (40, 7, 185)
best_high = (94, 255, 255)

def pipeline(img, low, high):

    blur = cv2.bilateralFilter(img, 7, 400, 10)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, low, high)

    return thresh

img = cv2.imread('image_35.png')
img[:, :, [0, 2]] = img[:, :, [2, 0]]

SETUP = '''
from __main__ import pipeline, best_low, best_high, img
'''

TEST = '''
pipeline(img, best_low, best_high)
'''

if __name__ == '__main__':
    print(timeit.repeat(setup=SETUP, stmt=TEST, number=10))
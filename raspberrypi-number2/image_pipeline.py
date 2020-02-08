
from __future__ import print_function
import cv2
import numpy as np
import pathlib
import random
from matplotlib import pyplot as plt

import argparse
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

cv2.namedWindow(window_capture_name)
cv2.namedWindow(window_detection_name)
cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

plt.ion()
plt.plot([1.6, 2.7])

p = pathlib.Path('.')
files = p.glob('**/images/*')

while True:
    for filename in files:
        print(filename)
        img = cv2.imread(str(filename))
        img[:, :,[0, 2]] = img[:, :,[2, 0]]

        blur = cv2.bilateralFilter(img, 9, 75, 75)
        blur_hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        key = 0
        while not key:
            thresh = cv2.inRange(blur_hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))
            edges = cv2.Canny(thresh,100,200)

            plt.clf()
            plt.subplot(221), plt.imshow(img,cmap = 'gray')
            plt.title('Original Image'), plt.xticks([]), plt.yticks([])
            plt.subplot(222), plt.imshow(blur ,cmap = 'gray')
            plt.title('Blur Image'), plt.xticks([]), plt.yticks([])
            plt.subplot(223), plt.imshow(thresh, cmap = 'gray')
            plt.title('Thresh Image'), plt.xticks([]), plt.yticks([])
            plt.subplot(224), plt.imshow(edges ,cmap = 'gray')
            plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

            plt.pause(0.001)
            key = 1
    if input() == 'exit':
        break
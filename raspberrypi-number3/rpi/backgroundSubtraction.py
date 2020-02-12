import cv2
import numpy as np
from math import cos, sin, sqrt
from clientbase import ClientBase

# Create a new ClientBase set to use the computer's webcam
client = ClientBase(client_id='RaspberryPi3', piCamera=False)

# Start the client. Very important
client.start()

target_color = (0, 244, 244) # r, g, b

tolerance = 10

# An infinite loop, terminated by a KeyboardInterrupt (CTRL + C)
while True:
	img = client.read() # Read an image from the camera

	b, g, r = cv2.split(img)

	ret,thresh_r = cv2.threshold(r,target_color[0] + tolerance,255,cv2.THRESH_BINARY)

	ret,thresh_g = cv2.threshold(g,target_color[1] - tolerance,255,cv2.THRESH_BINARY)

	ret,thresh_b = cv2.threshold(b,target_color[2] - tolerance,255,cv2.THRESH_BINARY)

	thresh_bg = cv2.bitwise_and(thresh_b, thresh_g)

	not_thresh_r = cv2.bitwise_not(thresh_r)

	mask = cv2.bitwise_and(thresh_bg, not_thresh_r)

	masked = cv2.bitwise_and(img,img,mask = mask)

	client.send(masked) # Send the image to the server
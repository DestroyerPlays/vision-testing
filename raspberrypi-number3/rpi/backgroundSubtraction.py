import cv2
import numpy as np
from math import cos, sin, sqrt
from clientbase import ClientBase

# Create a new ClientBase set to use the computer's webcam
client = ClientBase(client_id='RaspberryPi3', piCamera=False)

# Start the client. Very important
client.start()

backSub = cv2.createBackgroundSubtractorKNN()

# An infinite loop, terminated by a KeyboardInterrupt (CTRL + C)
while True:
	img = client.read() # Read an image from the camera

	#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert it to greyscale
	
	mask = backSub.apply(img)

	masked = cv2.bitwise_and(img, img, mask=mask)

	client.send(masked) # Send the image to the server
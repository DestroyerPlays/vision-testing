import cv2
import numpy as np
from math import cos, sin, sqrt
from clientbase import ClientBase

# Create a new ClientBase set to use the computer's webcam
client = ClientBase(client_id='RaspberryPi3', piCamera=False)

# Start the client. Very important
client.start()

# An infinite loop, terminated by a KeyboardInterrupt (CTRL + C)
while True:
	img = client.read() # Read an image from the camera

	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert it to greyscale as a test

	client.send(img) # Send the image to the server
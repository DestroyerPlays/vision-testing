import cv2
import numpy as np
from clientbase import ClientBase

# Create a new ClientBase set to use the computer's webcam
client = ClientBase(client_id='RaspberryPi3', piCamera=False)

# Start the client. Very important
client.start()

tensorflowNet = cv2.dnn.readNetFromTensorflow('../target_detector/transformed_frozen_inference_graph.pb',
											  '../target_detector/ssd_mobilenet_v1_target_2020_03_03.pbtxt')

# An infinite loop, terminated by a KeyboardInterrupt (CTRL + C)
while True:
	img = client.read() # Read an image from the camera

	rows, cols, channels = img.shape

	tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

	networkOutput = tensorflowNet.forward()

	for detection in networkOutput[0,0]:

	score = float(detection[2])

	targeted = img.copy()

	if score > 0.2:
			
			left = detection[3] * cols
			top = detection[4] * rows
			right = detection[5] * cols
			bottom = detection[6] * rows
			
			#draw a red rectangle around detected objects
			cv2.rectangle(targeted, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), thickness=2)

	client.send(targeted) # Send the image to the server
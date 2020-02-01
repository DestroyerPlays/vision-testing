from networktables import NetworkTables
from clientbase import ClientBase
import numpy as np
import cv2

NetworkTables.initialize()

sd = NetworkTables.getTable("SmartDashboard")

bounding_box = None

# Create a new ClientBase set to use the computer's webcam
client = ClientBase(client_id='RaspberryPi3', piCamera=False)

# Start the client. Very important
client.start()

tracker = cv2.TrackerKCF_create()

# An infinite loop, terminated by a KeyboardInterrupt (CTRL + C)
while True:
	img = client.read() # Read an image from the camera

	img_cy = int(img.shape[0] / 2)
	img_cx = int(img.shape[1] / 2)
	
	if bounding_box is not None:
		(success, box) = tracker.update(img)

		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

			cX = x + int(w / 2.0)
			cY = y + int(h / 2.0)

			cv2.circle(img, (cX, cY), 4, (0, 255, 0), -1)

			diff_x = cX - img_cx
			diff_y = cY - img_cy

			text = 'x error: {}, y error: {}'.format(diff_x, diff_y)

			print(text)

			sd.putNumber("error_x", diff_x)
			sd.putNumber("error_y", diff_y)

			cv2.putText(img, text, (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        cv2.rectangle(frame, (0, 0), (30, 80), (255, 255, 0), 1)

        client.send(img) # Send the image to the server

        _ = input('Press key to initialize')

        bounding_box = (30, 80)
 
		tracker.init(frame, bounding_box)
		
	cv2.rectangle(img, (img_cx - 1, img_cy + 10), (img_cx + 1, img_cy - 10), (0, 255, 255), -1)

	cv2.rectangle(img, (img_cx - 10, img_cy + 1), (img_cx + 10, img_cy - 1), (0, 255, 255), -1)

	client.send(img) # Send the image to the server

client.end()
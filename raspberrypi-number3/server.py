# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq.imagezmq as imagezmq
import argparse
import imutils
import cv2
	
# initialize the ImageHub object
imageHub = imagezmq.ImageHub()

raspberrypi = ""

(rpiName, frame) = imageHub.recv_image()
imageHub.send_reply(b'OK')

raspberrypi = rpiName
lastActiveTime = datetime.now()
currentFrame = None

print("[INFO] receiving data from {}...".format(rpiName))

# start looping over all the frames
while True:
    # receive RPi name and frame from the RPi and acknowledge
	# the receipt
	(rpiName, frame) = imageHub.recv_image()
	imageHub.send_reply(b'OK')
 
	print("[INFO] receiving data from {}...".format(rpiName))
 
	# record the last active time for the device from which we just
	# received a frame
	lastActive = datetime.now()

    # resize the frame to have a maximum width of 400 pixels, then
	# grab the frame dimensions and construct a blob
	frame = imutils.resize(frame, width=400)
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    
	# draw the sending device name on the frame
	cv2.putText(frame, rpiName, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
 
	# update the new frame in the frame dictionary
	currentFrame = frame

	cv2.imshow('image', currentFrame)
 
	# detect any kepresses
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
cv2.destroyAllWindows()
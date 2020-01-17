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

# start looping over all the frames
while True:
    # receive RPi name and frame from the RPi and acknowledge
	# the receipt
	(rpiName, frame) = imageHub.recv_image()
	imageHub.send_reply(b'OK')
 
	print("[INFO] receiving data from {}...".format(rpiName))

    # resize the frame to have a maximum width of 400 pixels, then
	frame = imutils.resize(frame, width=400)
    
	# draw the sending device name on the frame
	cv2.putText(frame, rpiName, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	cv2.imshow(rpiName, frame)
 
	# detect any kepresses
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
cv2.destroyAllWindows()
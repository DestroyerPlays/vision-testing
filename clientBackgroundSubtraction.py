from imutils.video import VideoStream
import imagezmq.imagezmq as imagezmq
import argparse
import socket
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, sqrt

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())
 
# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args["server_ip"]))

img_width = 320
img_height = 240
	
# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
#vs = VideoStream(usePiCamera=True, resolution=(img_width, img_height)).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

count=0
history = 10
nGauss = 3
bgThresh = 0.6
noise = 20
bgs = cv2.BackgroundSubtractorMOG(history,nGauss,bgThresh,noise)

plt.figure()
plt.hold(True)
plt.axis([0,480,360,0])

while True:
	img = vs.read()

measuredTrack=np.zeros((numframes,2))-1
while count<numframes:
    count+=1
    img2 = capture.read()[1]
    cv2.imshow("Video",img2)
    foremat=bgs.apply(img2)
    cv2.waitKey(100)
    foremat=bgs.apply(img2)
    ret,thresh = cv2.threshold(foremat,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        m= np.mean(contours[0],axis=0)
        measuredTrack[count-1,:]=m[0]
        plt.plot(m[0,0],m[0,1],'ob')
    cv2.imshow('Foreground',foremat)
    cv2.waitKey(80)
capture.release()
print measuredTrack
np.save("ballTrajectory", measuredTrack)
plt.show()


	# read the frame from the camera and send it to the server
	# frame = vs.read()
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	sender.send_image(rpiName, img)
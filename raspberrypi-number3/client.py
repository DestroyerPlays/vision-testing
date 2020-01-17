from imutils.video import VideoStream
import imagezmq.imagezmq as imagezmq
import argparse
import socket
import time
import cv2
import numpy as np
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
vs = VideoStream(usePiCamera=True, resolution=(img_width, img_height)).start()
#vs = VideoStream(src=0).start()
time.sleep(2.0)

kalman = cv2.KalmanFilter(2, 1, 0)

def calc_point(angle):
	return (np.around(img_width/2 + img_width/3*cos(angle), 0).astype(int),
			np.around(img_height/2 - img_width/3*sin(angle), 1).astype(int))

# plot points
def draw_cross(img, center, color, d):
	cv2.line(img,
				(center[0] - d, center[1] - d), (center[0] + d, center[1] + d),
				color, 1, cv2.LINE_AA, 0)
	cv2.line(img,
				(center[0] + d, center[1] - d), (center[0] - d, center[1] + d),
				color, 1, cv2.LINE_AA, 0)

while True:
	state = 0.1 * np.random.randn(2, 1)

	kalman.transitionMatrix = np.array([[1., 1.], [0., 1.]])
	kalman.measurementMatrix = 1. * np.ones((1, 2))
	kalman.processNoiseCov = 1e-5 * np.eye(2)
	kalman.measurementNoiseCov = 1e-1 * np.ones((1, 1))
	kalman.errorCovPost = 1. * np.ones((2, 2))
	kalman.statePost = 0.1 * np.random.randn(2, 1)

	state_angle = state[0, 0]
	state_pt = calc_point(state_angle)

	prediction = kalman.predict()
	predict_angle = prediction[0, 0]
	predict_pt = calc_point(predict_angle)

	measurement = kalman.measurementNoiseCov * np.random.randn(1, 1)

	# generate measurement
	measurement = np.dot(kalman.measurementMatrix, state) + measurement

	measurement_angle = measurement[0, 0]
	measurement_pt = calc_point(measurement_angle)

	img = vs.read()

	#img = np.zeros((img_height, img_width, 3), np.uint8)
	draw_cross(img, np.int32(state_pt), (255, 255, 255), 3)
	draw_cross(img, np.int32(measurement_pt), (0, 0, 255), 3)
	draw_cross(img, np.int32(predict_pt), (0, 255, 0), 3)

	cv2.line(img, state_pt, measurement_pt, (0, 0, 255), 3, cv2.LINE_AA, 0)
	cv2.line(img, state_pt, predict_pt, (0, 255, 255), 3, cv2.LINE_AA, 0)

	kalman.correct(measurement)

	process_noise = sqrt(kalman.processNoiseCov[0,0]) * np.random.randn(2, 1)
	state = np.dot(kalman.transitionMatrix, state) + process_noise

	# read the frame from the camera and send it to the server
	# frame = vs.read()
	# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	sender.send_image(rpiName, img)
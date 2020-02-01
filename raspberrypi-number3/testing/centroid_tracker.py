from networktables import NetworkTables
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import cv2
import time

NetworkTables.initialize()

sd = NetworkTables.getTable("SmartDashboard")

bounding_box = None

vs = VideoStream(src=0).start()
time.sleep(2.0)

tracker = cv2.TrackerKCF_create()

while True:
	frame = vs.read()

	frame = imutils.resize(frame, width=500)
	(h, w) = frame.shape[:2]

	img_cy = int(frame.shape[0] / 2)
	img_cx = int(frame.shape[1] / 2)

	if bounding_box is not None:
		(success, box) = tracker.update(frame)

		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

			cX = x + int(w / 2.0)
			cY = y + int(h / 2.0)

			cv2.circle(frame, (cX, cY), 4, (0, 255, 0), -1)

			diff_x = cX - img_cx
			diff_y = cY - img_cy

			text = 'x error: {}, y error: {}'.format(diff_x, diff_y)

			print(text)

			sd.putNumber("error_x", diff_x)
			sd.putNumber("error_y", diff_y)

			cv2.putText(frame, text, (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		
	cv2.rectangle(frame, (img_cx - 1, img_cy + 10), (img_cx + 1, img_cy - 10), (0, 255, 255), -1)

	cv2.rectangle(frame, (img_cx - 10, img_cy + 1), (img_cx + 10, img_cy - 1), (0, 255, 255), -1)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("s"):
		
		bounding_box = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
 
		tracker.init(frame, bounding_box)
	
	elif key == ord("q"):
		break

vs.stop()

cv2.destroyAllWindows()
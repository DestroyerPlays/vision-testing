import imutils
import cv2
import time
import os
from imutils.video import VideoStream

vs = VideoStream(src = 0, framerate = 30).start()

time.sleep(2)

save_location = 'images/raw'

im_count = 0

imcount_path = 'imcount.txt'

image_name = '{:04}_image.png'

if os.path.exists(imcount_path):
    with open(imcount_path, 'r') as fp:
        im_count = int(fp.read())
else:
    with open(imcount_path, 'w') as fp:
        fp.write('0')


def inc_imcount():
    global im_count

    im_count += 1
    
    with open(imcount_path, 'w') as fp:
        fp.write(str(im_count))

while True:

    frame = vs.read()

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    if key == ord("c"):
        frame_path = str(os.path.join(save_location, image_name.format(im_count)))

        cv2.imwrite(frame_path, frame)

        inc_imcount()

# do a bit of cleanup
cv2.destroyAllWindows()
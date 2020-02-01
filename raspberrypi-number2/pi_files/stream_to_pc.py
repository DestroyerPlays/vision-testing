from clientbase import ClientBase
import numpy as np
import cv2

client = ClientBase(client_id="RaspberryPi2", piCamera=True)
client.start()

while True:
    img = client.read()
    retval, threshold = cv2.threshold(img, 12, 255, cv2.THRESH_BINARY)
    client.send(img)
from clientbase import ClientBase
import time
import numpy as np
import cv2

client = ClientBase(client_id="RaspberryPi2", piCamera=True)
client.start()

while True:
    img = client.read()
    cv2.imwrite("images/test_image_{}".format(time.time())+".png", img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # client.send(img)
    client.send(img)
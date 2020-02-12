from clientbase import ClientBase
import time
import numpy as np
import cv2

client = ClientBase(client_id="RaspberryPi2", piCamera=True)
client.start()

while True:
    img = client.read()
    client.send(img)
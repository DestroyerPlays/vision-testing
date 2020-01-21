import os
import io
import cv2
import socket
import struct
import keyboard
import threading
import numpy as np

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
print("Opening socket")
server_socket = socket.socket()
server_socket.bind(('', 8000))
server_socket.listen(0)

cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Preview",  900, 600)
cont = True
searching = False

def check_for_quit():
    global cont
    global searching
    while cont:
        if keyboard.is_pressed('q'):
            print("Preparing to exit")
            cont = False
            if searching:
                os._exit(0)

thread = threading.Thread(target=check_for_quit, args=())
thread.daemon = True
thread.start()

while cont:
    
    print("Searching for Connection")
    searching = True
    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    print("Connection Estabilished")

    searching = False
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)

            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
            cv2.imshow("Preview", img)
            cv2.waitKey(1)
    finally:
        connection.close()

server_socket.close()
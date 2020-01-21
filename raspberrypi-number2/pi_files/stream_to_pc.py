import io
import tty
import cv2
import time
import select
import struct
import socket
import picamera
import termios
import numpy as np
from sys import stdin

def raw_keyboard_key():
    if select.select([stdin], [], [], 0) == ([stdin], [], []):
        return stdin.read(1)

old_settings = termios.tcgetattr(stdin)

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.15', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    tty.setcbreak(stdin.fileno())

    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    # Let the camera warm up for 2 seconds
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        foo, file_bytes = cv2.imencode('.jpeg', img)
        print(file_bytes)
        connection.write(file_bytes.tobytes())
        # If wish to quit, quit
        if raw_keyboard_key()=='\x1b':
            print("Exit key received")
            break
        
        # Reset the stream for the next capture

        stream.seek(0)
        stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    camera.close()
    connection.close()
    client_socket.close()
    termios.tcsetattr(stdin, termios.TCSADRAIN, old_settings)
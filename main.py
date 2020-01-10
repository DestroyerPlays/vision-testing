import picamera
from streaming import StreamingServer, StreamingOutput, StreamingHandler

def main():
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()

        camera.rotation = 180
        camera.start_recording(output, format='mjpeg')
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()

if __name__ == "__main__":
    main()
from .imagezmq.imagezmq import ImageSender
from imutils.video import VideoStream
from os import path
import json
import time

class ClientBase():
    def __init__(self, client_id=None, piCamera=False):
        self.config = {}
        self.port = 0
        self.server_ip = ''
        self.client_id = client_id
        self.piCamera = piCamera
        self.image_width = 0
        self.image_height = 0
        self.config_path = 'client-config.json'

        self.init_config()

    def init_config(self):
        if path.exists(self.config_path):
            with open(self.config_path, 'r') as fp:
                configjson = json.load(fp)
                port = configjson['port']
                server_ip = configjson['server-ip']
                client_id = configjson['client-id']
                image_width = configjson['image_width']
                image_height = configjson['image_height']
                piCamera = configjson['piCamera']
                self.port = port
                self.server_ip = server_ip
                self.image_width = image_width
                self.image_height = image_height
                self.piCamera = piCamera
                if self.client_id is None:
                    self.client_id = client_id
        else:
            with open(self.config_path, 'w') as fp:
                configjson = {
                    'port' : 5555,
                    'server-ip' : '192.168.1.27',
                    'client-id' : 'New-Raspberry-Pi',
                    'image_width' : 320,
                    'image_height' : 240,
                    'piCamera' : self.piCamera
                }
                json.dump(configjson, fp)
            self.init_config()

    def start(self):
        destination_str = "tcp://{}:{}".format(self.server_ip, self.port)
        width = self.image_width
        height = self.image_height
        piCamera = self.piCamera
        self.sender = ImageSender(connect_to=destination_str)
        if piCamera:
            self.video_stream = VideoStream(usePiCamera=True, resolution=(width, height)).start()
        else:
            self.video_stream = VideoStream(src=0).start()
        time.sleep(2)

    def read(self):
        return self.video_stream.read()

    def send(self, image):
        client_id = self.client_id
        self.sender.send_image(client_id, image)
    
    def end(self):
        self.video_stream.stop()

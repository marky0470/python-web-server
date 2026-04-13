import socket
from threading import Thread

class Handler:

    def __init__(self):
        self.routes = {
            ("GET", "/index.html"): (self.serve_file, "index.html"),
            ("GET", "/contacts.html"): (self.serve_file, "contacts.html"),
            ("GET", "/favicon.ico"): (self.serve_file, "favicon.ico"),
            ("GET", "/careers.html"): (self.serve_file, "careers.html")
        }

    def handle(self, route):

        try:
            handler, file_path = self.routes[route]
            res = handler(file_path)
        except KeyError:
            res = self.redirect_index()
        return res

    def success_header(self, body_length):
        return f"HTTP/1.1 200 OK\r\nContent-Length: {body_length}\r\nContent-Type: text/html\r\n\r\n"
    
    def redirect_index(self):
        return b"HTTP/1.1 301 Moved Permanently\r\nLocation: /index.html\r\n\r\n"
    
    def serve_file(self, file_path):
        with open(file_path, "rb") as f:
            body = f.read()
        res = self.success_header(len(body)).encode(encoding="utf-8") + body
        return res 

import functools
def threaded(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs).start()
        return thread
    return wrapper

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
                event.trigger("on_worker_end", self)
                break
    
            # print("REQUEST:", request)
            request_header, body = request.split("\r\n\r\n")
            request_line, headers = request_header.split("\r\n", maxsplit=1)

            method, path, protocol = request_line.split(" ")
            route = (method, path)

            response = self.handler.handle(route)

            # self.conn.send(b"hello")
            self.conn.send(response)

class Server:

    def __init__(self, event):
        self.id = 0
        self.workers = []
        self.event = event
        self.event.register_event("on_worker_end")
        self.event.register_callback("on_worker_end", self.kill_worker)
        self.start_listen()

    @threaded
    def start_listen(self):
        sock = socket.socket()
        sock.bind(("127.0.0.1", 8750))
        sock.listen()
        
        while True:
            conn, addr = sock.accept()
            print("New connection:", addr)
            print("# of Workers before append", len(self.workers))
            worker = Worker(conn, self.id, self.event)
            self.id += 1
            self.workers.append(worker)
            
    def kill_worker(self, worker):
        print(f"Killing Worker with id: {worker.id}")
        self.workers.remove(worker)

#issues: sub1: cb1, no args -> event_type <- cb2, args
class Event:

    def __init__(self):
        self.events = {}

    def register_event(self, event_type):
        try:
            self.events[event_type]
        except KeyError:
            self.events[event_type] = []

    def register_callback(self, event_type, callback, args=None):
        try:
            self.events[event_type].append(callback)
        except KeyError:
            print("Attempt to register callback to non-existent event type")

    def trigger(self, event_type, args):
        try:
            events = self.events[event_type]
        except KeyError:
            print("Attempt to trigger callbacks for event type that does not exist")
            return
        
        print(self.events[event_type])
        for event in events:
            print(f"Triggering callback {event} with arguments {args}")
            event(args)

event = Event()
Server(event)



import socket

from util.threaded import threaded
from worker import Worker
from event import Event

class Server:

    def __init__(self):
        self.id = 0
        self.workers = []
        self.event = Event()
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




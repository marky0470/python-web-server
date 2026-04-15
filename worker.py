import socket

from util.threaded import threaded

import time
class Worker:

    def __init__(self, conn : socket.socket, id, event, handler):
        self.id = id
        self.conn = conn
        self.event = event
        self.handler = handler
        self.event_loop()
        pass

    @threaded
    def event_loop(self):
        while True:
            time.sleep(0.5)

            request_line = self.recv_request_line()
            headers = self.recv_headers()

            try:
                content_length = int(headers["Content-Length"])
                body = self.conn.recv(content_length)
            except KeyError:
                pass

            method, path, protocol = request_line
            route = (method, path)

            response = self.handler.handle(route)

            self.conn.send(response)

    def recv_request_line(self):
        request_line = []
        s = ''
        while True:
            c = self.conn.recv(1).decode()
            if c == '':
                self.event.trigger("on_worker_end", self)
            if c == '\r':
                self.conn.recv(1)
                request_line.append(s)
                break
            if c == ' ':
                request_line.append(s)
                s=''
                continue     
            s += c


    def recv_headers(self):
        headers = {}
        key, val = '', ''
        state = 'key'
        crlf_count = 0
        encountered_colon = False
        while True:
            c = self.conn.recv(1).decode()
            if c == '\r':
                self.conn.recv(1)
                crlf_count += 1
                if crlf_count == 2: # POF? what if 3 crlf sent?
                    break
                headers[key] = val
                state = 'key'
                key, val = '', ''
                encountered_colon = False
                continue
            crlf_count = 0

            if c == ':' and not encountered_colon:
                encountered_colon = True
                self.conn.recv(1)
                state = 'val'
                continue

            if state == 'key':
                key += c
            elif state == 'val':
                val += c

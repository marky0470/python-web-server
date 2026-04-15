import os

class Handler:

    def __init__(self):
        self.routes = {}
        self.build_routes()

    def traverse(self, path):
        s = []
        for p in os.listdir(path):
            if '.' not in p:
                for x in self.traverse(f"{path}/{p}"):
                    s.append(x)
            else:
                s.append(f"{path}/{p}")
        return s
    
    def build_routes(self):
        for path in self.traverse("./public"):
            self.routes[("GET", path[8:])] = (self.serve_file, path)

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
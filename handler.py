class Handler:

    def __init__(self):
        self.routes = {
            ("GET", "/index.html"): (self.serve_file, "files/index.html"),
            ("GET", "/contacts.html"): (self.serve_file, "files/contacts.html"),
            ("GET", "/favicon.ico"): (self.serve_file, "files/favicon.ico"),
            ("GET", "/careers.html"): (self.serve_file, "files/careers.html")
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
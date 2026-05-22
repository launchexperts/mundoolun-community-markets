import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 4173


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionError, socket.error):
            self.close_connection = True


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        pass  # suppress noisy client-abort tracebacks


httpd = Server(("", PORT), Handler)
print(f"Serving (no-cache, threaded) on http://localhost:{PORT}")
httpd.serve_forever()

from http.server import BaseHTTPRequestHandler


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(bytes('[ { "name": "Burgerladen 1", "visitors": 12345, "lastTimestamp": 12345679.1234 }, { "name": "Burgerladen 2", "visitors": 12345, "lastTimestamp": 12345679.1234 }, { "name": "Burgerladen 3", "visitors": 12345, "lastTimestamp": 12345679.1234 } ]', "utf8"))

        return
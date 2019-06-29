from classes.server import Server
from http.server import HTTPServer

print("Run API-Server...")

httpServer = HTTPServer(('127.0.0.1', 8081), Server)
httpServer.serve_forever(poll_interval=0.5)
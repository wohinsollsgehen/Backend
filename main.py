import threading

from classes.server import Server
from http.server import HTTPServer

from classes.input.ttn import InputTTN

print("Start")

class APIThread(threading.Thread):
    def run(self):
        print("Run API-Server...")
        httpServer = HTTPServer(('127.0.0.1', 8081), Server)
        httpServer.serve_forever(poll_interval=0.5)

class InputThread(threading.Thread):
    def run(self):
        print("Run InputTTN...")
        ttnInstance = InputTTN()
        ttnInstance.fetch()

def main():
    api_thread = APIThread()
    api_thread.start()  # ...Start the thread, invoke the run method
    input_thread = InputThread()
    input_thread.start()  # ...Start the thread, invoke the run method

main()

import threading

from classes.server import Server
from http.server import HTTPServer

from classes.input.ttn import InputTTN
from classes.input.library import Library

class APIThread(threading.Thread):
    def run(self):
        print("Run API-Server...")
        httpServer = HTTPServer(('0.0.0.0', 8081), Server)
        httpServer.serve_forever(poll_interval=0.5)

class InputThread(threading.Thread):
    app_id = None
    access_key = None

    def __init__(self, app_id, access_key):
        threading.Thread.__init__(self)

        self.app_id = app_id
        self.access_key = access_key

    def run(self):
        print("Run InputTTN...")
        ttnInstance = InputTTN(self.app_id, self.access_key)
        ttnInstance.fetch()

class LibraryThread(threading.Thread):
    def run(self):
        print("Run Library...")
        library = Library()
        library.fetch()

def main():
    api_thread = APIThread()
    api_thread.start()

    input_thread1 = InputThread("paxcounter_hackaton19", "ttn-account-v2.YNWDg-ti8jPijk-DKl5PCT4ss8TJXyCTBoaMnV1gdy0")
    input_thread1.start()

    input_thread2 = InputThread("paxcounter_heltec_digihub", "ttn-account-v2.rFLbrMlZoaikMgeSmnX-vWNSFkorssZXkw2DSeykY2Y")
    input_thread2.start()

    library = LibraryThread()
    library.start()

main()
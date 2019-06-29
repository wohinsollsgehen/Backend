import sqlite3
from http.server import BaseHTTPRequestHandler
import json
from decimal import Decimal


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        result = {}
        result['locations'] = []

        with sqlite3.connect('data/storage.sqlite3') as connection:
            cursor = connection.cursor()

            cursor.execute('select location.name, location.capacity, location.image, input.value, input.timestamp, max(input.timestamp) from input join location on input.deviceId = location.deviceId and input.source = location.source group by input.source, input.deviceId;')

            for entry in cursor.fetchall():
                resultEntry = {}

                resultEntry['name'] = entry[0]
                resultEntry['capacity'] = entry[1]
                resultEntry['image'] = entry[2]
                resultEntry['pressure'] = str(min(1, Decimal(entry[3]) / Decimal(entry[1])))
                resultEntry['visitors'] = entry[3]
                resultEntry['lastTimestamp'] = entry[4]

                result['locations'].append(resultEntry)

        self.wfile.write(bytes(str(json.dumps(result)), "utf8"))
        return

    def log_message(self, format, *args):
        return
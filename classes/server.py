import sqlite3
from http.server import BaseHTTPRequestHandler
import json


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        result = []

        with sqlite3.connect('data/storage.db') as connection:
            cursor = connection.cursor()

            cursor.execute('select location.name, input.value, input.timestamp, max(input.timestamp) from input join location on input.deviceId = location.deviceId and input.source = location.source group by input.source, input.deviceId;')

            for entry in cursor.fetchall():
                print(entry)
                resultEntry = {}

                resultEntry['name'] = entry[0]
                resultEntry['visitors'] = entry[1]
                resultEntry['lastTimestamp'] = entry[2]

                result.append(resultEntry)

        self.wfile.write(bytes(str(json.dumps(result)), "utf8"))
        return
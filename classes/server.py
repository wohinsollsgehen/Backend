import sqlite3
from http.server import BaseHTTPRequestHandler
import json
from decimal import Decimal
import re
from urllib.parse import unquote


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        result = None
        if self.path == "/locations":
            result = self.loadLocations()
        elif self.path == "/listInputs":
            result = self.loadInputs()

        if result is None:
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(bytes(str(json.dumps(result, indent=4)), "utf8"))
        return

    def do_POST(self):
        regex = re.compile('^/editLocations/(?P<source>[\w\d\s]+)/(?P<deviceId>[\w\d\s]+)$')
        match = regex.search(unquote(self.path))

        if match is None:
            return

        source = match.group("source")
        deviceId = match.group("deviceId")
        name = self.headers['name']
        capacity = self.headers['capacity']
        image = self.headers['image']
        longitude = self.headers['longitude']
        latitude = self.headers['latitude']
        description = self.headers['description']
        informationUrl = self.headers['informationUrl']

        with sqlite3.connect('data/storage.sqlite3') as connection:
                cursor = connection.cursor()

                cursor.execute('SELECT id FROM location where source = \'' + source + '\' and deviceId = \'' + deviceId + '\';')
                result = cursor.fetchall()

                if len(result) == 0:
                    cursor.execute('INSERT INTO location (source, deviceId, name, capacity, image, longitude, latitude, description, informationUrl) VALUES (\'' + source + '\',\'' + deviceId + '\',\'' + name + '\',\'' + capacity + '\',\'' + image + '\',\'' + longitude + '\',\'' + latitude + '\', \'' + description + '\',\'' + informationUrl + '\');') # , description, informationUrl
                else:
                    cursor.execute('UPDATE location SET name = \'' + name + '\', capacity = \'' + capacity + '\', image = \'' + image + '\', longitude = \'' + longitude + '\', latitude = \'' + latitude + '\'  , description = \'' + description + '\', informationUrl = \'' + informationUrl + '\' where id = ' + str(result[0][0]) + ';')

                connection.commit()

        return

    def log_message(self, format, *args):
        return

    def loadLocations(self):
        result = {'locations': []}

        with sqlite3.connect('data/storage.sqlite3') as connection:
            cursor = connection.cursor()

            cursor.execute('select location.name, location.capacity, location.image, input.value, location.longitude, location.latitude, location.description, location.informationUrl, input.timestamp, max(input.timestamp) from input join location on input.deviceId = location.deviceId and input.source = location.source group by input.source, input.deviceId;')

            for entry in cursor.fetchall():
                resultEntry = {}

                resultEntry['name'] = entry[0]
                # resultEntry['capacity'] = entry[1]
                resultEntry['image'] = entry[2]
                resultEntry['pressure'] = float(max(0.1, min(1, Decimal(entry[3]) / Decimal(entry[1]))))
                # resultEntry['visitors'] = int(entry[3])
                resultEntry['longitude'] = entry[4]
                resultEntry['latitude'] = entry[5]
                resultEntry['description'] = entry[6]
                resultEntry['informationUrl'] = entry[7]
                resultEntry['lastTimestamp'] = entry[8]

                result['locations'].append(resultEntry)

        return result

    def loadInputs(self):
        result = []

        with sqlite3.connect('data/storage.sqlite3') as connection:
            cursor = connection.cursor()

            cursor.execute('SELECT DISTINCT source, deviceId FROM input WHERE NOT EXISTS (SELECT 1 from location l where l.source = input.source and l.deviceId = input.deviceId)')

            for entry in cursor.fetchall():
                resultEntry = {}

                resultEntry['source'] = entry[0]
                resultEntry['deviceId'] = entry[1]

                result.append(resultEntry)

        return result
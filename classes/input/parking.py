from classes.input.input import Input
import time
import urllib.request
import re


class Library(Input):
    def fetch(self):
        while True:
            request = urllib.request.Request('https://stadtplan.freiburg.de/viewer/pls/geojson.php?type=16&_=1561821010478')

            try:
				url = "https://stadtplan.freiburg.de/viewer/pls/geojson.php?type=16&_=1561821010478"
					
				json_decode = json.JSONDecoder()  # used to parse json response
				response = urllib.request.urlopen(url)
				response_string = response.read().decode('utf-8')
				data = json_decode.decode(response_string)            
			except Exception as e:
                print(e)
			
					
				

			for row in data["features"]:
				park_name, prozent = [(row["properties"][key])for key in ["park_name", "prozent"]]
				prozent= float(prozent)/100
				geo = row["geometry"]["coordinates"]
				lat = geo[0]
				lnt = geo[1]
				d = dict({'park_name': park_name, 'prozent': prozent, 'lat': lat, "lnt" : lnt})
						 
				
				

                self.storeInput('Parking', park_name, prozent, time.time())
            time.sleep(60)
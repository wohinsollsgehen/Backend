from classes.input.input import Input
import time
import urllib.request
import json


class Parking(Input):
	def fetch(self):
		while True:
			data = None
			try:
				url = "https://stadtplan.freiburg.de/viewer/pls/geojson.php?type=16&_=1561821010478"
					
				json_decode = json.JSONDecoder()  # used to parse json response
				response = urllib.request.urlopen(url)
				response_string = response.read().decode('utf-8')
				data = json_decode.decode(response_string)
			except Exception as e:
				print(e)

			if data is None:
				return

			for row in data["features"]:
				state, park_name, free, capacity = [(row["properties"][key])for key in ["obs_state", "park_name", "obs_free", "obs_max"]]
				geo = row["geometry"]["coordinates"]
				lat = geo[0]
				lnt = geo[1]

				if int(capacity) <= 0:
					continue

				self.storeInput('Parking', park_name, int(capacity) - int(free), time.time())
				self.updateLocation('Parking', park_name, capacity, lnt, lat)
			time.sleep(60)
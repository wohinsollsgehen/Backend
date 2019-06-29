from classes.input.input import Input
import time
import urllib.request
import re


class Library(Input):
    def fetch(self):
        while True:
            request = urllib.request.Request('https://www.ub.uni-freiburg.de/freie-plaetze/')

            try:
                content = urllib.request.urlopen(request).read().decode("utf8")
            except Exception as e:
                print(e)

            regex = re.compile('<div class=\"occupancy-label\">..*?<span class=\"title\">(?P<title>.*?)</span>.*?<div class=\"percentage-bar-container(?P<classes>.*?)>')
            regexOccupancy = re.compile('data-current-usage-percental=\"(?P<occupancy>[\d]+?)\"')
            matches = regex.finditer(content.replace('\n', ''))

            if matches is None:
                print('no match')
                return

            for match in matches:
                title = match.group("title")
                classes = match.group("classes")

                capacity = -1
                if classes.find("data-current-usage-percental"):
                    subMatch = regexOccupancy.search(classes)

                    if subMatch is not None:
                        capacity = int(subMatch.group('occupancy'))

                self.storeInput('Library', title, capacity, time.time())
            time.sleep(60)
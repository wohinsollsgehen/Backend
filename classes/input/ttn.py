from classes.input.input import Input
import time
import ttn
from datetime import datetime


class InputTTN(Input):
    app_id = None
    access_key = None

    def __init__(self, app_id, access_key):
        self.app_id = app_id
        self.access_key = access_key

    def fetch(self):
        def uplink_callback(msg, client):
            format_date = datetime.strptime(msg.metadata.time[:-5], '%Y-%m-%dT%H:%M:%S.%f')
            self.storeInput('TTN', msg.dev_id, msg.payload_fields.wifi, format_date.timestamp())

        handler = ttn.HandlerClient(self.app_id, self.access_key)

        mqtt_client = handler.data()
        mqtt_client.set_uplink_callback(uplink_callback)

        while True:
            mqtt_client.connect()
            time.sleep(60)
            mqtt_client.close()
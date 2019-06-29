from classes.input.input import Input
import time
import ttn
from datetime import datetime


class InputTTN(Input):

    def fetch(self):
        app_id = "paxcounter_hackaton19"
        access_key = "ttn-account-v2.Dc11UJqCIhSMBFdPk-7pMroNJK1jwSBK6vlV9_hV148"

        def uplink_callback(msg, client):
            format_date = datetime.strptime(msg.metadata.time[:-5], '%Y-%m-%dT%H:%M:%S.%f')
            self.storeInput('TTN', msg.dev_id, msg.payload_fields.wifi, format_date.timestamp())

        handler = ttn.HandlerClient(app_id, access_key)

        mqtt_client = handler.data()
        mqtt_client.set_uplink_callback(uplink_callback)

        while True:
            mqtt_client.connect()
            time.sleep(60)
            mqtt_client.close()
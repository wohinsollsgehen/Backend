import sqlite3


class Input(object):
    def fetch(self):
        return None

    def storeInput(self, source, device_id, value, timestamp):
        try:
            with sqlite3.connect('data/storage.sqlite3') as connection:
                cursor = connection.cursor()

                cursor.execute('create table if not exists input (id integer primary key, source text, deviceId text, value text, timestamp timestamp);')
                cursor.execute('INSERT INTO input (source, deviceId, value, timestamp) VALUES (\'' + source + '\',\'' + str(device_id) + '\',\'' + str(value) + '\', ' + str(timestamp) + ');')

                connection.commit()

        except sqlite3.Error as e:
            print(e)

        except Exception as e:
            print(e)

        return None
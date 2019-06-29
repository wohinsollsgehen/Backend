import sqlite3


class Input(object):
    db = None

    def __init__(self):
        pass

    def __enter__(self):
        # self.db = sqlite3.connect('data/storage', check_same_thread=False)
        #
        # cursor = self.db.cursor()
        # cursor.execute('create table if not exists input (id integer primary key, source text, deviceId text, value text, timestamp timestamp)')
        #
        # self.db.commit()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # self.db.close()

        return None

    def fetch(self):
        return None

    def storeInput(self, source, device_id, value, timestamp):

        print(source, device_id, value, timestamp)

        try:
            with sqlite3.connect('data/storage') as connection:
                cursor = connection.cursor()
                cursor.executescript('INSERT INTO input (source, deviceId, value, timestamp) VALUES (\'TTN\',\'14\',\'8977\', \'1561790952.80474\');')
                connection.commit()

        except sqlite3.Error as e:
            print(e)

        except Exception as e:
            print(e)

# cursor.executescript('INSERT INTO input (source, deviceId, value, timestamp) VALUES (\'' + source + '\',\'' + str(device_id) + '\',\'' + str(value) + '\', ' + str(timestamp) + ');')

        # cursor.execute("insert into input (source, deviceId, value, timestamp) values (?, ?, ?, ?)", (source, device_id, value, timestamp))



        print('executed')
        #
        # self.db.commit()
        #
        # print('commited')

        return None
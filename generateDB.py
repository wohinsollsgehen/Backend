import sqlite3

with sqlite3.connect('data/storage.sqlite3') as connection:
    cursor = connection.cursor()

    cursor.execute('create table input (id integer primary key, source text, deviceId text, value text, timestamp timestamp);')
    connection.commit()

    cursor.execute('create table location (id integer primary key, source text, deviceId text, name text, capacity integer, image text, longitude REAL, latitude REAL, description text, informationUrl text, state BOOLEAN);')
    connection.commit()
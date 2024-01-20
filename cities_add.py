import json
import sqlite3

connection = sqlite3.connect("cities.db")
cursor = connection.cursor()

with open('city_list.json', 'r') as file:
    cities = json.load(file)
    for city in cities:
        if city["state"] == "":
            cursor.execute(
                "INSERT INTO cities (city_id, name, country, lon, lat) VALUES (?, ?, ?, ?, ?)",
                (city["id"], city["name"], city["country"], city["coord"]["lon"], city["coord"]["lat"])
                )
        else:
            cursor.execute(
                "INSERT INTO cities (city_id, name, state, country, lon, lat) VALUES (?, ?, ?, ?, ?, ?)",
                (city["id"], city["name"], city["state"], city["country"], city["coord"]["lon"], city["coord"]["lat"])
                )
        print(city)
    connection.commit()
    connection.close()

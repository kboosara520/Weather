import json
import sqlite3

connection = sqlite3.connect("cities.db")
cursor = connection.cursor()

with open('city_list.json', 'r') as file:
    cities = json.load(file)
    for city in cities:
        print(city['name'])
        print(city['country'])
        if city["state"] == "":
            cursor.execute(
                "UPDATE cities SET name_string = ? WHERE city_id = ?",
                ((city['name'] + ',' + city['country']).replace(' ',''), city['id'])
            )
        else:
            cursor.execute(
                "UPDATE cities SET name_string = ? WHERE city_id = ?",    
                ((city['name'] + ',' + city['state'] + ',' + city['country']).replace(' ',''), city['id'])
            )
        print(city['name'] + ', ' + city['country'])
    connection.commit()
    connection.close()
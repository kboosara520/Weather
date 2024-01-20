import requests
import sqlite3

from json import dumps
from flask import session, redirect
from functools import wraps


def lookup(city_info, mode):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    
    """with open('api_key.txt', 'r') as file:
        API_KEY = file.read()"""
    API_KEY = "7ec2f457866ea045b50482af4a375541"

    if mode == "id":
        url = f"{BASE_URL}&id={city_info}&units=metric&APPID={API_KEY}"
    elif mode == "coords":
        url = f"{BASE_URL}&lat={city_info[0]}&lon={city_info[1]}&units=metric&APPID={API_KEY}"

    response = requests.get(url).json()
    return response


def format(cities, cursor):
    print(cursor)
    if cities is ():
        result = []
    else:
        print(cursor.description)
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, city)) for city in cities]
    return dumps(result)


def get_saved_cities():
    connection = sqlite3.connect("cities.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (session["user_id"],)
    )

    user_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT cities.city_id, cities.name, cities.state, cities.country FROM cities INNER JOIN favorites ON cities.city_id = favorites.city_id AND favorites.user_id = ?",
        (user_id,)
    )

    saved_cities = cursor.fetchall()

    return saved_cities


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

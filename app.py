import time
import sqlite3

from flask import Flask, render_template, redirect, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import lookup, format, login_required, get_saved_cities

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response"""


@app.route("/")
def index():
    if session.get("user_id") is None:
        logged_in = False
        saved_cities = []
    else:
        logged_in = True
        saved_cities = get_saved_cities()
    print(saved_cities) 
    return render_template("index.html", logged_in=logged_in, saved_cities=saved_cities)


@app.route("/search")
def search():
    connection = sqlite3.connect("cities.db")
    cursor = connection.cursor()
    city = request.args.get("city")
    print(city)
    LIMIT = 10

    if city:
        cursor.execute(
            "SELECT * FROM cities WHERE name_string LIKE ? LIMIT ?", 
            ("%" + city + "%", LIMIT)
            )
        cities = cursor.fetchall()
        
    else:
        cities = ()

        """cities = []"""

    connection.close()
        
    return format(cities, cursor)


@app.route("/saved_cities")
@login_required
def saved_cities():
    connection = sqlite3.connect("cities.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (session["user_id"],)
    )

    user_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT * FROM cities INNER JOIN favorites ON cities.city_id = favorites.city_id AND favorites.user_id = ?",
        (user_id,)
    )
    saved_cities = format(cursor.fetchall(), cursor)
    connection.close()
    return saved_cities


@app.route("/city")
def city():
    id = request.args.get("id")
    lat = request.args.get("lat")
    lon = request.args.get("lon")


    if id and not (lat and lon):
        response = lookup(id, "id")
    elif (lat and lon) and not id:
        response = lookup((lat, lon), "coords")
    
    city_id = response["id"]

    timezone = int(response['timezone'] / 3600)

    sunrise_time = time.gmtime(response['sys']['sunrise'] + response['timezone'])
    sunset_time = time.gmtime(response['sys']['sunset'] + response['timezone'])

    if timezone > 0:
        timezone = f"+{timezone}"

    items = [
        f"Coordinates(latitude, longitude): {response['coord']['lat']}, {response['coord']['lon']}",
        f"Weather: {response['weather'][0]['main']}, {response['weather'][0]['description']}",
        f"Temperature: {response['main']['temp']}°C",
        f"Feels like: {response['main']['feels_like']}°C",
        f"High: {response['main']['feels_like']}°C, Low: {response['main']['temp_min']}°C",
        f"Humidity: {response['main']['humidity']}%",
        f"Pressure: {response['main']['pressure']} hPa",
        f"Wind speed: {response['wind']['speed']} m/s, Direction: {response['wind']['deg']}°",
        f"Sunrise: {time.strftime('%H:%M', sunrise_time)}",
        f"Sunset: {time.strftime('%H:%M', sunset_time)}",
        f"Timezone: {timezone}"
    ]

    # Check if the user already saved the city
    if session.get("user_id") is None:
        logged_in = False
        disabled_att = "disabled"
        color = "btn-dark"
    else:
        logged_in = True
        connection = sqlite3.connect("cities.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (session["user_id"],)
        )

        user_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT city_id FROM favorites WHERE user_id = ?",
            (user_id,)
        )

        city_list = [city[0] for city in cursor.fetchall()]

        if city_id in city_list:
            color = "btn-dark"
            save = "Unsave"
        else:
            color = "btn-light"
            save = "Save"

        connection.close()

    if session.get("user_id") is None:
        disabled_att = "disabled"
        logged_in = False
        saved_cities = []
        save = ""
    else:
        disabled_att = ""
        logged_in = True
        saved_cities = get_saved_cities()  

    return render_template(
        "city.html", city=response["name"], items=items, button=city_id, save=save,
        color=color, logged_in=logged_in, saved_cities=saved_cities, disabled_att=disabled_att)


@app.route("/save")
@login_required
def save():
    city_id = request.args.get("city_id")
    connection = sqlite3.connect("cities.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (session["user_id"],)
        )

        user_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO favorites (user_id, city_id) VALUES (?, ?)",
            (user_id, city_id)
        )
        connection.commit()
        connection.close()
        return jsonify({'message': 'OK'}), 200
    
    except:
        print("failed")
        connection.close()
        return jsonify({'error': 'Failed to save data'}), 500
    

@app.route("/unsave")
@login_required
def unsave():
    city_id = request.args.get("city_id")
    connection = sqlite3.connect("cities.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (session["user_id"],)
        )

        user_id = cursor.fetchone()[0]

        cursor.execute(
            "DELETE FROM favorites WHERE user_id = ? AND city_id = ?",
            (user_id, city_id)
        )
        connection.commit()
        connection.close()
        return jsonify({'message': 'OK'}), 200
    
    except:
        print("failed")
        connection.close()
        return jsonify({'error': 'Failed to save data'}), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = sqlite3.connect("cities.db")
        cursor = connection.cursor()

        try:
            if not username or not password:
                render_template("error.html", message="invalid login credentials")

            cursor.execute(
                "SELECT username, hash FROM users WHERE username = ?",
                (username,)
            )

            rows = cursor.fetchall()

            if len(rows) != 1 or not check_password_hash(rows[0][1], password):
                return render_template("error.html", message="invalid login credentials")
            
            session["user_id"] = rows[0][0]
            print(session["user_id"])
            connection.close()

        except:
            connection.close()
            return render_template("error.html", message="Database error")
        
        return redirect("/")        

    else:
        return render_template("login.html")


@login_required
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not (username and password and confirmation):
            return render_template("error.html", message="must enter all fields")
        elif not password == confirmation:
            return render_template("error.html", message="passwords do not match")
        
        connection = sqlite3.connect("cities.db")
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT username FROM users")
            usernames = [tuple[0] for tuple in cursor.fetchall()]

            if username in usernames:
                return render_template("error.html", message="username already exists")
            
            cursor.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            connection.commit()
            connection.close()
        
        except:
            connection.close()
            return render_template("error.html", message="Database error")

        return redirect("/login")
    
    else:
        return render_template("register.html")


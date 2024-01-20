# Weather
#### Video Demo:  https://youtu.be/IbIy9I1BVts
#### Description:

Hello, This is Weather. It is a web application for finding weather information of cities. It uses python, SQL, HTML, CSS, Javasript, and Flask as the framework.

#### Main directory

In the main directory, you'll see
* `static/`
* `templates/`
* `app.py`
* `helpers.py`
* `cities.db`
* `city_list.json`
* `cities_add.py`
* `cities_name_string.py`
* `requirements.txt`
* `README.md`

In `app.py`, you'll see 9 functions. 
* `index` takes care of the index page and pass into Jinja a boolean value depending on if a user is logged in or not
* `search` takes care of the autocomplete in the search bar of the website
* `saved_cities` returns the list of all the cities the current user has saved to the client's Javascript code
* `city` gets the weather data from `lookup`, formats the data into a list of strings, and renders the city.html page
* `save` get's called asynchronously by the client's Javascript and saves the current city to the database
* `unsave` get's called asynchronously by the client's Javascript and deletes the current city from the database
* `login` renders the page that the user uses to log in by checking the username and the hashed password
* `logout` logs the user out, and redirects the user back to the index page
* `register` creates a new account and stores the user name and the hashed password into the database

In `helpers.py`, you'll see 4 function.
* `lookup` takes in an integer and a string, or a tuple and a string. The string is used to determine the method of requesting the api(either using the city id or using coordinates). It gets the weather data from openweathermap.org via their API and returns the weather data of that city as a list of dictionaries.
* `format` takes in the result of the query to the database in the form of a tuple and converts it to json to send the information to the browser.
* `get_saved_cities` queries the database and returns a list of city that the user has saved in the form of tuples
* `login_required` decorates the routes that require the users to log in before accessing the page

`city_list.json` is the data of every available city including, id, name, state(if applicable), country, and coordinates. The file is obtained from http://bulk.openweathermap.org/sample/city.list.json.gz.

#### `cities.db` 
contains 3 tables 
* `cities` has an id, name, state(for countries in USA), country, name_string(for seaching purposes), latitude, and longtitude for each city in the table. The data in the table is retrieved from http://bulk.openweathermap.org/sample/city.list.json.gz and formatted using `cities.py`
* `users` contains an id, a username, and a hashed password for each registered user
* `favorites` contains a user_id and city_id for each city the user has saved

`cities_add.py` contains the code that I used to add the cities in `city_list.json` into the database.

`cities_name_string.py` contains the code that I used to add each city's name string into the name_string column.

#### templates directory

In this directory, you'll see 7 files:
* `layout.html` is the basic layout. It contains a search bar, a div for the dropdown auto complete for the search, the buttons for log in and register, or log out and a button for the dropdown containing the user's saved cities.
* `layout2.html` is the layout for the log in or the register page
* `index.html` is the main page
* `city.html` is the page that displays the weather data for each city. If the user is logged in, there will be a button to save the city
* `login.html` is the page that contains the form to log in
* `register.html` is the page that contains the form to register a new account
* `error.html` is the page that gets rendered when the user fails to comply with the login or the register restrictions

#### static directory

In this directory, you'll see 1 file and 2 directories
* `styles.css` contains the majority of my own custom styling

##### images

This directory contains all the background images

##### js

In this directory, you'll see 4 JavaScript files:
* `auto_complete.js` contains the code that communicates with the server and handles the auto complete part of the search bar
* `background_image.js` contains the code that changes the background image depending on the time of day
* `location.js` contains the code that searches the city based on the user's coordinates using the geolocation API
* `favorites.js` contains the code that asynchronously saves or unsaves, and updates the list of the saved cities to be up to date with the database

In `requirements.txt` you'll see all the python libraries you need to install to be able to run this web app
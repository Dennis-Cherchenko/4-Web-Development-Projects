import os, requests, json

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv('DATABASE_URL'):
    raise RuntimeError('DATABASE_URL is not set')

# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set up database
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    if 'user_object' in session:
        #load main page
        return render_template('index.html', user_object = session["user_object"], location_object = None)
    else:
        #load log in/register page
        return render_template('login.html', user_object = None)



@app.route('/register', methods = ['POST'])
def register():

    if request.method == 'POST':

        username = request.form.get("username")
        usernameAlreadyExists = db.execute("SELECT username FROM users WHERE username = '" + username + "'").fetchone()

        if usernameAlreadyExists:
            return render_template('login.html', user_object = None)
        else:
            session.pop('user_object', None)
            password = request.form.get("password")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")

            db.execute("INSERT INTO users (username, password, first_name, last_name) VALUES ('" + username + "', '" + password + "', '" + first_name+ "', '"+ last_name + "');")
            db.execute("COMMIT;")
            session['user_object'] = db.execute("SELECT * FROM users WHERE username='"+ username +"' AND password ='" + password + "'").fetchone()

            return render_template('index.html', user_object = session['user_object'])


@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        rf = request.form
        username = rf.get("username")
        password = rf.get("password")
        user_object = db.execute("SELECT * FROM users WHERE username='"+ username +"' AND password ='" + password + "'").fetchone()

        if user_object is None:
            return render_template('login.html', user_object = None)
        else:
            session['user_object'] = user_object
            return render_template('index.html', user_object = user_object)



@app.route('/logout', methods = ['GET'])
def logout():
    if session['user_object'] is not None:
        session.pop('user_object', None)
    return render_template('login.html', user_object = None)

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        rf = request.form
        search_item = rf.get("search_item")

        results_object = db.execute("SELECT * FROM locations WHERE zip_code iLIKE '%" + search_item + "%' OR city iLIKE '%" + search_item + "%';").fetchall()
        if results_object is None or len(results_object) != 1:
            return render_template('location.html', user_object = session['user_object'], location_object = None, results_object = results_object)
        else:
            weather_data = json.loads(json.dumps(requests.get("https://api.darksky.net/forecast/7fe0732f8aa00cef25aca8605126fcb6/42.37,-71.11").json()["currently"], indent = 2))
            session['location_object'] = results_object[0]
            return render_template('location.html', user_object = session['user_object'], location_object = session['location_object'] , weather_data = weather_data, results_object = None)


@app.route('/location', methods = ['GET', 'POST'])
def location():
    if request.method == 'GET':
        weather_data = getWeather(location_data.latitude, location_data.longitude)
        return render_template('location.html', user_object = session['user_object'], location_object = session['location_object'] , weather_data = weather_data)

    if request.method == 'POST':
        if request.form.get('zip_code') is not None:
            results_object = db.execute("SELECT * FROM locations WHERE zip_code iLIKE '%" + request.form.get('zip_code') + "%';").fetchall()
            session['location_object'] = results_object[0]
            weather_data = json.loads(json.dumps(requests.get("https://api.darksky.net/forecast/7fe0732f8aa00cef25aca8605126fcb6/42.37,-71.11").json()["currently"], indent = 2))
            return render_template('location.html', user_object = session['user_object'], location_object = session['location_object'] , weather_data = weather_data, results_object = None)

        if request.form.get("review") is not None:
            db.execute("UPDATE locations SET review = '" + request.form.get("review") + "' WHERE location_id = '" + str(session['location_object']['location_id']) + "';")
            db.execute("COMMIT;")
            session_object = db.execute("SELECT * FROM locations WHERE location_id =" + str(session['location_object']['location_id']))
            weather_data = json.loads(json.dumps(requests.get("https://api.darksky.net/forecast/7fe0732f8aa00cef25aca8605126fcb6/42.37,-71.11").json()["currently"], indent = 2))
            return render_template('location.html', user_object = session['user_object'], location_object = session['location_object'] , weather_data = weather_data, results_object = None)


@app.route('/api/', methods = ['GET'])
def api():
    if request.method == 'GET':
        print('YOU HAVE SUCCESSFULLY GOTTEN THE ZIP')


def getWeather(latitude, longitude):
    return json.loads(json.dumps(requests.get("https://api.darksky.net/forecast/7fe0732f8aa00cef25aca8605126fcb6/"+ latitude +","+ longitude).json()['currently'], indent = 2))



import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from user_models import db, connect_db, User
from game_models import *
from playlog_models import *
import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///boardgames'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

BASE_URL = 'https://api.boardgameatlas.com/api'
client_id = 'XlXxjnv76F'

connect_db(app)



@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/search_results')
def show_search():
    query = request.args['search']
    resp = requests.get(f'{BASE_URL}/search',
                params={'fuzzy_,match': 'true', 'limit': 30, 'client_id': client_id, 'name': query})
    data = resp.json()
    return render_template('search.html', data=data, query=query)
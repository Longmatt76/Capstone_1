import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from user_models import db, connect_db, User
from game_models import *
from playlog_models import *
from forms import UserAddForm, UserEditForm, LoginForm
import requests
from flask_sqlalchemy import Pagination
from bs4 import BeautifulSoup
from functions import remove_tags

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


# **user routes signin and signup**


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle login of user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f'Welcome back {user.username}', 'success')
            return redirect('/')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have successfully logged out")

    return redirect('/')


@app.route('/users/<int:user_id>/profile')
def show_user_profile(user_id):
    """displays the user profile info"""

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)


@app.route('/users/<int:user_id>/update', methods=["GET", "POST"])
def profile(user_id):
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.header_image_url = form.header_image_url.data or "/static/images/boardgame_header.jpeg"

            db.session.commit()
            return redirect(f"/users/{user.id}/profile")
        flash("Access unauthorized, please reenter password", "danger")

    return render_template('users/update.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["DELETE"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


# **home and search routes**

@app.route('/')
def show_home():
    '''displays the homepage'''
    return render_template('home.html')


@app.route('/search')
def show_search():
    '''queries the API with the search request and displays the results'''

    query = request.args['search']
    resp = requests.get(f'{BASE_URL}/search',
                        params={'fuzzy_match': 'true', 'limit': 30, 'client_id': client_id, 'name': query})
    data = resp.json()
    return render_template('search.html', data=data, query=query)


@app.route('/search/<string:api_id>/game_details')
def show_game(api_id):
    '''Using the api's id for the clicked on game it queries the API three times
    (for game details,images, and videos)and displays that games details page 
    parsing out the html tags from the api data'''

    resp = requests.get(f'{BASE_URL}/search',
                        params={'client_id': client_id, 'ids': api_id})
    data = resp.json()
    
    soup = remove_tags(data['games'][0]['description'])

    resp2 = requests.get(f'{BASE_URL}/game/images',
                        params={'pretty': 'true', 'client_id': client_id, 'limit':50, 'game_id': api_id })
        
    images = resp2.json()

    resp3 = requests.get(f'{BASE_URL}/game/videos',
                        params={'pretty': 'true', 'client_id': client_id, 'limit':50, 'game_id': api_id })
    
    videos = resp3.json()

    return render_template('games/details.html', data=data, soup=soup, 
                           images=images, videos=videos)




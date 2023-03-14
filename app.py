import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from user_models import db, connect_db, User
from game_models import GameCollection, Wishlist
from playlog_models import Playlog, Player, Playthrough
from forms import UserAddForm, UserEditForm, LoginForm, DeleteUserForm
import requests
from flask_sqlalchemy import Pagination
from functions import average, get_categories, get_mechanics


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

# get_mechanics()
# get_categories()

# *******************************routes for signup, logging in, logging out******************************


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
            flash(f'Welcome back {user.username}', 'info')
            return redirect('/')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have successfully logged out", 'info')

    return redirect('/')


# *******************************basic user routes, view profile, edit profile****************************
# **********************************view collection, and delete user*****************************************


@app.route('/users/<int:user_id>/profile')
def show_user_profile(user_id):
    """displays the user profile info"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

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
            user.header_image_url = form.header_image_url.data or "/static/images/boardgame_shelf.png"

            db.session.commit()
            return redirect(f"/users/{user.id}/profile")
        flash("Access unauthorized, please reenter password", "danger")

    return render_template('users/update.html', form=form, user_id=user.id)


@app.route('/users/<int:user_id>/game_collection')
def show_game_collecion(user_id):
    """show a users collection"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template('/users/collection.html', user=user)


@app.route('/users/<int:user_id>/delete', methods=["GET", "POST"])
def delete_user(user_id):
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user

    """removes the games in a users game collection before removing the user, this was necessary do to 
       the use of composite keys"""
    games_to_delete = GameCollection.query.filter(
        GameCollection.user_id == user.id).all()
    for game in games_to_delete:
        db.session.delete(game)
    db.session.commit()

    form = DeleteUserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(form.username.data, form.password.data):
            do_logout()
            db.session.delete(user)
            db.session.commit()
            flash('Sorry to see you go, rejoin anytime!', 'success')
        return redirect('/')

    flash('Please verify your credentials and click "Self Destruct" if you really want to go', 'danger')
    return render_template('users/delete.html', form=form)


# *************************************basic game routes, add game, remove game,*******************************
# *************************************edit game rating, edit game comments************************************


@app.route('/games/add_game/<string:api_id>')
def add_game(api_id):
    """ adds game to the collective games db and then to the user's game_collection, if game already
    exists in the games db then it just adds it to the users collection"""

    if not g.user:
        flash("You must be logged in to add a game to your collection, please login or signup", "info")
        return redirect("/login")

    resp = requests.get(f'{BASE_URL}/search',
                        params={'client_id': client_id, 'ids': api_id})
    data = resp.json()

    added_game = GameCollection(user_id=g.user.id, game_id=api_id, name=data['games'][0]['name'],
                                thumb_url=data['games'][0]['thumb_url'])

    db.session.add(added_game)
    db.session.commit()

    return redirect(f'/users/{g.user.id}/game_collection')


@app.route('/games/remove_game/<string:game_id>')
def remove_game(game_id):
    """removes a game from a users collection and 
    returns them to the updated collection page"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user_id = g.user.id
    game_to_remove = GameCollection.query.get((user_id, game_id))
    db.session.delete(game_to_remove)
    db.session.commit()

    return redirect(f'/users/{g.user.id}/game_collection')


@app.route('/games/edit_rating/<string:game_id>', methods=['POST'])
def edit_rating(game_id):
    """edits a users game info for games in their game collection"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    game = GameCollection.query.get((g.user.id, game_id))

    game.rating = request.form['rating']
    db.session.commit()
    return render_template('users/collection.html')


@app.route('/games/edit_comments/<string:game_id>', methods=['POST'])
def edit_comments(game_id):
    """edits a users game info for games in their game collection"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    game = GameCollection.query.get((g.user.id, game_id))

    game.comments = request.form['comment']
    db.session.commit()
    return render_template('users/collection.html')


@app.route('/games/value_game/<string:game_id>', methods=['GET'])
def get_value(game_id):
    """checks the api for recent used sales prices and averages them"""

    resp = requests.get(f'{BASE_URL}/game/prices',
                        params={'pretty': 'true', 'game_id': game_id, 'client_id': client_id})
    
    data = resp.json()
    prices = []
    for num in range(len(data['gameWithPrices']['used'])):
        prices.append(data['gameWithPrices']['used'][num]['price'])

    avg = average(prices)
    rnd_avg = round(avg,2)
    
    game = GameCollection.query.get((g.user.id, game_id))
    game.used_value = rnd_avg
    db.session.commit()
    
    return redirect(f'/users/{g.user.id}/game_collection')


# **********************************home route and search routes****************************************


@app.route('/')
def show_home():
    '''displays the homepage'''
    return render_template('home.html')


@app.route('/search')
def show_search(start=0,per_page=30):
    '''queries the API with the search request and displays the results'''
    query = request.args['search']
    resp = requests.get(f'{BASE_URL}/search',
                        params={'fuzzy_match': 'true', 'limit': per_page, 'offset': start, 'client_id': client_id, 'name': query})
    data = resp.json()

    return render_template('search.html', data=data, query=query)


@app.route('/search/<string:api_id>/game_details')
def show_game(api_id):
    '''Using the api's id for the clicked on game it queries the API three times
    (for game details,images, and videos) then displays that games details page 
    parsing out the html tags from the api data'''

    # if g.user:
    #     ids = [g.user.games.game_id for game in g.user.games]

    resp = requests.get(f'{BASE_URL}/search',
                        params={'client_id': client_id, 'ids': api_id})
    data = resp.json()

    resp2 = requests.get(f'{BASE_URL}/game/images',
                         params={'pretty': 'true', 'client_id': client_id, 'limit': 50, 'game_id': api_id})

    images = resp2.json()

    resp3 = requests.get(f'{BASE_URL}/game/videos',
                         params={'pretty': 'true', 'client_id': client_id, 'limit': 50, 'game_id': api_id})

    videos = resp3.json()

    return render_template('games/details.html', data=data,
                           images=images, videos=videos)




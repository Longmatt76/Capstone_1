"""SQLAlchemy models for boardgame collection app"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,)

    email = db.Column(db.Text,
                      nullable=False,
                      unique=True,)

    username = db.Column(db.Text,
                         nullable=False,
                         unique=True,)

    image_url = db.Column(db.Text,
                          default="/static/images/default-pic.png",)

    header_image_url = db.Column(db.Text,
                                 default="/static/images/boardgame_header.jpeg")

    password = db.Column(db.Text,
                         nullable=False,)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    gamelogs = db.relationship('Gamelog',
                               backref='users')

    games = db.relationship('Game',
                            secondary='collections',
                            backref='users')

    wishes = db.relationship('Game',
                             secondary='wishes',
                             backref='users')

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password If can't find matching user
          (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Game(db.Model):
    """stores detailed game data in the db"""

    __tablename__ = 'games'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,)

    api_handle = db.Column(db.Text,
                           nullable=False,
                           unique=True,)

    name = db.Column(db.Text,
                     nullable=False,
                     unique=True,)

    year_published = db.Column(db.Integer)

    description = db.Column(db.Text)

    thumb_url = db.Column(db.Text)

    image_url = db.Column(db.Text)

    categories = db.Column(db.ARRAY)

    mechanics = db.Column(db.ARRAY)

    primary_designer = db.Column(db.Text)

    players = db.Column(db.Text)

    playtime = db.Column(db.Text)

    rules_url = db.Column(db.Text)

    offical_url = db.Column(db.Text)

    estimated_value = db.Column(db.Integer)

    def __repr__(self):
        return f"<Game #{self.id}: {self.api_handle}, {self.name}>"


class Mechanic(db.Model):
    """stores the api data for a games mechanics"""

    __tablename__ = "mechanics"

    id = db.Column(db.Text,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

    url = db.Column(db.Text)


class Category(db.Model):
    """stores the api data for a games categories"""

    __tablename__ = "categories"

    id = db.Column(db.Text,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False)

    url = db.Column(db.Text)


class Collection(db.Model):
    """stores the games in a users collection"""

    __tablename__ = "collections"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True,)

    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        primary_key=True,)


class Gamelog(db.Model):
    """stores a users gamelogs for game playthroughs"""

    __tablename__ = "gamelogs"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,)

    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        nullable=False,)

    date_of_playthrough = (db.Date)

    player_count = db.Column(db.Integer,
                             nullable=False)

    player_one_name = db.Column(db.Text,
                                default='N/A')

    player_two_name = db.Column(db.Text,
                                default='N/A')

    player_three_name = db.Column(db.Text,
                                  default='N/A')

    player_four_name = db.Column(db.Text,
                                 default='N/A')

    player_five_name = db.Column(db.Text,
                                 default='N/A')

    player_one_score = db.Column(db.Integer,
                                 default=0)

    player_two_score = db.Column(db.Integer,
                                 default=0)

    player_three_score = db.Column(db.Integer,
                                   default=0)

    player_four_score = db.Column(db.Integer,
                                  default=0)

    player_five_score = db.Column(db.Integer,
                                  default=0)

    notes = db.Column(db.Text)


class Wishlist(db.Model):
    '''stores games in a users wishlist'''

    __tablename__ = "wishes"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True,)

    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        primary_key=True,)

    subscribe_price_alerts = db.Column(db.Boolean,
                                       default=False)

    price_alert_trigger = db.Column(db.Integer)


def connect_db(app):
    """Connect this database to provided Flask app. """

    db.app = app
    db.init_app(app)

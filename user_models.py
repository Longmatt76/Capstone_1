"""SQLAlchemy user models for the Boardgame Shelf"""

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

    username = db.Column(db.String(25),
                         nullable=False,
                         unique=True,)

    image_url = db.Column(db.Text,
                          default="/static/images/default-pic.png",)

    header_image_url = db.Column(db.Text,
                                 default="/static/images/boardgame_shelf.png")

    password = db.Column(db.Text,
                         nullable=False,)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    playlogs = db.relationship('Playlog',
                               backref='users')

    games = db.relationship('GameCollection',
                               backref='users')

    wishes = db.relationship('Wishlist',
                             backref='users_wishes')

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




def connect_db(app):
    """Connect this database to provided Flask app. """

    db.app = app
    db.init_app(app)

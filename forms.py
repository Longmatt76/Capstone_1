from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired



class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    """Form for editing users"""

    username = StringField('Username:')
    email = StringField('E-mail:',validators= [Email()])
    image_url = StringField('Image URL:')
    header_image_url = StringField('Header Image Url:')
    password = PasswordField('Password:', validators=[Length(min=6)])



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class DeleteUserForm(FlaskForm):
    '''confirms a users creditials before deleting acct'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditWishForm(FlaskForm):
    """form for editing wishlish data"""
    subscribe_price_alerts = BooleanField('Submit checked box to subscribe or unchecked box to unsubscribe:')
    price_alert_trigger = IntegerField("Set price target in dollar amount:")


class AddPlaylogForm(FlaskForm):
    """form to add playlogs"""
    player_count = SelectField('Number of Players:', coerce=int, choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)])
    date_of_playthrough= DateField("Date Played:")
    location = StringField('Location:')
    notes = TextAreaField('Notes:', validators=[Length(max=140)])
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from web.models import User

# registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # ToDo: Add validator to check for @uni only emails
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # TODO add later
    #remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
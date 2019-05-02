from wtforms import *
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.data_required()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', [validators.data_required()], render_kw={"placeholder": "Passphrase"})
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.data_required()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8)
    ])
    confirm = PasswordField('Repeat Password', [validators.data_required()])
    submit = SubmitField('Submit')


class MakeThreadForm(FlaskForm):
    title = StringField('Title', [validators.data_required()], render_kw={"placeholder": "Title"})
    body = StringField('Body', render_kw={"placeholder": "Description"})
    submit = SubmitField('Make Thread!')



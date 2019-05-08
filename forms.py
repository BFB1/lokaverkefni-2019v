from wtforms import *
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.data_required()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', [validators.data_required()], render_kw={"placeholder": "Passphrase"})
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.data_required()], render_kw={"placeholder": "Username"})
    realName = StringField('Name', [validators.data_required()], render_kw={"placeholder": "Name"})
    email = EmailField('Email', [validators.data_required(), validators.email()], render_kw={"placeholder": 'Email'})
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8)
    ], render_kw={"placeholder": "Passphrase"})
    confirm = PasswordField('Repeat Password', [validators.data_required()],
                            render_kw={"placeholder": "Repeat Passphrase"})
    submit = SubmitField('Submit')


class MakeThreadForm(FlaskForm):
    title = StringField('Title', [validators.data_required()], render_kw={"placeholder": "Title"})
    description = StringField('Body', render_kw={"placeholder": "Description"})
    submit = SubmitField('Make Thread!')


class MakeCommentForm(FlaskForm):
    body = StringField('Body', render_kw={"placeholder": "Speak your mind!"})
    submit = SubmitField('Post comment!')



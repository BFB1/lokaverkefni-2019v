from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from model import *
from forms import *
from os import environ

app = Flask(__name__)
app.config.from_object(environ['APP_SETTINGS'])

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('threads.html')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def auth():

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Account.query.filter_by(username=login_form.username.data).first()
        if user is not None:
            if login_form.password.data == user.password:
                login_user(user)
                return redirect('/')

    return render_template('auth.html', form=login_form, failed=True if request.method == 'POST' else False)


if __name__ == '__main__':
    app.run()

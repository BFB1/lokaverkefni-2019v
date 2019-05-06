from flask import Flask, render_template, request, redirect, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from model import *
from forms import *
from os import environ

app = Flask(__name__)
app.config.from_object(environ['APP_SETTINGS'])

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    for i in Account.query.all():
        if i.get_id() == user_id:
            return i
    return None


@app.route('/', methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated:
        thread_form = MakeThreadForm()

        if thread_form.validate_on_submit():
            db.session.add(Thread(title=thread_form.title.data, description=thread_form.body.data,
                                  accountId=current_user.get_id()))
            db.session.commit()

        return render_template('threads.html', data=db.session.query(Thread).join(Account).all(), form=thread_form)
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


@app.route('/thread/<thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    try:
        data = Thread.query.filter_by(id=thread_id).first()
    except SQLAlchemyError:
        abort(404)
        return

    comment_form = MakeCommentForm()
    if comment_form.validate_on_submit():
        db.session.add(Comment(body=comment_form.body.data, accountId=current_user.get_id(), threadId=thread_id))
        db.session.commit()

    return render_template('thread.html', thread=data, form=comment_form)




if __name__ == '__main__':
    app.run()

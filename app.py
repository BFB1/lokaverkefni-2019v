from flask import Flask, render_template, request, redirect, abort, url_for
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
            db.session.add(Thread(title=thread_form.title.data, description=thread_form.description.data,
                                  accountId=current_user.get_id()))
            db.session.commit()

        return render_template('threads.html',
                               data=db.session.query(Thread).join(Account).all()[::-1],
                               form=thread_form)
    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Account.query.filter_by(username=login_form.username.data).first()
        if user is not None:
            if login_form.password.data == user.password:
                login_user(user)
                return redirect('/')
    return render_template('auth.html', form=login_form, failed=True if request.method == 'POST' else False)


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        try:
            user = Account(username=register_form.username.data, name=register_form.realName.data,
                           email=register_form.email.data, password=register_form.password.data)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            return render_template('auth.html', form=register_form, register=True, failed=True)
        login_user(user)
        return redirect('/')
    return render_template('auth.html', form=register_form, register=True, failed=False)


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
        data.timeModified = func.now()
        db.session.commit()

    return render_template('thread.html', thread=data, form=comment_form)


@app.route('/thread/<thread_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_thread(thread_id):
    try:
        data = Thread.query.filter_by(id=thread_id).first()
    except SQLAlchemyError:
        abort(404)
        return
    if (current_user.admin or current_user.id == data.owner.id) and data:
        edit_form = MakeThreadForm(obj=data)
        if edit_form.validate_on_submit():
            data.title = edit_form.title.data
            data.description = edit_form.description.data
            db.session.commit()
            return redirect(url_for('thread', thread_id=data.id))
        return render_template('edit_thread.html', form=edit_form)


@app.route('/thread/<thread_id>/delete')
@login_required
def delete_thread(thread_id):
    try:
        data = Thread.query.filter_by(id=thread_id).first()
    except SQLAlchemyError:
        abort(404)
        return
    if (current_user.admin or current_user.id == data.owner.id) and data:
        db.session.delete(data)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/profile/<accountId>')
def profile(accountId):
    # TODO Maybe implement this some day?
    return render_template('index.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == '__main__':
    app.run()

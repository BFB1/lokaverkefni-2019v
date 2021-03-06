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
        abort(500)
        return
    if data is None:
        abort(404)

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
        abort(500)
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
        abort(500)
        return
    if (current_user.admin or current_user.id == data.owner.id) and data:
        db.session.delete(data)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    try:
        data = Comment.query.filter_by(id=comment_id).first()
    except SQLAlchemyError:
        abort(500)
        return
    if (current_user.admin or current_user.id == data.owner.id) and data:
        edit_form = MakeCommentForm(obj=data)
        if edit_form.validate_on_submit():
            data.body = edit_form.body.data
            db.session.commit()
            return redirect(url_for('thread', thread_id=data.Thread.id))
        return render_template('edit_comment.html', form=edit_form)


@app.route('/comment/<comment_id>/delete')
@login_required
def delete_comment(comment_id):
    try:
        data = Comment.query.filter_by(id=comment_id).first()
    except SQLAlchemyError:
        abort(500)
        return  # Nothing is ever gonna reach here. But without it Pycharm yells at me.

    if data and (current_user.admin or current_user.id == data.owner.id):
        redirect_destination = data.Thread.id
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('thread', thread_id=redirect_destination))
    elif data:
        return redirect(url_for('thread', thread_id=data.Thread.id))
    else:
        abort(404)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404, message='The resource you are looking for was not found'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error=500, message='There was an error when handling your request'), 500


@app.errorhandler(401)
@app.errorhandler(403)
def server_error(e):
    return render_template('error.html', error=401, message='You are not authorized to access this page'), 401




if __name__ == '__main__':
    app.run()

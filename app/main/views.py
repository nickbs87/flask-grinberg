from datetime import datetime

from flask import render_template, session, redirect, url_for

from .import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email




@main.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@main.route('/users')
def users():
    users_list = [
        {'name':'Nick', 'age':39, 'role':'admin'},
        {'name':'Maria', 'age':27, 'role':'user'},
        {'name':'Giorgos', 'age':45, 'role':'user'},
        {'name':'Eleni', 'age':33, 'role':'user'}
    ]
    return render_template('users.html', users=users_list)



@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = NameForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.name.data).first()
        if existing_user is None:
            existing_user = User(username=form.name.data,
                        email=form.email.data
                        )
            db.session.add(existing_user)
            db.session.commit()
            session["Known"] = False
            send_email(
                existing_user.email,
                f"Welcome {existing_user.username}! ",
                'mail/new_user',
                user=existing_user
            )

        else:
            session["Known"] = True
        session["name"] = form.name.data

        return redirect(url_for('.feedback'))

    return render_template('feedback.html', form=form, name=session.get('name'),
                           Known= session.get("Known", False))

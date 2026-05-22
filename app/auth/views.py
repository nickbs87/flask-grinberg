from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user
from .forms import LoginForm
from . import auth
from ..models import User




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash("Invalid Email or Password! Try again")

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    return render_template('auth/login.html')


@auth.route('/register')
def register():
    return

from flask import render_template

from flask_login import login_required
from .forms import LoginForm

from . import auth



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    return render_template('auth/login.html')


@auth.route('/register')
def register():
    return

from datetime import datetime

from flask import render_template, session, redirect, url_for, flash, abort, request, current_app

from .import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import User, Permission, Role, Post
from ..email import send_email
from ..decorators import permission_required, admin_required
from flask_login import login_required, current_user



@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author = current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page = current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()

    return render_template('user.html', user = user, posts=posts)


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


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated. ')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit-profile.html', form=form, user=user)








@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators only!"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment Moderators"

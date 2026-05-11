from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Email config Setup
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')



db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)
mail = Mail(app)


class NameForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    
class Role(db.Model):
    __tablename__= "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")
    
    def __repr__(self):
        return f"<Name {self.name!r}>"
    
    
class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    
    
    def __repr__(self):
        return f"<User {self.username!r}>"


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.route('/')
def index():
    fruits = ['banana', 'apple', 'cherry', 'date', 'elderberry']
    return render_template('index.html', fruits=fruits,
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/users')
def users():
    users_list = [
        {'name':'Nick', 'age':39, 'role':'admin'},
        {'name':'Maria', 'age':27, 'role':'user'},
        {'name':'Giorgos', 'age':45, 'role':'user'},
        {'name':'Eleni', 'age':33, 'role':'user'}
    ]
    return render_template('users.html', users=users_list)

    
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["Known"] = False
        else:
            session["Known"] = True
        session["name"] = form.name.data
        
        return redirect(url_for('feedback'))
    
    return render_template('feedback.html', form=form, name=session.get('name'),
                           Known= session.get("Known", False))



    

if __name__ == "__main__":
    app.run(debug=True)
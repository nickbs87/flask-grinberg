from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime



app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


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
    

if __name__ == "__main__":
    app.run(debug=True)
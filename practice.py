from flask import Flask, request, g, session
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev-key-change-this'

@app.route('/')
def index():
    return '<h1>Welcome</h1><a href="/about">About</a'

@app.route('/about')
def about():
    return '<h3>This is about page!</h3>'


@app.route('/user/admin')
def admin():
    return "Welcome administrator"



@app.route('/user/<username>')
def user(username):
    return f"Welcome, {username}!"


@app.route('/calculate/<int:a>/<int:b>')
def calculate(a, b):
    return f"{a} + {b} = {a+b}"


@app.route('/greet')
def greet():
    name = request.args.get('name', 'stranger')
    return f"Hello, {name}!"


@app.route('/visit')
def visit():
    count = session.get('count', 0) + 1
    session['count'] = count
    return f"You have visited {count} times"


@app.before_request
def set_request_time():
    g.request_time = datetime.now()
    
    
@app.route('/time')
def show_time():
    return f"This request started at: {g.request_time}"
    
    
@app.route('/multiply')
def multiply():
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if a is None or b is None:
        return "Please provide both a and b as numbers", 400
    return f" {a} * {b} = {a*b}"



if __name__ == "__main__":
    app.run(debug=True)
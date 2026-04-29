from flask import Flask

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
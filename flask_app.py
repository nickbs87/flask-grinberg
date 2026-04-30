from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    fruits = ['banana', 'apple', 'cherry', 'date', 'elderberry']
    return render_template('index.html', fruits=fruits)


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
    
    

if __name__ == "__main__":
    app.run(debug=True)
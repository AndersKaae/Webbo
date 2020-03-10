from flask import Flask, render_template, request, flash, redirect, make_response
from database import CreateAccount, CheckIfAccountExists, CredentialsGood
from functions import CheckIfLoggedIn
import sys

app = Flask(__name__)
app.secret_key = "d4bb81b1-2038-4f56-8bec-9e35472c4826"

class User:
    email = ""
    password = ""
    realname = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    CheckIfLoggedIn(User)
    return render_template('home.html', User = User, cookieUsername = request.cookies.get('email'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        User.email = request.form['email']
        User.password = request.form['password']
        validated = CredentialsGood(User)
        print(validated, flush=True)
        print('Hello world!', file=sys.stderr)
    return render_template('login.html', User = User, cookieUsername = request.cookies.get('email'))


@app.route('/createaccount', methods=['GET', 'POST'])
def create_account():
    error = ""
    # If create account form is submitted
    if request.method == 'POST':
        # Getting data from form
        User.email = request.form['email']
        User.password = request.form['password']
        User.realname = request.form['name']
        # Checking if user exists
        if CheckIfAccountExists(User.email) == False:
            # Saving user to database and getting cookie token
            token = CreateAccount(User)
            # Saving token to cookie
            resp = make_response(redirect('/'))
            resp.set_cookie('token', token)
            return resp
        else:
            error = 'Brugeren findes allerede'
    return render_template('createaccount.html', User = User, cookieUsername = request.cookies.get('email'), error = error)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/logout')
def log_out():
    resp = make_response(redirect('/'))
    resp.delete_cookie('email')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
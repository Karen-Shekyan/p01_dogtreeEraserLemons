from flask import Flask, render_template, session, request, redirect
import requests, os
from database import *
app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def log_in():
    if 'username' in session:
        return render_template('home.html')
    return render_template('login.html')

@app.route('/login', methods = ['GET', "POST"])
def authenticate():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['password']
    if login(user,pw):
        if request.method == 'POST':
            session['username'] = request.form['username']
        if request.method == 'GET':
            session['username'] = request.args['username']
        return render_template('home.html')
    else:
        return render_template('login.html', errorTextL= "Please enter a valid username and password")

@app.route('/signup', methods = ['GET', "POST"])
def sign_up():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        email = request.form['email']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['password']
        email = request.args['email']
    if signup(user,pw,email):
        return render_template('login.html')
    else:
        return render_template('login.html', errorTextS= "User already exists")

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('http://127.0.0.1:5000/')
    
if __name__ == '__main__':
	app.debug = True
	app.run()

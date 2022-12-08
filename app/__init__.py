from flask import Flask, render_template, session, request
import requests, os
import database
app = Flask(__name__)
secret_key = os.urandom(32)

@app.route('/')
def login():
    if 'username' in session:
        return render_template('home.html')
    return render_template('login.html')

@app.route('/auth')
def authenticate():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['pass']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['pass']

    return render_template('login.html')

if __name__ == '__main__':
	app.debug = True
	app.run()

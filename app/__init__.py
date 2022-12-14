from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *
from characterdb import *

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def log_in():
    if 'username' in session:
        return render_template('home.html', heroes = get_all_ordered_heroes())
    return render_template('login.html')

@app.route('/home')
def home():
    if (session):
        return render_template('home.html', heroes = get_all_ordered_heroes())
    else:
        return redirect('/')

@app.route('/login', methods = ["POST"])
def authenticate():
    if 'username' in session:
        return render_template('home.html', heroes = get_all_ordered_heroes())
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
        return redirect('/home')
    else:
        return render_template('login.html', errorTextL= "Please enter a valid username and password")

@app.route('/signup', methods = ["POST"])
def sign_up():
    if 'username' in session:
        return render_template('home.html', heroes = get_all_ordered_heroes())
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        email = request.form['email']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['password']
        email = request.args['email']
    if '@' in email and '.' in email.split('@')[1]:
        if signup(user,pw,email):
            return render_template('login.html')
        else:
            return render_template('login.html', errorTextS= "User already exists")
    else:
        return render_template('login.html', errorTextS = "Invalid email")

@app.route('/hero/<int:hero_id>')
def display(hero_id):
    if (not hero_in_db(hero_id)):
        return render_template('noExist.html')
    else:
        bio = get_hero_bio(hero_id)
        image = get_hero_image(hero_id)
        print(image)
        powerstats = get_hero_powerstats(hero_id)
        powerstats = powerstats[1: -1]
        powerstats = powerstats.split(",")
        pstats = {}
        for elements in powerstats:
            temp = elements.split(":")
            pstats[temp[0][1:-1]] = temp[1][1:]
        name = get_hero_name(hero_id)
        return render_template('hero.html', Information = bio, picture = image, stats = pstats, title = name)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('http://127.0.0.1:5000/')

@app.route('/profile')
def userprofile():
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    return render_template('user_profile.html', username=session['username'], favorites=get_list_of_saved_jokes(session['username']))

@app.route('/profile/<user>')
def qruserprofile(user):
    return render_template('user_profile.html', username=user, favorites=get_all_ordered_heroes(user))

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    if request.method == 'GET':
        character = request.args['search']
        hero = get_hero_id(character)
        return redirect('/hero/' + str(hero))

if __name__ == '__main__':
	app.debug = True
	app.run()

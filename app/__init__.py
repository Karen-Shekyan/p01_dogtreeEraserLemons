from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *
from characterdb import *

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def log_in():
    if 'username' in session:
        return render_template('home.html')
    return render_template('login.html')

@app.route('/home')
def home():
    if (session):
         return render_template('home.html', heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())
    else:
        return redirect('/')

@app.route('/login', methods = ["POST"])
def authenticate():
    if 'username' in session:
        return render_template('home.html', heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())
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
        return render_template('home.html', heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())
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
        return render_template('hero.html', Information = bio, picture = image, stats = pstats, title = name, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())
@app.route('/pokemon/<int:poke_id>')
def display2(poke_id):
    if (not hero_in_db(poke_id)):
        return render_template('noExist.html')
    else:
        bio = get_pokemon_bio(poke_id)
        image = get_pokemon_image(poke_id)
        print(image)
        powerstats = get_pokemon_stats(poke_id)
        powerstats = powerstats[1: -1]
        powerstats = powerstats.split(",")
        pstats = {}
        count = 0
        for elements in powerstats:
            temp = elements.split(":")
            if(count == 0):
                pstats[temp[0][1:-1]] = temp[1][1:]
            else:
                pstats[temp[0][2:-1]] = temp[1][1:]
            count+=1
        print(powerstats)
        name = get_pokemon_name(poke_id)
        type = get_pokemon_poketype(poke_id)
        return render_template('pokemon.html', Information = bio, picture = image, stats = pstats, title = name, type=type, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('/')

@app.route('/profile')
def userprofile():
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    return render_template('user_profile.html', username=session['username'], favorites=get_list_of_saved_jokes(session['username']), heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon(), edit=True)

@app.route('/profile/<user>')
def qruserprofile(user):
    edit = False
    if(session['username'] == user):
        edit = True
    return render_template('user_profile.html', username=user, favorites=get_list_of_saved_jokes(user), heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), edit = edit, pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())

@app.route('/joke')
def joke():
    return render_template('view_joke.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    # print("a")
    if 'username' not in session:
        return redirect('/')
    else:
        # print(request.form['search'])
        # print("b")
        character = request.form['search']
        # print(character)
        heroes = get_all_ordered_heroes()
        pokemon = get_all_ordered_pokemon()
        search_results = []
        search_results_id = []
        Psearch_results = []
        Psearch_results_id = []
        for elements in heroes:
            if(character.upper().strip() in elements.upper()):
                search_results.append(elements)
                # print(elements)
                search_results_id.append(get_hero_id(elements))
        for elements in pokemon:
            if(character.upper().strip() in elements.upper()):
                Psearch_results.append(elements)
                # print(elements)
                Psearch_results_id.append(get_pokemon_id(elements))
        length = len(search_results_id)
        Plength = len(Psearch_results_id)
        #return render_template('search.html')
        return render_template('search.html', pleng = Plength , c = Psearch_results, d = Psearch_results_id, leng = length, a = search_results, b = search_results_id, heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())

if __name__ == '__main__':
	app.debug = True
	app.run()

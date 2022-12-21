from flask import Flask, render_template, session, request, redirect, url_for
import requests, os, json
from database import *
from characterdb import *
import random

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def log_in():
    if 'username' in session:
        return redirect('/home')
    return render_template('login.html')

@app.route('/home')
def home():
    if (session):
        print(get_list_of_saved_jokes(session['username']))
        favs = [(get_joke_from_id(jokeid)[0:25] + "...", jokeid) for jokeid in get_list_of_saved_jokes(session['username'])]
        count = len(favs) - 1
        index = 0
        favs2 = []
        while((count > -1) and index < 5):
            favs2.append(favs[count])
            count-=1
            index+=1
        return render_template('home.html', heroes = get_all_ordered_heroes(), favorites = favs2, heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())
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
    favs = [(get_joke_from_id(jokeid)[0:25] + "...", jokeid) for jokeid in get_list_of_saved_jokes(session['username'])]
    return render_template('user_profile.html', username=session['username'], email=get_email(session['username']), favorites=favs, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon(), edit=True, bio=get_bio(session['username']))

@app.route('/profile/<user>')
def qruserprofile(user):
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    edit = False
    if not(username_in_system(user)):
        return render_template('noExistC.html')
    if(session['username'] == user):
        edit = True
        return redirect("/profile")
    favs = [([get_joke_from_id(jokeid)[0:25] + "...", jokeid]) for jokeid in get_list_of_saved_jokes(user)]
    return render_template('user_profile.html', username=user, favorites=favs, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), edit = edit, pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon(), email=get_email(user), bio=get_bio(user))

@app.route('/profile/edit')
def edit():
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    favs = [([get_joke_from_id(jokeid)[0:25] + "...", jokeid]) for jokeid in get_list_of_saved_jokes(session['username'])]
    return render_template('user_profile.html', username=session['username'], favorites=favs, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon(), edit=True, editing=True, email=get_email(session['username']), bio=get_bio(session['username']))

@app.route('/edit', methods = ['POST', 'GET'])
def update_edits():
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    if request.method == 'POST':
        username = request.form["username"]
        bio = request.form["bio"]
    if request.method == 'GET':
        username = request.args["username"]
        bio = request.args["bio"]

    edit_username(session['username'], username) # update username
    session['username'] = username
    edit_bio(session['username'], bio) # update bio
    favs = [([get_joke_from_id(jokeid)[0:25] + "...", jokeid]) for jokeid in get_list_of_saved_jokes(session['username'])]
    return render_template('user_profile.html', username=session['username'], favorites=favs, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon(), edit=True, editing=False, email=get_email(session['username']), bio=get_bio(session['username']) )

@app.route('/deactivate')
def deactivate():
    if 'username' not in session:
        return redirect('http://127.0.0.1:5000/')
    print(remove_user(session['username']))
    session.pop('username')
    return redirect('http://127.0.0.1:5000/')

@app.route('/joke', methods = ['GET', 'POST'])
def joke():
    if 'username' not in session:
        return redirect('/')
    jokeid = random.randint(0, 250)
    return redirect(f"/joke/{jokeid}")
@app.route('/joke/<jokeid>', methods = ['GET', 'POST'])
def joke2(jokeid):
    if 'username' not in session:
        return redirect('/')
    joke = get_joke_from_id(jokeid)
    punchline = get_punchline_from_id(jokeid)
    hero_id = random.choice(get_all_hero_id())
    hero = get_hero_name(hero_id)
    hero_img = get_hero_image(hero_id)
    hero_bio = get_hero_bio(hero_id)
    poke_id = random.choice(get_all_pokemon_id())
    poke = get_pokemon_name(poke_id)
    poke_img = get_pokemon_image(poke_id)
    poke_bio = get_pokemon_bio(poke_id)
    favorited = (joke_in_user(session['username'], jokeid))
    print(favorited)
    if request.method == 'POST':
        if request.form.get("favorite") == "favorite":
            favorited = True
            print(add_joke_to_user(session['username'], jokeid))
    return render_template('view_joke.html', favorited = favorited, setup=joke, punchline=punchline, jokeid = jokeid, hero=hero, hero_id = hero_id, hero_png=hero_img, hero_info = hero_bio, poke=poke, poke_id = poke_id, poke_png=poke_img, poke_info=poke_bio)
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
        return render_template('search.html', pleng = Plength , c = Psearch_results, d = Psearch_results_id, leng = length, a = search_results, b = search_results_id, heroes = get_all_ordered_heroes(), heroesid = get_all_hero_id(), pokeid = get_all_pokemon_id(), pokemons = get_all_ordered_pokemon())

if __name__ == '__main__':
	app.debug = True
	app.run()

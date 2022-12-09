import sqlite3
db = sqlite3.connect("database.db", check_same_thread=False)
global c
c = db.cursor()
c.execute("CREATE TABLE if not exists users(username TEXT, password TEXT, email TEXT, favorite TEXT)")
c.execute("CREATE TABLE if not exists jokes(joke_id INTEGER, content TEXT, character TEXT)")
c.execute("CREATE TABLE if not exists heroes(hero_id INTEGER, name TEXT, powerstats TEXT, bio TEXT)")

# general method that can be used to get data easier
def select_from(table, data_want, datagive, datatype_give):
    temp = ((c.execute(f"SELECT {data_want} FROM {table} WHERE {datatype_give} = '{datagive}'")).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0

def username_in_system(username):
    temp = list(c.execute("SELECT username FROM users").fetchall())
    for element in temp:
        for element2 in element:
            if username == element2:
                return True
    return False

def signup(username, password, email):
    if(username_in_system(username)):
        return False
    else:
        c.execute("INSERT INTO users VALUES (?,?,?,'')", (username, password, email))
    db.commit()
    return True #save changes

def remove_user(username):
    c.execute(f'DELETE FROM main WHERE username = "{username}"')
    db.commit() #save changes

# to verify if the password given is right to login
def login(username, password):
    if(username_in_system(username)):
        if(select_from("users", "password", username, "username") == password):
            return True
    return False

def add_joke_into_jokedb(content, character, joke_id):
    if select_from("jokes", "joke_id", joke_id, "joke_id") == 0:
        c.execute(f"INSERT INTO jokes VALUES (?,?,?)", (joke_id, content, character))
        print("Joke added")
        db.commit() #save changes
    else:
        print("Joke already in database")

def get_list_of_saved_jokes(username):
    jokes = list(c.execute(f"SELECT favorite FROM users WHERE username = '{username}'").fetchall())
    returnlist = []
    for i in jokes:
        returnlist.append(i[0])
    return returnlist

# returns true if joke was successfully favorited by user
def add_joke_to_user(username, joke_id):
    if select_from("jokes", "joke_id", joke_id, "joke_id") != 0:
        if joke_id not in get_list_of_saved_jokes(username):
            c.execute(f"UPDATE users SET favorite = '{joke_id}' WHERE username = '{username}'")
            db.commit() #save changes
            return True
    return False

def add_hero(hero_id, name, powerstats, bio):
    if select_from("heroes", "hero_id", hero_id, "hero_id") == 0:
        c.execute(f"INSERT INTO heroes VALUES (?,?,?,?)", (hero_id, name, powerstats, bio))
        db.commit() #save changes
        print("Hero added")
    else:
        print("Hero already in database")
        
def hero_in_db(hero_id):
    if select_from("heroes", "hero_id", hero_id, "hero_id") != 0:
        return True
    return False

def get_hero_name(hero_id):
    if hero_in_db(hero_id):
        return c.execute(f"SELECT name FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False

def get_hero_powerstats(hero_id):
    if hero_in_db(hero_id):
        return c.execute(f"SELECT powerstats FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False

def get_hero_bio(hero_id):
    if hero_in_db(hero_id):
        return c.execute(f"SELECT bio FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False
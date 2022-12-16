import sqlite3
from database import *

db = sqlite3.connect("character.db", check_same_thread=False)
c = db.cursor()
unlisted_hero = [9, 16, 19, 21, 22, 27, 33, 46, 47, 50, 51, 54, 55, 59, 64, 65, 67, 74, 75, 77, 78, 85, 86, 89, 90, 91, 94, 101, 108, 113, 116, 117, 122, 123, 124, 125, 128, 129, 131, 132, 133, 134, 135, 138, 143, 153, 155, 159, 161, 163, 164, 166, 168, 173, 175, 179, 182, 183, 184, 187, 189, 190, 192, 193, 197, 199, 205, 223, 229, 243, 244, 250, 255, 262, 264, 272, 276, 279, 281, 282, 283, 290, 291, 292, 293, 295, 301, 302, 304, 316, 317, 318, 319, 324, 326, 328, 329, 331, 349, 359, 362, 363, 366, 368, 377, 378, 385, 399, 411, 417, 420, 434, 446, 447, 453, 464, 465, 466, 468, 473, 482, 486, 494, 500, 501, 507, 511, 512, 513, 515, 519, 525, 534, 544, 552, 553, 554, 560, 593, 596, 597, 603, 606, 614, 616, 617, 621, 622, 624, 626, 629, 662, 663, 669, 673, 674, 675, 682, 683, 684, 691, 694, 695, 698, 700, 704, 710, 712, 715, 721, 725]
created = False

c.execute("CREATE TABLE if not exists jokes(joke_id INTEGER PRIMARY KEY, content TEXT, character TEXT)")
c.execute("CREATE TABLE if not exists heroes(hero_id INTEGER PRIMARY KEY, name TEXT, powerstats TEXT, bio TEXT, image_link TEXT)")
c.execute("CREATE TABLE if not exists pokemon(pokemon_id INTEGER PRIMARY KEY, name TEXT, poke_type TEXT, stats TEXT, gen TEXT, bio TEXT, image_link TEXT)")

# to execute heroes table with all heroes
# general method that can be used to get data easier
def select_from(database, table, data_want, datagive, datatype_give):
    db = sqlite3.connect(database, check_same_thread=False)
    c = db.cursor()
    temp = ((c.execute(f"SELECT {data_want} FROM {table} WHERE {datatype_give} = '{datagive}'")).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0

def add_joke(content, character, joke_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if select_from("character.db", "jokes", "joke_id", joke_id, "joke_id") == 0:
        c.execute(f"INSERT INTO jokes VALUES (?,?,?)", (joke_id, content, character))
        print("Joke added")
        db.commit() #save changes
        db.close()
    else:
        print("Joke already in database")

def hero_in_db(hero_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if select_from("character.db", "heroes", "hero_id", hero_id, "hero_id") != 0:
        return True
    return False

def get_hero_name(hero_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if hero_in_db(hero_id):
        return c.execute(f"SELECT name FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False

def get_hero_id(hero_name):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    return c.execute(f"SELECT hero_id FROM heroes WHERE name = ?", (hero_name,)).fetchall()[0][0]

def get_hero_powerstats(hero_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if hero_in_db(hero_id):
        return c.execute(f"SELECT powerstats FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False

def get_hero_bio(hero_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if hero_in_db(hero_id):
        return c.execute(f"SELECT bio FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False

def get_hero_image(hero_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if hero_in_db(hero_id):
        return c.execute(f"SELECT image_link FROM heroes WHERE hero_id = '{hero_id}'").fetchall()[0][0]
    return False

def get_all_ordered_heroes():
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    a = c.execute("SELECT name FROM heroes").fetchall()
    list_of_heroes = []
    for x in a:
        list_of_heroes.append(x[0])
    return list_of_heroes

def get_all_hero_id():
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    data = c.execute(f"SELECT hero_id FROM heroes").fetchall()
    ids = []
    for x in data:
        ids.append(x[0])
    return ids

# to initialize table with heroes
created = hero_in_db(1)
print(created)
if (not created):
    for i in range(1, 732):
        if(not i in unlisted_hero):
            hero = apimethods.hero_info(i)
            c.execute("INSERT INTO heroes VALUES (?,?,?,?,?)", (i, str(hero[0]), str(hero[1]), str(hero[2]), str(hero[3])))
        print(i)
    created = True

def pokemon_in_db(pokemon_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if select_from("character.db", "pokemon", "pokemon_id", pokemon_id, "pokemon_id") != 0:
        return True
    return False

def get_pokemon_name(pokemon_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if pokemon_in_db(pokemon_id):
        return c.execute(f"SELECT name FROM pokemon WHERE pokemon_id = '{pokemon_id}'").fetchall()[0][0]
    return False

def get_pokemon_id(pokemon_name):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    return c.execute(f"SELECT pokemon_id FROM pokemon WHERE name = '{pokemon_name}'").fetchall()[0][0]

def get_pokemon_poketype(pokemon_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if pokemon_in_db(pokemon_id):
        return c.execute(f"SELECT poke_type FROM pokemon WHERE pokemon_id = '{pokemon_id}'").fetchall()[0][0]
    return False

def get_pokemon_stats(pokemon_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if pokemon_in_db(pokemon_id):
        return c.execute(f"SELECT stats FROM pokemon WHERE pokemon_id = '{pokemon_id}'").fetchall()[0][0]
    return False

def get_pokemon_image(pokemon_id):
    db = sqlite3.connect("character.db", check_same_thread=False)
    c = db.cursor()
    if pokemon_in_db(pokemon_id):
        return c.execute(f"SELECT image_link FROM pokemon WHERE pokemon_id = '{pokemon_id}'").fetchall()[0][0]
    return False
    
db.commit()
db.close()

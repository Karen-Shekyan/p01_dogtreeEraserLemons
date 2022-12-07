import sqlite3
db = sqlite3.connect("Database.db", check_same_thread=False)
global c
c = db.cursor()
c.execute("CREATE TABLE if not exist users(username TEXT, password TEXT, favorite TEXT)")
c.execute("CREATE TABLE if not exist jokes(joke_id INTEGER, content TEXT, character TEXT)")

def select_from(table, data_want, datagive, datatype_give): #general method that can be used to get data easier
    temp = ((c.execute(f"SELECT {data_want} FROM {table} WHERE {datatype_give} = '{datagive}'")).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0

def username_in_system(username):
    temp = list(c.execute("SELECT username FROM user").fetchall())
    for element in temp:
        for element2 in element:
            if username == element2:
                return True

def signup(username, password):
    if(username_in_system(username)):
        return False
    else:
        c.execute("INSERT INTO user VALUES (?,?)", (username, password))
    db.commit()
    return True #save changes

def remove_user(username):
    c.execute(f'DELETE FROM main WHERE username = "{username}"')
    db.commit() #save changes


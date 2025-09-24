import sqlite3
from Log import Log

def db_connect():
    return sqlite3.connect('data/data.db')

def db_create_tables():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL)''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL)''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            action_id INTEGER NOT NULL,
            log TEXT ,
            time INT)''')
    connection.commit()
    connection.close()

def db_add_user(username):
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username) VALUES (?)",
        (username,)
    )
    connection.commit()
    connection.close()

def db_add_action(user_id, action):
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO actions (user_id, action) VALUES (?, ?)",
        (user_id, action)
    )
    connection.commit()
    connection.close()

def db_add_log(action, log, time):
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO logs (action_id, log, time) VALUES (?, ?, ?)",
        (action, log, time) 
    )
    connection.commit()
    connection.close()

def db_get_action_id(user_id, action_name):
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM actions WHERE action = ? AND user_id = ?", (action_name, user_id))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

######
#LOAD
#####
def db_load_users():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users")
    users = [row[0] for row in cursor.fetchall()] 
    connection.close()
    return users

def db_load_actions(username):
    if isinstance(username, tuple):
        username = username[0]
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT actions.action
        FROM actions
        JOIN users ON actions.user_id = users.id
        WHERE users.username = ?
    """, (username,))
    
    actions = [row[0] for row in cursor.fetchall()]
    connection.close()
    return actions

def db_load_logs(username):
    if isinstance(username, tuple):
        username = username[0]
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT actions.action, logs.time, logs.log
        FROM logs
        JOIN actions ON logs.action_id = actions.id
        JOIN users ON actions.user_id = users.id
        WHERE users.username = ?;
    """, (username,)) 
    logs=[]
    for action_name, minutes, description in cursor.fetchall():
        logs.append(Log(minutes, action_name, description))

    connection.close()
    return logs

#search
def db_logs_search(username,action):
    if isinstance(username, tuple):
        username = username[0]
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT logs.log, logs.time
        FROM logs
        JOIN actions ON logs.action_id = actions.id
        JOIN users ON actions.user_id = users.id
        WHERE users.username = ?
        AND actions.action LIKE ?
    """, (username, f"%{action}%"))
    
    logs = cursor.fetchall()
    connection.close()
    return logs
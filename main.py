#Simple time/activity tracker
from Commands import Validate, login, users, load_data
from Database import db_create_tables
# CONSTANTS
APP_VERSION = 'VERSION: 1.0'

def APP_INIT():
    print(APP_VERSION)
    db_create_tables()
    login()
    load_data()
    Validate(users[0])

APP_INIT()
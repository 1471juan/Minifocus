#Simple time/activity tracker
from Commands import Validate, user_add, users
# CONSTANTS
APP_VERSION = 'VERSION: 0.1'

def APP_INIT():

    print(APP_VERSION)

    user_add('1471juan')
    user_add('jorgito')

    Validate(users[0])

APP_INIT()


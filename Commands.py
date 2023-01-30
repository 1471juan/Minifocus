import os
from User import User
from Log import Log
from MiniPlot import MiniPlot
from Pomodoro import Pomodoro

commands_list=[
    'action_add - Adds an action',
    'action_remove - Removes an action',
    'log_add - Adds a log',
    'time_total - Shows the total time spent in all actions',
    'time - Shows the total time spent in a specific action',
    'log_show - Shows all logs',
    'visualize - Visualize time spent',
    'pomodoro - Classing pomodoro timer, break down tasks into intervals of time.',    
    'help - Lists all commands',
    'exit - Exits the application']
users = []
users_logs = []

print('          _          ')
print('|\/| ._  |__  _    _ ')
print('|  ||| |||(_)(_|_|_> ')
print('---------------------')
print("'help' for a list of all commands.")
#Commands
def Validate(user):
    msg = input('_> ')
    os.system('clear')
    def validate_action(value):
        i=0
        while(i<len(user.USER_LOG_ACTIONS)):
            if value == user.USER_LOG_ACTIONS[i]:
                return True
            i+=1
        print('Action not found.')
        return False

    def validate_minutes(value):
        if int(value)>0:
            return True
        else:
            print('Minutes should be a positive number.')
            return False

    if(msg=='help'):
        print('Command list: ')
        for i in commands_list:
            print(" -> " + i)
    elif(msg=='action_add'):
        value=input('New action name: ')
        user.Log_action_add(value)
    elif(msg=='action_remove'):
        value=input('Action to remove: ')
        user.Log_action_remove(value)
    elif(msg=='log_add'):
        action=input('Action: ')
        minutes=input('Time(in minutes): ')
        description=input('Description: ')
        if(validate_action(action) & validate_minutes(minutes)):
            user_log_add(user,int(minutes),action,description)
    elif(msg=='time_total'):
        users_time_spent()
    elif(msg=='time'):
        action=input('Action: ')
        users_activity_time_spent(user,action)
    elif(msg=='log_show'):
        user_logs_show(user)
        Validate(user)
    elif(msg=='visualize'):
        user_data_visualize(user)
    elif(msg=='pomodoro'):
        user_pomodoro(user)
    elif(msg=='exit'):
        return True
    else:
        print('Incorrect command, try again.')
    #Come back
    Validate(user)

#Creates a user
def user_add(username):
    users.append(User(username))

#Adds all existing users logs to an array
def app_users_recollect():
    i=0
    while(i<len(users)):
        users_add(users[i])
        i+=1

#Adds a log to the users_logs array
def users_add(user):
    users_logs.append([user.username, user.Logs_get()])

#Adds a log to a user
def user_log_add(user, minutes, action, description):
    user.Log_add(Log(minutes, action, description))

#returns each user total time spent
def users_time_spent():
    print("----------------------------")
    for i in users:
        print(i.username +' total time spent in minutes: '+ str(i.time_minutes())+ "; in hours: "+ str(i.time_minutes()/60))
        user_data_visualize(i,'bar')
    print("----------------------------")

#returns a user's time spent on a specific action
def users_activity_time_spent(user,action):
    total_time = user.Log_action_time(action)
    print(user.username + ' total time spent in ' + action + ' in minutes: ' + str(total_time) + '; in hours:'+ str(total_time/60))

# Print all users logs
def users_logs_show():
    u = 0
    while (u < len(users_logs)):
        v = 0
        while (v < len(users_logs[u][1])):
            print("----------------------------")
            print("user: " + users_logs[u][0])
            print("action: " + str(users_logs[u][1][v].action))
            print("minutes: " + str(users_logs[u][1][v].minutes))
            print("description: " + users_logs[u][1][v].description)
            v+=1
        u += 1

#Prints an specific user logs
def user_logs_show(user):
    i = 0
    while (i < len(user.user_logs)):
        print("----------------------------")
        print("user: " + user.username)
        print("action: " + str(user.user_logs[i].action))
        print("minutes: " + str(user.user_logs[i].minutes))
        print("description: " + user.user_logs[i].description)
        i += 1

#visualize data with MiniPlot
def user_data_visualize(user,figure='bar'):
    time_spent_on_each_action=[] 
    i=0
    while(i<len(user.USER_LOG_ACTIONS)):
        time_spent_on_each_action.append(user.Log_action_time(user.USER_LOG_ACTIONS[i]))
        i+=1
    if(figure=='bar'):
        MiniPlot.bar(time_spent_on_each_action,user.USER_LOG_ACTIONS)
    elif(figure=='plot'):
        MiniPlot.plot(time_spent_on_each_action)
    

def user_pomodoro_tasks_sort(user,pomodoro_numberOfTasks):

    pomodoro_tasks = []
    while pomodoro_numberOfTasks:
        print("Select tasks: ")
        for task in user.USER_LOG_ACTIONS:
            if not task in pomodoro_tasks: print(" -> " + task)
        print("{} tasks remaining.".format(pomodoro_numberOfTasks))

        tmp_task=input("TASK: ")

        i=0
        while(i<len(user.USER_LOG_ACTIONS)):
            if tmp_task == user.USER_LOG_ACTIONS[i]:
                pomodoro_tasks.append(tmp_task)
                pomodoro_numberOfTasks -= 1
            else:
                print('Action not found. Please try again.')
            i+=1

    return pomodoro_tasks

def user_pomodoro(user):
    pomodoro_length=input('Task length(in minutes): ')
    pomodoro_break_length=input('Break length(in minutes): ')
    pomodoro_numberOfTasks = input('Quantity of tasks in the session: ')
    #Handle errors.
    if int(pomodoro_length) <= 0 or int(pomodoro_break_length) < 0 or int(pomodoro_numberOfTasks) <= 0:
        print("All parameters should be higher than 0.")
        user_pomodoro(user)
    else:
        #POMODORO
        pomodoro_tasks = user_pomodoro_tasks_sort(user,int(pomodoro_numberOfTasks))
        Pomodoro.pomodoro(int(pomodoro_length),int(pomodoro_break_length),pomodoro_tasks)
        #ADD TIME SPENT TO LOG
        for task in pomodoro_tasks:
            user.Log_add(Log(int(pomodoro_length), task, "Pomodoro"))




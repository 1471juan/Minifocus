import os
from User import User
from Log import Log
from MiniPlot import MiniPlot
from Pomodoro import Pomodoro
from Database import db_add_action, db_add_log, db_get_action_id,db_load_actions,db_load_logs,db_load_users,db_add_user,db_logs_search,db_remove_action

commands_list=[
    'action_add - Adds an action',
    'action_remove - Removes an action',
    'log_add - Adds a log',
    'time_total - Shows the total time spent in all actions',
    'time - Shows the total time spent in a specific action',
    'log_show - Shows all logs',
    'log_search <action> - Look up for all logs given a specific action',
    'visualize - Visualize time spent',
    'pomodoro - Classing pomodoro timer, break down tasks into intervals of time.',    
    'help - Lists all commands',
    'exit - Exits the application']
users = []
users_logs = []

print('          _          ')
print(r'|\/| ._  |__  _    _ ')
print('|  ||| |||(_)(_|_|_> ')
print('---------------------')

#login
def login():
    u=db_load_users()
    if u:
        for i, user in enumerate(u):
            user_add(user,i+1)
    msg = input('login username: ')
    os.system('cls' if os.name == 'nt' else 'clear')
    if msg not in u:
        user_add(msg,len(users)+1)
        db_add_user(msg)
    
#commands
def Validate(user):
    print("'help' for a list of all commands.")
    msg = input('_> ')
    os.system('cls' if os.name == 'nt' else 'clear')

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
        #save action
        db_add_action(user.id,value)

    elif(msg=='action_remove'):
        value=input('Action to remove: ')
        user.Log_action_remove(value)
        db_remove_action(user.username,value)

    elif(msg=='log_add'):
        action=input('Action: ')
        minutes=input('Time(in minutes): ')
        description=input('Description: ')
        if(validate_action(action) & validate_minutes(minutes)):
            user_log_add(user,int(minutes),action,description)
            #save log
            db_add_log(db_get_action_id(user.id, action), description, int(minutes))

    elif(msg=='time_total'):
        users_time_spent()

    elif(msg=='time'):
        action=input('Action: ')
        users_activity_time_spent(user,action)

    elif(msg=='log_show'):
        user_logs_show(user)
        Validate(user)

    elif msg.startswith('log_search'):
        param = msg.split(maxsplit=1)
        if len(param) < 2:
            print("you need to specify an action")
        else:
            users_logs_search(user,param)

    elif(msg=='visualize'):
        user_data_visualize(user)

    elif msg.startswith('visualize_plot'):
        param = msg.split(maxsplit=1)
        if len(param) < 2:
            print("you need to specify an action")
        else:
            user_data_visualize_plot(user,param)
        
    elif(msg=='pomodoro'):
        user_pomodoro(user)

    elif(msg=='exit'):
        return True
    
    else:
        print('Incorrect command, try again.')
    #go back
    Validate(user)

#add a user to the users array
def user_add(username,id):
    users.append(User(username,id))

#load data from the database
def load_data():
    for user in users:
        for a in db_load_actions(user.username):
            user.Log_action_add(a)
        for l in db_load_logs(user.username):
            user_log_add(user,l.minutes,l.action,l.description)
    
        users_add(user)
        os.system('cls' if os.name == 'nt' else 'clear')

#adds all existing users logs to an array
def app_users_recollect():
    i=0
    while(i<len(users)):
        users_add(users[i])
        i+=1

#adds a log to the users_logs array
def users_add(user):
    users_logs.append([user.username, user.Logs_get()])

#adds a log to a user
def user_log_add(user, minutes, action, description):
    user.Log_add(Log(minutes, action, description))

#returns each user total time spent
def users_time_spent():
    print("----------------------------")
    for i in users:
        print(i.username +' total time spent in minutes: '+ str(i.time_minutes())+ "; in hours: "+ str(i.time_minutes()/60))
        user_data_visualize(i)
    print("----------------------------")

#returns a user's time spent on a specific action
def users_activity_time_spent(user,action):
    total_time = user.Log_action_time(action)
    print(user.username + ' total time spent in ' + action + ' in minutes: ' + str(total_time) + '; in hours:'+ str(total_time/60))

#print all users logs
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

#get logs from a specific action and print them
def users_logs_search(user,param):
    tmp_action = param[1]
    tmp_logs = db_logs_search(user.username, tmp_action)

    if not tmp_logs:
        print(f"no logs found for {tmp_action}")
    else:
        for log, time in tmp_logs:
            print("----------------------------")
            print("user: " + user.username)
            print("action: " + tmp_action)
            print("minutes: " + str(time))
            print("description: " + log)

#print a specific user logs
def user_logs_show(user):
    i = 0
    while (i < len(user.user_logs)):
        print("----------------------------")
        print("user: " + user.username)
        print("action: " + str(user.user_logs[i].action))
        print("minutes: " + str(user.user_logs[i].minutes))
        print("description: " + user.user_logs[i].description)
        i += 1

#visualize data
def user_data_visualize(user):
    time_spent_on_each_action=[] 
    i=0
    while(i<len(user.USER_LOG_ACTIONS)):
        time_spent_on_each_action.append(user.Log_action_time(user.USER_LOG_ACTIONS[i]))
        i+=1
    MiniPlot.bar(time_spent_on_each_action,user.USER_LOG_ACTIONS)

#visualize plot
def user_data_visualize_plot(user,param):
    tmp_action = param[1]
    tmp_logs = db_logs_search(user.username, tmp_action)
    tmp_logs_time=[]
    if not tmp_logs:
        print(f"Either {tmp_action} does not exist or there is typo.")
    else:
        for log, time in tmp_logs:
            tmp_logs_time.append(time)

    MiniPlot.plot(tmp_logs_time)

#sort and select tasks
def user_pomodoro_tasks_sort(user,pomodoro_numberOfTasks):
    pomodoro_tasks = []
    while pomodoro_numberOfTasks:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Select tasks: ")
        for task in user.USER_LOG_ACTIONS:
            if not task in pomodoro_tasks: print(" -> " + task)
        print("{} tasks remaining.".format(pomodoro_numberOfTasks))
        tmp_task=input("TASK: ")

        if tmp_task in user.USER_LOG_ACTIONS:
            pomodoro_tasks.append(tmp_task)
            pomodoro_numberOfTasks -= 1
        else:
            print('Action not found. Please try again.')

    return pomodoro_tasks

#pomodoro
def user_pomodoro(user):
    pomodoro_length=input('Task length(in minutes): ')
    pomodoro_break_length=input('Break length(in minutes): ')
    pomodoro_numberOfTasks = input('Quantity of tasks in the session: ')
    #Handle errors.
    if int(pomodoro_length) <= 0 or int(pomodoro_break_length) < 0 or int(pomodoro_numberOfTasks) <= 0:
        print("All parameters should be higher than 0.")
        user_pomodoro(user)
    else:
        pomodoro_tasks = user_pomodoro_tasks_sort(user,int(pomodoro_numberOfTasks))
        Pomodoro.pomodoro(int(pomodoro_length),int(pomodoro_break_length),pomodoro_tasks)
        #add time
        for task in pomodoro_tasks:
            user.Log_add(Log(int(pomodoro_length), task, "Pomodoro"))
            db_add_log(db_get_action_id(user.id, task), "Pomodoro", int(pomodoro_length))




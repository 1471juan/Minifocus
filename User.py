class User():
    # USER_LOG_ACTIONS=['READING', 'LISTENING', 'WRITING']
    def __init__(self, username):
        self.username=username
        self.user_logs=[]
        self.USER_LOG_ACTIONS=['READING', 'LISTENING', 'WRITING']
    #Adds a log to the user logs
    def Log_add(self,LogObject):
        self.user_logs.append(LogObject)
    #adds an action to the user_log_actions array
    def Log_action_add(self,action):
        self.USER_LOG_ACTIONS.append(action)
        print('New action created: '+ action)
    #returns all the user's logs
    def Logs_get(self):
        return self.user_logs
    #returns the total time spent
    def time_minutes(self):
        time_minutes_spent=0
        i=0
        while(i<len(self.user_logs)):
            time_minutes_spent += self.user_logs[i].minutes
            i+=1
        return time_minutes_spent
    #returns all time spent in a specific action
    def Log_action_time(self,action):
        #check if there is a log with that action
        time_minutes_spent=0
        i=0
        while(i<len(self.user_logs)):
            if(self.user_logs[i].action==action):
                time_minutes_spent += self.user_logs[i].minutes
            i+=1
        return time_minutes_spent

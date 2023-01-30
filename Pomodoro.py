import time
import os

class Pomodoro:
    #write this function in utilities?
    def floor(n):
        return int(n - (n % 1))

    def timer(length):
        #minutes:seconds
        m=length/60
        s=length%60
        return '{:02}:{:02}'.format(Pomodoro.floor(m),Pomodoro.floor(s))

    def pomodoro(task_length_minutes,break_length_minutes,tasks):
        for task in tasks:
            task_length_seconds = task_length_minutes * 60
            break_length_seconds = break_length_minutes * 60
            #Task
            while task_length_seconds:
                os.system('clear')
                print(task)
                print(Pomodoro.timer(task_length_seconds))
                time.sleep(1)
                task_length_seconds -= 1
            #Break
            while break_length_seconds:
                os.system('clear')
                print(task + ' done! Take a break... ')
                print(Pomodoro.timer(break_length_seconds))
                time.sleep(1)
                break_length_seconds -= 1

        os.system('clear')

        print('Done!')

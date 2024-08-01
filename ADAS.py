import PySimpleGUI as sg
from proximity import *
import os
from datetime import datetime

def ADAS(v):
    if not os.path.isdir("./logs"):
        try:
            os.mkdir("./logs")
        except OSError:
            print("Could not create logs directory")
        else:
            print("Created logs directory")

    logfile = open("./logs/ALSETLogData.log", "a")
    if os.path.getsize("./logs/ALSETLogData.log")>0:
        logfile.write("/n")
    
    c = v[0] #car on
    s = v[1] #speed
    pos = v[2] #car_bounds
    obstacles = v[3]#obstacles
    obs = v[4] #obstr_data
    if(c == False):
        logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] ADAS Failed to turn on. \n")
        return "Car must be on"
    if("Front" in obs):
        #decrease speed
        s = s-1
        #recalculate car position
        y = car_bounds[1]
        y = y - 1
        pos = (car_bounds[0],y,car_bounds[2],car_bounds[3])
        obstr_data = get_car_obstructions(pos,obs)
        #log
        logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Speed reduced.\n")
        #recheck if obstruction is there
        return ADAS([c,s,pos,obstacles, obstr_data])
    if("Back" in obs):
        #increase speed
        s = s+1
        #recalculate car position
        y = pos[1]
        y = y + 1
        pos = (pos[0],y,pos[2],pos[3])
        #log
        logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Speed Increased.\n")
        #recheck if obstruction is there
        obstr_data = get_car_obstructions(pos,obstacles)
        return ADAS([c,s,pos,obstacles, obstr_data])
    if("Left" in obs):
        #recalculate car position
        x = pos[0]
        x = x + 10
        pos = (x,pos[1],pos[2],pos[3])
        #log
        logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Moved car right.\n")
        #recheck if obstruction is there
        obstr_data = get_car_obstructions(pos,obstacles)
        return ADAS([c,s,pos,obstacles, obstr_data])
    if("Right" in obs):
        #recalculate car position
        x = pos[0]
        x = x - 10
        pos = (x,pos[1],pos[2],pos[3])
        #log
        logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Moved car left.\n")
        #recheck if obstruction is there
        obstr_data = get_car_obstructions(pos,obstacles)
        return ADAS([c,s,pos,obstacles, obstr_data])
    else:
        return [s, pos]

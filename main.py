import PySimpleGUI as sg
import os
from datetime import datetime
from test import *
"""
    Dashboard using blocks of information.

    Copyright 2020 PySimpleGUI.org
"""

theme_dict = {
    'BACKGROUND': '#437EA3',
    'TEXT': '#FFFFFF',
    'INPUT': '#F2EFE8',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#F2EFE8',
    'BUTTON': ('#000000', '#C2D4D8'),
    'PROGRESS': ('#FFFFFF', '#C7D5E0'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20, 20), (20, 10))
BPAD_LEFT = ((20, 10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10, 20), (10, 20))
TOP_FONT = ("Tw Cen MTfont", 15, "bold")
BUTTON_FONT = ("Bahnschrift SemiLight SemiConde", 10)
HEADER_FONT = ("HP Simplified", 20, "bold")
LEFT_FONT = ("Dubai Medium", 15, "bold")
TITLE_FONT = ("Yu Gothic UI Light", 40)

image_file = rightCam
timer = 0
speed = 0
active_features = []
obstacles = []
technician_password_entry = ""
technician_password_answer = [ 1, 3]

#Obstructions
OFront = False
OBack = False
OLeft = False
ORight = False

#features
CruiseControl = False
AdvDriAsSys = False
Park = False
Sec = False

if not os.path.isdir("./logs"):
    try:
        os.mkdir("./logs")
    except OSError:
        print("Could not create logs directory")
    else:
        print("Created logs directory")

logfile = open("./logs/ALSETLogData.log", "w")

if os.path.getsize("./logs/ALSETLogData.log") > 0:
    logfile.write("\n")

logfile.write("[" + datetime.now().strftime("%H:%M:%S") + "] System Ready.\n")



#defining the various popup windows
def software_popup(win):  #popup asking to update
    layout = [
        [
            sg.Text(
                "Software update available. Would you like to proceed with software update?"
            )
        ],
        [
            sg.Button("Yes", key="SoftwareYes", enable_events=True),
            sg.Button("No", key="SoftwareNo", enable_events=True)
        ],
    ]
    win = sg.Window("My Popup",
                    layout,
                    modal=True,
                    grab_anywhere=True,
                    enable_close_attempted_event=True)
    event, value = win.read()
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
    window.write_event_value(event, None)


def no_network_popup(win):  #no network available popup
    layout = [
        [sg.Text("No networks available. :(")],
        [sg.Button("ok", key="okButton", enable_events=True)],
    ]
    win = sg.Window("My Popup",
                    layout,
                    modal=True,
                    grab_anywhere=True,
                    enable_close_attempted_event=True)
    event, value = win.read()
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
    window.write_event_value(event, None)


def networks_popup(win):
    layout = [
        [sg.Text("There is a network available. Connect to it?")],
        [[[sg.Button(f'{i} ', key=i)] for i in network_list],
         sg.Button("Cancel", key="ConnectNo", enable_events=True)],
    ]
    win = sg.Window("My Popup",
                    layout,
                    modal=True,
                    grab_anywhere=True,
                    enable_close_attempted_event=True)
    event, value = win.read()
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
    window.write_event_value(event, None)


def securityTime(win):
    layout = [
        [sg.Text("How many minutes do you want the security timer to wait?")],
        [sg.Text('Time(in minutes):', size =(15, 1))],
        [sg.InputText(key='TimeyWimey')],
        [sg.Button("Submit", key="submitted", enable_events=True)]
         
    ]
    win = sg.Window("My Popup",
                    layout,
                    modal=True,
                    grab_anywhere=True,
                    enable_close_attempted_event=True)
    event, values = win.read()
    global timer
    timer += int(values['TimeyWimey'])
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
    window.write_event_value(event, None)


def technician_popup(win):
    layout = [
        [sg.Text("Please enter the ALSET technician password")],
        [sg.Input(key='_PWRD_')],
        [sg.Button('Confirm'), sg.Button('Exit')]
    ]
    win = sg.Window("Technician Popup", layout, modal=True, grab_anywhere=True, enable_close_attempted_event=True)
    event, values = win.read()
    global technician_password_entry
    technician_password_entry += values['_PWRD_']
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        event = "CANCEL"
    win.close()
    window.write_event_value(event, None)

def getActiveFeaturesString():
    return active_features
    #return f'{active_features[i]}' for i in range(len(active_features))


def getSpeed():
    return speed


def getObstacles():
    return obstacles


top_banner = [[
    sg.Text('ASLET' + ' ' * 64,
            font=TOP_FONT,
            background_color=DARK_HEADER_COLOR),
    sg.Text('Tuesday 9 June 2020',
            size=(40, 1),
            justification='r',
            font=TOP_FONT,
            background_color=DARK_HEADER_COLOR)
]]

top = [
    [
        sg.Text('User Interface',
                size=(32, 1),
                justification='c',
                pad=BPAD_TOP,
                font=TITLE_FONT)
    ],
    [sg.T("version 1.0")],
]

block_2 = [[sg.Text('Features', font=HEADER_FONT)],
           [sg.Button('Cruise Control', font=BUTTON_FONT)],
           [sg.Button('Advanced Driver Assistance System', font=BUTTON_FONT)],
           [sg.Button('Network Settings', font=BUTTON_FONT)],
           [sg.Button('Security', font=BUTTON_FONT)],
           [sg.Button('Software', font=BUTTON_FONT)],
           [sg.Button('Parking', font=BUTTON_FONT)],
           [sg.Button('Technician\'s Interface', font=BUTTON_FONT)],
           [sg.Button('Off', font=BUTTON_FONT)]]

block_4 = [[sg.Text('Display', font=HEADER_FONT)],
           [sg.Text('Speed: ', font=LEFT_FONT)],
           [sg.Text(getSpeed(), key='-speed-', font=LEFT_FONT)],
           [sg.Text('Obstructions: ', font=LEFT_FONT)],
           [sg.Text(getObstacles(), key='-obstacles-', font=LEFT_FONT)],
           [sg.Text('Active Features: ', font=LEFT_FONT)],
           [
               sg.Text(getActiveFeaturesString(),
                       key='-features-',
                       font=LEFT_FONT)
           ]]

layout = [[
    sg.Column(top_banner,
              size=(960, 60),
              pad=(0, 0),
              background_color=DARK_HEADER_COLOR)
], [sg.Column(top, size=(920, 90), pad=BPAD_TOP)],
          [
              sg.Column(block_2, size=(450, 320), pad=BPAD_LEFT),
              sg.Column(block_4, size=(450, 320), pad=BPAD_RIGHT)
          ]]

window = sg.Window('Dashboard PySimpleGUI-Style',
                   layout,
                   margins=(0, 0),
                   background_color=BORDER_COLOR,
                   no_titlebar=True,
                   grab_anywhere=True)



while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Off':
        break
    if event == 'Cruise Control':
        if CruiseControl == True:  #turn CC off
            CruiseControl = False
            logfile.write("[" + datetime.now().strftime("%H:%M:%S") +
                          "] Cruise Control deactivated.\n")
            active_features.remove('Cruise Control')
            window['-features-'].update(getActiveFeaturesString())

        else:  #turn CC on
              CruiseControl = True
              CC(vectorCC1)
              speed = vectorCC1[2]
              logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Cruise Control activated.\n")
              active_features.append('Cruise Control')
              window['-features-'].update(getActiveFeaturesString())
              window['-speed-'].update(getSpeed())

    if event == 'Advanced Driver Assistance System':
        if AdvDriAsSys == True:#turn ADAS off
            AdvDriAsSys = False
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Advanced Driver Assistance System deactivated.\n")
            active_features.remove('ADAS')
            obstacles.remove(obstructions_to_str(obstr_dataADAS1))
            window['-features-'].update(getActiveFeaturesString())
            window['-obstacles-'].update(getObstacles())
        else: #Turn ADAS on
            ADAS(vectorADAS1)
            AdvDriAsSys = True
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Advanced Driver Assistance System activated.\n")
            speed=vectorADAS1[1]
            active_features.append('ADAS')
            obstacles.append(obstructions_to_str(obstr_dataADAS1))
            window['-speed-'].update(getSpeed())
            window['-obstacles-'].update(getObstacles())
            window['-features-'].update(getActiveFeaturesString())
            window['-speed-'].update(getSpeed())
            window['-obstacles-'].update(getObstacles())
            window['-features-'].update(getActiveFeaturesString())

    if event == 'Network Settings':
        logfile.write("[" + datetime.now().strftime("%H:%M:%S") +
                      "] Network Settings opened.\n")
        sg.popup_timed('Loading available networks...')
        if not network_list:  #If no networks available
            no_network_popup(window)
        else:
            networks_popup(window)
    if event in network_list:  # Accept network connection
        sg.popup_timed('Connecting to network...')
        if isConnected:  #If car could could connect to network
            sg.popup('car connected.')
        else:
            sg.popup('car could not connect to network.')
    if event == 'ConnectNo':  # Decline network connection
        sg.popup('Connection to network cancelled')
        logfile.write("[" + datetime.now().strftime("%H:%M:%S") +
                      "] Connection to network cancelled.\n")

    if event == 'Security':
        if Sec == True:  #Turn FNAF off
            Sec = False
            logfile.write("[" + datetime.now().strftime("%H:%M:%S") +
                          "] Fortified Network Assurance Field deactivated.\n")
            active_features.remove('FNAF')
            window['-features-'].update(getActiveFeaturesString())
        else:  #Turn FNAF on
            Sec = True
            logfile.write("[" + datetime.now().strftime("%H:%M:%S") +
                          "] Fortified Network Assurance Field activated.\n")
            active_features.append('FNAF')
            window['-features-'].update(getActiveFeaturesString())
            securityTime(window)

            if minutes == timer:
                logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Secutity data sent to client phone app.\n")
            else:
                logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] I got here.\n")
 
            
            

    if event == 'Software':
        logfile.write("[" + datetime.now().strftime("%H:%M:%S") +
                      "] Software Settings opened.\n")
        window['-features-'].update(getActiveFeaturesString())
        software_popup(window)
    if event == "SoftwareYes":
        for i in range(1, 10000):
            if not sg.one_line_progress_meter('Software Update', i + 1, 10000,
                                              'Software update in progress'):
                break
    if event == "SoftwareNo":
        sg.popup('Software Update Cancelled')

    if event == 'Parking':
        speed = vectorPark4[0]
        if Park == True: #Turn Park off
            Park = False
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Automated Parking deactivated.\n")
            active_features.remove('Parking')
            window['-features-'].update(getActiveFeaturesString())
        #check speed
        if(speed>10 or speed<0):
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Parking failed due to invalid speed. \n")
        else: #turn Park on
            Park = True
            is_parking_path_clear(vectorPark4)
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Automated Parking activated.\n")
            active_features.append('Parking')
            window['-speed-'].update(getSpeed())
            window['-features-'].update(getActiveFeaturesString())
            
    if event == 'Technician\'s Interface':
        logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Technician\'s password prompted.\n")
        technician_popup(window)
        if technician_password_entry=="13":
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Technician\'s correct password entered.\n")
            logfile.close()
            log = open("./logs/ALSETLogData.log","r")
            print(log.read())
            logfile = open("./logs/ALSETLogData.log","w")
        else:
            logfile.write("["+datetime.now().strftime("%H:%M:%S")+ "] Technician\'s wrong password entered.\n")

logfile.close()
window.close()


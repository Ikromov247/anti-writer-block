import PySimpleGUI as sg
import os
import time

PATH = f"C:\\Users\\CheShire\\vscode\\anti-writers-block\\"
FONT="Arial 11"
DURATION = 5
ERASE_TIME = 10
IS_SAVED=False
IS_GAME_ON=False
last_modified=None
sg.theme('DarkAmber')

layout = [
        [sg.Button("Start"), sg.Text(text="00:00",key="-TIMER-")],
        
        [sg.Multiline(size=(50, 10), expand_x=True, expand_y=True, k="-MLINE-", font="Arial 11", enable_events=True)],
        
        [sg.ProgressBar(100, orientation='h', size=(50, 10), key="-PROGRESS-BAR-")],
        
        [sg.Text("File title: ", font=FONT, visible=False, key="-FILE-TITLE-LABEL", enable_events=True), 
         sg.Text('demo.txt',  font=FONT, visible=False,key="-FILE-TITLE-", enable_events=True),
         sg.Button("Save", visible=False, key="-SAVE-BUTTON-", enable_events=True)]
    ]



"""Functions"""
def time_as_str(sec):
    mins = sec//60
    secs = int(sec%60)
    return f"0{mins}:{secs}" if secs>10 else f"0{mins}:0{secs}"

def time_as_int():
    return int(time.time())

# Create the Window
window = sg.Window('Writer\'s hell', layout, size=(500, 400))



while True:
    if IS_GAME_ON:
        event, values = window.read(timeout=100)
        no_change_time=0
        
        if last_modified is None:
            window['-PROGRESS-BAR-'].update(100)
            last_modified=int(time.time())
        
        "update last_modified only when change is detected"
        
        if event=="-MLINE-":
            last_modified=int(time.time())
            
        current_time=time_as_int()
        time_left = DURATION-(current_time-start_time)
        
        
        if time_left>=0:
            window["-TIMER-"].update(time_as_str(time_left))
            no_change_time=current_time-last_modified
            window["-PROGRESS-BAR-"].update(100-10*no_change_time)
        if no_change_time>10 and time_left>0:
            window["-MLINE-"].update(" ")

        if time_left<=1:
            window["-FILE-TITLE-LABEL"].update(visible=True)
            window["-FILE-TITLE-"].update(visible=True)
            window["-SAVE-BUTTON-"].update(visible=True)

        if event=="-SAVE-BUTTON-":
            print("button pressed")
            txt = values["-MLINE-"]
            title = "demo_"+txt[4]+".txt" if len(txt)>5 else "demo.txt"
            fold_or_file = sg.popup_get_folder("Choose your folder", 
                                            keep_on_top=True, 
                                            default_path=PATH+f"{title}")
            with open(PATH+title, "w") as f:
                f.write(str(txt))
                IS_SAVED=True
            
    
    else:
        start_time = int(time.time())
        
        event, values = window.read(timeout=1000)

        if event=="Start":
            timer = window["-TIMER-"]
            timer.update(time_as_str(DURATION))
            IS_GAME_ON=True
    
    if event==sg.WIN_CLOSED:
        break

window.close()
import threading
from universal import config
import json
from tkinter.filedialog import asksaveasfile
import pyautogui
import keyboard
from control.JSON_lingualizer import JSON_lingualizer, lang_to_json

from time import sleep
from PIL import Image
import time


def save_events(app):
    try:
        events = app.textbox.get('0.0', 'end')
        events = lang_to_json(events)
        events = add_id(events)
        app.exception_display(None)
        config.actions = events
        clean_data(app)

        return config.actions
    
    except Exception as ex:

        app.exception_display(ex)
        return 0


def clean_data(app):

    config.actions = add_id(config.actions)

    app.textbox.delete('0.0', 'end')
    app.textbox.insert('0.0', JSON_lingualizer(config.actions))


def insert_event(event, app):
    if event:
        config.actions.append(event)

    clean_data(app)


def add_id(events):

    for (i, event) in enumerate(events):
        new_event = dict(event)
        new_event['id'] = i + 1
        events[i] = new_event

    return events


def export_as_json(app):
    try:
        actions = save_events(app)
        if actions:
            files = [('JSON file', '*.json')]
            file = asksaveasfile(filetypes=files,
                                 defaultextension=files)
            if file:
                json.dump(actions, file, indent=4)
                file.close()
    except Exception as ex:

        app.exception_display(ex)


def play_recorded_event(app):
    
    global thread
    
    actions = save_events(app)
    
    if not actions:
        return

    if 'thread' not in globals():
        thread = threading.Thread(target=PlayRecorded()._try_playing, args=(app, ), daemon=True)
        thread.start()
    else:
        app.main_button.configure(text="Start execution")
        del globals()['thread']
        

class PlayRecorded():
    
    def _try_playing(self, app):
        
        app.main_button.configure(text="Stop execution")
        
        try:
            self.play_recorded()
        except Exception as ex:
            app.exception_display(ex)

        app.main_button.configure(text="Start execution")
            
    
    def play_recorded(self):

        i = 0
        
        # Does what's recorded

        for action in config.actions:
            for (key, value) in action.items():

                position = value

                # For moving

                if key == 'move':

                    i += 1

                    pyautogui.moveTo(position['x'], position['y'],
                                    config.Move_Speed,
                                    pyautogui.easeOutQuad)
                elif key == 'left_click':

                # For left Clicking

                    i += 1
                    pyautogui.click(button='left')
                    current_position = {}

                    # Saves position

                    (x, y) = pyautogui.position()
                    current_position['x'] = x
                    current_position['y'] = y
                elif key == 'right_click':

                # For right Clicking

                    i += 1
                    pyautogui.click(button='right')
                    current_position = {}

                    # Saves position

                    (x, y) = pyautogui.position()
                    current_position['x'] = x
                    current_position['y'] = y
                elif key == 'drag':

                # For dragging with cursor

                    i += 1

                    pyautogui.dragTo(position['x'], position['y'],
                                    config.Drag_Speed)
                elif key == 'write':

                # For text display

                    i += 1

                    pyautogui.write(action['write'],
                                    interval=config.Type_Speed)
                elif key == 'image':

                # For screen search

                    i += 1

                    Image.open(action['image']).convert('RGB'
                            ).save(r"assets\images\images.png")

                    pyautogui.DetectImage(r"assets\images\images.png")
                elif key == 'sleep':

                # For wait

                    i += 1

                    sleep(action['sleep'])
                elif key == 'hotkey':

                # For hotkey input

                    i += 1

                    for current_key in action['hotkey']:
                        keyboard.press(current_key)
                    for current_key in action['hotkey']:
                        keyboard.release(current_key)
                        
                elif key == 'key':

                # For key input

                    i += 1

                    # Clicks key

                    time.sleep(0.3)
                    keyboard.send(action['key'])

                elif key == 'wait_key':
                    i += 1
                    keyboard.wait(action['wait_key'])
                
                elif key == 'id':
                    pass
                    
                else:
                    raise KeyError(f"Invalid action'{action}'")
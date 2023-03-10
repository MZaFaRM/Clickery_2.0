import views.dialogs.dialogs as dialogs
from views.dialogs.directory import folder
from control.pickler import insert_event, save_events
import pyautogui
import keyboard

class MouseEventControl():

    def _perses(self, event = None, app=None):
        # input is given by the hook function
        # function returns a "KeyboardEvent(<key>(shift) <state>(up))"
        # therefore parses key to be clicked [shift]
        
        if event.event_type == "down":
            # filters 'key up' and 'key down'
            if event.name == "1":
                action = self.mouse_move_event()
            elif event.name == "2":
                action = self.left_click_event()
            elif event.name == "3":
                action = self.right_click_event()
            elif event.name == "4":
                action = self.mouse_drag_event()
            else:
                print(event.name)
                return
            
            if action:
                return insert_event(action, app)
            
    
    # For moving cursor
    def mouse_move_event(self):

        # Declares dictionaries
        action = {}
        current_position = {}

        # Saves position
        x, y = pyautogui.position()
        current_position["x"] = x
        current_position["y"] = y

        # Saves action
        action["move"] = current_position

        return action

    def left_click_event(self):

        # Declares dictionaries
        action = {}

        # Saves action
        action["left_click"] = 1

        return action

    def right_click_event(self):

        # Declares dictionaries
        action = {}

        # Saves action
        action["right_click"] = 1

        return action
    
    def mouse_drag_event(self):

        # Declares dictionaries
        action = {}
        current_position = {}

        # Saves position
        x, y = pyautogui.position()
        current_position["x"] = x
        current_position["y"] = y

        # Saves action
        action["drag"] = current_position

        return action
            
    def mouse_event(self, app=None):
            
        keys = [1, 2, 3, 4]
        [keyboard.hook_key(str(key), lambda event: self._perses(app=app, event=event)) for key in keys]


def key_input_dialog_event(app):
    dialog = dialogs.KeyInputDialog(text="Input a key:", title="Key Input")
    input_text = dialog.get_input()
    if input_text:
        save_events(app)
        return insert_event({"key": input_text}, app)
    return 0


def wait_key_dialog_event(app):
    dialog = dialogs.KeyInputDialog(text="Input a key to wait for:", title="Key Input")
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return insert_event({"wait_key": input_text}, app)
    return 0


def hotkey_input_dialog_event(app):
    dialog = dialogs.HotKeyInputDialog(
        text="Insert keyboard shortcut:", title="Keyboard Shortcut"
    )
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return insert_event({"hotkey": input_text}, app)
    return 0


def delay_option(value, app):
    if value == "- Key":
        return wait_key_dialog_event(app)

    elif value == "- Seconds":
        return wait_time_event(app)

    elif value == "- Image":
        ftypes = [("png files", "*.png"), ("All files", "*")]
        location = folder(ftypes)
        if location:
            return insert_event({"image": location}, app)
    return 0


def text_input_dialog_event(app):
    dialog = dialogs.TextInputDialog(text="Write the text here:", title="Text Insert")
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return insert_event({"write": input_text}, app)
    return 0


def wait_time_event(app):

    # gets input
    dialog = dialogs.WaitTimeDialog(
        text="Time to wait in seconds:", title="Wait for time"
    )
    time = dialog.get_input()
    if time:
        time = int(time)
        print("InputDialog:", time)
        return insert_event({"wait": time}, app)
    else:
        return 0


def remove_action_event(app):
    dialog = dialogs.RemoveActionDialog(
        text="Remove from ID:", text_1="Removing till ID:", title="Remove Actions"
    )
    action_id = dialog.get_input()
    if action_id:
        from universal import config
        # get the index of the element from the list based on user's input
        action_id_1 = config.actions.index(find(config.actions, action_id[0]))
        action_id_2 = config.actions.index(find(config.actions, action_id[1]))
        del config.actions[action_id_1 : action_id_2 + 1]
        print("InputDialog:", action_id)
        return insert_event(None, app)
    return 0


def duplicate_action_event(app):
    dialog = dialogs.DuplicateActionDialog(
        text="Number of times to repeat:",
        text_1="Duplicate from ID:",
        text_2="Duplicate till ID:",
        text_3="Insert After:",
        title="Duplicate Actions",
    )
    action_id = dialog.get_input()
    
    if action_id:
        
        from universal import config
        # slice and get the part ot repeat
        index_from = find(config.actions, action_id[1])
        index_to = find(config.actions, action_id[2])
        
        to_repeat = config.actions[config.actions.index(index_from): config.actions.index(index_to) + 1]

        to_repeat *= action_id[0]
        
        # gets the elements from the list
        action = find(config.actions, action_id[3])
        
        if action:       
            # gets the id of the element
            id_index = config.actions.index(action)
            
        else:      
            id_index = 0
        
        # insert action back to list
        for action in reversed(to_repeat):
            config.actions.insert(id_index, action)
            
        print("InputDialog:", action_id)
        return insert_event(None, app)
    return 0


def find(actions, action_id=None):
    for item in actions:
        if item["id"] == action_id:
            return item
    return 0
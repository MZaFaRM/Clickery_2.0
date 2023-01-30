from tkinter.filedialog import asksaveasfile
from keyboard import normalize_name
import pyautogui
import views.dialogs.dialogs as dialogs
from views.dialogs.directory import folder
from universal import config
import json


def key_input_dialog_event():
    dialog = dialogs.KeyInputDialog(text="Input a key:", title="Key Input")
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return {"key": input_text}
    return 0


def wait_key_dialog_event():
    dialog = dialogs.KeyInputDialog(text="Input a key to wait for:", title="Key Input")
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return {"wait_key": input_text}
    return 0


def hotkey_input_dialog_event():
    dialog = dialogs.HotKeyInputDialog(
        text="Insert keyboard shortcut:", title="Keyboard Shortcut"
    )
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return {"hotkey": input_text}
    return 0


def delay_option(value=""):
    if value == "- Key":
        return wait_key_dialog_event()
    
    elif value == "- Seconds":
        return wait_time_event()
    
    elif value == "- Image":
        ftypes = [("png files", "*.png"), ("All files", "*")]
        location = folder(ftypes)
        if location:
            return {"image": location}
    return 0


def text_input_dialog_event():
    dialog = dialogs.TextInputDialog(text="Write the text here:", title="Text Insert")
    input_text = dialog.get_input()
    if input_text:
        print("InputDialog:", input_text)
        return {"hotkey": input_text}
    return 0


def wait_time_event():

    # gets input
    dialog = dialogs.WaitTimeDialog(text="Time to wait in seconds:", title="Wait for time")
    time = int(dialog.get_input())
    if time:
        print("InputDialog:", time)
        return {"hotkey": time}
    else:
        return 0



# class ToModify:
#     # For moving cursor
#     def MoveCursor():

#         # Declares dictionaries
#         action = {}
#         current_position = {}

#         # Saves position
#         x, y = pyautogui.position()
#         current_position["x"] = x
#         current_position["y"] = y

#         # Saves action
#         action["move"] = current_position

#         return action

#     def LeftClickCursor():

#         # Declares dictionaries
#         action = {}

#         # Saves action
#         action["l-click"] = 1

#         return action

#     def RightClickCursor():

#         # Declares dictionaries
#         action = {}

#         # Saves action
#         action["r-click"] = 1

#         return action

#     def Pop(id=0):

#         if not id:
#             # Delete last action
#             try:
#                 delete = config.record.pop()

#             except IndexError:
#                 align_text(
#                     "[#D2001A italic]No actions to remove",
#                     "",
#                     ":cross_mark:",
#                     increment="None",
#                 )

#                 return
#         else:
#             delete = config.record.pop(id - 1)

#         align_text(
#             f"[#7D9D9C italic]{delete}",
#             "removed",
#             ":wilted_flower:",
#             description_style=False,
#             increment="Negative",
#         )

#     def DragCursor():

#         # Declares dictionaries
#         action = {}
#         current_position = {}

#         # Saves position
#         x, y = pyautogui.position()
#         current_position["x"] = x
#         current_position["y"] = y

#         # Saves action
#         action["drag"] = current_position

#         return action

#     def TakeScreenshot():
#         # Declares dictionaries
#         action = {}

#         files = [("image files", "*.png")]
#         file = asksaveasfile(filetypes=files, defaultextension=files)

#         # Checks if the user provided a location
#         if file:

#             # 'file' is an io.TextWrapper
#             # Take screenshot and save it to the given location
#             location = file.name
#             file.close()
#             # os.remove(location)
#             action["screenshot"] = location

#             # Saving to config
#             return action

#         else:
#             return 0

from keyboard import hook, unhook_all
from sample.helpers.dir import InputDialogueBox
import tkinter


key_clicked = ""
tyr = 1


def _save_key_Input(screen):
    # if user clicked on button assign keys displayed to return
    global returning_key
    global key_clicked

    returning_key = key_clicked

    screen.quit()
    screen.destroy()


def return_key_input():
    # this function is called by main to get the key_input
    global returning_key
    global key_clicked

    returning_key = ""
    # inititates window
    _Inserted_Key_window()
    # stops recording keyboard input
    unhook_all()
    # If save button clicked return data
    if returning_key:

        _returning_key = returning_key
        returning_key = ""

        return _returning_key
    # else do nothing
    return 0


def _perses(input):
    # input is given by the hook function
    # function returns a "KeyboardEvent(<key>(shift) <state>(up))"
    # therefore parses key to be clicked [shift]
    global key_clicked
    global tyr

    if tyr:
        tyr = 0
        # filters 'key up' and 'key down'

        key_clicked = key_input = str(input.name)

        # formats the 'input' to only have the key name
        InsertedKey.config(state="normal")
        InsertedKey.delete(0, "end")

        # for visuals key is capitalised
        # letter input are not capitalized
        if len(key_input) == 1:
            InsertedKey.insert(0, key_input)
        else:
            key_input = key_input.upper()
            InsertedKey.insert(0, key_input)

        InsertedKey.config(state="disabled")

    else:
        tyr = 1


def _Inserted_Key_window():

    # window of 'key insert'
    global InsertedKey

    tkwindow = InputDialogueBox()

    main_window = tkwindow.initialise_window(title="Insert Key")
    insertkey_frame, frame = tkwindow.main_frame(main_window, heading="      ENTER KEY")

    # label for text box
    InsertedKey_label = tkinter.Label(insertkey_frame, text="INSERT KEY")
    InsertedKey_label.configure(justify="center")
    InsertedKey = tkinter.Entry(insertkey_frame)

    InsertedKey_label.grid(row=1, column=2, pady=10, padx=75, columnspan=3)
    InsertedKey.grid(row=2, column=2, padx=75)
    InsertedKey.configure(
        background=tkwindow.ContentColor, foreground=tkwindow.TextColor
    )
    InsertedKey_label.configure(
        background=tkwindow.ContentColor, foreground=tkwindow.TextColor
    )
    InsertedKey.configure(
        justify="center",
        disabledforeground="white",
        disabledbackground=tkwindow.ContentColor,
        borderwidth=2,
    )

    # configures button
    button = tkinter.Button(
        frame, text="CONFIRM", command=lambda: _save_key_Input(main_window)
    )

    tkwindow.configure_button(button)

    # Records all keyboard activites
    hook(_perses)

    tkwindow.configure_window(main_window)

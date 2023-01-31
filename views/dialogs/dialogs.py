from keyboard import hook, unhook_all, normalize_name
from typing import Union, Tuple, Optional
import customtkinter
from universal import config


class BaseDialog(customtkinter.CTkToplevel):
    def __init__(
        self,
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        text_color: Optional[Union[str, Tuple[str, str]]] = None,
        button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
        button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
        entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
        entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,
        title: str = "CTkDialog",
        text: str = "CTkDialog",
        text_1: str = "CTkDialog"
    ):

        super().__init__(fg_color=fg_color)

        self._fg_color = (
            customtkinter.ThemeManager.theme["CTkToplevel"]["fg_color"]
            if fg_color is None
            else self._check_color_type(fg_color)
        )
        self._text_color = (
            customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
            if text_color is None
            else self._check_color_type(button_hover_color)
        )
        self._button_fg_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]
            if button_fg_color is None
            else self._check_color_type(button_fg_color)
        )
        self._button_hover_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]
            if button_hover_color is None
            else self._check_color_type(button_hover_color)
        )
        self._button_text_color = (
            customtkinter.ThemeManager.theme["CTkButton"]["text_color"]
            if button_text_color is None
            else self._check_color_type(button_text_color)
        )
        self._entry_fg_color = (
            customtkinter.ThemeManager.theme["CTkEntry"]["fg_color"]
            if entry_fg_color is None
            else self._check_color_type(entry_fg_color)
        )
        self._entry_border_color = (
            customtkinter.ThemeManager.theme["CTkEntry"]["border_color"]
            if entry_border_color is None
            else self._check_color_type(entry_border_color)
        )
        self._entry_text_color = (
            customtkinter.ThemeManager.theme["CTkEntry"]["text_color"]
            if entry_text_color is None
            else self._check_color_type(entry_text_color)
        )

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._text = text
        self._text_1 = text_1

        self.title(title)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(
            10, self._create_widgets
        )  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def _create_widgets(self):

        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._label = customtkinter.CTkLabel(
            master=self,
            width=300,
            wraplength=300,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text,
        )
        self._label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self._entry = customtkinter.CTkEntry(
            master=self,
            width=230,
            fg_color=self._entry_fg_color,
            border_color=self._entry_border_color,
            text_color=self._entry_text_color,
        )
        self._entry.grid(
            row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew"
        )

        self._ok_button = customtkinter.CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Ok",
            command=self._ok_event,
        )
        self._ok_button.grid(
            row=2, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew"
        )

        self._cancel_button = customtkinter.CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Cancel",
            command=self._cancel_event,
        )
        self._cancel_button.grid(
            row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew"
        )

        self.after(
            150, lambda: self._entry.focus()
        )  # set focus to entry with slight delay, otherwise it won't work
        self._entry.bind("<Return>", self._ok_event)

    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        self._user_input = None
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input

    def verification(self, message=""):
        self._entry.configure(text_color="red")
        self._entry.delete(0, "end")
        self._entry.insert(0, message)
        self.after(
            1000,
            lambda: (
                self._entry.configure(text_color=self._entry_text_color),
                self._entry.delete(0, "end"),
            ),
        )


# Granchildren
class TextInputDialog(BaseDialog, customtkinter.CTkToplevel):
    def _create_widgets(self):

        BaseDialog._create_widgets(self)

        self._entry = customtkinter.CTkTextbox(self, width=250)
        self._entry.grid(
            row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew"
        )

    def _ok_event(self, event=None):
        self._user_input = self._entry.get(1.0, "end-1c")
        self.grab_release()
        self.destroy()


class HotKeyInputDialog(BaseDialog, customtkinter.CTkToplevel):
    def _create_widgets(self):
        BaseDialog._create_widgets(self)
        self._entry.configure(state="disabled", justify="center")
        # List of keys
        self.hotkeyList = []
        # Records keyboard events
        hook(lambda event: self._perses(event, self._entry))

    def _ok_event(self, event=None):
        self._user_input = self.hotkeyList
        unhook_all()
        self.grab_release()
        self.destroy()

    def _on_closing(self):
        unhook_all()
        self.grab_release()
        self.destroy()

    def _cancel_event(self):
        unhook_all()
        self.grab_release()
        self.destroy()

    def _perses(self, input, _inputbox):
        # input is given by the hook function
        # function returns a "KeyboardEvent(<key>(shift) <state>(up))"
        # therefore parses key to be clicked [shift]

        if input.event_type == "down":
            # filters 'key up' and 'key down'

            key_input = str(normalize_name(input.name))

            self.hotkeyList.append(key_input)

            # formats the 'input' to only have the key name
            _inputbox.configure(state="normal")
            _inputbox.delete(0, "end")
            _inputbox.insert(0, " + ".join(self.hotkeyList))
            _inputbox.configure(state="disabled")


class KeyInputDialog(HotKeyInputDialog, customtkinter.CTkToplevel):
    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        unhook_all()
        self.grab_release()
        self.destroy()

    def _perses(self, input, _inputbox):
        # input is given by the hook function
        # function returns a "KeyboardEvent(<key>(shift) <state>(up))"
        # therefore parses key to be clicked [shift]

        if input.event_type == "down":
            # filters 'key up' and 'key down'

            key_input = str(normalize_name(input.name))

            # formats the 'input' to only have the key name
            _inputbox.configure(state="normal")
            _inputbox.delete(0, "end")
            _inputbox.insert(0, key_input)
            _inputbox.configure(state="disabled")


class WaitTimeDialog(BaseDialog, customtkinter.CTkToplevel):
    def _ok_event(self, event=None):
        self._user_input = self._entry.get()

        if self._user_input.isdigit():
            self.grab_release()
            self.destroy()

        else:
            self.verification(message="Value Error")


class RemoveActionDialog(WaitTimeDialog, BaseDialog, customtkinter.CTkToplevel):
    def _ok_event(self, event=None):
        self._user_input = self.action_id.get()

        if not self._user_input.isdigit():
            self.verification(message="Value Error")

        elif int(self._user_input) >= len(config.actions) or int(self._user_input) < 0:
            self.verification(message="Index Error")
        else:
            self.grab_release()
            self.destroy()


# if __name__ == "__main__":
#     dialog = (text="ID of action to move:", text_1="Index of destination:", title="Move Action")
#     print("CTkInputDialog:", dialog.get_input())

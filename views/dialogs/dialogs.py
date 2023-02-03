from keyboard import hook, unhook_all, normalize_name
from typing import Union, Tuple, Optional
import customtkinter
from views.dialogs import components
from universal import config

# from universal import config


# Granchildren
class TextInputDialog(components.BaseDialog, customtkinter.CTkToplevel):
    def _create_widgets(self):

        components.BaseDialog._create_widgets(self)

        self._entry = customtkinter.CTkTextbox(self, width=250)
        self._entry.grid(
            row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew"
        )

    def _ok_event(self, event=None):
        self._user_input = self._entry.get(1.0, "end-1c")
        self.grab_release()
        self.destroy()


class HotKeyInputDialog(components.BaseDialog, customtkinter.CTkToplevel):
    def _create_widgets(self):
        components.BaseDialog._create_widgets(self)
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


class WaitTimeDialog(components.BaseDialog, customtkinter.CTkToplevel):
    def _ok_event(self, event=None):
        self._user_input = self._entry.get()

        if self._user_input.isdigit():
            self.grab_release()
            self.destroy()

        else:
            self.return_error(message="Value Error")


class RemoveActionDialog(components.BaseDialog, customtkinter.CTkToplevel):
    def _create_widgets(self):

        # self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self._label = customtkinter.CTkLabel(
            master=self._frame,
            width=150,
            wraplength=150,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text,
        )
        self._label.grid(
            row=0, column=0, columnspan=1, padx=(20, 0), pady=(30, 10), sticky="ew"
        )

        self._spinbox_frame = customtkinter.CTkFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        self._spinbox_frame.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 20),
            pady=(30, 10),
        )
        self._spinbox = components.BaseDialog.customSpinBox(
            self, self._spinbox_frame, type="int"
        )

        self._label_1 = customtkinter.CTkLabel(
            master=self._frame,
            width=100,
            wraplength=150,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text_1,
        )
        self._label_1.grid(
            row=1, column=0, columnspan=1, padx=(20, 0), pady=(10, 30), sticky="ew"
        )

        self._spinbox_frame_1 = customtkinter.CTkFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        self._spinbox_frame_1.grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 20),
            pady=(10, 30),
        )
        self._spinbox_1 = components.BaseDialog.customSpinBox(
            self, self._spinbox_frame_1, type="int"
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
            150, lambda: self._spinbox.focus()
        )  # set focus to entry with slight delay, otherwise it won't work
        # self._entry.bind("<Return>", self._ok_event)
        
    def _ok_event(self):
        
        self._user_input = self.verify()
        
        if self._user_input:
            
            self.grab_release()
            self.destroy()
            
        
    def verify(self):
        
        self.widgets = [self._spinbox, self._spinbox_1]
        
        self._entry = self._spinbox.get()
        self._entry_1 = self._spinbox_1.get()
        
        if not self._entry.isdigit() or not self._entry_1.isdigit():
            return self.return_error(message="Type Error", widgets=self.widgets)
            
        self._entry = int(self._entry)
        self._entry_1 = int(self._entry_1)
        
        self.return_value = (self._entry, self._entry_1)
            
        if self._entry_1 < self._entry:
            return self.return_error(message="Index Error", widgets=self.widgets)
        if self._entry <= -1:
            return self.return_error(message="Index Error", widgets=self.widgets)
        if self._entry > len(config.actions) or self._entry_1 > len(config.actions):
            return self.return_error(message="Index Error", widgets=self.widgets)
            
        return self.return_value
    
    def return_error(self, message="", widgets = None):
        
        [item.configure(text_color="red") for item in widgets]
        [item.delete(0, "end") for item in widgets]
        [item.insert(0, message) for item in widgets]
        [item.configure(text_color="red") for item in widgets]

        self.after(
            1000,
            lambda: (
                [item.configure(text_color=self._entry_text_color) for item in widgets],
                [item.delete(0, "end") for item in widgets]
            ),
        )
            
            
class DuplicateActionDialog(RemoveActionDialog, components.BaseDialog, customtkinter.CTkToplevel):
    def _create_widgets(self):

        # self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self._label = customtkinter.CTkLabel(
            master=self._frame,
            width=150,
            wraplength=150,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text,
        )
        self._label.grid(
            row=0, column=0, columnspan=1, padx=(20, 0), pady=(30, 10), sticky="ew"
        )

        self._spinbox_frame = customtkinter.CTkFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        self._spinbox_frame.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 20),
            pady=(30, 10),
        )
        self._spinbox = components.BaseDialog.customSpinBox(
            self, self._spinbox_frame, type="int"
        )

        self._label_1 = customtkinter.CTkLabel(
            master=self._frame,
            width=100,
            wraplength=150,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text_1,
        )
        self._label_1.grid(
            row=1, column=0, columnspan=1, padx=(20, 0), pady=(10, 10), sticky="ew"
        )

        self._spinbox_frame_1 = customtkinter.CTkFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        self._spinbox_frame_1.grid(
            row=1,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 20),
            pady=(10, 10),
        )
        self._spinbox_1 = components.BaseDialog.customSpinBox(
            self, self._spinbox_frame_1, type="int"
        )
        
        self._label_2 = customtkinter.CTkLabel(
            master=self._frame,
            width=150,
            wraplength=150,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text_2,
        )
        self._label_2.grid(
            row=2, column=0, columnspan=1, padx=(20, 0), pady=(10, 10), sticky="ew"
        )

        self._spinbox_frame_2 = customtkinter.CTkFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        self._spinbox_frame_2.grid(
            row=2,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 20),
            pady=(10, 10),
        )
        self._spinbox_2 = components.BaseDialog.customSpinBox(
            self, self._spinbox_frame_2, type="int"
        )

        self._label_3 = customtkinter.CTkLabel(
            master=self._frame,
            width=100,
            wraplength=150,
            fg_color="transparent",
            text_color=self._text_color,
            text=self._text_3,
        )
        self._label_3.grid(
            row=3, column=0, columnspan=1, padx=(20, 0), pady=(10, 30), sticky="ew"
        )

        self._spinbox_frame_3 = customtkinter.CTkFrame(
            self._frame, corner_radius=0, fg_color="transparent"
        )
        self._spinbox_frame_3.grid(
            row=3,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(0, 20),
            pady=(10, 30),
        )
        self._spinbox_3 = components.BaseDialog.customSpinBox(
            self, self._spinbox_frame_3, type="int"
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
            row=4, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew"
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
            row=4, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew"
        )

        self.after(
            150, lambda: self._spinbox.focus()
        )  # set focus to entry with slight delay, otherwise it won't work
        
        
        # self._entry.bind("<Return>", self._ok_event)
    
        
    def _ok_event(self):
        
        self._user_input = self.verify()
        
        if self._user_input:
            
            self.grab_release()
            self.destroy()
            
        
    def verify(self):
        
        self.widgets = [self._spinbox, self._spinbox_1, self._spinbox_2, self._spinbox_3]
        
        try:
            self._entry =   int(self._spinbox.get())
            self._entry_1 = int(self._spinbox_1.get())
            self._entry_2 = int(self._spinbox_2.get())
            self._entry_3 = int(self._spinbox_3.get())
            self.return_value = (self._entry, self._entry_1, self._entry_2, self._entry_3)
            
        except OSError:
            
            return self.return_error(message="Type Error", widgets=self.widgets)
            
        if self._entry_1 > self._entry_2:
            return self.return_error(message="Index Error", widgets=self.widgets)
        if self._entry_1 <= -1:
            return self.return_error(message="Index Error", widgets=self.widgets)
        if self._entry_1 > len(config.actions) or self._entry_2 > len(config.actions):
            return self.return_error(message="Index Error", widgets=self.widgets)
            
        return self.return_value

if __name__ == "__main__":
    dialog = RemoveActionDialog(
        text="ID of action to move:",
        text_1="Index of destination:",
        title="Move Action",
    )
    print("CTkInputDialog:", dialog.get_input())

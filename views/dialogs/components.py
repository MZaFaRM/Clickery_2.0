import customtkinter
from typing import Union, Tuple, Optional


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
        text_1: str = "CTkDialog",
        text_2: str = "CTkDialog",
        text_3: str = "CTkDialog",
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
        self._text_2 = text_2
        self._text_3 = text_3

        self.title(title)
        self.lift()  # lift window on top
        # self.attributes("-topmost", True)  # stay on top
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
        
    def customSpinBox(self, frame, type="int"):
        
        self._spinbox_frame = frame

        self._spinbox_frame.grid_columnconfigure(
            (0, 2), weight=0
        )  # buttons don't expand
        self._spinbox_frame.grid_columnconfigure(1, weight=1)  # entry expands
        self._spinbox_frame.grid_rowconfigure(0, weight=1)
        entry = customtkinter.CTkEntry(
            self._spinbox_frame, width=75, height=26, border_width=0, justify="center"
        )
        self.subtract_button = customtkinter.CTkButton(
            self._spinbox_frame,
            text="-",
            width=32 - 6,
            command=lambda: self.subtract_button_event(entry),
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        entry.insert(0, "0")
        
        entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        
        self.add_button = customtkinter.CTkButton(
            self._spinbox_frame,
            text="+",
            width=32 - 6,
            height=32 - 6,
            command=lambda: self.add_button_event(entry)
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        
        return entry

    def add_button_event(self, entry):
        try:
            value = int(entry.get()) + 1
            entry.delete(0, "end")
            entry.insert(0, value)
        except ValueError:
            return
        
        
    def subtract_button_event(self, entry):
        value = int(entry.get())
        if value > 0:
            try:
                value = int(entry.get()) - 1
                entry.delete(0, "end")
                entry.insert(0, value)
            except ValueError:
                return

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

    def return_error(self, message=""):

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
                
        return 0


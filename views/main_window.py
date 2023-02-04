
import tkinter
import tkinter.messagebox
import customtkinter
from control import general
import sys
from control import pickler
import keyboard

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("main.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0 , 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Clickery 2.0",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(50, 50))

        self.TextInput = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Text Input",
            command=lambda: general.text_input_dialog_event(self),
        )
        self.TextInput.grid(row=1, column=0, padx=20, pady=10)

        # Option menu
        self.DelayOperation = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["- Seconds", "- Image", "- Key"],
            command=self.delay_option,
            variable=customtkinter.StringVar(value="Delay"),
            anchor="center",
        )
        self.DelayOperation.grid(row=2, column=0, padx=20, pady=10)

        self.KeyInput = customtkinter.CTkButton(
            self.sidebar_frame,
            command=lambda: general.key_input_dialog_event(self),
            text="Insert Key",
        )
        self.KeyInput.grid(row=3, column=0, padx=20, pady=10)
        self.HotkeyInput = customtkinter.CTkButton(
            self.sidebar_frame,
            command=lambda: general.hotkey_input_dialog_event (self),
            text="Insert Hotkey",
        )
        self.HotkeyInput.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )


        self.mouse_functions = customtkinter.CTkSwitch(
            self.sidebar_frame, text="Track Mouse", command=self.mouse_event
        )
        self.mouse_functions.grid(row=5, column=0, pady=10, padx=20, sticky="n")
        
        
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, wrap="word")
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew", rowspan=4)
        
        
        # create main entry and button
        self.exception_field = customtkinter.CTkTextbox(self, wrap="word")
        self.exception_field.grid(
            row=3, column=2, padx=(20, 20), pady=(0, 20), sticky="nsew"
        )

        self.main_button = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            text="Start Execution",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=lambda: pickler.play_recorded_event(self)
        )
        self.main_button.grid(
            row=2, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Save")
        self.tabview.add("Modify")
        self.tabview.add("Export")
        
        self.tabview.tab("Save").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Modify").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Export").grid_columnconfigure(0, weight=1)

        self.clean_data_event = customtkinter.CTkButton(
            self.tabview.tab("Save"),
            text="Clean data",
            command=lambda: pickler.clean_data(self)
        )
        self.clean_data_event.grid(row=0, column=0, padx=20, pady=(30, 10))
        
        self.input_save_event = customtkinter.CTkButton(
            self.tabview.tab("Save"),
            text="Save",
            command=lambda: pickler.save_events(self)
        )
        self.input_save_event.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        self.input_duplicate_event = customtkinter.CTkButton(
            self.tabview.tab("Modify"),
            text="Duplicate action",
            command=lambda: general.duplicate_action_event(self)
        )
        self.input_duplicate_event.grid(row=1, column=0, padx=20, pady=(30, 10))
        
        self.export_as_json_event = customtkinter.CTkButton(
            self.tabview.tab("Export"),
            text="JSON",
            command=lambda: pickler.export_as_json(self)
        )
        self.export_as_json_event.grid(row=0, column=0, padx=20, pady=(30, 10))

        self.input_remove_event = customtkinter.CTkButton(
            self.tabview.tab("Modify"),
            text="Remove action",
            command=lambda: general.remove_action_event(self)
        )
        self.input_remove_event.grid(row=2, column=0, padx=20, pady=(10, 10))

        # set default values
        self.mouse_functions.deselect()
        self.toggle = False
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert(
            "0.0",
            "[{\"wait_key\":\"caps lock\",\"id\": 1},{\"key\": \"esc\",\"id\": 2}]",
        )
        self.exception_field.configure(state="disabled")
    
        
    def mouse_event(self):

        if not self.toggle:
            general.MouseEventControl().mouse_event(app=self)
            self.toggle = True
        else:
            keyboard.unhook_all()
            self.toggle = False


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def delay_option(self, value=""):
        general.delay_option(value, self)
        self.DelayOperation.set("Delay")
        
    def exception_display(app, ex):
        
        app.exception_field.configure(state="normal")
        
        if ex:
            app.exception_field.configure(text_color="#CC3636")
            # Get current system exception
            ex_type, ex_value, ex_traceback = sys.exc_info()
            exception_details = f"Exception type : {ex_type.__name__}\nException message : {ex_value}"
            
        else:
            app.exception_field.configure(text_color="#367E18")
            exception_details = "Format Success!"
            
        app.exception_field.delete("0.0", "end")
        app.exception_field.insert("0.0", exception_details)
        app.exception_field.configure(state="disabled")
            
            

if __name__ == "__main__":
    app = App()
    app.mainloop()

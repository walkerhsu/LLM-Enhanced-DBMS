import customtkinter as ctk

class HotKeys:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.is_fullScreen = False
        self.master.geometry("800x600")
        
        self.master.bind('<Escape>', self.exit_fullscreen)
        self.master.bind('<Control-q>', self.close_window)
        self.master.bind('<Control-c>', self.close_window)
        self.master.bind('<Command-q>', self.close_window)
        self.master.bind('<Command-c>', self.close_window)

        # self.label = LabelWidget(self.master, "Enter some text:")
        # self.label.pack(pady=10)

        # self.input = InputWidget(self.master)
        # self.input.pack(pady=10)

        # self.button = ButtonWidget(self.master, "Submit", self.submit_input)
        # self.button.pack(pady=10)

    def submit_input(self):
        user_input = self.input.get_input()
        print("User input:", user_input)
        # Additional functionality for handling the input

    def exit_fullscreen(self, event=None):
        self.is_fullScreen = False
        self.master.attributes('-fullscreen', self.is_fullScreen)

    def close_window(self, event=None):
        self.master.destroy()

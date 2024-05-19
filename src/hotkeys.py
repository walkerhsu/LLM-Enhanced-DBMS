import customtkinter as ctk

class HotKeys:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.is_fullScreen = False
        
        self.master.bind('<Escape>', self.exit_fullscreen)
        self.master.bind('<Control-q>', self.close_window)
        self.master.bind('<Command-q>', self.close_window)

    def exit_fullscreen(self, event=None):
        self.is_fullScreen = False
        self.master.attributes('-fullscreen', self.is_fullScreen)

    def close_window(self, event=None):
        self.master.destroy()

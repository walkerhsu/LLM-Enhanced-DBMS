import customtkinter as ctk
from PIL import Image

class SQL_Logo(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.master = master
        self.my_image = ctk.CTkImage(dark_image=Image.open("image/Logo.png"),
                                  size=(70, 50))
        self.logo = ctk.CTkLabel(self.master, image=self.my_image, text="")
        self.logo.grid(row=0, column=0, padx=10, pady=10)

class MongoDB_Logo(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.master = master
        self.my_image = ctk.CTkImage(dark_image=Image.open("image/MongoDB.png"),
                                  size=(70, 50))
        self.logo = ctk.CTkLabel(self.master, image=self.my_image, text="")
        self.logo.grid(row=0, column=0, padx=10, pady=10)
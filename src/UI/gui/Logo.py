import customtkinter as ctk
from PIL import Image

class Logo(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.master = master
        self.my_image = ctk.CTkImage(dark_image=Image.open("/Users/walker/台大課程大三下/資料庫/LLM-Enhanced-DBMS/src/image/Logo.png"),
                                  size=(70, 50))
        self.logo = ctk.CTkLabel(self.master, image=self.my_image, text="")
        self.logo.grid(row=0, column=0, padx=10, pady=10)
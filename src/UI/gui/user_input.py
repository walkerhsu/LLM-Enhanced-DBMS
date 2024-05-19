import customtkinter as ctk
from customtkinter import filedialog
from openai import OpenAI  

class UserInput(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, openAI_client:OpenAI, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.master = master
        self.openAI_client = openAI_client
        
        self.inputLabel = ctk.CTkLabel(self.master, text="User Input : ", font=(self.master.font, 16), height=20, width=20)
        self.inputLabel.grid(row=2, column=0, padx=(10, 0), pady=2, sticky='e')
        self.userInput = ctk.CTkTextbox(self.master, font=(self.master.font, 14), height= 80, corner_radius=8, border_spacing=5, border_width=4, border_color="#dddddd", fg_color="#aaaaaa")
        self.userInput.grid(row=2, column=1, padx=0, pady=10, sticky="ew")
        # shoft+enter to change line
        self.userInput.bind("<Shift-Return>", self.change_line)

    def change_line(self, event):
        print("change line")
        self.userInput.insert(ctk.END, "\n")
        return "break"
        

        
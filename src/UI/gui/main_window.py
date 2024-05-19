import customtkinter as ctk
from customtkinter import filedialog

from openai import OpenAI

from hotkeys import HotKeys
from SQL_connection.connector import SQLConnector
from UI.gui.file_dialog import FileDialog
from UI.gui.user_input import UserInput
from UI.gui.chatBox import ChatBox
from UI.gui.Logo import Logo


class MainWindow(ctk.CTk):
    def __init__(self, openAI_client: OpenAI) -> None:
        super().__init__()
        # self.resizable(False, False)
        self.openAI_client = openAI_client
        self.geometry("1000x800")
        self.minsize(800, 550)
        self.is_fullScreen = False
        self.title("LLM-Enhanced-DBMS")
        self.font = 'Avenir Next'

        self.grid_rowconfigure(0, weight=3, minsize=100)
        self.grid_rowconfigure(1, weight=5, minsize=300)
        self.grid_rowconfigure(2, weight=3, minsize=40)
        self.grid_columnconfigure(0, weight=3, minsize=100)
        self.grid_columnconfigure(1, weight=8, minsize=570)
        self.grid_columnconfigure(2, weight=1, minsize=120)

        self.hotkeys = HotKeys(self)
        self.connector = SQLConnector(config='SQL_Connection/sql_config.json')
        self.Logo = Logo(self)
        self.fileDialog = FileDialog(self, self.openAI_client)
        self.chatBox = ChatBox(self)
        self.input = UserInput(self, self.openAI_client)

        self.dialogButon = ctk.CTkButton(self.master, text="🔊 Select Audio 🔊", command=self.selectfile)
        self.dialogButon.grid(row=0, column=2, padx=20, pady=20)
    
        self.submitButton = ctk.CTkButton(self, text="Send", command=self.submit, font=(self.font, 16), height=20, width=100)
        self.submitButton.grid(row=2, column=2, padx=(15, 20), pady=2, sticky='w')
        self.input.userInput.bind("<Return>", self.submit)  # Send message on Enter key press
    
    def submit(self, event=None):
        user_input = self.input.userInput.get("1.0", ctk.END)
        user_input = user_input[:-1].strip()
        if user_input == "":
            return "break"
        print(user_input)
        self.chatBox.add_message(user_input, "user")
        self.input.userInput.delete("1.0", ctk.END)
        return "break"

    def selectfile(self):
        filename = filedialog.askopenfilename()
        print(filename)
        self.fileDialog.translate(filename)
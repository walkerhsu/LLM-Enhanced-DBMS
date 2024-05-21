import customtkinter as ctk

from openai import OpenAI

from hotkeys import HotKeys
from SQL_connection.connector import SQLConnector
from UI.gui.upload.file_dialog import FileDialog
from UI.gui.chat.user_input import UserInput
from UI.gui.chat.chatBox import ChatBox
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
        self.Logo = Logo(self)

        self.connector = SQLConnector(config='SQL_Connection/sql_config.json')

        self.segmented_values = ["Upload Data", "Chat Playground"]
        self.segemented_button_var = ctk.StringVar(value="Upload Data")
        self.segemented_button = ctk.CTkSegmentedButton(self, values=self.segmented_values, font=(self.font, 16),
                                                            command=self.segmented_button_callback,
                                                            variable=self.segemented_button_var)
        self.segemented_button.grid(row=0, column=1, padx=20, pady=20)
    
        self.fileDialog = FileDialog(self, self.openAI_client)
        self.chatBox = ChatBox(self)
        self.input = UserInput(self, self.openAI_client)

        self.submitButton = ctk.CTkButton(self, text="Send", command=self.submit, font=(self.font, 16), height=20, width=100)
        self.submitButton.grid(row=2, column=2, padx=(15, 20), pady=2, sticky='w')
        self.input.userInput.bind("<Return>", self.submit)  # Send message on Enter key press

        self.segmented_button_callback("Upload Data")

    def segmented_button_callback(self, value):
        if value == "Chat Playground":
            # remove uploading grid
            self.fileDialog.remove_mul_grids()
            # set chatting grid
            self.chatBox.grid()
            self.input.set_mul_grids()
            self.submitButton.grid()
        elif value == "Upload Data":
            # remove chatting grid
            self.chatBox.grid_remove()
            self.input.remove_mul_grids()
            self.submitButton.grid_remove()
            # set uploading grid
            self.fileDialog.set_mul_grids()
        else:
            print("Error: segmented button value not found")
            return

    def submit(self, event=None):
        user_input = self.input.userInput.get("1.0", ctk.END)
        user_input = user_input[:-1].strip()
        if user_input == "":
            return "break"
        print(user_input)
        self.chatBox.add_message(user_input, "user")
        self.input.userInput.delete("1.0", ctk.END)
        return "break"
        
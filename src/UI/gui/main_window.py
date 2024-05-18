import customtkinter as ctk
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
        self.minsize(700, 550)
        self.is_fullScreen = False
        self.title("LLM-Enhanced-DBMS")

        self.grid_rowconfigure(0, weight=3, minsize=100)
        self.grid_rowconfigure(1, weight=5, minsize=300)
        self.grid_rowconfigure(2, weight=3, minsize=40)
        self.grid_columnconfigure(0, weight=1, minsize=50)
        self.grid_columnconfigure(1, weight=20, minsize=350)
        self.grid_columnconfigure(2, weight=1, minsize=60)

        self.hotkeys = HotKeys(self)
        self.connector = SQLConnector(config='SQL_Connection/sql_config.json')
        self.Logo = Logo(self)
        self.fileDialog = FileDialog(self, self.openAI_client)
        self.chatBox = ChatBox(self)
        self.userInput = UserInput(self, self.openAI_client)

        # self.empty0_0 = ctk.CTkFrame(self, fg_color="red", width=50)
        # self.empty0_0.grid(row=0, column=0, sticky="ewns")
        
        # self.empty0_1 = ctk.CTkFrame(self, fg_color="brown")
        # self.empty0_1.grid(row=0, column=1, sticky="ewns")

        # self.empty0_2 = ctk.CTkFrame(self, fg_color="blue")
        # self.empty0_2.grid(row=0, column=2, sticky="ewns")

        self.empty1_0 = ctk.CTkFrame(self, fg_color="green", width=50)
        self.empty1_0.grid(row=1, column=0, sticky="ewns")

        # self.empty1_1 = ctk.CTkFrame(self, fg_color="yellow")
        # self.empty1_1.grid(row=1, column=1, sticky="ewns")

        # self.empty1_2 = ctk.CTkFrame(self, fg_color="purple")
        # self.empty1_2.grid(row=1, column=2, sticky="ewns")

        # self.empty2_0 = ctk.CTkFrame(self, fg_color="orange")
        # self.empty2_0.grid(row=2, column=0, sticky="ewns")

        # self.empty2_1 = ctk.CTkFrame(self, fg_color="pink")
        # self.empty2_1.grid(row=2, column=1, sticky="ewns")

        # self.empty2_2 = ctk.CTkFrame(self, fg_color="black")
        # self.empty2_2.grid(row=2, column=2, sticky="ewns")
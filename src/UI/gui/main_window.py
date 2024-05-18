import customtkinter as ctk
from openai import OpenAI

from hotkeys import HotKeys
from SQL_connection.connector import SQLConnector
from UI.gui.file_dialog import FileDialog

class MainWindow:
    def __init__(self, master: ctk.CTk, openAI_client: OpenAI) -> None:
        self.master = master
        self.openAI_client = openAI_client
        self.master.geometry("800x600")
        self.is_fullScreen = False
        self.master.title("LLM-Enhanced-DBMS")
        self.hotkeys = HotKeys(self.master)
        self.connector = SQLConnector(config='SQL_Connection/sql_config.json')
        self.fileDialog = FileDialog(self.master, self.openAI_client)
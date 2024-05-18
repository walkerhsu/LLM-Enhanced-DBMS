import customtkinter as ctk

from hotkeys import HotKeys
from SQL_connection.connector import SQLConnector
from UI.gui.file_dialog import FileDialog

class MainWindow:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.master.title("LLM-Enhanced-DBMS")
        self.hotkeys = HotKeys(self.master)
        self.connector = SQLConnector(config='SQL_Connection/sql_config.json')
        self.fileDialog = FileDialog(self.master)
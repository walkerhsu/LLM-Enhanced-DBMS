import customtkinter as ctk

from hotkeys import HotKeys
from SQL_connection.connector import SQLConnector
# from gui.widgets.input_widget import InputWidget
# from gui.widgets.button_widget import ButtonWidget
# from gui.widgets.label_widget import LabelWidget

class MainWindow:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.master.title("LLM-Enhanced-DBMS")
        self.hotkeys = HotKeys(self.master)
        self.connector = SQLConnector(config='SQL_Connection/sql_config.json')

        # self.label = LabelWidget(self.master, "Enter some text:")
        # self.label.pack(pady=10)

        # self.input = InputWidget(self.master)
        # self.input.pack(pady=10)

        # self.button = ButtonWidget(self.master, "Submit", self.submit_input)
        # self.button.pack(pady=10)

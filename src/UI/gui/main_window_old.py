import customtkinter as ctk

from openai import OpenAI

from hotkeys import HotKeys
from SQLchain import SQL_Chain
from UI.gui.upload.file_dialog import FileDialog
from UI.gui.chat.user_input import UserInput
from UI.gui.chat.chatBox import ChatBox
from UI.gui.Logo import Logo
import json
import mysql
from tkinter import messagebox

class MainWindow(ctk.CTk):
    # def __init__(self, openAI_client: OpenAI) -> None:
    def __init__(self, openAI_client: OpenAI, SQL_config:dict) -> None:
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
        
        self.login_frame = ctk.CTkFrame(self, width=100, height=100)
        self.login_frame.grid(row=0, column=2, padx=10, pady=10, sticky='ne')
        self.login_frame.pack_propagate(False)

        self.connection_label = ctk.CTkLabel(self.login_frame, text="Connect to MySQL", font=(self.font, 12))
        self.connection_label.grid(row=0, columnspan=2, pady=5)

        self.host_label = ctk.CTkLabel(self.login_frame, text="Host", font=(self.font, 12))
        self.host_label.grid(row=1, column=0, padx=5, pady=5)
        self.host_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 12))
        self.host_entry.grid(row=1, column=1, padx=5, pady=5)

        self.user_label = ctk.CTkLabel(self.login_frame, text="User", font=(self.font, 12))
        self.user_label.grid(row=2, column=0, padx=5, pady=5)
        self.user_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 12))
        self.user_entry.grid(row=2, column=1, padx=5, pady=5)

        self.password_label = ctk.CTkLabel(self.login_frame, text="Password", font=(self.font, 12))
        self.password_label.grid(row=3, column=0, padx=5, pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", font=(self.font, 12))
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        self.database_label = ctk.CTkLabel(self.login_frame, text="Database", font=(self.font, 12))
        self.database_label.grid(row=4, column=0, padx=5, pady=5)
        self.database_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 12))
        self.database_entry.grid(row=4, column=1, padx=5, pady=5)

        # self.login_button = ctk.CTkButton(self.login_frame, text="Connect", command=self.handle_login, font=(self.font, 12))
        # self.login_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        self.SQL_Chain = SQL_Chain(SQL_config)

        self.segmented_values = ["Upload Data", "Chat Playground"]
        self.segemented_button_var = ctk.StringVar(value="Upload Data")
        self.segemented_button = ctk.CTkSegmentedButton(self, values=self.segmented_values, font=(self.font, 16),
                                                            command=self.segmented_button_callback,
                                                            variable=self.segemented_button_var)
        self.segemented_button.grid(row=0, column=1, padx=20, pady=20)
    
        self.fileDialog = FileDialog(self, self.openAI_client, self.SQL_Chain)
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
        self.chatBox.add_message(user_input, "user")
        self.input.userInput.delete("1.0", ctk.END)
        answer = self.SQL_Chain.run_query_chain(user_input)
        self.chatBox.add_message(answer, "bot")
        return "break"
        

    def handle_login(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        SQL_config = {
            "host": host,
            "user": user,
            "passwd": password,
            "database": database
        }

        # with open('./SQL_connection/sql_config.json', 'w') as config_file:
        #     json.dump(config, config_file, indent=4)

        try:
            # self.connector = SQLConnector(config='./SQL_connection/sql_config.json')
            self.SQL_Chain = SQL_Chain(SQL_config)
            messagebox.showinfo("Connection Successful", "Successfully connected to the database.")
            self.connection_label.grid_remove()
            self.host_label.grid_remove()
            self.host_entry.grid_remove()
            self.user_label.grid_remove()
            self.user_entry.grid_remove()
            self.password_label.grid_remove()
            self.password_entry.grid_remove()
            self.database_label.grid_remove()
            self.database_entry.grid_remove()
            self.login_button.grid_remove()
            connected_label = ctk.CTkLabel(self.login_frame, text="MySQL Connected", font=(self.font, 12))
            connected_label.grid(row=4, columnspan=2, pady=5)

        except mysql.connector.Error as e:
            messagebox.showinfo("Connection Error", f"Error: {e}")
            
        except Exception as e:
            messagebox.showinfo("Connection Error", f"Unexpected error: {e}")
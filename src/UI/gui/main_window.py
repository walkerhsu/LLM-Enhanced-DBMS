import customtkinter as ctk

from openai import OpenAI

from hotkeys import HotKeys
from SQLchain import SQL_Chain
from MongoDBchain import MongoDB_Chain
from UI.gui.upload.file_dialog import FileDialog
from UI.gui.chat.user_input import UserInput
from UI.gui.chat.chatBox import ChatBox
from UI.gui.Logo import SQL_Logo, MongoDB_Logo
import mysql
from tkinter import messagebox

class MainWindow(ctk.CTk):
    def __init__(self, openAI_client: OpenAI) -> None:
    # def __init__(self, openAI_client: OpenAI, SQL_config:dict) -> None:
        super().__init__()
        # self.resizable(False, False)
        self.openAI_client = openAI_client
        self.geometry("1000x800")
        self.minsize(800, 550)
        self.is_fullScreen = False
        self.title("LLM-Enhanced-DBMS")
        self.font = 'Avenir Next'

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.hotkeys = HotKeys(self)
        self.Logo = SQL_Logo(self)
        
        self.login_frame = ctk.CTkFrame(self, width=400, height=350)
        self.login_frame.grid_propagate(False)
        self.login_frame.grid(row=1, column=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)


        self.connection_label = ctk.CTkLabel(self.login_frame, text="Connect to MySQL", font=(self.font, 17, "bold"))
        self.connection_label.grid(row=0, columnspan=2, pady=5)

        self.database_label = ctk.CTkLabel(self.login_frame, text="Database", font=(self.font, 15))
        self.database_label.grid(row=1, column=0, padx=5, pady=5)
        self.database_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 15))
        self.database_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.host_label = ctk.CTkLabel(self.login_frame, text="Host", font=(self.font, 15))
        self.host_label.grid(row=2, column=0, padx=5, pady=5)
        self.host_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 15))
        self.host_entry.grid(row=2, column=1, padx=5, pady=5)

        self.port_label = ctk.CTkLabel(self.login_frame, text="Port", font=(self.font, 15))
        self.port_label.grid(row=3, column=0, padx=5, pady=5)
        self.port_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 15))
        self.port_entry.grid(row=3, column=1, padx=5, pady=5)

        self.user_label = ctk.CTkLabel(self.login_frame, text="User", font=(self.font, 15))
        self.user_label.grid(row=4, column=0, padx=5, pady=5)
        self.user_entry = ctk.CTkEntry(self.login_frame, font=(self.font, 15))
        self.user_entry.grid(row=4, column=1, padx=5, pady=5)

        self.password_label = ctk.CTkLabel(self.login_frame, text="Password", font=(self.font, 15))
        self.password_label.grid(row=5, column=0, padx=5, pady=5)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", font=(self.font, 15))
        self.password_entry.grid(row=5, column=1, padx=5, pady=5)

        self.login_button = ctk.CTkButton(self.login_frame, text="Connect", command=self.handle_SQL_login, font=(self.font, 15))
        self.login_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        self.switch_mongodb_button = ctk.CTkButton(self.login_frame, text="Change to MongoDB", command=self.switch_login_page, font=(self.font, 15), fg_color="purple")
        self.switch_mongodb_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

        self.switch_mySQL_button = ctk.CTkButton(self.login_frame, text="Change to MySQL", command=self.switch_login_page, font=(self.font, 15), fg_color="purple")
        self.switch_mySQL_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)
    
        self.switch_mySQL_button.grid_remove()

    def switch_login_page(self):
        if not self.switch_mongodb_button.winfo_ismapped():
            self.Logo.remove_logo()
            self.Logo = SQL_Logo(self)
            self.switch_mongodb_button.grid()
            self.switch_mySQL_button.grid_remove()
            self.login_frame.configure(width=400, height=350)
            self.connection_label.configure(text="Connect to MySQL")
            self.database_label.configure(text="Database")
            self.host_label.configure(text="Host")
            self.port_label.grid()
            self.port_entry.grid()
            self.user_label.grid()
            self.user_entry.grid()
            self.password_label.configure(text="Password")
            self.login_button.configure(command=self.handle_SQL_login)
        else:
            self.Logo.remove_logo()
            self.Logo = MongoDB_Logo(self)
            self.switch_mySQL_button.grid()
            self.switch_mongodb_button.grid_remove()
            self.login_frame.configure(width=400, height=350)
            self.connection_label.configure(text="Connect to MongoDB")
            self.database_label.configure(text="Database")
            self.host_label.configure(text="Collection")
            self.port_label.grid_remove()
            self.port_entry.grid_remove()
            self.user_label.grid_remove()
            self.user_entry.grid_remove()
            self.password_label.configure(text="Connection String")
            self.login_button.configure(command=self.handle_mongoDB_login)
            

    def show_real_ui(self):
        self.grid_rowconfigure(0, weight=3, minsize=100)
        self.grid_rowconfigure(1, weight=5, minsize=300)
        self.grid_rowconfigure(2, weight=3, minsize=40)
        self.grid_columnconfigure(1, weight=8, minsize=570)
        self.grid_columnconfigure(2, weight=1, minsize=120)

        self.segmented_values = ["Upload Data", "Chat Playground"]
        self.segemented_button_var = ctk.StringVar(value="Upload Data")
        self.segemented_button = ctk.CTkSegmentedButton(self, values=self.segmented_values, font=(self.font, 16),
                                                            command=self.segmented_button_callback,
                                                            variable=self.segemented_button_var)
        self.segemented_button.grid(row=0, column=1, padx=20, pady=20)
    
        self.fileDialog = FileDialog(self, self.openAI_client, self.DB_LLM_Chain)
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
        answer = self.DB_LLM_Chain.run_query_chain(user_input)
        self.chatBox.add_message(answer, "bot")
        return "break"
        

    def handle_SQL_login(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()
        port = self.port_entry.get()
        
        host = "127.0.0.1"
        user = "root"
        password = "jessy0129!"
        database = "interview"
        port = "3306"

        SQL_config = {
            "host": host,
            "user": user,
            "passwd": password,
            "database": database,
            "port": port
        }


        try:
            self.DB_LLM_Chain = SQL_Chain(SQL_config)
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
            self.login_frame.grid_remove()
            self.show_real_ui()

        except mysql.connector.Error as e:
            messagebox.showinfo("Connection Error", f"Error: {e}")
            
        except Exception as e:
            messagebox.showinfo("Connection Error", f"Unexpected error: {e}")

    def handle_mongoDB_login(self):
        database = self.database_entry.get()
        collection = self.host_entry.get()
        connection_string = self.password_entry.get()

        mongoDB_config = {
            "database": database,
            "collection": collection,
            "connection_string": connection_string
        }

        try:
            self.DB_LLM_Chain = MongoDB_Chain(mongoDB_config)
            messagebox.showinfo("Connection Successful", "Successfully connected to the MongoDB collection.")
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
            self.login_frame.grid_remove()
            self.show_real_ui()

        except Exception as e:
            messagebox.showinfo("Connection Error", f"Unexpected error: {e}")
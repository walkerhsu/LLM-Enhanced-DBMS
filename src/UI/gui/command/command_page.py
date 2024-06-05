import customtkinter as ctk
from SQL_connection.connector import SQLConnector

# from SQLchain import DB_LLM_Chain
class CommandPage(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, config:dict, DB_type:str) -> None:
        super().__init__(master)
        self.grid(row=1, column=1, padx=20, pady=20, ipadx=20, ipady=20, sticky="nesw")
        if DB_type == "MongoDB":
            pass
            # self.connector = MongoDBConnector(config=config)
        elif DB_type == "SQL":
            self.connector = SQLConnector(config=config)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.master = master

        self.radioLabel = ctk.CTkLabel(self, text="Command line", font=(self.master.font, 16))
        self.radioLabel.grid(row=0, column=0, columnspan=2, pady=20, sticky='new')

        self.command = ctk.CTkEntry(self, font=(self.master.font, 15))
        self.command.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky='nesw')
        self.command.bind("<Return>", self.run_command)  # Send message on Enter key press

        self.command_output = ctk.CTkTextbox(self, font=(self.master.font, 15))
        self.command_output.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='nesw')
        self.command_output.configure(state="disabled")

    def run_command(self, event):
        self.command_output.delete("1.0", "end")
        command = self.command.get()
        result = self.connector.run_select(query=command)
        self.command_output.configure(state="normal")
        for row in result:
            self.command_output.insert("end", f"{row}\n")
        self.command_output.configure(state="disabled")
    
    def remove_mul_grids(self):
        self.grid_remove()
        self.radioLabel.grid_remove()
        self.command.grid_remove()
        self.command_output.grid_remove()


    def set_mul_grids(self):
        self.grid()
        self.radioLabel.grid()
        self.command.grid()
        self.command_output.grid()
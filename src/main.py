import json
from UI.gui.main_window import MainWindow
import customtkinter as ctk

import os
from openai import OpenAI
from dotenv import load_dotenv

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    openAI_client = OpenAI(
        api_key=api_key
    )

    if not os.path.exists("SQL_Connection/sql_config.json"):
        database    =   input("Enter database name (eg: interview)  : ")
        host        =   input("Enter database host (eg: 127.0.0.1)  : ")
        user        =   input("Enter database user (eg: root)       : ")
        passwd      =   input("Enter database password              : ")
        config = {
            "host": host,
            "user": user,
            "passwd": passwd,
            "database": database
        }
        with open("SQL_Connection/sql_config.json", "w") as f:
            json.dump(config, f)

    else:
        with open("SQL_Connection/sql_config.json", "r") as f:
            SQL_config = json.load(f)
            
    app = MainWindow(openAI_client, SQL_config=SQL_config)
    app.mainloop()

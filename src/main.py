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
        
    root = ctk.CTk()
    app = MainWindow(root, openAI_client)
    root.mainloop()

import customtkinter as ctk
from openai import OpenAI  

class FileDialog(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, openAI_client:OpenAI) -> None:
        super().__init__(master)
        self.openAI_client = openAI_client
        self.master = master
        self._filename = None
        self._transcription = None

    def translate(self, filename:str):
        self._filename = filename
        if not self._filename == "/Users/walker/台大課程大三下/資料庫/LLM-Enhanced-DBMS/audio/test.mp3":
            return
        audio_file = open(self._filename, "rb")
        self._transcription = self.openAI_client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text",
            language="zh"
        )
        print(self._transcription)

    @property
    def filename(self):
        return self._filename
    
    @property
    def transcription(self):
        return self._transcription
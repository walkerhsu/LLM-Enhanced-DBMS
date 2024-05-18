import customtkinter as ctk
from customtkinter import filedialog
from openai import OpenAI  

class FileDialog():
    def __init__(self, master: ctk.CTk, openAI_client:OpenAI) -> None:
        self.master = master
        self.openAI_client = openAI_client
        self._filename = None
        self._transcription = None
        self.dialogButon = ctk.CTkButton(self.master, text="🔊 Select Audio 🔊", command=self.selectfile)
        self.dialogButon.pack(pady=10)

    def selectfile(self):
        self._filename = filedialog.askopenfilename()
        print(self._filename)
        self.translate()

    def translate(self):
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
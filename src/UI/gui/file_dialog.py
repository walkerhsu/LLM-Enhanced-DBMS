import customtkinter as ctk
from customtkinter import filedialog  

class FileDialog():
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self._filename = None
        self.dialogButon = ctk.CTkButton(self.master, text="🔊 Select Audio 🔊", command=self.selectfile)
        self.dialogButon.pack(pady=10)

    def selectfile(self):
        self._filename = filedialog.askopenfilename()
        print(self._filename)

    @property
    def filename(self):
        return self._filename


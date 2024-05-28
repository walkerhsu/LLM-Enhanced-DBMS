from tkinter import filedialog
import customtkinter as ctk
from openai import OpenAI  
import pymupdf

from SQLchain import SQL_Chain
class FileDialog(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, openAI_client:OpenAI, SQL_Chain:SQL_Chain) -> None:
        super().__init__(master)
        self.grid(row=1, column=1, padx=20, pady=20, ipadx=20, ipady=20, sticky="nesw")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.openAI_client = openAI_client
        self.master = master
        self.SQL_Chain = SQL_Chain

        self._filetype = ("Audio Files", "*.mp3 *.wav")
        self._filename = ""
        self._transcription = None
        self.radioLabel = ctk.CTkLabel(self, text="Select File Type: ", font=(self.master.font, 16))
        self.radioLabel.grid(row=0, column=0, columnspan=2, pady=20, sticky='new')

        self.radio_var = ctk.IntVar(value=1)
        self.audioButton = ctk.CTkRadioButton(self, text="AUDIO",
                                             command=self.radiobutton_event, variable= self.radio_var, value=1)
        self.pdfButton = ctk.CTkRadioButton(self, text="PDF",
                                             command=self.radiobutton_event, variable= self.radio_var, value=2)
        self.audioButton.grid(row=1, column=0, padx=10, pady=10, sticky='n')
        self.pdfButton.grid(row=1, column=1, padx=10, pady=10, sticky='n')

        self.dialogButton = ctk.CTkButton(self, text="Select Data", command=self.selectfile, font=(self.master.font, 16))
        self.dialogButton.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky='n')

        self.fileLabel = None
        self.uploadButton = None
        self.uploadStateLabel = None
        self.confirmButton = None
        self.cancelButton = None


    def translate(self, filename:str):
        self._filename = filename
        self._transcription = ""
        # if not self._filename == "/Users/walker/台大課程大三下/資料庫/LLM-Enhanced-DBMS/audio/test.mp3":
        #     return
        if self._filename.endswith(".mp3") or self._filename.endswith(".wav"):
            audio_file = open(self._filename, "rb")
            self._transcription = self.openAI_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="text",
                language="zh"
            )
        elif self._filename.endswith(".pdf"):
            doc = pymupdf.open(self._filename) # open a document
            for page in doc: # iterate the document pages
                text = page.get_text() # get plain text encoded as UTF-8
                self._transcription += text

    def radiobutton_event(self):
        self.remove_upload_state()
        if self.radio_var.get() == 1:
            self._filetype = ("Audio Files", "*.mp3 *.wav")
        elif self.radio_var.get() == 2:
            self._filetype = ("PDF Files", "*.pdf")

    def selectfile(self):
        self.remove_upload_state()
        filename = filedialog.askopenfilename(
            filetypes=[
                self.filetype
            ],
        )
        if filename == "":
            return
        self.translate(filename)
        self.fileLabel = ctk.CTkLabel(self, text=f"Selected File: {self._filename.split('/')[-1]}", font=(self.master.font, 16))
        self.fileLabel.grid(row=3, column=0, columnspan=2, pady=20, sticky='n')

        self.uploadButton = ctk.CTkButton(self, text="Upload", command=self.upload, font=(self.master.font, 16))
        self.uploadButton.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky='n')

    def upload(self):
        if self._transcription is None:
            print("Error: No file selected")
            return
        print("Uploading...")

        self.fileLabel.grid_remove()
        self.fileLabel = None
        self.uploadButton.grid_remove()
        self.uploadButton = None
        self.uploadStateLabel = ctk.CTkLabel(self, text="Extracting...", font=(self.master.font, 16))
        self.uploadStateLabel.grid(row=3, column=0, columnspan=2, pady=20, sticky='n')

        self.uploadData()

    def uploadData(self):
        self.dialogButton.configure(state="disabled")
        self.audioButton.configure(state="disabled")
        self.pdfButton.configure(state="disabled")
        
        extract_data = self.SQL_Chain.run_upload_chain(self._transcription)
        self.uploadStateLabel.configure(text=extract_data)
        self.confirmButton = ctk.CTkButton(self, text="Upload", command=self.confirm_upload, font=(self.master.font, 16))
        self.confirmButton.grid(row=4, column=0, padx=20, pady=20, sticky='n')

        self.cancelButton = ctk.CTkButton(self, text="Cancel", command=self.cancel_upload, font=(self.master.font, 16))
        self.cancelButton.grid(row=4, column=1, padx=20, pady=20, sticky='n')

        self.dialogButton.configure(state="normal")
        self.audioButton.configure(state="normal")
        self.pdfButton.configure(state="normal")

    def confirm_upload(self):
        self.uploadStateLabel.configure(text="Uploading...")
        self.confirmButton.grid_remove()
        self.confirmButton = None
        self.cancelButton.grid_remove()
        self.cancelButton = None
        self.SQL_Chain.run_insert()

        print("Upload Complete")
        self.uploadStateLabel.configure(text="Upload Complete")


    def cancel_upload(self):
        self.uploadStateLabel.grid_remove()
        self.confirmButton.grid_remove()
        self.confirmButton = None
        self.cancelButton.grid_remove()
        self.cancelButton = None
        print("Cancel Upload")

    def remove_upload_state(self):
        if self.uploadStateLabel:
            self.uploadStateLabel.grid_remove()
            self.uploadStateLabel = None
        if self.fileLabel:
            self.fileLabel.grid_remove()
            self.fileLabel = None
        if self.uploadButton:
            self.uploadButton.grid_remove()
            self.uploadButton = None

    def set_mul_grids(self):
        self.radioLabel.grid()
        self.audioButton.grid()
        self.pdfButton.grid()
        if self.dialogButton:
            self.dialogButton.grid()
        if self.fileLabel:
            self.fileLabel.grid()
        if self.uploadButton:
            self.uploadButton.grid()
        if self.uploadStateLabel:
            self.uploadStateLabel.grid()
        if self.confirmButton:
            self.confirmButton.grid()
        if self.cancelButton:
            self.cancelButton.grid()

    def remove_mul_grids(self):
        self.radioLabel.grid_remove()
        self.audioButton.grid_remove()
        self.pdfButton.grid_remove()
        if self.dialogButton:
            self.dialogButton.grid_remove()
        if self.fileLabel:
            self.fileLabel.grid_remove()
        if self.uploadButton:
            self.uploadButton.grid_remove()
        if self.uploadStateLabel:
            self.uploadStateLabel.grid_remove()
        if self.confirmButton:
            self.confirmButton.grid_remove()
        if self.cancelButton:
            self.cancelButton.grid_remove()

    @property
    def filename(self):
        return self._filename
    
    @property
    def transcription(self):
        return self._transcription
    
    @property
    def filetype(self):
        return self._filetype
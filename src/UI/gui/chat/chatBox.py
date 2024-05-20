from tkinter.font import Font
import customtkinter as ctk
import tkinter as tk

class ChatBox(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.master = master
        self.grid(row=1, column=1, columnspan=2, padx=20, pady=20, ipadx=20, ipady=20, sticky="nesw")
        self.messages = []
        self.message_width=550
        self.message_count = 0
        
        self.add_message("Hello, I am your agent. How can I help you? Hello, I am your agent. How can I help you? ", "bot")
        
    def add_message(self, msg:str, sender:str):

        def count_lines(message_box: ctk.CTkTextbox, msg:str):
            font = Font(family=self.master.font, size=20, weight="normal")
            cur_width = 0
            word_width = 0
            msg = msg.split('\n')
            lines = 0

            for sentence in msg:
                lines += 1
                words = sentence.split(' ')
                for word in words:
                    word_width = font.measure(word)
                    if self.message_width < cur_width + word_width:
                        cur_width = 0
                        lines += 1
                    cur_width += word_width
                cur_width = 0
                word_width = 0
            return lines
                

        def set_message(message_box: ctk.CTkTextbox, msg:str):
            message.configure(state="normal")
            message_box.insert(ctk.END, msg)
            message.configure(state="disabled")
            return count_lines(message_box, msg)

        def calculate_height(message_box: ctk.CTkTextbox, num_lines:int, max_height:int=200):
            # Calculate the height needed for the text
            message_box.update_idletasks()
            line_height = int(message_box.dlineinfo('1.0')[3])  # height of a single line in pixels
            total_height = line_height * (num_lines+1)

            # Set max height and enable scrollbar if necessary
            if total_height > max_height:
                message_box.configure(height=max_height)
                # scrollbar = ctk.CTkScrollbar(self, orient="vertical", command=message_box.yview)
                # scrollbar.grid(row=row, column=2, sticky="ns")
                # message_box.configure(yscrollcommand=scrollbar.set)
            else:
                message_box.configure(height=total_height)

        row = self.message_count
        if sender == "user":
            message = ctk.CTkTextbox(self, width=self.message_width, font=(self.master.font, 20), fg_color="#7fb4a1", corner_radius=8, border_color="#d0d0d0", border_width=2, wrap="word")
            message.grid(row=row, column=1, columnspan=2, sticky="e", padx=10, pady=5)
        else:
            message = ctk.CTkTextbox(self, width=self.message_width, font=(self.master.font, 20), fg_color="#707070", corner_radius=8, border_color="#d0d0d0", border_width=2, wrap="word")
            message.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        lines = set_message(message, msg)
        calculate_height(message, lines, 250)

        self.messages.append(message)
        # Update row weights to allow messages to expand
        self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.message_count += 1

        self.after(10, self._parent_canvas.yview_moveto, 1.0)

    def clear_messages(self):
        for message in self.messages:
            message.destroy()
        self.messages = []
        self.message_count = 0
        self.add_message("Hello, I am your agent. How can I help you.", "bot")


        
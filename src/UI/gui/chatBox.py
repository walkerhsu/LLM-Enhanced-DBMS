import customtkinter as ctk

class ChatBox(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.chatbox = ctk.CTkTextbox(self.master)
        self.chatbox.grid(row=1, column=1,padx=20, pady=20, sticky="nesw")
        self.add_message("Hello, I am LLM-Enhanced-DBMS, how can I help you? asdfasdfasaljkdfl;ajkdfl;adfjl;ajkdfl;ajdfl;akjsdfl;ajksdfljal;sdkfjl;ajksdfl;akjsdf;lajksdfl;kajsdfl;kjasdl;fkjl;asdjkflajksdl;fjal;djksfl;ajksdl;fkjal;sdfjl;ajksdflkjasdl;fjal;sdjkflajksdfl;jkalsdkfjalskjdflakjsdfl;kjasldfjl;ajksdfl;ajksdfl;kajsdfal;sdkfjas;dfdffasdfasdfashdfklahjsdlfkjahsdfkljhaklsdfhjklasjdhfklajhsdfkljahsdfklhjasldfhjalkshjdfklahjsdfljkahsdfklahjsdfljahsdfkhjaskldfjhklasdhjfklahjsdfkahjsdfihyiloxcuvyhailsbdjgailosckasgdioawdfv")

    def add_message(self, message:str):
        self.chatbox.insert(ctk.END, message + "\n")
        self.chatbox.see(ctk.END)

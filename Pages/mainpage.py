import customtkinter as ctk

class mainpage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Ana Sayfa", font=("Arial", 24))
        label.pack(pady=20)

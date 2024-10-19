import customtkinter as ctk

class settings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Ayarlar", font=("Arial", 24))
        label.pack(pady=20)

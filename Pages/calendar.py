import customtkinter as ctk

class calendar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Takvim", font=("Arial", 24))
        label.pack(pady=20)

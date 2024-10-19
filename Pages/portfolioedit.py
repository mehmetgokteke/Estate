import customtkinter as ctk

class portfolioedit(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Portföy Düzenleme", font=("Arial", 24))
        label.pack(pady=20)

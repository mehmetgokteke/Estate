import customtkinter as ctk

class customerprofile(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Müşteri Profili", font=("Arial", 24))
        label.pack(pady=20)

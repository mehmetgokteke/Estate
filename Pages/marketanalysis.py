import customtkinter as ctk
import matplotlib.pyplot as plt

class marketanalysis(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ctk.CTkLabel(
            self, text="PİYASA ANALİZİ", font=("Helvetica", 30, "bold"), text_color="#000000", fg_color="#00BCD4", corner_radius=15
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        self.create_labeled_entry("İl:", "il")
        self.create_labeled_entry("İlçe:", "ilce")

        self.property_type_var = ctk.StringVar(value="Kiralık")
        self.create_radio_buttons()

        self.room_count_var = ctk.StringVar(value="1")
        self.create_room_count_buttons()

        self.analyze_button = ctk.CTkButton(
            self, text="Analiz Yap", command=self.analyze_data, fg_color="#00ACC1", hover_color="#388E3C", font=("Helvetica", 20, "bold"), corner_radius=20, width=500
        )
        self.analyze_button.pack(pady=10)
        self.bind("<Return>", lambda event: self.analyze_data())

    def create_labeled_entry(self, label_text, attribute_name):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text=label_text, font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        setattr(self, f"{attribute_name}_label", label)
        entry = ctk.CTkEntry(frame, placeholder_text=label_text, width=300, height=30, corner_radius=10, text_color="#000000", fg_color="#ECEFF1", font=("Helvetica", 14))
        entry.pack(side="right", padx=(10, 5), pady=5) 
        setattr(self, f"{attribute_name}_entry", entry)

    def create_radio_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text="Kiralık / Satılık:", font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        kiralik_button = ctk.CTkRadioButton(frame, text="Satılık",font=("Helvetica", 14), text_color="#000000", variable=self.property_type_var, value="Satılık", fg_color="#388E3C")
        kiralik_button.pack(side="right", padx=10, pady=5)
        satilik_button = ctk.CTkRadioButton(frame, text="Kiralık",font=("Helvetica", 14), text_color="#000000", variable=self.property_type_var, value="Kiralık", fg_color="#388E3C")
        satilik_button.pack(side="right", padx=10, pady=5)

    def create_room_count_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text="Oda Sayısı Seçiniz:", font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        room_1_button = ctk.CTkRadioButton(frame, text="Hepsi",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="5", fg_color="#388E3C")
        room_1_button.pack(side="right", padx=10, pady=5)
        room_2_button = ctk.CTkRadioButton(frame, text="4+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="4", fg_color="#388E3C")
        room_2_button.pack(side="right", padx=10, pady=5)
        room_3_button = ctk.CTkRadioButton(frame, text="3+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="3", fg_color="#388E3C")
        room_3_button.pack(side="right", padx=10, pady=5)
        room_4_button = ctk.CTkRadioButton(frame, text="2+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="2", fg_color="#388E3C")
        room_4_button.pack(side="right", padx=10, pady=5)
        room_5_button = ctk.CTkRadioButton(frame, text="1+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="1", fg_color="#388E3C")
        room_5_button.pack(side="right", padx=10, pady=5)

    def analyze_data(self):
        pass
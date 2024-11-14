import customtkinter as ctk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class mainpage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        estate_name = self.get_estate_name()

        welcome_label = ctk.CTkLabel(
            self, 
            text=f"HOŞ GELDİN {estate_name}",
            font=("Helvetica", 30, "bold"), 
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15
        )
        welcome_label.pack(pady=20, padx=20, fill="x", ipady=20)

        summary_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        summary_frame.pack(pady=20, padx=20, fill="x")

        total_properties = ctk.CTkLabel(
            summary_frame, 
            text="Toplam Portföy: 120 Mülk", 
            font=("Arial", 16), 
            text_color="#333"
        )
        total_properties.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        rented_properties = ctk.CTkLabel(
            summary_frame, 
            text="Kiralık Mülkler: 45", 
            font=("Arial", 16), 
            text_color="#FF9800"
        )
        rented_properties.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        sold_properties = ctk.CTkLabel(
            summary_frame, 
            text="Satılık Mülkler: 30", 
            font=("Arial", 16), 
            text_color="#03A9F4"
        )
        sold_properties.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        available_properties = ctk.CTkLabel(
            summary_frame, 
            text="Mevcut Portföy: 45", 
            font=("Arial", 16), 
            text_color="#4CAF50"
        )
        available_properties.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.add_pie_chart(summary_frame)

        quick_actions_frame = ctk.CTkFrame(self, fg_color="#f9f9f9", corner_radius=10)
        quick_actions_frame.pack(pady=20, padx=20, fill="x")

        quick_add_customer = ctk.CTkButton(
            quick_actions_frame, 
            text="Müşteri Ekle", 
            fg_color="#4CAF50",
            text_color="white",
            command=self.add_customer
        )
        quick_add_customer.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        quick_add_property = ctk.CTkButton(
            quick_actions_frame, 
            text="Mülk Ekle", 
            fg_color="#03A9F4",
            text_color="white",
            command=self.add_property
        )
        quick_add_property.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        quick_analysis = ctk.CTkButton(
            quick_actions_frame, 
            text="Piyasa Analizi", 
            fg_color="#FF9800",
            text_color="white",
            command=self.market_analysis
        )
        quick_analysis.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    def add_pie_chart(self, frame):
        fig, ax = plt.subplots(figsize=(4, 4))
        labels = ['Kiralık', 'Satılık', 'Mevcut']
        sizes = [45, 30, 45]
        colors = ['#FF9800', '#03A9F4', '#4CAF50']
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=3, padx=10, pady=20)

    def get_estate_name(self):
        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT emlak_adi FROM estateagentsettings WHERE id=1")
        result = cursor.fetchone()
        
        conn.close()
        
        if result and result[0]:
            return result[0]
        else:
            return '"Ayarlardan Emlak Adı Ekle"'

    def add_customer(self):
        print("Müşteri ekleme işlemi başlatıldı.")

    def add_property(self):
        print("Mülk ekleme işlemi başlatıldı.")

    def market_analysis(self):
        print("Piyasa analizi işlemi başlatıldı.")
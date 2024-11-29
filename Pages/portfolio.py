import customtkinter as ctk
import sqlite3

class portfolio(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Başlık etiketi
        self.label = ctk.CTkLabel(
            self,
            text="PORTFÖY",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15,
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        # Ana çerçeve (scrollable)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tablo çerçevesi
        self.table_frame = ctk.CTkFrame(self.scrollable_frame)
        self.table_frame.pack(fill="both", expand=True)

        # Kayıtları görüntüleme
        self.view_portfolio()

    def view_portfolio(self):
        # Veritabanına bağlan
        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()

        # Tüm kayıtları seç
        cursor.execute("SELECT * FROM portfolio")
        records = cursor.fetchall()

        # Sütun başlıkları (veritabanı sütunları)
        column_headers = [
            "ID", "TC Kimlik", "Oda Sayısı", "Bina Yaşı", "Kat Sayısı", "Fiyat", "İlan Tarihi", 
            "İlan Açıklaması", "Site Adı", "Aidat", "Depozito", "Banyo Sayısı", "Balkon", "Mutfak",
            "Isınma Tipi", "Yakıt Tipi", "Cephe", "Tapu Durumu", "Yapı Tipi", "Yapı Durumu", 
            "Kimden", "Otopark", "Asansör", "Kullanım Durumu", "Site İçerisinde", "Balkon Tipi", 
            "İlan Durumu", "Resim Adları"
        ]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg_color="#00BCD4",
                text_color="white",
                corner_radius=8,
                padx=10,
                pady=5,
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        # Kayıtları tabloya yerleştir
        for row_index, record in enumerate(records):
            for col_index, value in enumerate(record):
                label = ctk.CTkLabel(
                    self.table_frame,
                    text=value,
                    font=("Arial", 10),
                    fg_color="white",
                    text_color="#000000",
                    padx=10,
                    pady=5,
                )
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="nsew")

        # Grid tasarımı için kolonları genişlet
        for i in range(len(column_headers)):
            self.table_frame.grid_columnconfigure(i, weight=1)

        conn.close()

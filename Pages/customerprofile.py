import customtkinter as ctk
import sqlite3

class CustomerProfile(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(
            self,
            text="MÜŞTERİ PROFİLİ",
            font=("Helvetica", 30, "bold"), 
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        # Tablo oluşturma
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True)

        # Kayıtları görüntüle
        self.view_customers()

    def view_customers(self):
        # Mevcut tüm kayıtları görüntülemek için veritabanı bağlantısı
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers")
        records = cursor.fetchall()
        conn.close()

        # Tablo başlıkları (sütun isimleri)
        column_headers = ["ID", "Ad Soyad", "TC Kimlik", "Telefon", "E-posta", "İkametgah","Yaş", "Cinsiyet", "Kişisel Not"]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg_color="#00BCD4",  # Başlıklara arka plan rengi
                text_color="white",  # Yazı rengini beyaz yap
                corner_radius=8,  # Kenarları yuvarlat
                padx=10,  # İçerik boşluğu
                pady=5
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        # Kayıtları tabloya yerleştir
        for row_index, record in enumerate(records):
            for col_index, value in enumerate(record):
                label = ctk.CTkLabel(
                    self.table_frame,
                    text=value,
                    font=("Arial", 10),
                    fg_color="white",  # Hücre arka plan rengi
                    text_color="#000000",  # Siyah yazı rengi
                    padx=10,  # İçerik boşluğu
                    pady=5
                )
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="nsew")

        # Grid tasarımı iyileştirmek için sütun genişliğini ayarla
        for i in range(len(column_headers)):
            self.table_frame.grid_columnconfigure(i, weight=1)


import customtkinter as ctk
import sqlite3

class CustomerProfile(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Başlık
        self.label_title = ctk.CTkLabel(self, text="Müşteri Profilleri", font=("Arial", 24))
        self.label_title.pack(pady=20)

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

        # Başlıkları oluştur (sütun isimleri)
        column_headers = ["ID", "Ad Soyad", "TC Kimlik", "Telefon", "E-posta", "İkametgah", "Cinsiyet", "Kişisel Not"]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        # Kayıtları satır ve sütun olarak yerleştir
        for row_index, record in enumerate(records):
            for col_index, value in enumerate(record):
                label = ctk.CTkLabel(self.table_frame, text=value, font=("Arial", 10))
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5)

import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class customeredit(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Giriş alanlarını oluştur
        self.label_name = ctk.CTkLabel(self, text="Ad Soyad:")
        self.label_name.pack(pady=5)
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack(pady=5)

        self.label_tc = ctk.CTkLabel(self, text="TC Kimlik:")
        self.label_tc.pack(pady=5)
        self.entry_tc = ctk.CTkEntry(self)
        self.entry_tc.pack(pady=5)

        self.label_phone = ctk.CTkLabel(self, text="Telefon:")
        self.label_phone.pack(pady=5)
        self.entry_phone = ctk.CTkEntry(self)
        self.entry_phone.pack(pady=5)

        self.label_email = ctk.CTkLabel(self, text="E-posta (isteğe bağlı):")
        self.label_email.pack(pady=5)
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.pack(pady=5)

        self.label_address = ctk.CTkLabel(self, text="İkametgah:")
        self.label_address.pack(pady=5)
        self.entry_address = ctk.CTkEntry(self)
        self.entry_address.pack(pady=5)

        self.label_gender = ctk.CTkLabel(self, text="Cinsiyet:")
        self.label_gender.pack(pady=5)
        self.entry_gender = ctk.CTkEntry(self)
        self.entry_gender.pack(pady=5)

        self.label_note = ctk.CTkLabel(self, text="Kişisel Not:")
        self.label_note.pack(pady=5)
        self.entry_note = ctk.CTkEntry(self)
        self.entry_note.pack(pady=5)

        # Veritabanına kaydet butonu
        self.save_button = ctk.CTkButton(self, text="Kaydet", command=self.save_customer)
        self.save_button.pack(pady=10)

        # Veritabanındaki kayıtları görme butonu
        self.view_button = ctk.CTkButton(self, text="Kayıtları Görüntüle", command=self.view_customers)
        self.view_button.pack(pady=10)

    def save_customer(self):
        # Veritabanına müşteri bilgilerini kaydetme
        name = self.entry_name.get()
        tc_kimlik = self.entry_tc.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        address = self.entry_address.get()
        gender = self.entry_gender.get()
        personal_note = self.entry_note.get()

        # SQLite bağlantısı
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        # Veriyi veritabanına ekleme
        cursor.execute('''INSERT INTO customers (name, tc_kimlik, phone, email, address, gender, personal_note) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (name, tc_kimlik, phone, email, address, gender, personal_note))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Müşteri bilgileri kaydedildi!")

    def view_customers(self):
        # Kayıtlı müşterileri gösterme
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers")
        records = cursor.fetchall()
        conn.close()

        # Kayıtları gösterecek yeni pencere oluştur
        records_window = ctk.CTkToplevel(self)
        records_window.geometry("800x400")
        records_window.title("Müşteri Kayıtları")

        # Pencereyi önde tutma
        records_window.focus_force()
        records_window.grab_set()  # Diğer pencerelerin üzerine çıkmasını sağlar

        # Başlıkları oluştur (sütun isimleri)
        column_headers = ["ID", "Ad Soyad", "TC Kimlik", "Telefon", "E-posta", "İkametgah", "Cinsiyet", "Kişisel Not"]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(records_window, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5)

        # Kayıtları satır ve sütun olarak yerleştir
        for row_index, record in enumerate(records):
            for col_index, value in enumerate(record):
                label = ctk.CTkLabel(records_window, text=value, font=("Arial", 10))
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5)


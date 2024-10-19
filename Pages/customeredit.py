import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class CustomerEdit(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Sol tarafta müşteri ekleme alanı
        self.label_add = ctk.CTkLabel(self, text="Müşteri Ekle", font=("Arial", 16, "bold"))
        self.label_add.grid(row=0, column=0, padx=20, pady=10)

        self.label_name = ctk.CTkLabel(self, text="Ad Soyad:")
        self.label_name.grid(row=1, column=0, padx=20, pady=5)
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.grid(row=1, column=1, padx=20, pady=5)

        self.label_tc = ctk.CTkLabel(self, text="TC Kimlik:")
        self.label_tc.grid(row=2, column=0, padx=20, pady=5)
        self.entry_tc = ctk.CTkEntry(self)
        self.entry_tc.grid(row=2, column=1, padx=20, pady=5)

        self.label_phone = ctk.CTkLabel(self, text="Telefon:")
        self.label_phone.grid(row=3, column=0, padx=20, pady=5)
        self.entry_phone = ctk.CTkEntry(self)
        self.entry_phone.grid(row=3, column=1, padx=20, pady=5)

        self.label_email = ctk.CTkLabel(self, text="E-posta:")
        self.label_email.grid(row=4, column=0, padx=20, pady=5)
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.grid(row=4, column=1, padx=20, pady=5)

        self.label_address = ctk.CTkLabel(self, text="İkametgah:")
        self.label_address.grid(row=5, column=0, padx=20, pady=5)
        self.entry_address = ctk.CTkEntry(self)
        self.entry_address.grid(row=5, column=1, padx=20, pady=5)

        # Cinsiyet için Radiobutton grubu
        self.gender_label = ctk.CTkLabel(self, text="Cinsiyet:")
        self.gender_label.grid(row=6, column=0, padx=20, pady=5)
        self.gender_var = ctk.StringVar(value="Erkek")
        self.gender_male = ctk.CTkRadioButton(self, text="Erkek", variable=self.gender_var, value="Erkek")
        self.gender_male.grid(row=6, column=1, padx=5, pady=5)
        self.gender_female = ctk.CTkRadioButton(self, text="Kadın", variable=self.gender_var, value="Kadın")
        self.gender_female.grid(row=6, column=2, padx=5, pady=5)

        self.label_note = ctk.CTkLabel(self, text="Kişisel Not:")
        self.label_note.grid(row=7, column=0, padx=20, pady=5)
        self.entry_note = ctk.CTkEntry(self)
        self.entry_note.grid(row=7, column=1, padx=20, pady=5)

        # Kaydetme butonu
        self.save_button = ctk.CTkButton(self, text="Müşteri Ekle", command=self.save_customer)
        self.save_button.grid(row=8, column=0, padx=20, pady=20)

        # Sağ tarafta otomatik doldurma ve güncelleme alanları
        self.label_search = ctk.CTkLabel(self, text="TC Kimlik ile Müşteri Ara", font=("Arial", 16, "bold"))
        self.label_search.grid(row=0, column=3, padx=20, pady=10)

        self.label_search_tc = ctk.CTkLabel(self, text="TC Kimlik:")
        self.label_search_tc.grid(row=1, column=3, padx=20, pady=5)
        self.entry_search_tc = ctk.CTkEntry(self)
        self.entry_search_tc.grid(row=1, column=4, padx=20, pady=5)

        # TC Kimlik ile otomatik doldurma butonu
        self.search_button = ctk.CTkButton(self, text="Ara", command=self.search_customer)
        self.search_button.grid(row=2, column=3, padx=20, pady=20)

        # Güncelleme ve silme butonları
        self.update_button = ctk.CTkButton(self, text="Güncelle", command=self.update_customer)
        self.update_button.grid(row=8, column=3, padx=20, pady=20)

        self.delete_button = ctk.CTkButton(self, text="Sil", command=self.delete_customer)
        self.delete_button.grid(row=8, column=4, padx=20, pady=20)



    def save_customer(self):
        # Yeni müşteri ekleme fonksiyonu
        name = self.entry_name.get()
        tc_kimlik = self.entry_tc.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        address = self.entry_address.get()
        gender = self.gender_var.get()
        personal_note = self.entry_note.get()

        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO customers (name, tc_kimlik, phone, email, address, gender, personal_note)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (name, tc_kimlik, phone, email, address, gender, personal_note))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Müşteri başarıyla eklendi!")

    def search_customer(self):
        # Müşteri arama fonksiyonu
        tc_kimlik = self.entry_search_tc.get()

        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers WHERE tc_kimlik = ?", (tc_kimlik,))
        result = cursor.fetchone()

        if result:
            self.entry_name.delete(0, 'end')
            self.entry_name.insert(0, result[1])

            self.entry_tc.delete(0, 'end')
            self.entry_tc.insert(0, result[2])

            self.entry_phone.delete(0, 'end')
            self.entry_phone.insert(0, result[3])

            self.entry_email.delete(0, 'end')
            self.entry_email.insert(0, result[4])

            self.entry_address.delete(0, 'end')
            self.entry_address.insert(0, result[5])

            self.gender_var.set(result[6])

            self.entry_note.delete(0, 'end')
            self.entry_note.insert(0, result[7])

        else:
            messagebox.showwarning("Hata", "Müşteri bulunamadı!")

        conn.close()

    def update_customer(self):
        # Müşteri güncelleme fonksiyonu
        name = self.entry_name.get()
        tc_kimlik = self.entry_tc.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        address = self.entry_address.get()
        gender = self.gender_var.get()
        personal_note = self.entry_note.get()

        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute('''UPDATE customers 
                          SET name=?, phone=?, email=?, address=?, gender=?, personal_note=?
                          WHERE tc_kimlik=?''', 
                          (name, phone, email, address, gender, personal_note, tc_kimlik))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Müşteri başarıyla güncellendi!")

    def delete_customer(self):
        # Müşteri silme fonksiyonu
        tc_kimlik = self.entry_search_tc.get()

        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM customers WHERE tc_kimlik = ?", (tc_kimlik,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Başarılı", "Müşteri başarıyla silindi!")
    


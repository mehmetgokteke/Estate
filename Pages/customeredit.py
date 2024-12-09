import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class CustomerEdit(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

                # Üst başlık
        self.label_header = ctk.CTkLabel(
            self,
            text="MÜŞTERİ DÜZENLEME",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",  # Arka plan rengi
            corner_radius=20,
        )

        # Başlığın yerleşimi ve boyutlandırma
        self.label_header.grid(row=0, column=0, columnspan=10, padx=20, pady=20, sticky="ew", ipady=20)

        # Sol tarafta müşteri ekleme alanı
        self.label_add = ctk.CTkLabel(
            self, text="Müşteri Ekle", font=("Arial", 16, "bold"), text_color="#FFFFFF", fg_color="#00BCD4", corner_radius=20
        )
        self.label_add.grid(row=1, column=0, columnspan=5, padx=20, pady=10, sticky="ew")

        self.label_name = ctk.CTkLabel(self, text="Ad Soyad:", corner_radius=20)
        self.label_name.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(self, corner_radius=20)
        self.entry_name.grid(row=2, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        self.label_tc = ctk.CTkLabel(self, text="TC Kimlik:", corner_radius=20)
        self.label_tc.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.entry_tc = ctk.CTkEntry(self, corner_radius=20)
        self.entry_tc.grid(row=3, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        self.label_phone = ctk.CTkLabel(self, text="Telefon:", corner_radius=20)
        self.label_phone.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.entry_phone = ctk.CTkEntry(self, corner_radius=20)
        self.entry_phone.grid(row=4, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        self.label_email = ctk.CTkLabel(self, text="E-posta:", corner_radius=20)
        self.label_email.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self, corner_radius=20)
        self.entry_email.grid(row=5, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        self.label_address = ctk.CTkLabel(self, text="İkametgah:", corner_radius=20)
        self.label_address.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.entry_address = ctk.CTkEntry(self, corner_radius=20)
        self.entry_address.grid(row=6, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        # Yaş için etiket ve giriş alanı
        self.label_age = ctk.CTkLabel(self, text="Yaş:", corner_radius=20)
        self.label_age.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.entry_age = ctk.CTkEntry(self, corner_radius=20)
        self.entry_age.grid(row=7, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        # Cinsiyet için Radiobutton grubu
        self.gender_label = ctk.CTkLabel(self, text="Cinsiyet:", corner_radius=20)
        self.gender_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        self.gender_var = ctk.StringVar(value="Erkek")
        self.gender_male = ctk.CTkRadioButton(self, text="Erkek", variable=self.gender_var, value="Erkek", corner_radius=20)
        self.gender_male.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        self.gender_female = ctk.CTkRadioButton(self, text="Kadın", variable=self.gender_var, value="Kadın", corner_radius=20)
        self.gender_female.grid(row=8, column=2, padx=5, pady=5, sticky="w")

        self.label_note = ctk.CTkLabel(self, text="Kişisel Not:", corner_radius=20)
        self.label_note.grid(row=9, column=0, padx=20, pady=5, sticky="w")
        self.entry_note = ctk.CTkEntry(self, corner_radius=20)
        self.entry_note.grid(row=9, column=1, columnspan=4, padx=20, pady=5, sticky="ew")

        # Kaydetme butonu
        self.save_button = ctk.CTkButton(self, text="Müşteri Ekle", command=self.save_customer, corner_radius=20)
        self.save_button.grid(row=10, column=0, columnspan=5, padx=20, pady=20, sticky="ew")

        # Sağ tarafta otomatik doldurma ve güncelleme alanları
        self.label_search = ctk.CTkLabel(
            self, text="TC Kimlik ile Müşteri Ara", font=("Arial", 16, "bold"), text_color="#FFFFFF", fg_color="#00BCD4", corner_radius=20
        )
        self.label_search.grid(row=1, column=5, columnspan=5, padx=20, pady=10, sticky="ew")

        self.label_search_tc = ctk.CTkLabel(self, text="TC Kimlik:", corner_radius=20)
        self.label_search_tc.grid(row=2, column=5, padx=20, pady=5, sticky="w")
        self.entry_search_tc = ctk.CTkEntry(self, corner_radius=20)
        self.entry_search_tc.grid(row=2, column=6, columnspan=3, padx=20, pady=5, sticky="ew")

        # TC Kimlik ile otomatik doldurma butonu
        self.search_button = ctk.CTkButton(self, text="Ara", command=self.search_customer, corner_radius=20)
        self.search_button.grid(row=3, column=5, columnspan=5, padx=20, pady=10, sticky="ew")

        # Güncelleme ve silme butonları
        self.update_button = ctk.CTkButton(self, text="Güncelle", command=self.update_customer, corner_radius=20)
        self.update_button.grid(row=10, column=5, columnspan=2, padx=20, pady=20, sticky="ew")

        self.delete_button = ctk.CTkButton(self, text="Sil", command=self.delete_customer, corner_radius=20)
        self.delete_button.grid(row=10, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Dikey ve yatay yönlerde boşlukları sıfırlamak için 'sticky' kullanımı
        self.grid_rowconfigure(0, weight=1)  # Başlık için yukarıya doğru esneme
        self.grid_rowconfigure(1, weight=1)  # Müşteri ekleme başlığı için
        self.grid_rowconfigure(2, weight=1)  # Diğer alanlar için
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)  # Butonlar için

        self.grid_columnconfigure(0, weight=1)  # İlk sütun
        self.grid_columnconfigure(1, weight=1)  # İkinci sütun
        self.grid_columnconfigure(2, weight=1)  # Üçüncü sütun
        self.grid_columnconfigure(3, weight=1)  # Dördüncü sütun
        self.grid_columnconfigure(4, weight=1)  # Beşinci sütun
        self.grid_columnconfigure(5, weight=1)  # Sağ alan
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(7, weight=1)

    def save_customer(self):
        # Yeni müşteri ekleme fonksiyonu
        name = self.entry_name.get()
        tc_kimlik = self.entry_tc.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        address = self.entry_address.get()
        age = self.entry_age.get()  # Yaş bilgisini al
        gender = self.gender_var.get()
        personal_note = self.entry_note.get()

        # personal_note uzunluğunu kontrol et
        if len(personal_note) > 256:
            messagebox.showwarning("Uyarı", "Not 256 karakteri aşamaz!")
            return

        # Yaş filtresi
        if not age.isdigit() or not (1 <= int(age) <= 150):
            messagebox.showwarning("Uyarı", "Lütfen 1 ile 150 arasında bir yaş giriniz!")
            return

        try:
            conn = sqlite3.connect("customers.db")
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO customers (name, tc_kimlik, phone, email, address, age, gender, personal_note)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (name, tc_kimlik, phone, email, address, age, gender, personal_note))

            conn.commit()
            messagebox.showinfo("Başarılı", "Müşteri başarıyla eklendi!")

            
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "TC kimlik zaten mevcut!")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        finally:
            conn.close()


    def search_customer(self):
        # Müşteri arama fonksiyonu
        tc_kimlik = self.entry_search_tc.get()

        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers WHERE tc_kimlik = ?", (tc_kimlik,))
        result = cursor.fetchone()

        if result:
            # Arama sonucu bulunduğunda alanları doldur
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

            self.entry_age.delete(0, 'end')  # Yaş alanını temizle
            self.entry_age.insert(0, result[6])  # Yaşı göster

            self.gender_var.set(result[7])

            self.entry_note.delete(0, 'end')
            self.entry_note.insert(0, result[8])
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
        age = self.entry_age.get()  # Yeni yaş alanı
        gender = self.gender_var.get()
        personal_note = self.entry_note.get()

        # personal_note uzunluğunu kontrol et
        if len(personal_note) > 256:
            messagebox.showwarning("Uyarı", "Not 256 karakteri aşamaz!")
            return

        try:
            conn = sqlite3.connect("customers.db")
            cursor = conn.cursor()

            cursor.execute('''UPDATE customers 
                            SET name=?, phone=?, email=?, address=?, age=?, gender=?, personal_note=? 
                            WHERE tc_kimlik=?''', 
                        (name, phone, email, address, age, gender, personal_note, tc_kimlik))

            conn.commit()
            messagebox.showinfo("Başarılı", "Müşteri başarıyla güncellendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Müşteri güncellenemedi: {e}")
        finally:
            conn.close()

    def delete_customer(self):
        # Müşteri silme fonksiyonu
        tc_kimlik = self.entry_search_tc.get()

        try:
            conn = sqlite3.connect("customers.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM customers WHERE tc_kimlik = ?", (tc_kimlik,))

            conn.commit()
            messagebox.showinfo("Başarılı", "Müşteri başarıyla silindi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Böyle bir müşteri mevcut değil!")
        finally:
            conn.close()
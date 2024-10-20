import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from password import PasswordEntry

class Settings(ctk.CTkFrame):
    def __init__(self, parent, settings_button):
        super().__init__(parent)
        self.settings_button = settings_button
        
        # Veritabanı bağlantısını kur
        self.conn = sqlite3.connect('estateagentsettings.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        
        # Başlık için stil
        self.label = ctk.CTkLabel(
            self,
            text="Ayarlar", 
            font=("Helvetica", 30, "bold"), 
            text_color="#37474F"
        )
        self.label.pack(pady=20)

        # Giriş alanlarını ve açıklamaları ayarla
        self.create_labeled_entry("Emlak Adı:", "emlak_adi")
        self.create_labeled_entry("Sahibinden Mail:", "sahibinden_mail")
        self.create_password_entry("Sahibinden Şifre:", "sahibinden_sifre")
        self.create_labeled_entry("Hepsiemlak Mail:", "hepsiemlak_mail")
        self.create_password_entry("Hepsiemlak Şifre:", "hepsiemlak_sifre")
        self.create_labeled_entry("Emlakjet Mail:", "emlakjet_mail")
        self.create_password_entry("Emlakjet Şifre:", "emlakjet_sifre")
        self.create_password_entry("Uygulama Şifresi:", "uygulama_sifre")

        # Kaydet butonu için stil
        self.save_button = ctk.CTkButton(
            self, 
            text="Kaydet/Güncelle", 
            command=self.save_settings,
            fg_color="#00ACC1", 
            hover_color="#00838F",
            font=("Helvetica", 25, "bold"),
            corner_radius=20,
            width=400
        )
        self.save_button.pack(pady=20)

        # Veritabanından verileri yükle
        self.load_settings()

        # Uygulama şifre kontrolü
        self.check_password()

        # Enter tuşu ile kaydetme işlevi
        self.bind("<Return>", lambda event: self.save_settings())

    def check_password(self):
        """Veritabanındaki şifreyi kontrol eder ve gerekirse şifre giriş penceresini açar."""
        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()

        # Şifreyi sorgula
        cursor.execute("SELECT uygulama_sifre FROM estateagentsettings WHERE id=1")
        stored_password = cursor.fetchone()

        if stored_password is None or stored_password[0] is None or stored_password[0] == "":
            conn.close()
            return
        
        self.password_window = PasswordEntry()
        self.password_window.grab_set() 
        self.wait_window(self.password_window)
        conn.close()

    def get_stored_password(self):
        """Veritabanından uygulama şifresini alır."""
        self.cursor.execute('SELECT uygulama_sifre FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        return data[0] if data else ""

    def create_table(self):
        """Veritabanında tabloyu oluşturur."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS estateagentsettings (
            id INTEGER PRIMARY KEY,
            emlak_adi TEXT,
            sahibinden_mail TEXT,
            sahibinden_sifre TEXT,
            hepsiemlak_mail TEXT,
            hepsiemlak_sifre TEXT,
            emlakjet_mail TEXT,
            emlakjet_sifre TEXT,
            uygulama_sifre TEXT
        )''')
        self.conn.commit()

    def create_labeled_entry(self, label_text, attribute_name, show=""):
        """Giriş alanları için etiket ve giriş kutusu oluşturur."""        
        frame = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")

        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            font=("Helvetica", 14), 
            text_color="#546E7A"
        )
        label.pack(side="left", padx=10, pady=5)

        entry = ctk.CTkEntry(
            frame, 
            placeholder_text=label_text,
            show=show,
            width=300,
            height=40,
            corner_radius=10,
            fg_color="#ECEFF1",
            font=("Helvetica", 14)
        )
        entry.pack(side="right", padx=(10, 5), pady=5)
        setattr(self, f"{attribute_name}_entry", entry)

    def create_password_entry(self, label_text, attribute_name):
        """Şifre giriş alanları için göz ikonu ekleyerek özel giriş kutusu oluşturur."""        
        frame = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")

        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            font=("Helvetica", 14), 
            text_color="#546E7A"
        )
        label.pack(side="left", padx=10, pady=5)

        entry_frame = ctk.CTkFrame(frame)  # Giriş kutusunun yer alacağı çerçeve
        entry_frame.pack(side="right", padx=(10, 5), pady=5)

        entry = ctk.CTkEntry(
            entry_frame, 
            placeholder_text=label_text,
            show="*",
            width=250,
            height=40,
            corner_radius=10,
            fg_color="#ECEFF1",
            font=("Helvetica", 14)
        )
        entry.pack(side="left", fill="x", padx=0)

        # Şifreyi göster/gizle ikonu
        self.show_password = False
        self.toggle_button_color = "#B0BEC5"
        toggle_button = ctk.CTkButton(
            entry_frame, 
            text="👁", 
            command=lambda e=entry: self.toggle_password_visibility(e, toggle_button),
            width=30,
            height=30,
            fg_color=self.toggle_button_color,
            corner_radius=15
        )
        toggle_button.pack(side="right", padx=(5, 0))

        setattr(self, f"{attribute_name}_entry", entry)

    def toggle_password_visibility(self, entry, toggle_button):
        """Şifre alanının görünürlüğünü değiştirir."""
        if entry.cget("show") == "*":
            entry.configure(show="")
            toggle_button.configure(fg_color="#1E88E5")
        else:
            entry.configure(show="*")
            toggle_button.configure(fg_color="#B0BEC5")

    def save_settings(self):
        """Emlakçı bilgilerini veritabanına kaydeder veya günceller."""        
        emlak_adi = self.emlak_adi_entry.get()
        sahibinden_mail = self.sahibinden_mail_entry.get()
        sahibinden_sifre = self.sahibinden_sifre_entry.get()
        hepsiemlak_mail = self.hepsiemlak_mail_entry.get()
        hepsiemlak_sifre = self.hepsiemlak_sifre_entry.get()
        emlakjet_mail = self.emlakjet_mail_entry.get()
        emlakjet_sifre = self.emlakjet_sifre_entry.get()
        uygulama_sifre = self.uygulama_sifre_entry.get()

        # Verilerin daha önce kaydedilip kaydedilmediğini kontrol et        
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        
        if data:
            # Eğer kayıt varsa güncelle
            if (data[1] == emlak_adi and data[2] == sahibinden_mail and data[3] == sahibinden_sifre and 
                data[4] == hepsiemlak_mail and data[5] == hepsiemlak_sifre and data[6] == emlakjet_mail and 
                data[7] == emlakjet_sifre and data[8] == uygulama_sifre):
                messagebox.showerror("Hata", "Hiçbir değişiklik yok. Lütfen bilgileri güncelleyiniz.")
                return

            self.cursor.execute('''UPDATE estateagentsettings 
                SET emlak_adi=?, sahibinden_mail=?, sahibinden_sifre=?, hepsiemlak_mail=?, hepsiemlak_sifre=?, emlakjet_mail=?, emlakjet_sifre=?, uygulama_sifre=?
                WHERE id=1''', (emlak_adi, sahibinden_mail, sahibinden_sifre, hepsiemlak_mail, hepsiemlak_sifre, emlakjet_mail, emlakjet_sifre, uygulama_sifre))
        else:
            # Kayıt yoksa yeni kayıt oluştur
            self.cursor.execute('''INSERT INTO estateagentsettings (id, emlak_adi, sahibinden_mail, sahibinden_sifre, hepsiemlak_mail, hepsiemlak_sifre, emlakjet_mail, emlakjet_sifre, uygulama_sifre) 
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)''', (emlak_adi, sahibinden_mail, sahibinden_sifre, hepsiemlak_mail, hepsiemlak_sifre, emlakjet_mail, emlakjet_sifre, uygulama_sifre))
        
        self.conn.commit()
        messagebox.showinfo("Başarılı", "Bilgiler başarıyla kaydedildi.")
        if uygulama_sifre is None or uygulama_sifre.strip() == "":
            self.settings_button.configure(
                text="⚠️ Ayarlar",
                text_color="red")
            self.show_security_message()
        else:
            self.settings_button.configure(
                text="Ayarlar",
                text_color="white")

    def show_security_message(self):
        messagebox.showinfo(
            "Güvenlik Uyarısı", 
            "Uygulama şifresi koymak, güvenliğinizi artıracaktır. Lütfen en kısa sürede şifre koyun !")

    def load_settings(self):
        """Veritabanından emlakçı bilgilerini yükler ve giriş alanlarına yazar."""        
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        
        if data:
            self.emlak_adi_entry.insert(0, data[1])
            self.sahibinden_mail_entry.insert(0, data[2])
            self.sahibinden_sifre_entry.insert(0, data[3])
            self.hepsiemlak_mail_entry.insert(0, data[4])
            self.hepsiemlak_sifre_entry.insert(0, data[5])
            self.emlakjet_mail_entry.insert(0, data[6])
            self.emlakjet_sifre_entry.insert(0, data[7])
            self.uygulama_sifre_entry.insert(0, data[8])

    def __del__(self):
        """Veritabanı bağlantısını kapatır."""
        try:
            if self.conn:
                self.conn.close()
        except AttributeError:
            pass
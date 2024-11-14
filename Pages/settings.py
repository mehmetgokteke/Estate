import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from password import PasswordEntry
import re

class Settings(ctk.CTkFrame):
    def __init__(self, parent, settings_button):
        super().__init__(parent)
        self.settings_button = settings_button
        
        self.conn = sqlite3.connect('estateagentsettings.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        
        self.label = ctk.CTkLabel(
            self,
            text="AYARLAR",
            font=("Helvetica", 30, "bold"), 
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        self.create_labeled_entry("Emlak Adı:", "emlak_adi")
        self.create_labeled_entry("Sahibinden Mail:", "sahibinden_mail")
        self.create_password_entry("Sahibinden Şifre:", "sahibinden_sifre")
        self.create_labeled_entry("Hepsiemlak Mail:", "hepsiemlak_mail")
        self.create_password_entry("Hepsiemlak Şifre:", "hepsiemlak_sifre")
        self.create_labeled_entry("Emlakjet Mail:", "emlakjet_mail")
        self.create_password_entry("Emlakjet Şifre:", "emlakjet_sifre")
        self.create_password_entry("Uygulama Şifresi:", "uygulama_sifre")

        self.save_button = ctk.CTkButton(
            self, 
            text="Kaydet/Güncelle", 
            command=self.save_settings,
            fg_color="#00ACC1",
            hover_color="#388E3C",
            font=("Helvetica", 25, "bold"),
            corner_radius=20,
            width=500
        )
        self.save_button.pack(pady=20)

        self.load_settings()

        self.check_password()

        self.bind("<Return>", lambda event: self.save_settings())

    def check_password(self):
        """Veritabanındaki şifreyi kontrol eder ve gerekirse şifre giriş penceresini açar."""
        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()

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
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")

        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            font=("Helvetica", 16), 
            text_color="#000000"
        )
        label.pack(side="left", padx=10, pady=5)
        setattr(self, f"{attribute_name}_label", label)

        entry = ctk.CTkEntry(
            frame, 
            placeholder_text=label_text,
            show=show,
            width=300,
            height=40,
            corner_radius=10,
            text_color="#000000",
            fg_color="#ECEFF1",
            font=("Helvetica", 16)
        )
        entry.pack(side="right", padx=(10, 5), pady=5)
        if attribute_name == "emlak_adi":
            entry.bind("<KeyRelease>", self.convert_to_uppercase)   
        setattr(self, f"{attribute_name}_entry", entry)

    def convert_to_uppercase(self, event):
        """Emlak Adı giriş kutusuna yazılan metni büyük harfe çevirir."""
        widget = event.widget
        current_text = widget.get()
        widget.delete(0, "end")
        widget.insert(0, current_text.upper())

    def create_password_entry(self, label_text, attribute_name):
        """Şifre giriş alanları için göz ikonu ekleyerek özel giriş kutusu oluşturur."""        
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")

        label = ctk.CTkLabel(
            frame, 
            text=label_text, 
            font=("Helvetica", 16), 
            text_color="#546E7A"
        )
        label.pack(side="left", padx=10, pady=5)
        setattr(self, f"{attribute_name}_label", label)

        entry_frame = ctk.CTkFrame(frame)
        entry_frame.pack(side="right", padx=(10, 5), pady=5)

        entry = ctk.CTkEntry(
            entry_frame, 
            placeholder_text=label_text,
            show="*",
            width=250,
            height=40,
            corner_radius=10,
            text_color="#000000",
            fg_color="#ECEFF1",
            font=("Helvetica", 16)
        )
        entry.pack(side="left", fill="x", padx=0)

        self.show_password = False
        self.toggle_button_color = "#00ACC1"
        toggle_button = ctk.CTkButton(
            entry_frame, 
            text="👁", 
            command=lambda e=entry: self.toggle_password_visibility(e, toggle_button),
            width=30,
            height=30,
            hover_color="#388E3C",
            fg_color=self.toggle_button_color,
            corner_radius=15
        )
        toggle_button.pack(side="right", padx=(2, 2))

        setattr(self, f"{attribute_name}_entry", entry)

    def toggle_password_visibility(self, entry, toggle_button):
        """Şifre alanının görünürlüğünü değiştirir."""
        if entry.cget("show") == "*":
            entry.configure(show="")
            toggle_button.configure(fg_color="#388E3C")
        else:
            entry.configure(show="*")
            toggle_button.configure(fg_color="#00ACC1")

    def update_field_colors(self):
        """Giriş alanlarının ve etiketlerin renklerini günceller."""
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()

        def update_entry_and_label(entry, label, value):
            if value is None or value.strip() == "":
                entry.configure(fg_color="#FFCDD2")
                label.configure(text_color="#FF0000")
            else:
                entry.configure(fg_color="#ECEFF1")
                label.configure(text_color="#000000")

        if data:
            update_entry_and_label(self.emlak_adi_entry, self.emlak_adi_label, data[1])
            update_entry_and_label(self.sahibinden_mail_entry, self.sahibinden_mail_label, data[2])
            update_entry_and_label(self.sahibinden_sifre_entry, self.sahibinden_sifre_label, data[3])
            update_entry_and_label(self.hepsiemlak_mail_entry, self.hepsiemlak_mail_label, data[4])
            update_entry_and_label(self.hepsiemlak_sifre_entry, self.hepsiemlak_sifre_label, data[5])
            update_entry_and_label(self.emlakjet_mail_entry, self.emlakjet_mail_label, data[6])
            update_entry_and_label(self.emlakjet_sifre_entry, self.emlakjet_sifre_label, data[7])
            update_entry_and_label(self.uygulama_sifre_entry, self.uygulama_sifre_label, data[8])

    def is_valid_email(self, email):
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

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

        if not all(self.is_valid_email(mail) for mail in [sahibinden_mail, hepsiemlak_mail, emlakjet_mail]):
            messagebox.showerror("Hata", "Geçersiz e-posta adresi. Lütfen geçerli bir e-posta adresi giriniz!")
            return
       
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        
        if data:
            if (data[1] == emlak_adi and data[2] == sahibinden_mail and data[3] == sahibinden_sifre and 
                data[4] == hepsiemlak_mail and data[5] == hepsiemlak_sifre and data[6] == emlakjet_mail and 
                data[7] == emlakjet_sifre and data[8] == uygulama_sifre):
                messagebox.showerror("Hata", "Hiçbir değişiklik yok. Lütfen bilgileri güncelleyiniz.")
                return

            self.cursor.execute('''UPDATE estateagentsettings 
                SET emlak_adi=?, sahibinden_mail=?, sahibinden_sifre=?, hepsiemlak_mail=?, hepsiemlak_sifre=?, emlakjet_mail=?, emlakjet_sifre=?, uygulama_sifre=?
                WHERE id=1''', (emlak_adi, sahibinden_mail, sahibinden_sifre, hepsiemlak_mail, hepsiemlak_sifre, emlakjet_mail, emlakjet_sifre, uygulama_sifre))
        else:
            self.cursor.execute('''INSERT INTO estateagentsettings (id, emlak_adi, sahibinden_mail, sahibinden_sifre, hepsiemlak_mail, hepsiemlak_sifre, emlakjet_mail, emlakjet_sifre, uygulama_sifre) 
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)''', (emlak_adi, sahibinden_mail, sahibinden_sifre, hepsiemlak_mail, hepsiemlak_sifre, emlakjet_mail, emlakjet_sifre, uygulama_sifre))
        
        self.conn.commit()
        messagebox.showinfo("Başarılı", "Bilgiler başarıyla kaydedildi.")
        self.update_field_colors()

        if uygulama_sifre is None or uygulama_sifre.strip() == "":
            self.settings_button.configure(
                text="❗ Ayarlar",
                text_color="red")
            self.show_security_message()
        else:
            self.settings_button.configure(
                text="⚙️ Ayarlar",
                text_color="#000000")

    def show_security_message(self):
        messagebox.showinfo(
            "Güvenlik Uyarısı", 
            "Uygulama şifresi koymak, güvenliğinizi artıracaktır. Lütfen en kısa sürede şifre koyun !")

    def load_settings(self):
        """Veritabanından emlakçı bilgilerini yükler ve giriş alanlarına yazar."""        
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()

        def set_entry_value(entry, value):
            if value is None or value.strip() == "":
                entry.configure(fg_color="#FFCDD2")
            else:
                entry.configure(fg_color="#ECEFF1")
                entry.insert(0, value)

        def set_label_color(label, entry_value):
            if entry_value is None or entry_value.strip() == "":
                label.configure(text_color="#FF0000")
            else:
                label.configure(text_color="#000000")
        
        if data:
            set_entry_value(self.emlak_adi_entry, data[1])
            set_entry_value(self.sahibinden_mail_entry, data[2])
            set_entry_value(self.sahibinden_sifre_entry, data[3])
            set_entry_value(self.hepsiemlak_mail_entry, data[4])
            set_entry_value(self.hepsiemlak_sifre_entry, data[5])
            set_entry_value(self.emlakjet_mail_entry, data[6])
            set_entry_value(self.emlakjet_sifre_entry, data[7])
            set_entry_value(self.uygulama_sifre_entry, data[8])

            set_label_color(self.emlak_adi_label, data[1])
            set_label_color(self.sahibinden_mail_label, data[2])
            set_label_color(self.sahibinden_sifre_label, data[3])
            set_label_color(self.hepsiemlak_mail_label, data[4])
            set_label_color(self.hepsiemlak_sifre_label, data[5])
            set_label_color(self.emlakjet_mail_label, data[6])
            set_label_color(self.emlakjet_sifre_label, data[7])
            set_label_color(self.uygulama_sifre_label, data[8])
        else:
            for entry_name in [
                "emlak_adi_entry",
                "sahibinden_mail_entry", 
                "sahibinden_sifre_entry", 
                "hepsiemlak_mail_entry", 
                "hepsiemlak_sifre_entry", 
                "emlakjet_mail_entry", 
                "emlakjet_sifre_entry", 
                "uygulama_sifre_entry"
            ]:
                entry = getattr(self, entry_name)
                entry.configure(fg_color="#FF0000")

            for label_name in [
                "emlak_adi_entry",
                "sahibinden_mail_entry", 
                "sahibinden_sifre_entry", 
                "hepsiemlak_mail_entry", 
                "hepsiemlak_sifre_entry", 
                "emlakjet_mail_entry", 
                "emlakjet_sifre_entry", 
                "uygulama_sifre_entry"
            ]:
                label = getattr(self, label_name)
                label.configure(text_color="#FF0000")

    def __del__(self):
        """Veritabanı bağlantısını kapatır."""
        try:
            if self.conn:
                self.conn.close()
        except AttributeError:
            pass
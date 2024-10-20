import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class PasswordEntry(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Emlak Yönetim Sistemi (EYS)")
        self.geometry("400x250")
        self.resizable(False, False)

        # Başlık için stil
        label = ctk.CTkLabel(
            self, 
            text="Uygulama Şifresi", 
            font=("Helvetica", 25, "bold"), 
            text_color="#37474F"
        )
        label.pack(pady=20)

        # Şifre giriş alanı
        self.password_entry = ctk.CTkEntry(
            self, 
            show="*", 
            placeholder_text="Şifreyi girin", 
            width=300, 
            height=40, 
            corner_radius=10
        )
        self.password_entry.pack(pady=10)

        # Giriş butonu
        self.login_button = ctk.CTkButton(
            self, 
            text="Giriş Yap", 
            command=self.check_password,
            fg_color="#00ACC1", 
            hover_color="#00838F",
            font=("Helvetica", 18, "bold"),
            corner_radius=10
        )
        self.login_button.pack(pady=20)

        # Pencereyi kapatma işlemi
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Enter tuşuna basıldığında giriş yap butonunu tıklat
        self.password_entry.bind("<Return>", self.enter_pressed)

        # Uygulama ilk açıldığında şifre giriş alanına odaklan
        self.password_entry.focus()

    def enter_pressed(self, event):
        """Enter tuşuna basıldığında check_password fonksiyonunu çağırır."""
        self.check_password()

    def check_password(self):
        """Veritabanındaki şifre ile karşılaştırır ve giriş izni verir."""
        password = self.password_entry.get()

        # Veritabanı bağlantısı
        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()

        # Şifreyi sorgula
        cursor.execute("SELECT uygulama_sifre FROM estateagentsettings WHERE id=1")
        stored_password = cursor.fetchone()

        if stored_password and stored_password[0] == password:
            self.destroy()  # Pencereden çık
        else:
            messagebox.showerror("Hata", "Geçersiz şifre. Lütfen tekrar deneyin.")
            self.password_entry.focus()  # Şifre giriş alanına odaklan

        conn.close()

    def on_close(self):
        """Kapatma işlemi sırasında uygulamanın tamamen kapanmasını sağlar."""
        if messagebox.askquestion("Çıkış", "Uygulamayı kapatmak istediğinize emin misiniz?") == 'yes':
            self.destroy()  # Pencereyi kapat
            exit()  # Uygulamayı kapat
        else:
            self.deiconify()
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class PasswordEntry(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Emlak Yönetim Sistemi (EYS)")
        self.geometry("400x250")
        self.resizable(False, False)

        label = ctk.CTkLabel(
            self, 
            text="Uygulama Şifresi", 
            font=("Helvetica", 25, "bold"), 
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=50
        )
        label.pack(pady=20)

        self.password_entry = ctk.CTkEntry(
            self, 
            show="*", 
            placeholder_text="Şifreyi girin", 
            width=300, 
            height=40,
            corner_radius=10
        )
        self.password_entry.pack(pady=10)

        self.show_password_button = ctk.CTkButton(
            self,
            text="👁",
            command=self.toggle_password_visibility,
            width=30,
            height=30,
            fg_color="#00ACC1",
            hover_color="#388E3C",
            corner_radius=15
        )
        self.show_password_button.place(relx=0.8, rely=0.4, anchor="center")

        self.login_button = ctk.CTkButton(
            self, 
            text="Giriş Yap", 
            command=self.check_password,
            fg_color="#00ACC1", 
            hover_color="#388E3C",
            font=("Helvetica", 18, "bold"),
            corner_radius=10
        )
        self.login_button.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.password_entry.bind("<Return>", self.enter_pressed)

        self.password_entry.focus()

        self.password_visible = False

    def enter_pressed(self, event):
        """Enter tuşuna basıldığında check_password fonksiyonunu çağırır."""
        self.check_password()

    def toggle_password_visibility(self):
        """Şifre giriş alanının görünürlüğünü değiştirir."""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.configure(show="")
            self.show_password_button.configure(fg_color="#388E3C")
        else:
            self.password_entry.configure(show="*")
            self.show_password_button.configure(fg_color="#00ACC1")

    def check_password(self):
        """Veritabanındaki şifre ile karşılaştırır ve giriş izni verir."""
        password = self.password_entry.get()

        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()

        cursor.execute("SELECT uygulama_sifre FROM estateagentsettings WHERE id=1")
        stored_password = cursor.fetchone()

        if stored_password and stored_password[0] == password:
            self.destroy()
        else:
            messagebox.showerror("Hata", "Geçersiz şifre. Lütfen tekrar deneyin.")
            self.password_entry.focus()

        conn.close()

    def on_close(self):
        """Kapatma işlemi sırasında uygulamanın tamamen kapanmasını sağlar."""
        if messagebox.askquestion("Çıkış", "Uygulamayı kapatmak istediğinize emin misiniz?") == 'yes':
            self.master.withdraw()
            self.destroy()
            exit()
        else:
            self.deiconify()
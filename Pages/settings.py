import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import messagebox
from password import PasswordEntry
import re
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
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

        self.button_frame = ctk.CTkFrame(self, corner_radius=20)
        self.button_frame.pack(pady=20, padx=20, fill="x")

        self.save_button = ctk.CTkButton(self.button_frame, text="Kaydet/Güncelle", text_color="black", command=self.save_settings, fg_color="#00ACC1", hover_color="#388E3C", font=("Helvetica", 15, "bold"), corner_radius=20, width=400)
        self.save_button.pack(side="right", padx=10)
        self.emlakjet = ctk.CTkButton(self.button_frame, text="Emlakjet", text_color="black", command=self.emlakjet, fg_color="#3BBF9F", hover_color="#2D9F85", font=("Helvetica", 15, "bold"),corner_radius=20, width=200)
        self.emlakjet.pack(side="left", padx=10)
        self.sahibinden = ctk.CTkButton(self.button_frame, text="Sahibinden", text_color="black", command=self.sahibinden, fg_color="#F6C91B", hover_color="#D7B31D", font=("Helvetica", 15, "bold"),corner_radius=20, width=200)
        self.sahibinden.pack(side="left", padx=10)
        self.hepsiemlak = ctk.CTkButton(self.button_frame, text="Hepsiemlak", text_color="black", command=self.hepsiemlak, fg_color="#F2545B", hover_color="#E04F66", font=("Helvetica", 15, "bold"),corner_radius=20, width=200)
        self.hepsiemlak.pack(side="left", padx=20)

        self.load_settings()

        self.check_password()

        self.bind("<Return>", lambda event: self.save_settings())

    def check_password(self):
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
        self.cursor.execute('SELECT uygulama_sifre FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        return data[0] if data else ""

    def create_table(self):
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
        widget = event.widget
        current_text = widget.get()
        widget.delete(0, "end")
        widget.insert(0, current_text.upper())

    def create_password_entry(self, label_text, attribute_name):       
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
        if entry.cget("show") == "*":
            entry.configure(show="")
            toggle_button.configure(fg_color="#388E3C")
        else:
            entry.configure(show="*")
            toggle_button.configure(fg_color="#00ACC1")

    def update_field_colors(self):
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
        messagebox.showinfo("Güvenlik Uyarısı", "Uygulama şifresi koymak, güvenliğinizi artıracaktır. Lütfen en kısa sürede şifre koyun !")

    def load_settings(self):       
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
        try:
            if self.conn:
                self.conn.close()
        except AttributeError:
            pass

    def emlakjet(self):
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        mail = data[6]
        password = data[7]
        if mail and password:
            self.emlakjet.configure(state=tk.DISABLED, text="Giriş yapılıyor...")
            self.save_button.configure(state=tk.DISABLED)
            self.sahibinden.configure(state=tk.DISABLED)
            self.hepsiemlak.configure(state=tk.DISABLED)
            threading.Thread(target=self.emlakjet_login, args=(mail, password)).start()
        else:
            messagebox.showerror("Hata", "Lütfen ilk önce Emlakjet için mail ve şifre ekleyiniz !")
        return
    
    def emlakjet_login(self, mail, password):
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            driver.get("https://www.emlakjet.com/#giris")
            email = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="custom-css-outlined-input" and @type="text"]')))
            email.send_keys(f"{mail}")
            key = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="custom-css-outlined-input" and @type="password"]')))
            key.send_keys(f"{password}")
            login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ej27 ej1 ej3 ej6 _3gH3oX nWFrjm" and @style="width: 100%; border-radius: 3px; margin-bottom: 16px;" and @type="button"]')))
            login.click()
            time.sleep(2)
            if driver.current_url == "https://www.emlakjet.com/#giris":
                messagebox.showwarning("Uyarı", "Emlakjet mail adresiniz ve/veya şifreniz hatalı.")
                driver.quit()
            else:
                profile = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="_3TtF9S"]')))
                profile.click()
                advert = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="ej27 ej33 ej36 ej41 ej42 ej30 ej31" and @tabindex="0"]')))
                advert.click()
                messagebox.showinfo("Bilgi", "Emlakjet'e otomatik giriş başarılı 😊")
        except TimeoutException as e:
            print("Zaman aşımı hatası:", str(e))
        finally:
            self.emlakjet.configure(state=tk.NORMAL, text="Emlakjet")
            self.save_button.configure(state=tk.NORMAL)
            self.sahibinden.configure(state=tk.NORMAL)
            self.hepsiemlak.configure(state=tk.NORMAL)
        
    def sahibinden(self):
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        mail = data[2]
        password = data[3]
        if mail and password:
            self.sahibinden.configure(state=tk.DISABLED, text="Giriş yapılıyor...")
            self.save_button.configure(state=tk.DISABLED)
            self.emlakjet.configure(state=tk.DISABLED)
            self.hepsiemlak.configure(state=tk.DISABLED)
            threading.Thread(target=self.sahibinden_login, args=(mail, password)).start()
        else:
            messagebox.showerror("Hata", "Lütfen ilk önce Sahibinden için mail ve şifre ekleyiniz !")
        return
    
    def sahibinden_login(self, mail, password):
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            driver.get("https://secure.sahibinden.com/giris")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="clearfix diagnostic-wrapper"]')))
            messagebox.showwarning("Uyarı", "Üzgünüm Sahibinden sitesi için CloudFlare'e yakalandım 😞")
            driver.quit()
        except TimeoutException:
            email = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="username" and @name="username"]')))
            email.send_keys(f"{mail}")
            key = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password" and @name="password"]')))
            key.send_keys(f"{password}")
            login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="userLoginSubmitButton"]')))
            login.click()
            time.sleep(3)
            url = driver.current_url
            if url == "https://secure.sahibinden.com/giris":
                messagebox.showwarning("Uyarı", "Sahibinden mail adresiniz ve/veya şifreniz hatalı.")
                driver.quit()
            else:
                messagebox.showinfo("Bilgi", "Sahibinden'e otomatik giriş başarılı 😊")
        finally:
            self.sahibinden.configure(state=tk.NORMAL, text="Sahibinden")
            self.save_button.configure(state=tk.NORMAL)
            self.emlakjet.configure(state=tk.NORMAL)
            self.hepsiemlak.configure(state=tk.NORMAL)

    def hepsiemlak(self):
        self.cursor.execute('SELECT * FROM estateagentsettings WHERE id=1')
        data = self.cursor.fetchone()
        mail = data[4]
        password = data[5]
        if mail and password:
            self.hepsiemlak.configure(state=tk.DISABLED, text="Giriş yapılıyor...")
            self.save_button.configure(state=tk.DISABLED)
            self.sahibinden.configure(state=tk.DISABLED)
            self.emlakjet.configure(state=tk.DISABLED)
            threading.Thread(target=self.hepsiemlak_login, args=(mail, password)).start()
        else:
            messagebox.showerror("Hata", "Lütfen ilk önce Hepsiemlak için mail ve şifre ekleyiniz !")
        return
        
    def hepsiemlak_login(self, mail, password):
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            driver.get("https://giris.hepsiemlak.com/giris-yap")
            email = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//input[@autocomplete="email" and @type="text"]')))
            email.send_keys(f"{mail}")
            key = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//input[@autocomplete="password" and @type="password"]')))
            key.send_keys(f"{password}")
            login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="w-full leading-tight hover:bg-red-dark transition-all ease-linear focus:outline-none flex text-16p items-center justify-center font-bold bg-red rounded-4p py-13p px-6 text-white cursor-pointer select-none mb-20p"]')))
            login.click()
            time.sleep(4)
            if driver.current_url == "https://giris.hepsiemlak.com/giris-yap":
                messagebox.showwarning("Uyarı", "Hepsiemlak mail adresiniz ve/veya şifreniz hatalı.")
                driver.quit()
            else:
                driver.get("https://www.hepsiemlak.com/bireysel/profilim")
                messagebox.showinfo("Bilgi", "Hepsiemlak'a otomatik giriş başarılı 😊")
        except TimeoutException as e:
            print("Zaman aşımı hatası:", str(e))
        finally:
            self.hepsiemlak.configure(state=tk.NORMAL, text="Hepsiemlak")
            self.save_button.configure(state=tk.NORMAL)
            self.sahibinden.configure(state=tk.NORMAL)
            self.emlakjet.configure(state=tk.NORMAL)
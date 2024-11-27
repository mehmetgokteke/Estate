import customtkinter as ctk
import tkinter as tk
import sqlite3
from tkinter import messagebox
from Pages import mainpage
from Pages import customerprofile
from Pages import customeredit
from Pages import portfolio
from Pages import portfolioedit
from Pages.marketanalysis import marketanalysis
from Pages import calendar
from Pages import settings
from password import PasswordEntry
class Estate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x750")
        self.minsize(1500, 750)
        self.title("Emlak Yönetim Sistemi (EYS)")
        # self.iconbitmap("")  # İkon eklemek için

        self.control = 1
        self.fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.logo_label = ctk.CTkLabel(
        self.left_frame,
        text="🏠 Emlak Yönetim Sistemi 🏠",
        font=("Arial", 25, "bold"),
        text_color="#000000",
        corner_radius=10,
        fg_color="#40E0D0"
        )
        self.logo_label.pack(padx=10, pady=25)

        self.buttons = {
            "🏠 Anasayfa": mainpage.mainpage,
            "👤 Müşteri Profili": customerprofile.CustomerProfile,
            "📋 Müşteri Düzenleme": customeredit.CustomerEdit,
            "📂 Portföy": portfolio.portfolio,
            "📝 Portföy Düzenleme": portfolioedit.portfolioedit,
            "📊 Piyasa Analizi": marketanalysis,
            "📅 Takvim": calendar.calendar,
            "⚙️ Ayarlar": settings.Settings  
        }

        self.create_buttons()

        self.change_page(mainpage.mainpage)

        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(
            self.left_frame, 
            text="Light Mode", 
            command=self.switch_event,
            variable=self.switch_var, 
            onvalue="on", 
            offvalue="off"
        )
        self.switch.place(relx=0.019, rely=1.0, anchor=tk.SW)

        self.check_password()

        marketanalysis(self, self.update_analysis_button_status)

    def create_buttons(self):
        for button_text, page_class in self.buttons.items():
            button = ctk.CTkButton(
                self.left_frame,
                text=button_text,
                command=lambda p=page_class: self.change_page(p),
                fg_color="#00BCD4",
                hover_color="#388E3C",
                text_color="#000000",
                font=("Arial", 18),
                corner_radius=50,
                height=40
            )
            button.pack(fill="x", padx=25, pady=20)

            if button_text == "⚙️ Ayarlar":
                self.settings_button = button

    def check_password(self):
        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()

        cursor.execute("SELECT uygulama_sifre FROM estateagentsettings WHERE id=1")
        stored_password = cursor.fetchone()

        if stored_password is None or stored_password[0] is None or stored_password[0] == "":
            conn.close()
            self.settings_button.configure(
                text="❗ Ayarlar",
                text_color="red"
            )
            self.show_security_message()
            self.change_page(settings.Settings)
            return
        
        self.password_window = PasswordEntry()
        self.wait_window(self.password_window)
        conn.close()
    
    def show_security_message(self):
        messagebox.showinfo("Güvenlik Uyarısı", "Uygulama şifresi koymak, güvenliğinizi artıracaktır. Lütfen ayarlar kısmından bir şifre ekleyin.")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def update_analysis_button_status(self, disable):
        if disable:
            self.control = 0
        else:
            self.control = 1

    def change_page(self, page_class):
        if self.control == 0:
            messagebox.showwarning("Uyarı", "Analiz işlemi bitmeden sayfa değiştiremezsiniz !")
            return
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        if page_class == marketanalysis:
            page = page_class(self.right_frame, self.update_analysis_button_status)
        elif page_class == settings.Settings:
            page = page_class(self.right_frame, self.settings_button)
        else:
            page = page_class(self.right_frame)
        page.pack(fill="both", expand=True)

    def switch_event(self):
        if self.switch_var.get() == "on":
            ctk.set_appearance_mode("dark")
            self.switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("light")
            self.switch.configure(text="Light Mode")

if __name__ == "__main__":
    app = Estate()
    app.mainloop()
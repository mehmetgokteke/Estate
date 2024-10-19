import customtkinter as ctk
import tkinter as tk
from Pages import mainpage
from Pages import customerprofile
from Pages import customeredit
from Pages import portfolio
from Pages import portfolioedit
from Pages import marketanalysis
from Pages import calendar
from Pages import settings

class Estate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x750")
        self.minsize(1500, 750)
        self.title("Emlak Yönetim Sistemi (EYS)")
        # self.iconbitmap("")  # İkon eklemek için

        # Tam ekran moduna geçiş
        self.fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        # Frame'leri oluştur
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Başlık için logo veya uygulama ismi
        self.logo_label = ctk.CTkLabel(
        self.left_frame,
        text="Emlak Yönetim Sistemi",
        font=("Arial", 25, "bold"),
        text_color="#9C27B0",
        corner_radius=10,
        fg_color="#FFEBEE"
        )
        self.logo_label.pack(padx=10, pady=25)

        # Buton isimleri ve sayfa sınıfları
        self.buttons = {
            "Anasayfa": mainpage.mainpage,
            "Müşteri Profili": customerprofile.customerprofile,
            "Müşteri Düzenleme": customeredit.customeredit,
            "Portföy": portfolio.portfolio,
            "Portföy Düzenleme": portfolioedit.portfolioedit,
            "Piyasa Analizi": marketanalysis.marketanalysis,
            "Takvim": calendar.calendar,
            "Ayarlar": settings.settings  
        }

        # Butonları oluştur
        self.create_buttons()

        # Sağ frame'deki içeriklerin başlangıç durumu
        self.change_page(mainpage.mainpage)

        # Switch değişkeni
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

    def toggle_fullscreen(self, event=None):
        """Tam ekran modunu açar veya kapatır."""
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        """Tam ekran modundan çıkar."""
        self.fullscreen = False
        self.attributes("-fullscreen", False)

    def create_buttons(self):
        """Sol frame'e butonları oluştur ve ekle."""
        for button_text, page_class in self.buttons.items():
            button = ctk.CTkButton(
                self.left_frame,
                text=button_text,
                command=lambda p=page_class: self.change_page(p),
                fg_color="#00BCD4",
                hover_color="#388E3C",
                text_color="white",
                font=("Arial", 17),
                corner_radius=50,
                height=40
            )
            button.pack(fill="x", padx=25, pady=20)

    def change_page(self, page_class):
        """Sayfa değiştirme fonksiyonu."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        page = page_class(self.right_frame)
        page.pack(fill="both", expand=True)

    def switch_event(self):
        """Switch'in durumuna göre görünüm modunu değiştirir."""
        if self.switch_var.get() == "on":
            ctk.set_appearance_mode("dark")
            self.switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("light")
            self.switch.configure(text="Light Mode")

if __name__ == "__main__":
    app = Estate()
    app.mainloop()
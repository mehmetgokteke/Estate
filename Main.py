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
buttons = {
    "Anasayfa": Anasayfa,
    "Müşteri Profili": MusteriProfili,
    "Müşteri Düzenleme": MusteriDuzenleme,
    "Portföy": Portfoy,
    "Portföy Düzenleme": PortfoyDuzenleme,
    "Piyasa Analizi": PiyasaAnalizi,
    "Takvim": Takvim,
    "Ayarlar": Ayarlar  
}

# Butonları oluştur ve sol frame'e ekle
for button_text, page_class in buttons.items():
    button = ctk.CTkButton(left_frame, text=button_text, command=lambda p=page_class: change_page(p))
    button.pack(fill="x", padx=10, pady=5)

root.mainloop()

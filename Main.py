import customtkinter as ctk
from Pages import mainpage
from Pages import customerprofile
from Pages import customeredit
from Pages import portfolio
from Pages import portfolioedit
from Pages import marketanalysis
from Pages import calendar
from Pages import settings

# Ana pencereyi oluştur
root = ctk.CTk()
root.geometry("1280x720")
root.title("Anasayfa")

# Soldaki butonlar için frame oluştur
left_frame = ctk.CTkFrame(root, width=128, height=720)
left_frame.pack(side="left", fill="y")

# Sağdaki içerik için frame oluştur
right_frame = ctk.CTkFrame(root)
right_frame.pack(side="left", fill="both", expand=True)

# Sayfa değiştirme fonksiyonu
def change_page(page_class):
    for widget in right_frame.winfo_children():
        widget.destroy()
    page = page_class(right_frame)
    page.pack(fill="both", expand=True)

# Buton isimleri ve sayfa sınıfları
buttons = {
    "Anasayfa": mainpage.mainpage,
    "Müşteri Profili": customerprofile.customerprofile,
    "Müşteri Düzenleme": customeredit.customeredit,
    "Portföy": portfolio.portfolio,
    "Portföy Düzenleme": portfolioedit.portfolioedit,
    "Piyasa Analizi": marketanalysis.marketanalysis,
    "Takvim": calendar.calendar,
    "Ayarlar": settings.settings  
}

# Butonları oluştur ve sol frame'e ekle
for button_text, page_class in buttons.items():
    button = ctk.CTkButton(left_frame, text=button_text, command=lambda p=page_class: change_page(p),fg_color="yellow",text_color="black")
    button.pack(fill="x", padx=10, pady=5)

root.mainloop()

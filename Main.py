import customtkinter as ctk

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
def change_page(page_name):
    for widget in right_frame.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(right_frame, text=page_name, font=("Arial", 24))
    label.pack(pady=20)

# Buton isimleri ve sayfa başlıkları
buttons = {
    "Anasayfa": "Anasayfa",
    "Müşteri Profili": "Müşteri Profili",
    "Müşteri Düzenleme": "Müşteri Düzenleme",
    "Portföy": "Portföy Sayfası",
    "Portföy Düzenleme": "Portföy Düzenleme",
    "Piyasa Analizi": "Piyasa Analizi",
    "Takvim": "Takvim",
    "Ayarlar": "Ayarlar"
}

# Butonları oluştur ve sol frame'e ekle
for button_text, page_name in buttons.items():
    button = ctk.CTkButton(left_frame, text=button_text, command=lambda p=page_name: change_page(p))
    button.pack(fill="x", padx=10, pady=5)

root.mainloop()

import customtkinter as ctk

class mainpage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Hoş geldiniz mesajı
        welcome_label = ctk.CTkLabel(
            self, 
            text="Hoş Geldiniz, Emlak Yönetim Sistemi!",
            font=("Arial", 24, "bold"),
            fg_color="#4CAF50",  # Yeşil arka plan rengi
            corner_radius=10,
            text_color="white"
        )
        welcome_label.pack(pady=20, padx=20, fill="x", ipady=10)

        # Özet bilgileri içeren bir frame
        summary_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        summary_frame.pack(pady=20, padx=20, fill="x")

        # Özet bilgiler: Mülk sayıları, kiralık, satılık ve portföy bilgileri
        total_properties = ctk.CTkLabel(
            summary_frame, 
            text="Toplam Portföy: 120 Mülk", 
            font=("Arial", 16), 
            text_color="#333"
        )
        total_properties.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        rented_properties = ctk.CTkLabel(
            summary_frame, 
            text="Kiralık Mülkler: 45", 
            font=("Arial", 16), 
            text_color="#FF9800"  # Turuncu renk
        )
        rented_properties.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        sold_properties = ctk.CTkLabel(
            summary_frame, 
            text="Satılık Mülkler: 30", 
            font=("Arial", 16), 
            text_color="#03A9F4"  # Mavi renk
        )
        sold_properties.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        available_properties = ctk.CTkLabel(
            summary_frame, 
            text="Mevcut Portföy: 45", 
            font=("Arial", 16), 
            text_color="#4CAF50"  # Yeşil renk
        )
        available_properties.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Hızlı İşlemler butonları
        quick_actions_frame = ctk.CTkFrame(self, fg_color="#f9f9f9", corner_radius=10)
        quick_actions_frame.pack(pady=20, padx=20, fill="x")

        quick_add_customer = ctk.CTkButton(
            quick_actions_frame, 
            text="Müşteri Ekle", 
            fg_color="#4CAF50",
            text_color="white",
            command=self.add_customer
        )
        quick_add_customer.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        quick_add_property = ctk.CTkButton(
            quick_actions_frame, 
            text="Mülk Ekle", 
            fg_color="#03A9F4",
            text_color="white",
            command=self.add_property
        )
        quick_add_property.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        quick_analysis = ctk.CTkButton(
            quick_actions_frame, 
            text="Piyasa Analizi", 
            fg_color="#FF9800",
            text_color="white",
            command=self.market_analysis
        )
        quick_analysis.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Placeholder fonksiyonlar (Gerçek işlemlerle değiştirilmesi gerekecek)
    def add_customer(self):
        print("Müşteri ekleme işlemi başlatıldı.")

    def add_property(self):
        print("Mülk ekleme işlemi başlatıldı.")

    def market_analysis(self):
        print("Piyasa analizi işlemi başlatıldı.")

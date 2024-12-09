import customtkinter as ctk
import sqlite3
import tkinter as tk


class portfolio(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Başlık etiketi
        self.label = ctk.CTkLabel(
            self,
            text="PORTFÖY",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=20,
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        # TC Kimlik giriş ve Ara butonu ile filtreleme için Frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=20, padx=20, anchor="w")

        # Sol taraftaki TC Kimlik giriş alanı ve Ara butonu
        self.tc_label = ctk.CTkLabel(self.search_frame, text="TC Kimlik Numarası:", font=("Arial", 14), corner_radius=20)
        self.tc_label.pack(side="left", padx=(0, 10))

        self.tc_entry = ctk.CTkEntry(self.search_frame, placeholder_text="TC Kimlik Numarası", font=("Arial", 14), width=300, corner_radius=20)
        self.tc_entry.pack(side="left", padx=(0, 10))

        self.search_button = ctk.CTkButton(self.search_frame, text="Ara", command=self.search_portfolio, corner_radius=20)
        self.search_button.pack(side="left")

        # Sağ taraftaki yeni TextBox ve Filtrele butonu
        self.filter_label = ctk.CTkLabel(self.search_frame, text="Filtrele:", font=("Arial", 14), corner_radius=20)
        self.filter_label.pack(side="left", padx=(20, 10))

        self.filter_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Filtreleme Kriteri", font=("Arial", 14), width=300, corner_radius=20)
        self.filter_entry.pack(side="left", padx=(0, 10))

        self.filter_button = ctk.CTkButton(self.search_frame, text="Filtrele", command=self.filter_portfolio, corner_radius=20)
        self.filter_button.pack(side="left")

        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=1000, height=400, corner_radius=20)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tablo çerçevesi
        self.table_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=20)
        self.table_frame.pack(fill="both", expand=True)

        # İlk tabloyu göster
        self.show_all_portfolio()

    def show_all_portfolio(self):
        """Varsayılan olarak tüm portföyleri gösterir."""
        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio")
        records = cursor.fetchall()
        conn.close()

        self.populate_table(records)

    def search_portfolio(self):
        """Kullanıcının girdiği TC Kimlik'e ait verileri arar."""
        tc_kimlik = self.tc_entry.get().strip()

        if not tc_kimlik:
            tk.messagebox.showerror("Hata", "Lütfen bir TC Kimlik numarası girin.")
            return

        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio WHERE tc_kimlik = ?", (tc_kimlik,))
        records = cursor.fetchall()
        conn.close()

        if not records:
            tk.messagebox.showinfo("Bilgi", "Bu TC Kimlik numarasına ait kayıt bulunamadı.")
        else:
            self.populate_table(records)

    def filter_portfolio(self):
        """Kullanıcının girdiği filtre kriterine göre verileri filtreler."""
        filter_text = self.filter_entry.get().strip()

        if not filter_text:
            tk.messagebox.showerror("Hata", "Lütfen bir filtreleme kriteri girin.")
            return

        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        query = """
            SELECT * FROM portfolio
            WHERE id LIKE ? OR tc_kimlik LIKE ? OR oda_sayisi LIKE ? OR bina_yasi LIKE ? OR kat_sayisi LIKE ? 
            OR fiyat LIKE ? OR ilan_tarihi LIKE ? OR ilan_aciklamasi LIKE ? OR site_adi LIKE ? OR aidat LIKE ? 
            OR depozito LIKE ? OR banyo_sayisi LIKE ? OR balkon LIKE ? OR mutfak LIKE ? OR isinma_tipi LIKE ? 
            OR yakit_tipi LIKE ? OR cephe LIKE ? OR tapu_durumu LIKE ? OR yapi_tipi LIKE ? OR yapinin_durumu LIKE ? 
            OR kimden LIKE ? OR otopark LIKE ? OR asansor LIKE ? OR kullanim_durumu LIKE ? OR site_icerisinde LIKE ? 
            OR balkon_tipi LIKE ? OR ilan_durumu LIKE ? OR resim_adlari LIKE ? OR m2 LIKE ? OR bulundugu_kat LIKE ? 
            OR esya_durumu LIKE ? OR yetkili_ofis LIKE ? OR wc_sayisi LIKE ?
        """
        filter_pattern = f"%{filter_text}%"
        cursor.execute(query, tuple([filter_pattern] * 33))  # 33 sütun için aynı filtreyi uygular
        records = cursor.fetchall()
        conn.close()

        if not records:
            tk.messagebox.showinfo("Bilgi", "Filtre kriterine uyan kayıt bulunamadı.")
        else:
            self.populate_table(records)

    def populate_table(self, records):
        """Verilen kayıtları tabloya yerleştirir."""
        # Mevcut tabloyu temizle
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Sütun başlıkları
        column_headers = ["ID", "TC Kimlik", "Görüntüle"]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg_color="#00BCD4",
                text_color="white",
                corner_radius=20,
                padx=10,
                pady=5,
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        # Kayıtları tabloya yerleştir
        for row_index, record in enumerate(records):
            # TC Kimlik ve Görüntüle butonu
            ctk.CTkLabel(
                self.table_frame,
                text=record[0],  # ID
                font=("Arial", 10),
                fg_color="white",
                text_color="#000000",
                padx=10,
                pady=5,
                corner_radius=20
            ).grid(row=row_index + 1, column=0, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(
                self.table_frame,
                text=record[1],  # TC Kimlik
                font=("Arial", 10),
                fg_color="white",
                text_color="#000000",
                padx=10,
                pady=5,
                corner_radius=20
            ).grid(row=row_index + 1, column=1, padx=5, pady=5, sticky="nsew")

            # Görüntüle butonu
            ctk.CTkButton(
                self.table_frame,
                text="Görüntüle",
                command=lambda record=record: self.show_details(record),
                corner_radius=20
            ).grid(row=row_index + 1, column=2, padx=5, pady=5)

        # Grid tasarımı için kolonları genişlet
        for i in range(3):  # Sadece 3 sütun var
            self.table_frame.grid_columnconfigure(i, weight=1)

    def show_details(self, record):
        """Seçilen kaydın detaylarını yeni bir pencerede gösterir."""
        # Yeni pencere oluştur
        details_window = ctk.CTkToplevel(self)
        details_window.title("Kayıt Detayları")
        details_window.geometry("900x600")
        details_window.resizable(False, False)
        details_window.attributes('-topmost', True)  # Pencerenin önde kalmasını sağlar
        
        # Sol tarafta resim çerçevesi
        image_scroll_frame = ctk.CTkScrollableFrame(details_window, width=300, corner_radius=20)
        image_scroll_frame.pack(side="left", fill="y", padx=10, pady=10)

        try:
            # record[-1] (son eleman) resim adlarını içeriyor olmalı
            images = record[-1]
            
            # Eğer None veya boşsa, images listesini boş yap
            if images is None or images.strip() == "":
                images = []
            else:
                images = images.split(",")  # Virgülle ayırarak listeye dönüştür

            # Resimleri yükle ve göster
            for img in images:
                if img.strip():  # Boş resim adlarını geç
                    image_path = os.path.join("resimler", img.strip())  # Resimlerin kaydedildiği dizin
                    if os.path.exists(image_path):  # Resim dosyası mevcutsa
                        image = ctk.CTkImage(
                            Image.open(image_path),
                            size=(200, 150)  # Resmin boyutlandırılması
                        )
                        label = ctk.CTkLabel(
                            image_scroll_frame,
                            text=f"Resim: {img}",
                            image=image,
                            font=("Arial", 10),
                            fg_color="#DDDDDD",
                            text_color="#000000",
                            width=200,
                            height=150,
                            corner_radius=20,
                        )
                        label.pack(pady=5)
                    else:
                        label = ctk.CTkLabel(
                            image_scroll_frame,
                            text=f"Resim dosyası bulunamadı: {img}",
                            font=("Arial", 10),
                            fg_color="#FFDDDD",
                            text_color="#000000",
                            width=200,
                            height=150,
                            corner_radius=20,
                        )
                        label.pack(pady=5)
        except Exception as e:
            print(f"Resim yükleme hatası: {e}")
            tk.messagebox.showerror("Hata", "Resimler yüklenemedi!")

        # Sağ tarafta detaylar
        details_scroll_frame = ctk.CTkScrollableFrame(details_window)
        details_scroll_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Sütun başlıkları ve detay değerleri
        column_headers = [
            "ID", "TC Kimlik", "Oda Sayısı", "Bina Yaşı", "Kat Sayısı", "Fiyat", "İlan Tarihi",
            "İlan Açıklaması", "Site Adı", "Aidat", "Depozito", "Banyo Sayısı", "Balkon", "Mutfak",
            "Isınma Tipi", "Yakıt Tipi", "Cephe", "Tapu Durumu", "Yapı Tipi", "Yapı Durumu",
            "Kimden", "Otopark", "Asansör", "Kullanım Durumu", "Site İçerisinde", "Balkon Tipi",
            "İlan Durumu", "Resim Adları", "m2", "Bulunduğu Kat", "Eşya Durumu", "Yetkili Ofis", "WC Sayısı"
        ]

        for i, (header, value) in enumerate(zip(column_headers, record)):
            label = ctk.CTkLabel(details_scroll_frame, text=f"{header}:", font=("Arial", 12, "bold"), corner_radius=20)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            value_label = ctk.CTkLabel(details_scroll_frame, text=value, font=("Arial", 12), corner_radius=20)
            value_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # Detaylar için grid tasarımı
        details_scroll_frame.grid_columnconfigure(0, weight=1)
        details_scroll_frame.grid_columnconfigure(1, weight=2)



# Test için ana pencere
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x800")
    app = portfolio(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
    
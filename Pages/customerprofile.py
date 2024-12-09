import customtkinter as ctk
import sqlite3


class CustomerProfile(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(
            self,
            text="MÜŞTERİ PROFİLİ",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=20
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        # Filtre çerçevesi
        self.filter_frame = ctk.CTkFrame(self, corner_radius=20)
        self.filter_frame.pack(pady=10, fill="x")

        self.filter_label = ctk.CTkLabel(
            self.filter_frame,
            text="Filtre:",
            font=("Arial", 12, "bold"),
            text_color="#000000"
        )
        self.filter_label.pack(side="left", padx=10)

        self.filter_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="Ad Soyad / TC Kimlik / Telefon")
        self.filter_entry.pack(side="left", padx=10, expand=True, fill="x")

        self.filter_button = ctk.CTkButton(
            self.filter_frame,
            text="Filtrele",
            command=self.filter_customers
        )
        self.filter_button.pack(side="left", padx=10)

        # Tablo çerçevesi
        self.table_frame = ctk.CTkFrame(self, corner_radius=20)
        self.table_frame.pack(fill="both", expand=True)

        # Bilgilendirme etiketi
        self.info_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12, "bold"),
            text_color="#000000",
            corner_radius=20
        )
        self.info_label.pack(pady=10)

        # Kayıtları görüntüle
        self.view_customers()

    def view_customers(self, filter_value=None):
        # Mevcut tüm kayıtları görüntülemek için veritabanı bağlantısı
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()

        if filter_value:
            # Filtreleme sorgusu
            cursor.execute(
                """
                SELECT * FROM customers
                WHERE name LIKE ? OR tc_kimlik LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR age LIKE ? OR gender LIKE ? OR personal_note 
                """,
                (f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%")
            )
        else:
            cursor.execute("SELECT * FROM customers")

        records = cursor.fetchall()

        # TC Kimlik numaralarına göre benzersiz müşteri sayısını hesaplama
        cursor.execute("SELECT COUNT(DISTINCT tc_kimlik) FROM customers")
        unique_tc_count = cursor.fetchone()[0]
        conn.close()

        # Eğer filtre sonucu boşsa mesaj göster
        if filter_value and not records:
            self.info_label.configure(
                text=f"'{filter_value}' ile eşleşen bir kayıt bulunamadı!"
            )
            self.clear_table()
            return

        # Toplam ve benzersiz kayıt sayısını göster
        total_records = len(records)
        self.info_label.configure(
            text=f"Toplam Kayıt: {total_records} (Benzersiz TC Kimlik Sayısı: {unique_tc_count})"
        )

        # Eski tabloyu temizle
        self.clear_table()

        # Tablo başlıkları (sütun isimleri)
        column_headers = ["ID","Name", "TC Kimlik", "Phone", "Email", "Address", "Age", "Gender", "Personal Note"]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg_color="#00BCD4",  # Başlıklara arka plan rengi
                text_color="white",  # Yazı rengini beyaz yap
                corner_radius=20,  # Kenarları yuvarlat
                padx=10,  # İçerik boşluğu
                pady=5
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        # Kayıtları tabloya yerleştir
        for row_index, record in enumerate(records):
            for col_index, value in enumerate(record):
                label = ctk.CTkLabel(
                    self.table_frame,
                    text=value,
                    font=("Arial", 10),
                    fg_color="white",  # Hücre arka plan rengi
                    text_color="#000000",  # Siyah yazı rengi
                    padx=10,  # İçerik boşluğu
                    pady=5,
                    corner_radius=20
                )
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="nsew")

        # Grid tasarımı iyileştirmek için sütun genişliğini ayarla
        for i in range(len(column_headers)):
            self.table_frame.grid_columnconfigure(i, weight=1)

    def clear_table(self):
        """Tabloyu temizler."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def filter_customers(self):
        print("Filtreleme başlatıldı...")  # Bu satır eklendi
        filter_value = self.filter_entry.get().strip()
        if not filter_value:
            self.info_label.configure(text="Lütfen bir bilgi giriniz!")
            return

        # Veritabanı bağlantısı ve filtreleme
        conn = sqlite3.connect("customers.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM customers
            WHERE name LIKE ? OR tc_kimlik LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ? OR age LIKE ? OR gender LIKE ? OR personal_note LIKE ?
            """,
            (f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%", f"%{filter_value}%")
        )
        records = cursor.fetchall()
        conn.close()

        if not records:
            self.info_label.configure(text=f"'{filter_value}' ile eşleşen bir kayıt bulunamadı!")
        else:
            # Yeni pencere oluştur ve filtre sonucunu göster
            filter_window = ctk.CTkToplevel(self)
            filter_window.title("Filtre Sonuçları")
            filter_window.geometry("800x400")
            filter_window.resizable(True, True)

            filter_window.lift()  # Bu komut, pencerenin üstte görünmesini sağlar
            filter_window.attributes("-topmost", True)  # Bu komut pencerenin her zaman üstte olmasını sağlar


            filter_table_frame = ctk.CTkFrame(filter_window, corner_radius=20)
            filter_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

            column_headers = ["ID","Name", "TC Kimlik", "Phone", "Email", "Address", "Age", "Gender", "Personal Note"]

            for i, header in enumerate(column_headers):
                label = ctk.CTkLabel(
                    filter_table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    fg_color="#00BCD4",
                    text_color="white",
                    corner_radius=20,
                    padx=10,
                    pady=5
                )
                label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

            # Kayıtları tabloya yerleştir
            for row_index, record in enumerate(records):
                for col_index, value in enumerate(record):
                    label = ctk.CTkLabel(
                        filter_table_frame,
                        text=value,
                        font=("Arial", 10),
                        fg_color="white",
                        text_color="#000000",
                        padx=10,
                        pady=5,
                        corner_radius=20
                    )
                    label.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="nsew")

            # Sütun genişliğini ayarla
            for i in range(len(column_headers)):
                filter_table_frame.grid_columnconfigure(i, weight=1)

    def show_filtered_data(self, records):
        # Yeni pencere oluştur
        filtered_window = ctk.CTkToplevel(self)
        filtered_window.title("Filtrelenmiş Veri")
        filtered_window.geometry("800x200")

        # Çerçeve oluştur
        frame = ctk.CTkFrame(filtered_window, corner_radius=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tablo başlıkları (sütun isimleri)
        column_headers = ["ID", "Ad Soyad", "TC Kimlik", "Telefon", "E-posta", "İkametgah", "Yaş", "Cinsiyet", "Kişisel Not"]

        # Sütun başlıklarını ekle
        for i, header in enumerate(column_headers):
            label = ctk.CTkLabel(
                frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg_color="#00BCD4",
                text_color="white",
                corner_radius=20,
                padx=10,
                pady=5
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        # Kayıtları tabloya yerleştir
        for row_index, record in enumerate(records):
            for col_index, value in enumerate(record):
                label = ctk.CTkLabel(
                    frame,
                    text=value,
                    font=("Arial", 10),
                    fg_color="white",
                    text_color="#000000",
                    padx=10,
                    pady=5,
                    corner_radius=20
                )
                label.grid(row=row_index + 1, column=col_index, padx=5, pady=5, sticky="nsew")

        # Grid tasarımı iyileştirmek için sütun genişliğini ayarla
        for i in range(len(column_headers)):
            frame.grid_columnconfigure(i, weight=1)
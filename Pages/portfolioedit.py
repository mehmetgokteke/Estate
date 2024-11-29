
import os
from tkinter import filedialog, messagebox
import sqlite3
import customtkinter as ctk

class portfolioedit(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Başlık
        self.label_header = ctk.CTkLabel(
            self,
            text="PORTFÖY DÜZENLEME",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15,
        )
        self.label_header.pack(fill="x", padx=20, pady=20,ipady=20)

        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Alanlar ve seçenekler (önceden tanımlanan alanlar burada yer alacak)
        self.combo_vars = {}
        self.radio_vars = {}
        self.entries = {}
        self.selected_images = []  # Yüklenen resimleri takip etmek için


        

	# Alanlar ve seçenekler
        combo_box_options = {
            "Oda Sayısı": ["1+1", "2+1", "3+1", "4+1"],
            "Bina Yaşı": ["0-5", "6-10", "11-20", "21 ve üzeri"],
            "Bulunduğu Kat": ["Zemin", "1", "2", "3 ve üzeri"],
            "Isınma Tipi": ["Merkezi", "Doğalgaz", "Soba", "Yerden Isıtma"],
            "Kat Sayısı": ["1", "2-4", "5-10", "10 ve üzeri"],
            "Banyo Sayısı": ["1", "2", "3 ve üzeri"],
            "Cephe": ["Kuzey", "Güney", "Doğu", "Batı"],
            "Yakıt Tipi": ["Elektrik", "Doğalgaz", "Kömür", "Diğer"],
            "Mutfak": ["Açık", "Kapalı", "Amerikan"],
            "Balkon": ["Var", "Yok"],
            "Wc Sayısı": ["1", "2", "3 ve üzeri"]
        }

        radio_button_options = {
            "Balkon Tipi": ["Açık", "Kapalı"],
            "Kimden": ["Sahibinden", "Emlakçıdan"],
            "Site İçerisinde": ["Evet", "Hayır"],
            "Kullanım Durumu": ["Boş", "Kiracı Var", "Ev Sahibi Oturuyor"],
            "Asansör": ["Var", "Yok"],
            "Otopark": ["Var", "Yok"],
            "Yetkili Ofis": ["Var", "Yok"],
            "Tapu Durumu": ["Kat Mülkiyeti", "Kat İrtifakı", "Arsa Tapusu"],
            "Yapının Durumu": ["Sıfır", "İkinci El"],
            "Yapı Tipi": ["Betonarme", "Ahşap", "Çelik"],
            "İlan Durumu": ["Kiralık", "Satılık"]
        }

        entry_fields = [
            "m2", "Aidat", "Depozito", "Fiyat", "İlan Tarihi", "İlan Açıklaması", "Site Adı"
        ]
	
	# ComboBox alanları
        row = 0
        for field, options in combo_box_options.items():
            label = ctk.CTkLabel(self.scrollable_frame, text=field + ":", font=("Arial", 12))
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            self.combo_vars[field] = ctk.StringVar(value="Seçim Yok")
            combo_box = ctk.CTkComboBox(
                self.scrollable_frame,
                variable=self.combo_vars[field],
                values=options,
                state="readonly"  # Kullanıcı sadece belirlenen değerleri seçebilir
            )
            combo_box.grid(row=row, column=1, padx=10, pady=5, sticky="ew", columnspan=5)
            row += 1

        # RadioButton alanları
        for field, options in radio_button_options.items():
            label = ctk.CTkLabel(self.scrollable_frame, text=field + ":", font=("Arial", 12))
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            self.radio_vars[field] = ctk.StringVar(value="Seçim Yok")
            for i, option in enumerate(options):
                rb = ctk.CTkRadioButton(
                    self.scrollable_frame, text=option, variable=self.radio_vars[field], value=option
                )
                rb.grid(row=row, column=i + 1, padx=5, pady=5, sticky="w")
            row += 1

        # Entry alanları
        for field in entry_fields:
            label = ctk.CTkLabel(self.scrollable_frame, text=field + ":", font=("Arial", 12))
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            self.entries[field] = ctk.CTkEntry(self.scrollable_frame)
            self.entries[field].grid(row=row, column=1, columnspan=5, padx=10, pady=5, sticky="ew")
            row += 1

        # Resim Yükleme Butonu
        self.image_button = ctk.CTkButton(
            self.scrollable_frame, text="Resim Yükle", command=self.upload_image
        )
        self.image_button.grid(row=row, column=0, columnspan=6, padx=20, pady=20, sticky="ew")
        row += 1

            # Kaydetme butonu
        self.save_button = ctk.CTkButton(self.scrollable_frame, text="Kaydet", command=self.save_portfolio)
        self.save_button.grid(row=row, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
        row += 1

        # Portföy Arama Butonu
        self.search_button = ctk.CTkButton(self.scrollable_frame, text="Portföy Ara", command=self.search_portfolio)
        self.search_button.grid(row=row, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
        row += 1

        # Portföy Güncelleme Butonu
        self.update_button = ctk.CTkButton(self.scrollable_frame, text="Portföy Güncelle", command=self.update_portfolio)
        self.update_button.grid(row=row, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
        row += 1

        # Portföy Silme Butonu
        self.delete_button = ctk.CTkButton(self.scrollable_frame, text="Portföy Sil", command=self.delete_portfolio)
        self.delete_button.grid(row=row, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
        row += 1


        # Kolonları esnek hale getirme
        for col in range(6):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
        
        self.scrollable_frame.grid_rowconfigure(row, weight=1)
        
        self.selected_images = []


    def save_portfolio(self):
        # TC kimlik doğrulama
        tc_kimlik = self.ask_for_tc_kimlik()
        if tc_kimlik:
            data = self.collect_form_data()
            if data:
                self.save_to_portfolio_db(data, tc_kimlik)
                messagebox.showinfo("Başarılı", "Portföy başarıyla kaydedildi.")
        else:
            messagebox.showerror("Hata", "Geçersiz TC kimliği.")
     
    def upload_image(self):
        # Resim seçme
        file_path = filedialog.askopenfilename(
            title="Resim Seç",
            filetypes=[("Resim Dosyaları", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.selected_images.append(file_path)  # Yalnızca listeye ekle
            messagebox.showinfo("Başarılı", f"{os.path.basename(file_path)} seçildi.")

    def ask_for_tc_kimlik(self):
        # Kullanıcıdan TC kimlik al
        tc_kimlik_window = ctk.CTkToplevel(self)
        tc_kimlik_window.title("TC Kimlik")
        tc_kimlik_var = ctk.StringVar()  # Girdi için değişken oluştur
        tc_kimlik_label = ctk.CTkLabel(tc_kimlik_window, text="TC Kimlik No:")
        tc_kimlik_label.pack(padx=20, pady=10)
        tc_kimlik_entry = ctk.CTkEntry(tc_kimlik_window, textvariable=tc_kimlik_var)
        tc_kimlik_entry.pack(padx=20, pady=10)
        
        def on_confirm():
            tc_kimlik_window.destroy()
            
        confirm_button = ctk.CTkButton(tc_kimlik_window, text="Onayla", command=on_confirm)
        confirm_button.pack(padx=20, pady=10)
        
        tc_kimlik_window.wait_window(tc_kimlik_window)  # Pencere kapanana kadar bekle
        return tc_kimlik_var.get()  # Değeri döndür

    def check_tc_exists(self, tc_kimlik):
        try:
            conn = sqlite3.connect("customers.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE tc_kimlik = ?", (tc_kimlik,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
            return False

        print(f"T.C. Kimlik sorgulandı: {tc_kimlik}, Sonuç: {result}")


    def collect_form_data(self):
        data = {field: var.get() for field, var in self.combo_vars.items()}
        data.update({field: var.get() for field, var in self.radio_vars.items()})
        data.update({field: entry.get() for field, entry in self.entries.items()})
        return data

    def save_to_portfolio_db(self, data, tc_kimlik):
        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tc_kimlik TEXT,
                oda_sayisi TEXT,
                bina_yasi TEXT,
                kat_sayisi TEXT,
                fiyat TEXT,
                ilan_tarihi TEXT,
                ilan_aciklamasi TEXT,
                site_adi TEXT,
                yapi_durumu TEXT
            )
            '''
        )
        cursor.execute(
            '''
            INSERT INTO portfolio (
                tc_kimlik, oda_sayisi, bina_yasi, kat_sayisi, fiyat, ilan_tarihi, ilan_aciklamasi, site_adi, yapi_durumu
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                tc_kimlik,
                data.get("Oda Sayısı", ""),
                data.get("Bina Yaşı", ""),
                data.get("Kat Sayısı", ""),
                data.get("Fiyat", ""),
                data.get("İlan Tarihi", ""),
                data.get("İlan Açıklaması", ""),
                data.get("Site Adı", ""),
                data.get("Yapının Durumu", ""),
            ),
        )
        conn.commit()
        conn.close()


    def save_images(self, tc_kimlik):
        # Resimleri resimler klasörüne kaydet
        if not os.path.exists("resimler"):
            os.makedirs("resimler")
        for image_path in self.selected_images:
            file_name = os.path.basename(image_path)
            destination = os.path.join("resimler", f"{tc_kimlik}_{file_name}")
            os.rename(image_path, destination)
    
    def search_portfolio(self):
        tc_kimlik = self.ask_for_tc_kimlik()
        if not tc_kimlik:
            messagebox.showerror("Hata", "Geçersiz TC kimliği.")
            return
        
        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio WHERE tc_kimlik = ?", (tc_kimlik,))
        results = cursor.fetchall()
        conn.close()
        
        if results:
            self.show_table(results, "Arama Sonuçları", include_all_columns=True)
        else:
            messagebox.showerror("Hata", "Girilen TC kimliğine ait kayıt bulunamadı.")


    def update_portfolio(self):
        """
        Kullanıcının verdiği TC kimlik numarasına ait portföy verilerini getirir ve düzenlenebilir bir tabloda gösterir.
        Kullanıcı değişiklik yaptıktan sonra 'Kaydet' butonuna basarak verileri güncelleyebilir.
        """
        tc_kimlik = self.ask_for_tc_kimlik()
        if not tc_kimlik:
            messagebox.showerror("Hata", "Geçersiz TC kimlik numarası.")
            return

        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio WHERE tc_kimlik = ?", (tc_kimlik,))
        results = cursor.fetchall()

        # Sütun adlarını alın
        cursor.execute("PRAGMA table_info(portfolio)")
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()

        if results:
            # Değişiklikleri kaydetme fonksiyonu
            def save_changes(entries):
                try:
                    conn = sqlite3.connect("portfolio.db")
                    cursor = conn.cursor()
                    for entry_row in entries:
                        row_id = int(entry_row[0].cget("text"))  # ID sütunundan alınır
                        new_values = [e.get() for e in entry_row[1:]]  # ID hariç diğer değerleri al
                        update_query = f'''
                            UPDATE portfolio
                            SET {", ".join(f"{col} = ?" for col in columns[1:])}
                            WHERE id = ?
                        '''
                        cursor.execute(update_query, (*new_values, row_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Başarılı", "Güncellemeler başarıyla kaydedildi.")
                except Exception as e:
                    messagebox.showerror("Hata", f"Güncelleme sırasında bir hata oluştu: {e}")
                    conn.rollback()
                    conn.close()

            # Düzenlenebilir tabloyu göster
            self.show_table(results, "Portföy Güncelle", editable=True, on_save=save_changes, include_all_columns=True)
        else:
            messagebox.showerror("Hata", "Girilen TC kimlik numarasına ait kayıt bulunamadı.")



    def delete_portfolio(self):
        tc_kimlik = self.ask_for_tc_kimlik()
        if not tc_kimlik:
            messagebox.showerror("Hata", "Geçersiz TC kimliği.")
            return

        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio WHERE tc_kimlik = ?", (tc_kimlik,))
        results = cursor.fetchall()
        conn.close()

        if results:
            def delete_selected(selected_rows):
                conn = sqlite3.connect("portfolio.db")
                cursor = conn.cursor()
                for checkbox, row_id in selected_rows:
                    if checkbox.get():  # Eğer checkbox seçiliyse
                        cursor.execute("DELETE FROM portfolio WHERE id = ?", (row_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Başarılı", "Seçilen kayıt(lar) silindi.")

            self.show_table(results, "Portföy Sil", on_delete=delete_selected)
        else:
            messagebox.showerror("Hata", "Girilen TC kimliğine ait kayıt bulunamadı.")


    def show_table(self, data, title, editable=False, on_save=None, include_all_columns=False):
        """
        Verilen verilerle tabloyu bir pencere olarak gösterir (kaydırma çubuğu eklenmiş).
        :param data: [(id, ...) formatında liste]
        :param title: Pencere başlığı
        :param editable: Tablonun düzenlenebilir olup olmadığı
        :param on_save: Düzenleme sonrası kaydetme fonksiyonu
        :param include_all_columns: Bütün sütun adlarının dahil edilip edilmeyeceği
        """
        table_window = ctk.CTkToplevel(self)
        table_window.title(title)
        table_window.geometry("1000x500")

        # Çerçeve ve kaydırma çubuğu
        outer_frame = ctk.CTkFrame(table_window)
        outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = ctk.CTkCanvas(outer_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Yatay ve dikey kaydırma çubukları
        vertical_scrollbar = ctk.CTkScrollbar(outer_frame, command=canvas.yview)
        vertical_scrollbar.pack(side="left", fill="y")

        horizontal_scrollbar = ctk.CTkScrollbar(table_window, command=canvas.xview, orientation="horizontal")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        inner_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Tüm sütun adlarını ekle ve Türkçeleştir
        if include_all_columns:
            conn = sqlite3.connect("portfolio.db")
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(portfolio)")
            columns = [col[1] for col in cursor.fetchall()]  # Sütun adlarını al
            conn.close()
        else:
            columns = ["ID", "oda_sayisi", "bina_yasi", "kat_sayisi", "fiyat", "ilan_tarihi", "ilan_aciklamasi", "site_adi"]

        column_headers = {
            "oda_sayisi": "Oda Sayısı",
            "bina_yasi": "Bina Yaşı",
            "kat_sayisi": "Kat Sayısı",
            "fiyat": "Fiyat",
            "ilan_tarihi": "İlan Tarihi",
            "ilan_aciklamasi": "İlan Açıklaması",
            "site_adi": "Site Adı",
            # Diğer sütunları ekleyebilirsin
        }

        # Tablo başlıkları
        for col_index, col_name in enumerate(columns):
            display_name = column_headers.get(col_name, col_name.replace("_", " ").title())
            header = ctk.CTkLabel(inner_frame, text=display_name, font=("Arial", 12, "bold"))
            header.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")

        entry_widgets = []

        # Tablo satırları
        for row_index, row in enumerate(data, start=1):
            row_widgets = []
            for col_index, cell in enumerate(row):
                if editable and col_index > 0:
                    entry = ctk.CTkEntry(inner_frame)
                    entry.insert(0, str(cell))
                    entry.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")
                    row_widgets.append(entry)
                else:
                    label = ctk.CTkLabel(inner_frame, text=str(cell))
                    label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")
                    row_widgets.append(label)
            entry_widgets.append(row_widgets)

        # Kaydet butonu
        if editable and on_save:
            save_button = ctk.CTkButton(inner_frame, text="Kaydet", command=lambda: on_save(entry_widgets))
            save_button.grid(row=row_index + 1, column=0, columnspan=len(columns), pady=10, padx=5, sticky="ew")

        # Canvas boyutlarını güncelle
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))







	


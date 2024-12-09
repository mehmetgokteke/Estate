import re
import os
from tkinter import filedialog, messagebox
import sqlite3
import customtkinter as ctk
from datetime import datetime
from PIL import Image

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
            corner_radius=20,
        )
        self.label_header.pack(fill="x", padx=20, pady=20,ipady=20)

        # Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=20)
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
            label = ctk.CTkLabel(self.scrollable_frame, text=field + ":", font=("Arial", 12), corner_radius=20)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            self.combo_vars[field] = ctk.StringVar(value=options[0])  # Varsayılan olarak ilk seçenek seçili
            
            # ComboBox oluşturuluyor
            combo_box = ctk.CTkComboBox(
                self.scrollable_frame,
                variable=self.combo_vars[field],
                values=options,
                corner_radius=20,
                state="readonly",  # Kullanıcı sadece belirlenen değerleri seçebilir
                command=lambda value, field=field: on_combo_box_select(value, field)  # Tıklama sonrası yapılacak işlem
            )
            combo_box.grid(row=row, column=1, padx=10, pady=5, sticky="ew", columnspan=5)
            
            row += 1

        def on_combo_box_select(value, field):
            # ComboBox'a tıklanarak seçim yapıldığında yapılacak işlemler
            print(f"{field} seçildi: {value}")

            # RadioButton alanları
        for field, options in radio_button_options.items():
            label = ctk.CTkLabel(self.scrollable_frame, text=field + ":", font=("Arial", 12), corner_radius=20)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            # İlk seçeneği varsayılan olarak seçili yapmak için
            self.radio_vars[field] = ctk.StringVar(value=options[0])  # İlk seçeneği varsayılan yapıyoruz
            
            for i, option in enumerate(options):
                rb = ctk.CTkRadioButton(
                    self.scrollable_frame, text=option, variable=self.radio_vars[field], value=option, corner_radius=20
                )
                rb.grid(row=row, column=i + 1, padx=5, pady=5, sticky="w")
            
            row += 1

        # Doğrulama işlevi (Sadece rakamları kabul eder)
        def only_numbers(char):
            return char.isdigit() or char == ""  # Boşluğu da kabul eder (silme işlemi için)
        
        # Doğrulama işlevi (Sadece rakam ve çizgiyi kabul eder)
        def only_date_chars(char):
            return char.isdigit() or char == "-" or char == ""  # Boşluğu da kabul eder (silme işlemi için)

        # Tarih formatını kontrol eden fonksiyon (Doğru format: gün-ay-yıl)
        def validate_date(date):
            pattern = r"^(0[1-9]|[12][0-9]|3[01])\-(0[1-9]|1[0-2])\-(19|20)\d{2}$"
            return bool(re.match(pattern, date)) or date == ""  # Doğru format veya boş ise True
        
        # Doğrulama komutlarını oluştur
        vcmd_numbers = self.register(only_numbers)
        vcmd_date_chars = self.register(only_date_chars)
        vcmd_date_format = self.register(validate_date)

        for field in entry_fields:
            label = ctk.CTkLabel(self.scrollable_frame, text=field + ":", font=("Arial", 12), corner_radius=20)
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            if field in ["m2", "Aidat", "Depozito", "Fiyat"]:  # Sadece bu alanlar için sayı doğrulama
                self.entries[field] = ctk.CTkEntry(
                    self.scrollable_frame, corner_radius=20,
                    validate="key", validatecommand=(self.register(lambda char: char.isdigit() or char == ""), "%S")
                )
            elif field == "İlan Tarihi":  # Sadece bu alan için tarih doğrulama
                self.entries[field] = ctk.CTkEntry(
                    self.scrollable_frame, corner_radius=20,
                    validate="key", validatecommand=(vcmd_date_chars, "%S")  # %S: girilen karakter
                )
                # Odak kaybedildiğinde format kontrolü
                self.entries[field].bind("<FocusOut>", lambda event: (
                    messagebox.showerror("Hata", "Tarih formatı: gün-ay-yıl olmalı!")
                    if not validate_date(event.widget.get()) else None
                ))
            else:
                self.entries[field] = ctk.CTkEntry(self.scrollable_frame, corner_radius=20)

            self.entries[field].grid(row=row, column=1, columnspan=5, padx=10, pady=5, sticky="ew")
            row += 1

        # Resim Yükleme Butonu
        self.image_button = ctk.CTkButton(
            self.scrollable_frame, text="Resim Yükle", command=self.upload_image, corner_radius=20
        )
        self.image_button.grid(row=row, column=0, columnspan=6, padx=20, pady=20, sticky="ew")
        row += 1

            # Kaydetme butonu
        self.save_button = ctk.CTkButton(self.scrollable_frame, text="Kaydet", command=self.save_portfolio, corner_radius=20)
        self.save_button.grid(row=row, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
        row += 1

        # Portföy Güncelleme Butonu
        self.update_button = ctk.CTkButton(self.scrollable_frame, text="Portföy Düzenleme", command=self.show_portfolio, corner_radius=20)
        self.update_button.grid(row=row, column=0, columnspan=6, padx=20, pady=10, sticky="ew")
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
        tc_kimlik_window.attributes('-topmost', True)  # Pencereyi önde tutar

        tc_kimlik_var = ctk.StringVar()  # Girdi için değişken oluştur
        tc_kimlik_label = ctk.CTkLabel(tc_kimlik_window, text="TC Kimlik No:", corner_radius=20)
        tc_kimlik_label.pack(padx=20, pady=10)
        tc_kimlik_entry = ctk.CTkEntry(tc_kimlik_window, textvariable=tc_kimlik_var, corner_radius=20)
        tc_kimlik_entry.pack(padx=20, pady=10)
        
        def on_confirm():
            tc_kimlik_window.destroy()
            
        confirm_button = ctk.CTkButton(tc_kimlik_window, text="Onayla", command=on_confirm, corner_radius=20)
        confirm_button.pack(padx=20, pady=10)
        
        tc_kimlik_window.wait_window(tc_kimlik_window)  # Pencere kapanana kadar bekle
        return tc_kimlik_var.get()


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
        try:
            # İlan Tarihi doğrulaması
            ilan_tarihi = data.get("İlan Tarihi", "")
            try:
                datetime.strptime(ilan_tarihi, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Hata", "İlan Tarihi formatı yanlış! Lütfen DD-MM-YYYY formatında bir tarih giriniz.")
                return

            # Fiyatı al ve formatla: Kullanıcıdan herhangi bir formatta alabiliriz, ancak 3 basamaktan sonra nokta ekleyeceğiz.
            fiyat = data.get("Fiyat", "")
            # Sayıyı alıp, virgül ve nokta içermeyen sadece sayıya dönüştür
            fiyat = re.sub(r'[^\d]', '', fiyat)

            # 3 basamaktan sonra nokta koyarak formatla
            if fiyat:
                fiyat = "{:,.0f}".format(int(fiyat)).replace(",", ".")  # 1.000.000 gibi formatla ve virgülü nokta ile değiştir

            # Veritabanı bağlantısı
            conn = sqlite3.connect("portfolio.db")
            cursor = conn.cursor()

            # Resimlerin adlarını veritabanına ekle
            resim_adlari = ",".join([os.path.basename(image) for image in self.selected_images])

            # Veritabanı tabloyu oluştur
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
                    yapinin_durumu TEXT,
                    resim_adlari TEXT
                )
                '''
            )

            # Veriyi veritabanına kaydet
            cursor.execute(
                '''
                INSERT INTO portfolio (
                    tc_kimlik, oda_sayisi, bina_yasi, kat_sayisi, fiyat, ilan_tarihi, ilan_aciklamasi, site_adi, yapinin_durumu, resim_adlari
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    tc_kimlik,
                    data.get("Oda Sayısı", ""),
                    data.get("Bina Yaşı", ""),
                    data.get("Kat Sayısı", ""),
                    fiyat,
                    ilan_tarihi,
                    data.get("İlan Açıklaması", ""),
                    data.get("Site Adı", ""),
                    data.get("Yapının Durumu", ""),
                    resim_adlari  # Resimlerin adı burada saklanır
                ),
            )

            conn.commit()

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        finally:
            conn.close()
            


    def save_images(self, tc_kimlik):
        # Resimleri resimler klasörüne kaydet
        if not os.path.exists("resimler"):
            os.makedirs("resimler")
        for image_path in self.selected_images:
            file_name = os.path.basename(image_path)
            destination = os.path.join("resimler", f"{tc_kimlik}_{file_name}")
            os.rename(image_path, destination)
 

    def show_portfolio(self):
        # TC Kimlik No'yu iste
        tc_kimlik = self.ask_for_tc_kimlik()
        print(f"Girilen T.C. Kimlik: {tc_kimlik}")

        # TC Kimlik No kontrolü
        if self.check_tc_exists(tc_kimlik):
            print("T.C. kimlik doğrulandı, pencere açılıyor...")

            # Portföy yönetim penceresi
            conn = sqlite3.connect("portfolio.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ilan_durumu, oda_sayisi, m2, bulundugu_kat, bina_yasi, isinma_tipi, kat_sayisi, 
                    esya_durumu, banyo_sayisi, yapi_tipi, yapinin_durumu, kullanim_durumu, aidat, 
                    cephe, depozito, yakit_tipi, tapu_durumu, yetkili_ofis, fiyat, ilan_tarihi, 
                    ilan_aciklamasi, mutfak, balkon, asansor, otopark, site_icerisinde, site_adi, 
                    kimden, wc_sayisi, balkon_tipi, id
                FROM portfolio
            """)
            data = cursor.fetchall()
            conn.close()

            # Yeni pencere oluştur
            portfolio_window = ctk.CTkToplevel(self)
            portfolio_window.title("Portföy Yönetimi")
            portfolio_window.geometry("1200x600")
            portfolio_window.resizable(True, True)

            # Çerçeve ve tuval
            container_frame = ctk.CTkFrame(portfolio_window)
            container_frame.pack(fill="both", expand=True, padx=10, pady=10)

            canvas = ctk.CTkCanvas(container_frame, highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar_y = ctk.CTkScrollbar(container_frame, orientation="vertical", command=canvas.yview)
            scrollbar_y.pack(side="right", fill="y")

            scrollbar_x = ctk.CTkScrollbar(portfolio_window, orientation="horizontal", command=canvas.xview)
            scrollbar_x.pack(side="bottom", fill="x")

            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            # İçerik çerçevesi
            frame = ctk.CTkFrame(canvas)
            canvas.create_window((0, 0), window=frame, anchor="nw")

            # Tablo başlıkları
            headers = [
                "İlan Durumu", "Oda Sayısı", "m²", "Bulunduğu Kat", "Bina Yaşı", "Isınma Tipi", "Kat Sayısı",
                "Eşya Durumu", "Banyo Sayısı", "Yapı Tipi", "Yapının Durumu", "Kullanım Durumu", "Aidat",
                "Cephe", "Depozito", "Yakıt Tipi", "Tapu Durumu", "Yetkili Ofis", "Fiyat", "İlan Tarihi",
                "İlan Açıklaması", "Mutfak", "Balkon", "Asansör", "Otopark", "Site İçerisinde", "Site Adı",
                "Kimden", "WC Sayısı", "Balkon Tipi", "Sil", "Kaydet"
            ]
            for col_index, header in enumerate(headers):
                label = ctk.CTkLabel(frame, text=header, font=("Arial", 12, "bold"), fg_color="#00BCD4", text_color="white", corner_radius=8, padx=10, pady=5)
                label.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")

            # Verileri tablo olarak göster
            for row_index, row in enumerate(data, start=1):
                entries = []
                for col_index, cell in enumerate(row[:-1]):  # id hariç
                    entry = ctk.CTkEntry(frame, font=("Arial", 10))
                    entry.insert(0, str(cell))
                    entry.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")
                    entries.append(entry)

                # Silme butonu
                delete_button = ctk.CTkButton(
                    frame, text="Sil", width=60,
                    command=lambda id=row[-1]: self.delete_portfolio_entry(id, frame),
                    corner_radius=20
                )
                delete_button.grid(row=row_index, column=len(headers) - 2, padx=5, pady=5)

                # Kaydetme butonu
                save_button = ctk.CTkButton(
                    frame, text="Kaydet", width=60,
                    command=lambda id=row[-1], entry_list=entries: self.save_portfolio_entry(id, entry_list),
                    corner_radius=20
                )
                save_button.grid(row=row_index, column=len(headers) - 1, padx=5, pady=5)

            # Dinamik kaydırma alanı
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        else:
            print("T.C. kimlik doğrulanamadı!")
            messagebox.showerror("Hata", "Girilen TC Kimlik No veritabanında bulunamadı!")

    def delete_portfolio_entry(self, id, frame):
        try:
            conn = sqlite3.connect("portfolio.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM portfolio WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Başarılı", f"ID {id} silindi!")
            frame.destroy()
            self.show_portfolio()  # Güncel tabloyu yükle
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Silme işlemi başarısız: {e}")

    def save_portfolio_entry(self, id, entries):
        try:
            conn = sqlite3.connect("portfolio.db")
            cursor = conn.cursor()

            # Yeni değerleri al
            updated_values = [entry.get() for entry in entries]

            # Sorgu oluştur
            cursor.execute("""
                UPDATE portfolio SET 
                    ilan_durumu=?, oda_sayisi=?, m2=?, bulundugu_kat=?, bina_yasi=?, isinma_tipi=?, kat_sayisi=?, 
                    esya_durumu=?, banyo_sayisi=?, yapi_tipi=?, yapinin_durumu=?, kullanim_durumu=?, aidat=?, 
                    cephe=?, depozito=?, yakit_tipi=?, tapu_durumu=?, yetkili_ofis=?, fiyat=?, ilan_tarihi=?, 
                    ilan_aciklamasi=?, mutfak=?, balkon=?, asansor=?, otopark=?, site_icerisinde=?, site_adi=?, 
                    kimden=?, wc_sayisi=?, balkon_tipi=? 
                WHERE id=?
            """, (*updated_values, id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Başarılı", f"ID {id} güncellendi!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Kaydetme işlemi başarısız: {e}")


        
    







	


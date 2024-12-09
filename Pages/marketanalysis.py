import customtkinter as ctk
import tkinter as tk
from tkinter import ttk,messagebox
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import threading
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException, NoSuchWindowException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, urlunparse
import re
import time
class marketanalysis(ctk.CTkFrame):
    def __init__(self, parent, disable_button_callback):
        super().__init__(parent)
        self.site = ""
        self.label = ctk.CTkLabel(self, text="PİYASA ANALİZİ", font=("Helvetica", 30, "bold"), text_color="#000000", fg_color="#00BCD4", corner_radius=15)
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        self.style = ttk.Style()
        self.style.configure("TCombobox",background="red", selectbackground="#00BCD4", selectforeground="#000000")

        self.create_dropdown_menu("İl:", "il", self.get_il_names(), self.on_il_selected)
        self.create_dropdown_menu("İlçe:", "ilce", [], self.on_ilce_selected)
        self.create_dropdown_menu("Mahalle:", "mahalle", [])

        self.property_type_var = ctk.StringVar(value="Kiralık")
        self.owner_var = ctk.StringVar(value="Sahibinden")
        self.create_radio_buttons()

        self.room_count_var = ctk.StringVar(value="1")
        self.create_room_count_buttons()

        self.button_frame = ctk.CTkFrame(self, corner_radius=20)
        self.button_frame.pack(pady=5, padx=20, fill="x")

        self.progress_bar = ctk.CTkProgressBar(self.button_frame, width=300, height=22, progress_color="#00BCD4")
        self.progress_bar.pack(side="left", padx=10)

        self.analyze_button_emlakjet = ctk.CTkButton(self.button_frame, text="Emlakjet", text_color="black", command=self.analyze_data_emlakjet, fg_color="#3BBF9F", hover_color="#2D9F85", font=("Helvetica", 15, "bold"),corner_radius=20, width=200)
        self.analyze_button_emlakjet.pack(side="right", padx=10)
        self.analyze_button_sahibinden = ctk.CTkButton(self.button_frame, text="Sahibinden", text_color="black", command=self.analyze_data_sahibinden, fg_color="#F6C91B", hover_color="#D7B31D", font=("Helvetica", 15, "bold"),corner_radius=20, width=200)
        self.analyze_button_sahibinden.pack(side="right", padx=10)
        self.analyze_button_hepsiemlak = ctk.CTkButton(self.button_frame, text="Hepsiemlak", text_color="black", command=self.analyze_data_hepsiemlak, fg_color="#F2545B", hover_color="#E04F66", font=("Helvetica", 15, "bold"),corner_radius=20, width=200)
        self.analyze_button_hepsiemlak.pack(side="right", padx=10)
        self.offer_button = ctk.CTkButton(self.button_frame, text="Öneri", text_color="black", command=self.offer, fg_color="#fd7e14", hover_color="#ffb84d", font=("Roboto", 14, "bold"),corner_radius=20, width=100, state=tk.DISABLED)
        self.offer_button.pack(side="right", padx=10)
        self.disable_button_callback = disable_button_callback
        self.dynamic_color_progress(0)
        
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.left_frame = ctk.CTkFrame(master=self.frame, width=574, height=350,fg_color="#00BCD4")
        self.left_frame.grid(row=0, column=0)
        self.left_frame.pack_propagate(False)
        self.right_frame = ctk.CTkFrame(master=self.frame, width=574, height=350,fg_color="#00BCD4")
        self.right_frame.grid(row=0, column=1)
        self.right_frame.pack_propagate(False)

        self.price_label = ctk.CTkLabel(self.left_frame, text="Fiyat Grafiği", font=("Arial", 18), text_color="#000000")
        self.price_label.pack()
        self.size_label = ctk.CTkLabel(self.right_frame, text="m² Grafiği", font=("Arial", 18), text_color="#000000")
        self.size_label.pack()

        self.create_result_labels()
        self.is_processing = False

    def load_json(self, file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            except FileNotFoundError:
                print(f"Hata: {file_path} bulunamadı.")
                return []
            
    def load_all_mahalle_json(self):
        mahalle_files = [
            ".vscode/mahalleler-1.json",
            ".vscode/mahalleler-2.json",
            ".vscode/mahalleler-3.json",
            ".vscode/mahalleler-4.json"
        ]
        all_mahalleler = []
        for file_path in mahalle_files:
            mahalleler = self.load_json(file_path)
            all_mahalleler.extend(mahalleler)
        return all_mahalleler

    def create_dropdown_menu(self, label_text, attribute_name, options, command=None):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text=label_text, font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)

        combo = ttk.Combobox(frame, values=options, state="readonly", font=("Helvetica", 14), width=30, height=20, style="TCombobox")
        combo.pack(side="right", padx=(10, 5), pady=5)
        combo.bind("<<ComboboxSelected>>", command)
        setattr(self, f"{attribute_name}_combo", combo)

    def get_il_names(self):
        iller = self.load_json(".vscode/il.json")
        return [il["sehir_adi"] for il in iller]

    def on_il_selected(self, event):
        selected_il = self.il_combo.get()
        self.update_ilce_options(selected_il)

    def update_ilce_options(self, selected_il):
        ilceler = self.load_json(".vscode/ilce.json")
        ilce_list = [
            ilce["ilce_adi"]
            for ilce in ilceler
            if ilce["sehir_adi"] == selected_il
        ]
        self.ilce_combo["values"] = ilce_list
        self.ilce_combo.set("")
        self.mahalle_combo["values"] = []
        self.mahalle_combo.set("")

    def on_ilce_selected(self, event):
        selected_ilce = self.ilce_combo.get()
        self.update_mahalle_options(selected_ilce)

    def update_mahalle_options(self, selected_ilce):
        all_mahalleler = self.load_all_mahalle_json()
        mahalle_list = [
            mahalle["mahalle_adi"]
            for mahalle in all_mahalleler
            if mahalle["ilce_adi"] == selected_ilce
        ]
        self.mahalle_combo["values"] = mahalle_list
        self.mahalle_combo.set("")

    def create_radio_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text="Sahibinden - Tüm İlanlar / Kiralık - Satılık:", font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        kiralik_button = ctk.CTkRadioButton(frame, text="Satılık",font=("Helvetica", 14), text_color="#000000", variable=self.property_type_var, value="Satılık", fg_color="#F6C91B")
        kiralik_button.pack(side="right", padx=10, pady=5)
        satilik_button = ctk.CTkRadioButton(frame, text="Kiralık",font=("Helvetica", 14), text_color="#000000", variable=self.property_type_var, value="Kiralık", fg_color="#F6C91B")
        satilik_button.pack(side="right", padx=10, pady=5)
        self.all_button = ctk.CTkRadioButton(frame, text="Tüm İlanlar",font=("Helvetica", 14), text_color="#000000", variable=self.owner_var, value="Tüm", fg_color="#F2545B")
        self.all_button.pack(side="right", padx=10, pady=5)
        self.sahibinden_button = ctk.CTkRadioButton(frame, text="Sahibinden",font=("Helvetica", 14), text_color="#000000", variable=self.owner_var, value="Sahibinden", fg_color="#F2545B")
        self.sahibinden_button.pack(side="right", padx=10, pady=5)

    def create_room_count_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text="Oda Sayısı Seçiniz:", font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        room_1_button = ctk.CTkRadioButton(frame, text="Hepsi",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="4", fg_color="#3BBF9F")
        room_1_button.pack(side="right", padx=10, pady=5)
        room_2_button = ctk.CTkRadioButton(frame, text="3+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="3", fg_color="#3BBF9F")
        room_2_button.pack(side="right", padx=10, pady=5)
        room_3_button = ctk.CTkRadioButton(frame, text="2+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="2", fg_color="#3BBF9F")
        room_3_button.pack(side="right", padx=10, pady=5)
        room_4_button = ctk.CTkRadioButton(frame, text="1+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="1", fg_color="#3BBF9F")
        room_4_button.pack(side="right", padx=10, pady=5)

    def create_result_labels(self):
        self.result_labels = {}
        self.price_frame = ctk.CTkFrame(master=self.left_frame)
        self.price_frame.pack(fill="both", expand=True)
        self.result_labels["Fiyat Grafiği"] = self.price_frame

        self.size_frame = ctk.CTkFrame(master=self.right_frame)
        self.size_frame.pack(fill="both", expand=True)
        self.result_labels["m2 Grafiği"] = self.size_frame

    def turkish_to_english(self, text):
        replacements = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
        return text.translate(replacements)
    
    def turkish_to_lowercase(self, text):
        text = text.replace("İ", "i")
        return text.lower()

    def dynamic_color_progress(self, value):
        if self.analyze_button_emlakjet.cget("text") == "Analiz Yapılıyor...":
            color = "#3BBF9F"
        elif self.analyze_button_sahibinden.cget("text") == "Analiz Yapılıyor...":
            color = "#F6C91B"
        elif self.analyze_button_hepsiemlak.cget("text") == "Analiz Yapılıyor...":
            color = "#F2545B"
        else:
            if "emlakjet" in self.site:
                color = "#3BBF9F"
            elif "hepsiemlak" in self.site:
                color = "#F2545B"
            elif "sahibinden" in self.site:
                color = "#F6C91B"
            else:
                color = "#00BCD4"
        self.progress_bar.configure(progress_color=color)
        self.progress_bar.set(value)
        
    # EMLAKJET ANALİZ
    def analyze_data_emlakjet(self):
        self.selected_il = self.il_combo.get()
        if self.selected_il:
            self.selected_ilce = self.ilce_combo.get()
            self.selected_mahalle = self.mahalle_combo.get()
            self.property_type = self.property_type_var.get()
            self.owner = self.owner_var.get()
            self.room_count = self.room_count_var.get()
            self.is_processing = True
            self.disable_button_callback(True)
            self.analyze_button_emlakjet.configure(state=tk.DISABLED, text="Analiz Yapılıyor...")
            self.analyze_button_sahibinden.configure(state=tk.DISABLED)
            self.analyze_button_hepsiemlak.configure(state=tk.DISABLED)
            self.dynamic_color_progress(0)
            threading.Thread(target=self.emlakjet).start()
        else:
            messagebox.showerror("Hata", "Lütfen bir il seçiniz.")
            return
        
    def emlakjet(self):
        self.selected_il = self.turkish_to_lowercase(self.selected_il)
        self.selected_il = self.turkish_to_english(self.selected_il)

        if self.selected_ilce:
            self.selected_ilce = self.turkish_to_lowercase(self.selected_ilce)
            self.selected_ilce = self.turkish_to_english(self.selected_ilce)

        if self.selected_mahalle:
            self.selected_mahalle = self.turkish_to_lowercase(self.selected_mahalle)
            mahalle_parts = self.selected_mahalle.strip().split()
            cleaned_mahalle = ""
            for i, word in enumerate(mahalle_parts):
                cleaned_word = word.strip(",")
                if cleaned_word == "köyü":
                    cleaned_mahalle = " ".join(mahalle_parts[:i+1])
                    break
            if not cleaned_mahalle:
                cleaned_mahalle = " ".join(mahalle_parts)
            cleaned_mahalle = cleaned_mahalle.replace(",", "").replace(" ", "-")
            self.selected_mahalle = self.turkish_to_english(cleaned_mahalle)

        if int(self.room_count) == 1:
            self.room_count = 3
        elif int(self.room_count) == 2:
            self.room_count = 5
        elif int(self.room_count) == 3:
            self.room_count = 7

        self.dynamic_color_progress(0.2)

        options = webdriver.FirefoxOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self.driver = webdriver.Firefox(options=options)
        if self.property_type == "Kiralık":
            if not self.selected_ilce and not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.emlakjet.com/kiralik-konut/{self.selected_il}/?oda_sayisi[]={self.room_count}")
                else:
                    self.driver.get(f"https://www.emlakjet.com/kiralik-konut/{self.selected_il}")
            elif not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.emlakjet.com/kiralik-konut/{self.selected_il}-{self.selected_ilce}/?oda_sayisi[]={self.room_count}")
                else:
                    self.driver.get(f"https://www.emlakjet.com/kiralik-konut/{self.selected_il}-{self.selected_ilce}") 
            else:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.emlakjet.com/kiralik-konut/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}/?oda_sayisi[]={self.room_count}")
                else:
                    self.driver.get(f"https://www.emlakjet.com/kiralik-konut/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}")
        else:
            if not self.selected_ilce and not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.emlakjet.com/satilik-konut/{self.selected_il}/?oda_sayisi[]={self.room_count}")
                else:
                    self.driver.get(f"https://www.emlakjet.com/satilik-konut/{self.selected_il}")
            elif not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.emlakjet.com/satilik-konut/{self.selected_il}-{self.selected_ilce}/?oda_sayisi[]={self.room_count}")
                else:
                    self.driver.get(f"https://www.emlakjet.com/satilik-konut/{self.selected_il}-{self.selected_ilce}") 
            else:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.emlakjet.com/satilik-konut/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}/?oda_sayisi[]={self.room_count}")
                else:
                    self.driver.get(f"https://www.emlakjet.com/satilik-konut/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}")
        time.sleep(3)
        if self.owner == "Sahibinden":
            self.driver.execute_script("window.scrollTo(0, 250);")
            owner_button = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-test-selector="listing-sub-filter-Sahibinden"]')))
            owner_button.click()

        self.dynamic_color_progress(0.4)
        self.site = self.driver.current_url
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="_3w4Reh"]')))
            self.dynamic_color_progress(0.8)
            self.update_results(data = {
            "prices": "",
            "average_price": "0",
            "sizes": "",
            "average_size": "0",})
            messagebox.showinfo("Bilgi", "Girdiğiniz bilgiler için ilan bulunamadı")
        except TimeoutException:
            self.data = self.fetch_data_emlakjet()
            if self.data:
                threading.Thread(target=self.update_results, args=(self.data,), daemon=True).start()
        finally:
            print(self.data)
            self.disable_button_callback(False)  
            self.analyze_button_emlakjet.configure(state=tk.NORMAL, text="Emlakjet", fg_color="#3BBF9F")
            self.analyze_button_sahibinden.configure(state=tk.NORMAL)
            self.analyze_button_hepsiemlak.configure(state=tk.NORMAL)
            self.driver.quit()
            return

    def fetch_data_emlakjet(self):
        try:
            prices, sizes = [], []
            self.extract_data_emlakjet(prices, sizes)
            self.dynamic_color_progress(0.8)

            average_price = sum(prices) / len(prices) if prices else 0
            average_size = round(sum(sizes) / len(sizes)) if sizes else 0
            average_formatted_price = '{:,.0f}'.format(average_price).replace(',', '.')

            data = {
                "prices": prices,
                "average_price": average_formatted_price,
                "sizes": sizes,
                "average_size": average_size,
            }
            return data
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
            print(f"An error occurred while fetching data: {e}")
            return None
        
    def extract_data_emlakjet(self, prices, sizes):
        try:
            retries = 3
            invalid_indices = []
            size_indices = []
            self.dynamic_color_progress(0.6)
            while retries > 0:
                try:
                    price_elements = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//p[@class="_2C5UCT"]'))
                    )
                    for index, elem in enumerate(price_elements):
                        try:
                            true_prices = int(elem.text.replace("TL", "").replace(".", "").strip())
                            if self.property_type == "Kiralık":
                                if true_prices < 500000:
                                    prices.append(true_prices)
                                else:
                                    invalid_indices.append(index)
                            else:
                                if true_prices > 500000 and true_prices <500000000:
                                    prices.append(true_prices)
                                else:
                                    invalid_indices.append(index)
                        except ValueError:
                            invalid_indices.append(index)

                    size_elements = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2UELHn"]/span[4]'))
                    )
                    for index, elem in enumerate(size_elements):
                        if index in invalid_indices:
                            continue
                        try:
                            sizes.append(int(elem.text.replace("m²", "").replace("texture", "").strip()))
                        except ValueError:
                            size_indices.append(index)

                    try:
                        next_page_button = WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//li[@class="_3au2n_ OTUgAO"]'))
                        )
                        next_page_button.click()
                        WebDriverWait(self.driver, 30).until(EC.staleness_of(next_page_button))
                    except (NoSuchElementException, TimeoutException):
                        break
                except StaleElementReferenceException as e:
                    print(f"Stale element reference exception encountered: {e}. Retrying...")
                    retries -= 1
                except TimeoutException as e:
                    print(f"Timeout exception encountered: {e}. Retrying...")
                    retries -= 1
                except NoSuchElementException as e:
                    print(f"No such element exception encountered: {e}. Retrying...")
                    retries -= 1
            print(f"m2 kaybolan ilanlar:{size_indices}")
        except (WebDriverException,NoSuchWindowException,NoSuchElementException):
            return

    # SAHİBİNDEN ANALİZ
    def analyze_data_sahibinden(self):
        self.selected_il = self.il_combo.get()
        if self.selected_il:
            self.selected_ilce = self.ilce_combo.get()
            self.selected_mahalle = self.mahalle_combo.get()
            self.property_type = self.property_type_var.get()
            self.owner = self.owner_var.get()
            self.room_count = self.room_count_var.get()
            self.is_processing = True
            self.disable_button_callback(True)
            self.analyze_button_sahibinden.configure(state=tk.DISABLED, text="Analiz Yapılıyor...")
            self.analyze_button_emlakjet.configure(state=tk.DISABLED)
            self.analyze_button_hepsiemlak.configure(state=tk.DISABLED)
            self.dynamic_color_progress(0)
            threading.Thread(target=self.sahibinden).start()
        else:
            messagebox.showerror("Hata", "Lütfen bir il seçiniz.")
            return
        
    def sahibinden(self):
        self.selected_il = self.turkish_to_lowercase(self.selected_il)
        self.selected_il = self.turkish_to_english(self.selected_il)

        if self.selected_ilce:
            self.selected_ilce = self.turkish_to_lowercase(self.selected_ilce)
            self.selected_ilce = self.turkish_to_english(self.selected_ilce)

        if self.selected_mahalle:
            self.selected_mahalle = self.turkish_to_lowercase(self.selected_mahalle)
            mahalle_parts = self.selected_mahalle.strip().split()
            cleaned_mahalle = ""
            for i, word in enumerate(mahalle_parts):
                cleaned_word = word.strip(",")
                if cleaned_word == "köyü":
                    cleaned_mahalle = " ".join(mahalle_parts[:i+1])
                    break
            else:
                cleaned_mahalle = " ".join(mahalle_parts)
                cleaned_mahalle = cleaned_mahalle.replace("mahallesi", "mah")
            cleaned_mahalle = cleaned_mahalle.replace(",", "").replace(" ", "-")
            self.selected_mahalle = self.turkish_to_english(cleaned_mahalle)

        if int(self.room_count) == 1:
            self.room_count = 38473
        elif int(self.room_count) == 2:
            self.room_count = 38470
        elif int(self.room_count) == 3:
            self.room_count = 38474

        self.dynamic_color_progress(0.2)

        options = webdriver.FirefoxOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self.driver = webdriver.Firefox(options=options)
        if self.property_type == "Kiralık":
            if not self.selected_ilce and not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.sahibinden.com/kiralik-daire/{self.selected_il}?a20={self.room_count}")
                else:
                    self.driver.get(f"https://www.sahibinden.com/kiralik-daire/{self.selected_il}")
            elif not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.sahibinden.com/kiralik-daire/{self.selected_il}-{self.selected_ilce}?a20={self.room_count}")
                else:
                    self.driver.get(f"https://www.sahibinden.com/kiralik-daire/{self.selected_il}-{self.selected_ilce}") 
            else:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.sahibinden.com/kiralik-daire/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}?a20={self.room_count}")
                else:
                    self.driver.get(f"https://www.sahibinden.com/kiralik-daire/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}")
        else:
            if not self.selected_ilce and not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.sahibinden.com/satilik-daire/{self.selected_il}?a20={self.room_count}")
                else:
                    self.driver.get(f"https://www.sahibinden.com/satilik-daire/{self.selected_il}")
            elif not self.selected_mahalle:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.sahibinden.com/satilik-daire/{self.selected_il}-{self.selected_ilce}?a20={self.room_count}")
                else:
                    self.driver.get(f"https://www.sahibinden.com/satilik-daire/{self.selected_il}-{self.selected_ilce}") 
            else:
                if int(self.room_count) != 4:
                    self.driver.get(f"https://www.sahibinden.com/satilik-daire/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}?a20={self.room_count}")
                else:
                    self.driver.get(f"https://www.sahibinden.com/satilik-daire/{self.selected_il}-{self.selected_ilce}-{self.selected_mahalle}")
        time.sleep(3)
        if self.owner == "Sahibinden":
            try:
                owner_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="phdef" and @title="Sahibinden"]')))
                owner_button.click()
            except TimeoutException:
                control = 1
        self.dynamic_color_progress(0.4)
        self.site = self.driver.current_url
        try:
            if control != 1:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="clearfix diagnostic-wrapper"]')))
            self.dynamic_color_progress(0.8)
            self.update_results(data = {
                "prices": "",
                "average_price": "0",
                "sizes": "",
                "average_size": "0",})
            messagebox.showwarning("Uyarı", "Üzgünüm Sahibinden sitesi için CloudFlare'e yakalandım 😞")
            self.disable_button_callback(False)
            self.analyze_button_sahibinden.configure(state=tk.NORMAL, text="Sahibinden", fg_color="#F6C91B")
            self.analyze_button_emlakjet.configure(state=tk.NORMAL)
            self.analyze_button_hepsiemlak.configure(state=tk.NORMAL)
            self.driver.quit()
        except TimeoutException:
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//p[@class="searchNoResultTitle"]')))
                self.dynamic_color_progress(0.8)
                self.update_results(data = {
                "prices": "",
                "average_price": "0",
                "sizes": "",
                "average_size": "0",})
                messagebox.showinfo("Bilgi", "Girdiğiniz bilgiler için ilan bulunamadı")
            except TimeoutException:
                self.data = self.fetch_data_sahibinden()
                if self.data:
                    threading.Thread(target=self.update_results, args=(self.data,), daemon=True).start()
            finally:
                print(self.data)
                self.disable_button_callback(False)  
                self.analyze_button_sahibinden.configure(state=tk.NORMAL, text="Sahibinden", fg_color="#F6C91B")
                self.analyze_button_emlakjet.configure(state=tk.NORMAL)
                self.analyze_button_hepsiemlak.configure(state=tk.NORMAL)
                self.driver.quit()

    def fetch_data_sahibinden(self):
        try:
            prices, sizes = [], []
            self.extract_data_sahibinden(prices, sizes)
            self.dynamic_color_progress(0.8)

            average_price = sum(prices) / len(prices) if prices else 0
            average_size = round(sum(sizes) / len(sizes)) if sizes else 0
            average_formatted_price = '{:,.0f}'.format(average_price).replace(',', '.')

            data = {
                "prices": prices,
                "average_price": average_formatted_price,
                "sizes": sizes,
                "average_size": average_size,
            }
            return data
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
            print(f"An error occurred while fetching data: {e}")
            return None
        
    def extract_data_sahibinden(self, prices, sizes):
        try:
            retries = 3
            invalid_indices = []
            size_indices = []
            self.dynamic_color_progress(0.6)
            while retries > 0:
                try:
                    price_elements = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="classified-price-container "]'))
                    )
                    for index, elem in enumerate(price_elements):
                        try:
                            true_prices = int(elem.text.replace("TL", "").replace(".", "").strip())
                            if self.property_type == "Kiralık":
                                if true_prices < 500000:
                                    prices.append(true_prices)
                                else:
                                    invalid_indices.append(index)
                            else:
                                if true_prices > 500000 and true_prices <500000000:
                                    prices.append(true_prices)
                                else:
                                    invalid_indices.append(index)
                        except ValueError:
                            invalid_indices.append(index)

                    invalid_indices = [x * 2 for x in invalid_indices]
                    size_elements = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//td[@class="searchResultsAttributeValue"]'))
                    )
                    for index, elem in enumerate(size_elements):
                        if index % 2 == 0:
                            if index in invalid_indices:
                                continue
                            try:
                                sizes.append(int(elem.text.replace("m²", "").strip()))
                            except ValueError:
                                size_indices.append(index)
                    try:
                        next_page_button = WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//a[@class="prevNextBut"]'))
                        )
                        next_page_button.click()
                        WebDriverWait(self.driver, 30).until(EC.staleness_of(next_page_button))
                    except (NoSuchElementException, TimeoutException):
                        break
                except StaleElementReferenceException as e:
                    print(f"Stale element reference exception encountered: {e}. Retrying...")
                    retries -= 1
                except TimeoutException as e:
                    print(f"Timeout exception encountered: {e}. Retrying...")
                    retries -= 1
                except NoSuchElementException as e:
                    print(f"No such element exception encountered: {e}. Retrying...")
                    retries -= 1
            print(f"m2 kaybolan ilanlar:{size_indices}")
        except (WebDriverException,NoSuchWindowException,NoSuchElementException):
            return

    # HEPSİEMLAK ANALİZ
    def analyze_data_hepsiemlak(self):
        self.selected_il = self.il_combo.get()
        if self.selected_il:
            self.selected_ilce = self.ilce_combo.get()
            self.selected_mahalle = self.mahalle_combo.get()
            self.property_type = self.property_type_var.get()
            self.owner = self.owner_var.get()
            self.room_count = self.room_count_var.get()
            self.is_processing = True
            self.disable_button_callback(True)
            self.analyze_button_hepsiemlak.configure(state=tk.DISABLED, text="Analiz Yapılıyor...")
            self.analyze_button_sahibinden.configure(state=tk.DISABLED)
            self.analyze_button_emlakjet.configure(state=tk.DISABLED)
            self.dynamic_color_progress(0)
            threading.Thread(target=self.hepsiemlak).start()
        else:
            messagebox.showerror("Hata", "Lütfen bir il seçiniz.")
            return

    def hepsiemlak(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("https://www.hepsiemlak.com/")
        self.dynamic_color_progress(0.1)
        search_box = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "search-input"))
        )
        search_box.send_keys(f"{self.selected_il} {self.selected_ilce}")
        search_box.send_keys(Keys.RETURN)

        if self.property_type == "Kiralık":
            category_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@id="categoryType-kiralik"]'))
            )
            category_button.click()
            self.bool = 1
        else:
            self.bool = 0
        time.sleep(3)

        if self.owner == "Sahibinden":
            owner_button = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//li[@id="realty-owner-sahibinden"]')))
            owner_button.click()
            time.sleep(3)
        self.dynamic_color_progress(0.2)

        if self.selected_mahalle:
            mahalle_parts = self.selected_mahalle.strip().lower().split()
            cleaned_mahalle = ""

            for i, word in enumerate(mahalle_parts):
                cleaned_word = word.strip(",")
                if cleaned_word == "köyü":
                    cleaned_mahalle = " ".join(mahalle_parts[:i+1])
                    break
            if cleaned_mahalle == "":
                cleaned_mahalle = " ".join(mahalle_parts[:-1])

            cleaned_mahalle = cleaned_mahalle.replace(",", "")
            self.selected_mahalle = cleaned_mahalle.upper()

            mahalle_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="he-control-base he-tree-select js-district-filter"]'))
            )
            mahalle_button.click()

            mahalle_search_box = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@class="he-select-base__search"]'))
            )
            mahalle_search_box.send_keys(self.selected_mahalle)
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(3)
            self.dynamic_color_progress(0.3)

            mahalle_options = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@class, "he-tree-select__parent-option-text")]'))
            )
            mahalle_options[0].click()

            search_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-red btn-large"]'))
            )
            search_button.click()
            time.sleep(3)
            self.dynamic_color_progress(0.4)

        if int(self.room_count) != 4:
            current_url = self.driver.current_url
            current_url = current_url + f"-{self.room_count}-1"
            self.driver.get(current_url)

        self.site = self.driver.current_url
        self.dynamic_color_progress(0.5)

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="empty-state-wrapper"]')))
            self.dynamic_color_progress(0.8)
            self.update_results(data = {
            "prices": "",
            "average_price": "0",
            "sizes": "",
            "average_size": "0",})
            messagebox.showinfo("Bilgi", "Girdiğiniz bilgiler için ilan bulunamadı")
        except TimeoutException:
            self.data = self.fetch_data_hepsiemlak()
            self.dynamic_color_progress(0.9)
            if self.data:
                threading.Thread(target=self.update_results, args=(self.data,), daemon=True).start()
        finally:
            print(self.data)
            self.disable_button_callback(False)  
            self.analyze_button_hepsiemlak.configure(state=tk.NORMAL, text="Hepsiemlak", fg_color="#F2545B")
            self.analyze_button_emlakjet.configure(state=tk.NORMAL)
            self.analyze_button_sahibinden.configure(state=tk.NORMAL)
            self.driver.quit()

    def fetch_data_hepsiemlak(self):
        try:
            prices, sizes = [], []
            self.extract_data_hepsiemlak(prices, sizes)
            self.dynamic_color_progress(0.8)

            average_price = sum(prices) / len(prices) if prices else 0
            average_size = round(sum(sizes) / len(sizes)) if sizes else 0
            average_formatted_price = '{:,.0f}'.format(average_price).replace(',', '.')

            data = {
                "prices": prices,
                "average_price": average_formatted_price,
                "sizes": sizes,
                "average_size": average_size,
            }
            return data
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
            print(f"An error occurred while fetching data: {e}")
            return None
        
    def extract_data_hepsiemlak(self, prices, sizes):
        try:
            retries = 3
            invalid_indices = []
            size_indices = []
            self.dynamic_color_progress(0.7)
            while retries > 0:
                try:
                    price_elements = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//span[@class="list-view-price"]'))
                    )
                    for index, elem in enumerate(price_elements):
                        try:
                            true_prices = int(elem.text.replace("TL", "").replace(".", "").strip())
                            if self.bool == 1:
                                if true_prices < 500000:
                                    prices.append(true_prices)
                                else:
                                    invalid_indices.append(index)
                            else:
                                if true_prices > 500000 and true_prices <500000000:
                                    prices.append(true_prices)
                                else:
                                    invalid_indices.append(index)
                        except ValueError:
                            invalid_indices.append(index)

                    size_elements = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//span[@class="celly squareMeter list-view-size"]'))
                    )
                    for index, elem in enumerate(size_elements):
                        if index in invalid_indices:
                            continue
                        try:
                            sizes.append(int(elem.text.replace("m²", "").strip()))
                        except ValueError:
                            size_indices.append(index)

                    try:
                        next_page_button = WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//a[@class="he-pagination__navigate-text he-pagination__navigate-text--next"]'))
                        )
                        next_page_button.click()
                        WebDriverWait(self.driver, 30).until(EC.staleness_of(next_page_button))
                    except (NoSuchElementException, TimeoutException):
                        break
                except StaleElementReferenceException as e:
                    print(f"Stale element reference exception encountered: {e}. Retrying...")
                    retries -= 1
                except TimeoutException as e:
                    print(f"Timeout exception encountered: {e}. Retrying...")
                    retries -= 1
                except NoSuchElementException as e:
                    print(f"No such element exception encountered: {e}. Retrying...")
                    retries -= 1
            print(f"m2 kaybolan ilanlar:{size_indices}")
        except (WebDriverException,NoSuchWindowException,NoSuchElementException):
            return

    # Grafik
    def update_results(self, data):
        self.data = data
        self.dynamic_color_progress(1)
        self.is_processing = False
        self.plot_graph(data["prices"], "Fiyat Grafiği","İlan Numarası", "FİYAT", self.result_labels["Fiyat Grafiği"],color='#388E3C',explanation="FİYAT")
        self.price_label.configure(text=f"Ortalama Fiyat: {data['average_price']} TL")

        self.plot_graph(data["sizes"], "M² Grafiği","İlan Numarası", "M²", self.result_labels["m2 Grafiği"],color='red',explanation="M²")
        self.size_label.configure(text=f"Ortalama M²: {data['average_size']} M²")
        self.update_offer_button_state()

    def plot_graph(self, data, title, x_label, y_label, frame, color, explanation):
        fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
        x_values = range(1, len(data) + 1)
        ax.plot(x_values, data, marker='o', linestyle="-", color=color, label=explanation)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend()

        cursor = mplcursors.cursor(ax, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{y_label}: {sel.target[1]:.2f}"))

        def on_click(event):
            if event.xdata and event.ydata:
                clicked_index = int(round(event.xdata))
                if 1 <= clicked_index <= len(data) and not self.is_processing:
                    self.is_processing = True
                    self.ilan_no = clicked_index - 1
                    if "emlakjet" in self.site:
                        threading.Thread(target=self.emlakjet_islem).start()
                    elif "hepsiemlak" in self.site:
                        threading.Thread(target=self.hepsiemlak_islem).start() 
                    elif "sahibinden" in self.site:
                        threading.Thread(target=self.sahibinden_islem).start()

        fig.canvas.mpl_connect("button_press_event", on_click)

        for widget in frame.winfo_children():
                widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    #İlan Yönlendirmesi
    def emlakjet_islem(self):
        try:
            messagebox.showinfo("Bilgi", "İlanın linkini hazırlıyorum")
            self.disable_button_callback(True)
            self.analyze_button_emlakjet.configure(state=tk.DISABLED)
            self.analyze_button_sahibinden.configure(state=tk.DISABLED)
            self.analyze_button_hepsiemlak.configure(state=tk.DISABLED)
            self.dynamic_color_progress(0)
            page = self.ilan_no // 30
            self.ilan_no = self.ilan_no - (page * 30) 
            page += 1

            if self.room_count != 4:
                parsed_url = urlparse(self.site)
                query_string = parsed_url.query
                path_parts = parsed_url.path.strip("/").split("/")
                if len(path_parts) < 5 or not path_parts[-2].isdigit():
                    path_parts.append(str(page))
                new_path = "/" + "/".join(path_parts)
                site = urlunparse(
                    (
                        parsed_url.scheme,
                        parsed_url.netloc,
                        new_path,
                        parsed_url.params,
                        query_string,
                        parsed_url.fragment,
                    ))
            else:
                site = f"{self.site}/{page}"
            self.dynamic_color_progress(0.3)
            print(site)

            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--headless")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            self.driver = webdriver.Firefox(options=options)
            self.driver.get(site)
            self.dynamic_color_progress(0.5)

            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="_3qUI9q"]')))
            links = self.driver.find_elements(By.XPATH, '//a[@class="_3qUI9q"]')
            if 0 <= self.ilan_no < len(links):
                target_link = links[self.ilan_no].get_attribute("href")
            self.dynamic_color_progress(0.8)

            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            self.dynamic_color_progress(1)
            self.driver = webdriver.Firefox(options=options)
            self.driver.maximize_window()
            self.driver.get(target_link)
        finally:
            self.disable_button_callback(False)
            self.analyze_button_emlakjet.configure(state=tk.NORMAL)
            self.analyze_button_sahibinden.configure(state=tk.NORMAL)
            self.analyze_button_hepsiemlak.configure(state=tk.NORMAL)
            self.is_processing = False

    def sahibinden_islem(self):
        try:
            messagebox.showinfo("Bilgi", "İlanın linkini hazırlıyorum")
            self.disable_button_callback(True)
            self.analyze_button_emlakjet.configure(state=tk.DISABLED)
            self.analyze_button_sahibinden.configure(state=tk.DISABLED)
            self.analyze_button_hepsiemlak.configure(state=tk.DISABLED)
            self.dynamic_color_progress(0)
            page = self.ilan_no // 20
            self.ilan_no = self.ilan_no - (page * 20) 
            page *= 20

            if self.room_count != 4:
                self.site = re.sub(r'pagingOffset=\d+', f'pagingOffset={page}', self.site)
            else:
                self.site = f"{self.site}?pagingOffset={page}"
            self.dynamic_color_progress(0.3)

            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--headless")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            self.driver = webdriver.Firefox(options=options)
            self.driver.get(self.site)
            self.dynamic_color_progress(0.5)

            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="classifiedTitle"]')))
            links = self.driver.find_elements(By.XPATH, '//a[@class="classifiedTitle"]')
            if 0 <= self.ilan_no < len(links):
                target_link = links[self.ilan_no].get_attribute("href")
            self.dynamic_color_progress(0.8)

            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            self.dynamic_color_progress(1)
            self.driver = webdriver.Firefox(options=options)
            self.driver.maximize_window()
            self.driver.get(target_link)
        finally:
            self.disable_button_callback(False)
            self.analyze_button_emlakjet.configure(state=tk.NORMAL)
            self.analyze_button_sahibinden.configure(state=tk.NORMAL)
            self.analyze_button_hepsiemlak.configure(state=tk.NORMAL)
            self.is_processing = False

    def hepsiemlak_islem(self):
        try:
            messagebox.showinfo("Bilgi", "İlanın linkini hazırlıyorum")
            self.disable_button_callback(True)
            self.analyze_button_emlakjet.configure(state=tk.DISABLED)
            self.analyze_button_sahibinden.configure(state=tk.DISABLED)
            self.analyze_button_hepsiemlak.configure(state=tk.DISABLED)
            self.dynamic_color_progress(0)
            page = self.ilan_no // 24
            self.ilan_no = self.ilan_no - (page * 24) 
            page += 1

            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("--headless")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            self.driver = webdriver.Firefox(options=options)
            self.driver.get(f"{self.site}?page={page}")
            self.dynamic_color_progress(0.5)

            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="card-link"]')))
            links = self.driver.find_elements(By.XPATH, '//a[@class="card-link"]')
            if 0 <= self.ilan_no < len(links):
                target_link = links[self.ilan_no].get_attribute("href")
            self.dynamic_color_progress(0.8)

            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            self.dynamic_color_progress(1)
            self.driver = webdriver.Firefox(options=options)
            self.driver.maximize_window()
            self.driver.get(target_link)
        finally:
            self.disable_button_callback(False)
            self.analyze_button_emlakjet.configure(state=tk.NORMAL)
            self.analyze_button_sahibinden.configure(state=tk.NORMAL)
            self.analyze_button_hepsiemlak.configure(state=tk.NORMAL)
            self.is_processing = False

    #Öneri
    def update_offer_button_state(self):
        post_com = re.split(r'\.com', self.site, maxsplit=1)[-1]
        if "sahibinden" in post_com:
            if hasattr(self, "data") and self.data.get("prices") and self.data.get("sizes"):
                fiyatlar = self.data["prices"]
                m2_degerleri = self.data["sizes"]
                if len(fiyatlar) > 1 and len(m2_degerleri) > 1:
                    self.offer_button.configure(state=tk.NORMAL)
                    return
        self.offer_button.configure(state=tk.DISABLED)

    def offer(self):
        if getattr(self, "results_window", None) and self.results_window.winfo_exists():
            messagebox.showwarning("Uyarı", "Öneri penceresi zaten açık !")
            return
        threading.Thread(target=self.perform_analysis).start()

    def perform_analysis(self):
        fiyatlar = self.data["prices"]
        m2_degerleri = self.data["sizes"]
        ort_fiyat = sum(fiyatlar) / len(fiyatlar)
        ort_m2 = sum(m2_degerleri) / len(m2_degerleri)
        
        kategori1 = [
            (index + 1, fiyat, m2, fiyat / m2)
            for index, (fiyat, m2) in enumerate(zip(fiyatlar, m2_degerleri))
            if fiyat < ort_fiyat * 0.75 and m2 > ort_m2 * 1.25
        ]
        kategori1.sort(key=lambda x: x[3])

        kategori2 = [
            (index + 1, fiyat, m2, fiyat / m2)
            for index, (fiyat, m2) in enumerate(zip(fiyatlar, m2_degerleri))
            if fiyat < ort_fiyat and m2 > ort_m2
        ]
        kategori2.sort(key=lambda x: x[3])

        kategori3 = [
            (index + 1, fiyat, m2, fiyat / m2)
            for index, (fiyat, m2) in enumerate(zip(fiyatlar, m2_degerleri))
            if fiyat < ort_fiyat * 0.75
        ]
        kategori3.sort(key=lambda x: x[3])

        if not kategori1 and not kategori2 and not kategori3:
            messagebox.showinfo("Bilgi", "Önerilecek ilan bulunamadı 😞")
            return
        self.show_analysis_results(kategori1, kategori2, kategori3)

    def show_analysis_results(self, kategori1, kategori2, kategori3):
        messagebox.showinfo("Genel Bilgiler", "FIRSAT İLANLAR: Fiyat ortalamasının %25 altında ve aynı zamanda m2 ortalamasının %25 üstünde olan ilanlar gösterilir.\n\nÖNERİLEN İLANLAR: Fiyat ortalamasının altında ve aynı zamanda m2 ortalamasının üstünde olan ilanlar gösterilir.\n\nDÜŞÜK FİYATLI İLANLAR: Fiyat ortalamasının %25 altında olan ilanlar gösterilir.\n\nNOT: İlan No kısmına tıklayarak istenilen ilanın web sayfasına gidilebilir.")
        self.results_window = ctk.CTkToplevel(self)
        self.results_window.title("Öneri")
        self.results_window.geometry("425x600")
        self.results_window.resizable(False, False)
        
        scrollable_frame = ctk.CTkScrollableFrame(self.results_window, width=480, height=580)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        if kategori1:
            ctk.CTkLabel(scrollable_frame, text=" Fırsat İlanlar ", fg_color="#F2545B", text_color="black", font=("Arial", 14, "bold")).pack(pady=10)
            frame1 = ctk.CTkFrame(scrollable_frame)
            frame1.pack(fill="x", padx=75, pady=(0,30))
            self.populate_analysis_table(kategori1, frame1, ["İlan No", "Fiyat (TL)", "M²", "Fiyat/M²"])
        
        if kategori2:
            ctk.CTkLabel(scrollable_frame, text=" Önerilen İlanlar ", fg_color="#F6C91B", text_color="black", font=("Arial", 14, "bold")).pack(pady=10)
            frame2 = ctk.CTkFrame(scrollable_frame)
            frame2.pack(fill="x", padx=75, pady=(0,30))
            self.populate_analysis_table(kategori2, frame2, ["İlan No", "Fiyat (TL)", "M²", "Fiyat/M²"])
        
        if kategori3:
            ctk.CTkLabel(scrollable_frame, text=" Düşük Fiyatlı İlanlar ", fg_color="#3BBF9F", text_color="black", font=("Arial", 14, "bold")).pack(pady=10)
            frame3 = ctk.CTkFrame(scrollable_frame)
            frame3.pack(fill="x", padx=75, pady=(0,30))
            self.populate_analysis_table(kategori3, frame3, ["İlan No", "Fiyat (TL)", "M²", "Fiyat/M²"])

    def close_results_window(self):
        if hasattr(self, "results_window") and self.results_window:
            self.results_window.destroy()
            del self.results_window

    def populate_analysis_table(self, data, parent_frame, headers):
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                parent_frame,
                text=header,
                font=("Arial", 12, "bold"),
                corner_radius=5,
                fg_color="#dcdcdc"
            ).grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

        for row, row_data in enumerate(data, start=1):
            for col, value in enumerate(row_data):
                if col == 3:
                    value = round(value)
                label = ctk.CTkLabel(parent_frame, text=value, font=("Arial", 10))
                label.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                if col == 0:
                    label.bind("<Button-1>", lambda event, ilan_no=row_data[0]: self.open_property_page(ilan_no))

    def open_property_page(self, ilan_no):
        if not self.is_processing:
            self.is_processing = True
            self.ilan_no = ilan_no - 1
            if "emlakjet" in self.site:
                threading.Thread(target=self.emlakjet_islem).start()
            elif "hepsiemlak" in self.site:
                threading.Thread(target=self.hepsiemlak_islem).start() 
            elif "sahibinden" in self.site:
                threading.Thread(target=self.sahibinden_islem).start()
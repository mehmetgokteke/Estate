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
import time

class marketanalysis(ctk.CTkFrame):
    def __init__(self, parent, disable_button_callback):
        super().__init__(parent)
        self.label = ctk.CTkLabel(
            self, text="PİYASA ANALİZİ", font=("Helvetica", 30, "bold"), text_color="#000000", fg_color="#00BCD4", corner_radius=15
        )
        self.label.pack(pady=20, padx=20, fill="x", ipady=20)

        self.style = ttk.Style()
        self.style.configure("TCombobox",
                             background="red", 
                             selectbackground="#00BCD4", 
                             selectforeground="#000000")

        self.create_dropdown_menu("İl:", "il", self.get_il_names(), self.on_il_selected)
        self.create_dropdown_menu("İlçe:", "ilce", [], self.on_ilce_selected)
        self.create_dropdown_menu("Mahalle:", "mahalle", [])

        self.property_type_var = ctk.StringVar(value="Kiralık")
        self.create_radio_buttons()

        self.room_count_var = ctk.StringVar(value="1")
        self.create_room_count_buttons()

        self.button_frame = ctk.CTkFrame(self, corner_radius=20)
        self.button_frame.pack(pady=5, padx=20, fill="x")

        self.progress_bar = ctk.CTkProgressBar(self.button_frame, width=550, height=22)
        self.progress_bar.pack(side="left", padx=20)
        self.dynamic_color_progress(0)

        self.analyze_button = ctk.CTkButton(
            self.button_frame, text="Analiz Yap", command=self.analyze_data_threaded, fg_color="#00ACC1", hover_color="#388E3C", font=("Helvetica", 20, "bold"),corner_radius=20, width=500
        )
        self.analyze_button.pack(side="right", padx=20)
        self.bind("<Return>", lambda event: self.analyze_data_threaded())
        self.disable_button_callback = disable_button_callback
        
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
        label = ctk.CTkLabel(frame, text="Kiralık / Satılık:", font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        kiralik_button = ctk.CTkRadioButton(frame, text="Satılık",font=("Helvetica", 14), text_color="#000000", variable=self.property_type_var, value="Satılık", fg_color="#388E3C")
        kiralik_button.pack(side="right", padx=10, pady=5)
        satilik_button = ctk.CTkRadioButton(frame, text="Kiralık",font=("Helvetica", 14), text_color="#000000", variable=self.property_type_var, value="Kiralık", fg_color="#388E3C")
        satilik_button.pack(side="right", padx=10, pady=5)

    def create_room_count_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=10)
        frame.pack(pady=10, padx=20, fill="x")
        label = ctk.CTkLabel(frame, text="Oda Sayısı Seçiniz:", font=("Helvetica", 16), text_color="#000000")
        label.pack(side="left", padx=10, pady=5)
        room_1_button = ctk.CTkRadioButton(frame, text="Hepsi",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="4", fg_color="#388E3C")
        room_1_button.pack(side="right", padx=10, pady=5)
        room_2_button = ctk.CTkRadioButton(frame, text="3+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="3", fg_color="#388E3C")
        room_2_button.pack(side="right", padx=10, pady=5)
        room_3_button = ctk.CTkRadioButton(frame, text="2+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="2", fg_color="#388E3C")
        room_3_button.pack(side="right", padx=10, pady=5)
        room_4_button = ctk.CTkRadioButton(frame, text="1+1",font=("Helvetica", 14), text_color="#000000", variable=self.room_count_var, value="1", fg_color="#388E3C")
        room_4_button.pack(side="right", padx=10, pady=5)

    def create_result_labels(self):
        self.result_labels = {}
        self.price_frame = ctk.CTkFrame(master=self.left_frame)
        self.price_frame.pack(fill="both", expand=True)
        self.result_labels["Fiyat Grafiği"] = self.price_frame

        self.size_frame = ctk.CTkFrame(master=self.right_frame)
        self.size_frame.pack(fill="both", expand=True)
        self.result_labels["m2 Grafiği"] = self.size_frame

    def dynamic_color_progress(self, value):
        if value <= 0.3:
            color = "red"
        elif value <= 0.6:
            color = "yellow"
        else:
            color = "green"
        self.progress_bar.configure(progress_color=color)
        self.progress_bar.set(value)

    def analyze_data_threaded(self):
        if self.analyze_button.cget("state") == "normal":
            self.dynamic_color_progress(0)
            self.selected_il = self.il_combo.get()
            if self.selected_il:
                self.selected_ilce = self.ilce_combo.get()
                self.selected_mahalle = self.mahalle_combo.get()
                self.property_type = self.property_type_var.get()
                self.room_count = self.room_count_var.get()
                self.disable_button_callback(True)
                self.analyze_button.configure(state=tk.DISABLED, text=" Analiz Yapılıyor...", fg_color="#388E3C")
                threading.Thread(target=self.analyze_data).start()
            else:
                messagebox.showerror("Hata", "Lütfen bir il seçiniz.")
                return
        else:
            return

    def analyze_data(self):
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
        time.sleep(5)
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
            self.data = self.fetch_data()
            self.dynamic_color_progress(0.9)
            if self.data:
                threading.Thread(target=self.update_results, args=(self.data,), daemon=True).start()
        finally:
            print(self.data)
            self.disable_button_callback(False)      
            self.analyze_button.configure(state=tk.NORMAL, text="Analiz Yap", fg_color="#00ACC1")
            self.driver.quit()

    def fetch_data(self):
        try:
            prices, sizes = [], []
            self.extract_data(prices, sizes)
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
        
    def extract_data(self, prices, sizes):
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

    def update_results(self, data):
        self.data = data
        self.dynamic_color_progress(1)
        self.plot_graph(data["prices"], "Fiyat Grafiği","İlan Sayısı", "FİYAT", self.result_labels["Fiyat Grafiği"],color='#388E3C',explanation="FİYAT")
        self.price_label.configure(text=f"Ortalama Fiyat: {data['average_price']} TL")

        self.plot_graph(data["sizes"], "M² Grafiği","İlan Sayısı", "M²", self.result_labels["m2 Grafiği"],color='red',explanation="M²")
        self.size_label.configure(text=f"Ortalama M²: {data['average_size']} M²")

    def plot_graph(self, data, title, x_label, y_label, frame, color, explanation):
        fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
        ax.plot(data, marker='o', linestyle="-", color=color, label=explanation)
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend()

        cursor = mplcursors.cursor(ax, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{y_label}: {sel.target[1]:.2f}"))

        for widget in frame.winfo_children():
                widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
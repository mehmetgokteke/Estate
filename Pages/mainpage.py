import customtkinter as ctk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
class mainpage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        estate_name = self.get_estate_name()
        welcome_label = ctk.CTkLabel(
            self,
            text=f"{estate_name}",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15,
        )
        welcome_label.pack(pady=20, padx=20, fill="x", ipady=20)

        self.scrollable_frame = self.create_scrollable_frame()
        self.create_portfolio_summary()
        self.create_customer_summary()
        self.create_old_listings_table()

    def get_estate_name(self):
        conn = sqlite3.connect('estateagentsettings.db')
        cursor = conn.cursor()
        cursor.execute("SELECT emlak_adi FROM estateagentsettings WHERE id=1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result and result[0] else "Ayarlardan Emlak Adı Ekle"

    def create_scrollable_frame(self):
        scrollable_frame = ctk.CTkScrollableFrame(self, width=1200, height=600, fg_color="#EDE6C9")
        scrollable_frame.pack(fill="both", expand=True)
        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        return scrollable_frame

    def create_portfolio_summary(self):
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM portfolio")
        result = cursor.fetchone()
        total_portfolio = result[0] if result else 0

        cursor.execute("SELECT oda_sayisi, COUNT(*) FROM portfolio WHERE oda_sayisi IN ('1+1', '2+1', '3+1', '4+1') GROUP BY oda_sayisi")
        room_data = cursor.fetchall()
        if not room_data:
            oda_labels = ['Veri Yok']
            oda_counts = [0]
        else:
            oda_labels = [f"{row[0]} Oda" for row in room_data]
            oda_counts = [row[1] for row in room_data]

        cursor.execute("SELECT ilan_durumu, COUNT(*) FROM portfolio WHERE ilan_durumu IN ('Kiralık', 'Satılık') GROUP BY ilan_durumu")
        ilan_data = cursor.fetchall()
        if not ilan_data:
            ilan_labels = ['Veri Yok']
            ilan_counts = [0]
        else:
            ilan_labels = [row[0] for row in ilan_data]
            ilan_counts = [row[1] for row in ilan_data]

        cursor.execute("""SELECT fiyat FROM portfolio WHERE ilan_durumu = 'Kiralık'""")
        prices = cursor.fetchall()
        if not prices:
            min_kiralik_fiyat = max_kiralik_fiyat = "0"
        else:
            numeric_prices = [float(price[0].replace('.', '').replace(',', '.')) for price in prices]
            min_price = min(numeric_prices)
            max_price = max(numeric_prices)

            min_kiralik_fiyat = next(price[0] for price in prices if float(price[0].replace('.', '').replace(',', '.')) == min_price)
            max_kiralik_fiyat = next(price[0] for price in prices if float(price[0].replace('.', '').replace(',', '.')) == max_price)

        cursor.execute("""SELECT fiyat FROM portfolio WHERE ilan_durumu = 'Satılık'""")
        satilik_prices = cursor.fetchall()
        if not satilik_prices:
            min_satilik_fiyat = max_satilik_fiyat = "0"
        else:
            satilik_numeric_prices = [float(price[0].replace('.', '').replace(',', '.')) for price in satilik_prices]
            min_satilik_price = min(satilik_numeric_prices)
            max_satilik_price = max(satilik_numeric_prices)

            min_satilik_fiyat = next(price[0] for price in satilik_prices if float(price[0].replace('.', '').replace(',', '.')) == min_satilik_price)
            max_satilik_fiyat = next(price[0] for price in satilik_prices if float(price[0].replace('.', '').replace(',', '.')) == max_satilik_price)

        conn.close()

        portfolio_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F6C91B", corner_radius=15)
        portfolio_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        portfolio_label = ctk.CTkLabel(portfolio_frame, text_color="black", text=f"Toplam Portföy: {total_portfolio}", font=("Helvetica", 16, "bold"))
        portfolio_label.pack(pady=10)

        self.create_doughnut_chart(portfolio_frame, ilan_labels, ilan_counts, "İlan Durumu")

        self.create_pie_chart(portfolio_frame, oda_labels, oda_counts, "Oda Sayısı Dağılımı")

        fiyat_label = ctk.CTkLabel(portfolio_frame, text_color="black", text=f"KİRALIK | En Düşük İlan: {min_kiralik_fiyat} TL - En Yüksek İlan: {max_kiralik_fiyat} TL\nSATILIK | En Düşük İlan: {min_satilik_fiyat} TL - En Yüksek İlan: {max_satilik_fiyat} TL", font=("Helvetica", 16, "bold"))
        fiyat_label.pack(pady=10)

    def create_customer_summary(self):
        conn = sqlite3.connect('customers.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers")
        result = cursor.fetchone()
        total_customers = result[0] if result else 0

        cursor.execute("SELECT gender, COUNT(*) FROM customers WHERE gender IN ('Erkek', 'Kadın') GROUP BY gender")
        gender_data = cursor.fetchall()
        if not gender_data:
            gender_labels = ['Veri Yok']
            gender_counts = [0]
        else:
            gender_labels = [row[0] for row in gender_data]
            gender_counts = [row[1] for row in gender_data]

        cursor.execute("SELECT age FROM customers")
        age_data = [row[0] for row in cursor.fetchall() if row[0] is not None]

        try:
            age_data = [int(age) for age in age_data]
        except ValueError:
            age_data = []

        avg_age = round(sum(age_data) / len(age_data), 2) if age_data else 0

        conn.close()

        customer_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#3BBF9F", corner_radius=15)
        customer_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        customer_label = ctk.CTkLabel(customer_frame, text_color="black", text=f"Toplam Müşteri: {total_customers}", font=("Helvetica", 16, "bold"))
        customer_label.pack(pady=10)

        self.create_bar_chart(customer_frame, gender_labels, gender_counts, "Cinsiyet Dağılımı")

        self.create_histogram_chart(customer_frame, age_data, "Yaş Dağılımı")

        age_label = ctk.CTkLabel(customer_frame, text_color="black", text=f"Ortalama Yaş: {avg_age}", font=("Helvetica", 16, "bold"))
        age_label.pack(pady=10)

    def create_old_listings_table(self):
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()

        one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        cursor.execute("""SELECT tc_kimlik, ilan_tarihi FROM portfolio WHERE date(substr(ilan_tarihi, 7, 4) || '-' || substr(ilan_tarihi, 4, 2) || '-' || substr(ilan_tarihi, 1, 2)) < ? AND ilan_tarihi <> ''""", (one_month_ago,))
        old_listings = cursor.fetchall()

        conn.close()

        old_listings_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F2545B", corner_radius=15)
        old_listings_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        old_listings_label = ctk.CTkLabel(old_listings_frame, text_color="black", text="Güncellenecek İlanlar", font=("Helvetica", 18, "bold"))
        old_listings_label.pack(pady=10)

        if old_listings:
            for listing in old_listings:
                tc_label = ctk.CTkLabel(old_listings_frame, text_color="black", text=f"TC Kimlik: {listing[0]}  ~  İlan Tarihi: {listing[1]} ❌", font=("Helvetica", 16))
                tc_label.pack(fill="x", padx=10, pady=5)
        else:
            no_listings_label = ctk.CTkLabel(old_listings_frame, text_color="black", text="Güncellenecek İlan Yok (✓)", font=("Helvetica", 16))
            no_listings_label.pack(pady=10)

    def create_doughnut_chart(self, frame, labels, data, title):
        colors = ['#F15B67', '#3FBF99']
        plt.rcParams['figure.facecolor'] = '#F6C91B'
        plt.rcParams['axes.facecolor'] = '#A7C7E7'
        plt.rcParams['axes.edgecolor'] = 'black'
        fig, ax = plt.subplots(figsize=(5, 3.4))
        if len(data) == 0 or all(value == 0 for value in data):
            ax.text(0.5, 0.5, "Veri Yok", horizontalalignment='center', verticalalignment='center', fontsize=14, color="black", weight='bold')
        else:
            wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.3), colors=colors)
            for text in texts:
                text.set_fontsize(12)
                text.set_fontname('Arial')
                text.set_color('black')
            plt.setp(autotexts, size=10, weight="bold")

        ax.set_title(title, fontdict={'fontsize': 12, 'fontweight': 'bold', 'color': 'black', 'family': 'Arial'})

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=6)
        canvas.draw()

    def create_histogram_chart(self, frame, data, title):
        plt.rcParams['figure.facecolor'] = '#3BBF9F'
        plt.rcParams['axes.facecolor'] = '#CBC3E3'
        plt.rcParams['axes.edgecolor'] = 'black'
        fig, ax = plt.subplots(figsize=(5, 3.4))
        if len(data) == 0 or all(value == 0 for value in data):
            ax.text(0.5, 0.5, "Veri Yok", horizontalalignment='center', verticalalignment='center', fontsize=14, color="black", weight='bold')
        else:
            ax.hist(data, bins=10, color="#FFA500", edgecolor="black")
        
        ax.set_title(title, fontdict={'fontsize': 12, 'fontweight': 'bold', 'color': 'black', 'family': 'Arial'})

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=6)
        canvas.draw()

    def create_pie_chart(self, frame, labels, data, title):
        colors = ['#6A0DAD', '#FF7F50', '#D2691E', '#C0C0C0', '#66CDAA']
        plt.rcParams['figure.facecolor'] = '#F6C91B'
        plt.rcParams['axes.facecolor'] = '#FFB3B3'
        plt.rcParams['axes.edgecolor'] = 'black'
        fig, ax = plt.subplots(figsize=(5, 3.4))
        if len(data) == 0 or all(value == 0 for value in data):
            ax.text(0.5, 0.5, "Veri Yok", horizontalalignment='center', verticalalignment='center', fontsize=14, color="black", weight='bold')
        else:
            wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            for text in texts:
                text.set_fontsize(12)
                text.set_fontname('Arial')
                text.set_color('black')
            plt.setp(autotexts, size=10, weight="bold")

        ax.set_title(title, fontdict={'fontsize': 12, 'fontweight': 'bold', 'color': 'black', 'family': 'Arial'})

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=6)
        canvas.draw()

    def create_bar_chart(self, frame, labels, data, title):
        colors = ["#007FFF", "#8A2BE2"]
        plt.rcParams['figure.facecolor'] = '#3BBF9F'
        plt.rcParams['axes.facecolor'] = '#FFD1DC'
        plt.rcParams['axes.edgecolor'] = 'black'
        fig, ax = plt.subplots(figsize=(5, 3.4))
        if len(data) == 0 or all(value == 0 for value in data):
            ax.text(0.5, 0.5, "Veri Yok", horizontalalignment='center', verticalalignment='center', fontsize=14, color="black", weight='bold')
        else:
            ax.bar(labels, data, color=colors, width=0.25, edgecolor="black")
            for label in ax.get_xticklabels():
                label.set_fontsize(12)
                label.set_fontname('Arial')
                label.set_color('black')
        
        ax.set_title(title, fontdict={'fontsize': 12, 'fontweight': 'bold', 'color': 'black', 'family': 'Arial'})

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=6)
        canvas.draw()
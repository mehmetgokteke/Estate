from tkcalendar import Calendar
import tkinter as tk
import customtkinter as ctk
import sqlite3
from datetime import datetime


class calendar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Başlık
        self.label_header = ctk.CTkLabel(
            self,
            text="TAKVİM",
            font=("Helvetica", 30, "bold"),
            text_color="#000000",
            fg_color="#00BCD4",
            corner_radius=15,
        )
        self.label_header.pack(fill="x", padx=20, pady=20, ipady=20)

        self.selected_date = tk.StringVar()
        self.selected_date.set(datetime.now().strftime("%d.%m.%Y"))  # Varsayılan tarih formatı gün.ay.yıl

        # Tarih seçimi
        self.date_entry = ctk.CTkEntry(self, textvariable=self.selected_date, font=("Arial", 14), width=200)
        self.date_entry.pack(pady=10)

        # Not metin alanı
        self.note_text = ctk.CTkTextbox(self, height=100, width=500, font=("Arial", 14), corner_radius=20)
        self.note_text.pack(pady=10)

        # Not kaydet butonu
        save_button = ctk.CTkButton(self, text="Notu Kaydet", command=self.save_note, corner_radius=20
        )
        save_button.pack(pady=5)

        # Notları göster butonu
        show_button = ctk.CTkButton(self, text="Notları Göster", command=self.show_notes, corner_radius=20)
        show_button.pack(pady=5)

        # Ekstra notlar butonu
        extra_notes_button = ctk.CTkButton(self, text="Ekstra Notlar", command=self.show_all_notes, corner_radius=20)
        extra_notes_button.pack(pady=5)

        # Takvim için çerçeve
        calendar_frame = ctk.CTkFrame(self)
        calendar_frame.pack(fill="both", expand=True, pady=10)

        # Takvim widget'ı
        self.calendar_widget = Calendar(
            calendar_frame,
            date_pattern="dd.mm.yyyy",
            font=("Arial", 16),
            selectmode="day",
            disabledforeground="gray",
            headersbackground="lightblue",
            headersforeground="black",
            background="white",
            foreground="black",
            selectbackground="#00BCD4",
            selectforeground="white",
            borderwidth=2,
        )
        self.calendar_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Tarih seçimini dinleme
        self.calendar_widget.bind("<<CalendarSelected>>", self.update_date_from_calendar)

    def save_note(self):
        date = self.selected_date.get()
        note = self.note_text.get("1.0", "end").strip()

        if not date or not note:
            tk.messagebox.showerror("Hata", "Tarih ve not alanları boş bırakılamaz.")
            return

        conn = sqlite3.connect("calendar_notes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (date, note) VALUES (?, ?)", (date, note))
        conn.commit()
        conn.close()

        self.note_text.delete("1.0", "end")
        tk.messagebox.showinfo("Başarılı", "Not kaydedildi.")

    def show_notes(self):
        date = self.selected_date.get()

        conn = sqlite3.connect("calendar_notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT note FROM notes WHERE date = ?", (date,))
        notes = cursor.fetchall()
        conn.close()

        if notes:
            notes_text = "\n".join(note[0] for note in notes)
            tk.messagebox.showinfo("Notlar", f"{date} için notlar:\n\n{notes_text}")
        else:
            tk.messagebox.showinfo("Bilgi", f"{date} için herhangi bir not bulunamadı.")

    def show_all_notes(self):
        conn = sqlite3.connect("calendar_notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, note FROM notes")
        notes = cursor.fetchall()
        conn.close()

        # Yeni pencere oluştur
        notes_window = ctk.CTkToplevel(self)
        notes_window.title("Tüm Notlar")
        notes_window.geometry("800x400")
        notes_window.resizable(False,False)
        notes_window.attributes('-topmost', True)

        # Çerçeve ve kaydırma çubuğu
        frame = ctk.CTkFrame(notes_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tablo başlıkları
        headers = ["ID", "Tarih", "Not", "Sil"]
        for col_index, header in enumerate(headers):
            label = ctk.CTkLabel(frame, text=header, font=("Arial", 12, "bold"), fg_color="#00BCD4", text_color="white", corner_radius=8, padx=10, pady=5)
            label.grid(row=0, column=col_index, padx=5, pady=5, sticky="ew")

        # Verileri tablo olarak göster
        for row_index, row in enumerate(notes, start=1):
            for col_index, cell in enumerate(row):
                label = ctk.CTkLabel(frame, text=str(cell), font=("Arial", 10), anchor="w")
                label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")

            # Sil butonu
            delete_button = ctk.CTkButton(
                frame, text="Sil", width=60,
                command=lambda note_id=row[0]: self.delete_note(note_id, notes_window),
                corner_radius=20
            )
            delete_button.grid(row=row_index, column=len(headers) - 1, padx=5, pady=5)

    def delete_note(self, note_id, parent_window):
        conn = sqlite3.connect("calendar_notes.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()

        tk.messagebox.showinfo("Başarılı", "Not silindi.")
        parent_window.destroy()
        self.show_all_notes()  # Tabloyu yeniden oluştur

    def update_date_from_calendar(self, event):
        """Takvimden seçilen tarihi giriş alanına aktar."""
        selected_date = self.calendar_widget.get_date()
        self.selected_date.set(selected_date)

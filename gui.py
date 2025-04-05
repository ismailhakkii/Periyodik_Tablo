#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox

from data import TURKCE_ALFABE, KATMAN1_ELEMENTLER, KATMAN2_ELEMENTLER, KATMAN3_ELEMENTLER
from cipher import PeriodicCipher


class PeriodicCipherGUI:
    """
    Periyodik tablo şifreleme uygulaması arayüzü
    """

    def __init__(self):
        self.cipher = PeriodicCipher()
        self.setup_gui()

    def setup_gui(self):
        """
        Ana GUI bileşenlerini oluşturur
        """
        self.root = tk.Tk()
        self.root.title("Periyodik Tablo Şifreleme")
        self.root.geometry("800x800")

        # Notebook (Sekmeli arayüz)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # Şifreleme sekmesi
        self.encryption_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encryption_frame, text='Şifreleme')

        # Deşifreleme sekmesi
        self.decryption_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decryption_frame, text='Deşifreleme')

        # Element eşleşmeleri sekmesi
        self.matches_reference_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.matches_reference_frame, text='Element Eşleşmeleri')

        # Periyodik Tablo sekmesi
        self.periodic_table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.periodic_table_frame, text='Periyodik Tablo')

        # Diğer arayüzler
        self.setup_periodic_table_tab()
        self.setup_element_matches()
        self.setup_encryption_interface()
        self.setup_decryption_interface()

    def setup_periodic_table_tab(self):
        """
        Periyodik tablo sekmesini oluşturur ve elementlere tıklama özelliği ekler
        """
        title_label = ttk.Label(self.periodic_table_frame, text="Periyodik Tablo", font=("Arial", 18))
        title_label.pack(pady=10)

        # İpucu metni
        hint_label = ttk.Label(self.periodic_table_frame,
                               text="İpucu: Element bilgilerini görmek için element simgelerine tıklayın",
                               font=("Arial", 10, "italic"))
        hint_label.pack(pady=5)

        try:
            # Element bilgilerini import etmeye çalış
            from element_info import ELEMENT_INFO
            self.element_info = ELEMENT_INFO
        except ImportError:
            # Dosya bulunamazsa boş sözlük kullan
            self.element_info = {}

        for katman_num, katman_dict in [("Katman 1", KATMAN1_ELEMENTLER),
                                        ("Katman 2", KATMAN2_ELEMENTLER),
                                        ("Katman 3", KATMAN3_ELEMENTLER)]:
            frame = ttk.LabelFrame(self.periodic_table_frame, text=katman_num)
            frame.pack(padx=10, pady=5, fill="x")
            for letter, info in katman_dict.items():
                r, c = info.get('konum', (0, 0))
                element_symbol = info['element']
                btn = ttk.Button(frame, text=element_symbol, width=4)

                # Element bilgisi varsa tıklama fonksiyonu ekle
                if hasattr(self, 'element_info') and element_symbol in self.element_info:
                    btn.config(command=lambda sym=element_symbol: self.show_element_info(sym))
                else:
                    btn.config(command=lambda sym=element_symbol: self.show_basic_element_info(sym))

                btn.grid(row=r, column=c, padx=2, pady=2)

    def show_element_info(self, element_symbol):
        """
        Element hakkında bilgi kutusunu gösterir
        """
        if hasattr(self, 'element_info') and element_symbol in self.element_info:
            element_data = self.element_info[element_symbol]
            info_text = f"{element_data['ad']} ({element_data['sembol']})\n"
            info_text += f"Atom Numarası: {element_data['atom_numarasi']}\n"
            info_text += f"Atom Ağırlığı: {element_data['atom_agirligi']}\n"
            info_text += f"Kategori: {element_data['kategori']}\n\n"
            info_text += f"{element_data['bilgi']}"

            messagebox.showinfo(f"{element_data['ad']} Bilgileri", info_text)
        else:
            self.show_basic_element_info(element_symbol)

    def show_basic_element_info(self, element_symbol):
        """
        ELEMENT_INFO'da olmayan elementler için temel bilgi gösterir
        """
        # Tüm katmanlarda elementi ara
        element_info = None
        harf = None
        katman = None

        for katman_num, layer_dict in [(1, KATMAN1_ELEMENTLER),
                                       (2, KATMAN2_ELEMENTLER),
                                       (3, KATMAN3_ELEMENTLER)]:
            for letter, info in layer_dict.items():
                if info['element'] == element_symbol:
                    element_info = info
                    harf = letter
                    katman = katman_num
                    break
            if element_info:
                break

        if element_info:
            info_text = f"Element: {element_symbol}\n"
            info_text += f"Türkçe Alfabe Karşılığı: {harf} (Katman {katman})\n"
            info_text += f"Orbital Dizilimi: {element_info['orbital']}\n"
            info_text += f"Son Katman Elektron Sayısı: {element_info['son_katman']}\n"
            info_text += f"Periyodik Tablo Konumu: Satır {element_info['konum'][0]}, Sütun {element_info['konum'][1]}"

            messagebox.showinfo(f"{element_symbol} Hakkında", info_text)
        else:
            messagebox.showinfo("Bilgi Bulunamadı",
                                f"{element_symbol} elementi hakkında detaylı bilgi bulunmamaktadır.")

    def setup_element_matches(self):
        """
        Element eşleşmeleri sekmesini oluşturur
        """
        columns = ("harf", "element1", "orbital1", "katman1", "konum1",
                   "element2", "orbital2", "katman2", "konum2",
                   "element3", "orbital3", "katman3", "konum3")

        tree = ttk.Treeview(self.matches_reference_frame, columns=columns, show="headings")
        tree.heading("harf", text="Harf")
        tree.heading("element1", text="1. Element")
        tree.heading("orbital1", text="1. Orbital")
        tree.heading("katman1", text="1. Son Katman")
        tree.heading("konum1", text="1. Konum")
        tree.heading("element2", text="2. Element")
        tree.heading("orbital2", text="2. Orbital")
        tree.heading("katman2", text="2. Son Katman")
        tree.heading("konum2", text="2. Konum")
        tree.heading("element3", text="3. Element")
        tree.heading("orbital3", text="3. Orbital")
        tree.heading("katman3", text="3. Son Katman")
        tree.heading("konum3", text="3. Konum")

        for col in columns:
            tree.column(col, width=100)
        tree.column("harf", width=50)

        scrollbar_y = ttk.Scrollbar(self.matches_reference_frame, orient="vertical", command=tree.yview)
        scrollbar_x = ttk.Scrollbar(self.matches_reference_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.matches_reference_frame.grid_rowconfigure(0, weight=1)
        self.matches_reference_frame.grid_columnconfigure(0, weight=1)

        for harf in TURKCE_ALFABE:
            element1 = KATMAN1_ELEMENTLER.get(harf, {})
            element2 = KATMAN2_ELEMENTLER.get(harf, {})
            element3 = KATMAN3_ELEMENTLER.get(harf, {})

            tree.insert("", "end", values=(
                harf,
                element1.get('element', '-'),
                element1.get('orbital', '-'),
                element1.get('son_katman', '-'),
                f"({element1.get('konum', (0, 0))[0]},{element1.get('konum', (0, 0))[1]})",
                element2.get('element', '-'),
                element2.get('orbital', '-'),
                element2.get('son_katman', '-'),
                f"({element2.get('konum', (0, 0))[0]},{element2.get('konum', (0, 0))[1]})",
                element3.get('element', '-'),
                element3.get('orbital', '-'),
                element3.get('son_katman', '-'),
                f"({element3.get('konum', (0, 0))[0]},{element3.get('konum', (0, 0))[1]})"
            ))

    def setup_encryption_interface(self):
        """
        Şifreleme sekmesini oluşturur
        """
        self.input_frame = ttk.LabelFrame(self.encryption_frame, text="Metin Girişi")
        self.input_frame.pack(padx=10, pady=10, fill="x")

        self.input_text = tk.Text(self.input_frame, height=5)
        self.input_text.pack(padx=5, pady=5, fill="x")

        self.button_frame = ttk.Frame(self.encryption_frame)
        self.button_frame.pack(pady=5)

        self.encrypt_button = ttk.Button(self.button_frame, text="Şifrele", command=self.encrypt_text)
        self.encrypt_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Temizle", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.result_frame = ttk.LabelFrame(self.encryption_frame, text="Sonuç")
        self.result_frame.pack(padx=10, pady=5, fill="x")

        self.result_text = tk.Text(self.result_frame, height=5)
        self.result_text.pack(padx=5, pady=5, fill="x")

        self.copy_button = ttk.Button(self.result_frame, text="Sonucu Kopyala", command=self.copy_result)
        self.copy_button.pack(pady=5)

        self.log_frame = ttk.LabelFrame(self.encryption_frame, text="Şifreleme Adımları")
        self.log_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.log_text = tk.Text(self.log_frame, height=10)
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)

        self.matches_frame = ttk.LabelFrame(self.encryption_frame, text="Harf-Element Eşleşmeleri")
        self.matches_frame.pack(padx=10, pady=5, fill="x")

        self.matches_table = ttk.Treeview(self.matches_frame,
                                          columns=("harf", "element", "orbital", "son_katman", "oteleme"),
                                          show="headings",
                                          height=5)
        self.matches_table.heading("harf", text="Harf")
        self.matches_table.heading("element", text="Element")
        self.matches_table.heading("orbital", text="Orbital")
        self.matches_table.heading("son_katman", text="Son Katman")
        self.matches_table.heading("oteleme", text="Öteleme")
        self.matches_table.column("harf", width=50)
        self.matches_table.column("element", width=100)
        self.matches_table.column("orbital", width=100)
        self.matches_table.column("son_katman", width=100)
        self.matches_table.column("oteleme", width=100)
        self.matches_table.pack(padx=5, pady=5, fill="x")

    def setup_decryption_interface(self):
        """
        Deşifreleme sekmesini oluşturur
        """
        self.decrypt_input_frame = ttk.LabelFrame(self.decryption_frame, text="Şifreli Metin Girişi")
        self.decrypt_input_frame.pack(padx=10, pady=10, fill="x")

        self.decrypt_input_text = tk.Text(self.decrypt_input_frame, height=5)
        self.decrypt_input_text.pack(padx=5, pady=5, fill="x")

        self.decrypt_button_frame = ttk.Frame(self.decryption_frame)
        self.decrypt_button_frame.pack(pady=5)

        self.decrypt_button = ttk.Button(self.decrypt_button_frame, text="Deşifrele", command=self.decrypt_text)
        self.decrypt_button.pack(side=tk.LEFT, padx=5)

        self.decrypt_clear_button = ttk.Button(self.decrypt_button_frame, text="Temizle",
                                               command=self.clear_decrypt_text)
        self.decrypt_clear_button.pack(side=tk.LEFT, padx=5)

        self.decrypt_result_frame = ttk.LabelFrame(self.decryption_frame, text="Sonuç")
        self.decrypt_result_frame.pack(padx=10, pady=5, fill="x")

        self.decrypt_result_text = tk.Text(self.decrypt_result_frame, height=5)
        self.decrypt_result_text.pack(padx=5, pady=5, fill="x")

        self.decrypt_copy_button = ttk.Button(self.decrypt_result_frame, text="Sonucu Kopyala",
                                              command=self.copy_decrypt_result)
        self.decrypt_copy_button.pack(pady=5)

        self.decrypt_log_frame = ttk.LabelFrame(self.decryption_frame, text="Deşifreleme Adımları")
        self.decrypt_log_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.decrypt_log_text = tk.Text(self.decrypt_log_frame, height=10)
        self.decrypt_log_text.pack(padx=5, pady=5, fill="both", expand=True)

        # Alternatif çözümlerin gösterileceği bölüm - geliştirilmiş:
        self.alternatives_frame = ttk.LabelFrame(self.decryption_frame, text="Alternatif Çözümler")
        self.alternatives_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.alternatives_table = ttk.Treeview(self.alternatives_frame,
                                               columns=("koordinat", "adaylar", "katmanlar", "secilen"),
                                               show="headings",
                                               height=5)
        self.alternatives_table.heading("koordinat", text="Koordinat")
        self.alternatives_table.heading("adaylar", text="Aday Harfler")
        self.alternatives_table.heading("katmanlar", text="Katmanlar")
        self.alternatives_table.heading("secilen", text="Seçilen Harf")
        self.alternatives_table.column("koordinat", width=80)
        self.alternatives_table.column("adaylar", width=120)
        self.alternatives_table.column("katmanlar", width=80)
        self.alternatives_table.column("secilen", width=80)
        self.alternatives_table.pack(padx=5, pady=5, fill="both", expand=True)

    # Şifreleme fonksiyonları

    def encrypt_text(self):
        """
        Şifreleme işlemini başlatır
        """
        self.result_text.delete("1.0", "end")
        self.log_text.delete("1.0", "end")
        for item in self.matches_table.get_children():
            self.matches_table.delete(item)

        input_text = self.input_text.get("1.0", "end-1c")

        # Şifreleme işlemini gerçekleştir
        result, log_messages, matches = self.cipher.encrypt(input_text, self.add_to_log)

        # Sonucu göster
        self.result_text.insert("1.0", result)

        # Eşleşmeleri tabloya ekle
        for match in matches:
            self.matches_table.insert("", "end", values=(
                match['harf'],
                match['element'],
                match['orbital'],
                match['son_katman'],
                match['oteleme']
            ))

    def decrypt_text(self):
        """
        Deşifreleme işlemini başlatır
        """
        self.decrypt_result_text.delete("1.0", "end")
        self.decrypt_log_text.delete("1.0", "end")
        for item in self.alternatives_table.get_children():
            self.alternatives_table.delete(item)

        input_text = self.decrypt_input_text.get("1.0", "end-1c").strip()

        # Deşifreleme işlemini gerçekleştir
        result, log_messages, alternatives = self.cipher.decrypt(input_text, self.add_to_decrypt_log)

        # Sonucu göster
        self.decrypt_result_text.insert("1.0", result)

        # Alternatifleri tabloya ekle - Geliştirilmiş format ile
        for alt in alternatives:
            aday_harfler = ", ".join([c['harf'] for c in alt['adaylar']])
            katmanlar = ", ".join([str(c['katman']) for c in alt['adaylar']])

            self.alternatives_table.insert("", "end", values=(
                alt['koordinat'],
                aday_harfler,
                katmanlar,
                alt['secilen']
            ))

    # Yardımcı fonksiyonlar

    def clear_text(self):
        """
        Şifreleme sekmesindeki metinleri temizler
        """
        self.input_text.delete("1.0", "end")
        self.result_text.delete("1.0", "end")
        self.log_text.delete("1.0", "end")
        for item in self.matches_table.get_children():
            self.matches_table.delete(item)

    def clear_decrypt_text(self):
        """
        Deşifreleme sekmesindeki metinleri temizler
        """
        self.decrypt_input_text.delete("1.0", "end")
        self.decrypt_result_text.delete("1.0", "end")
        self.decrypt_log_text.delete("1.0", "end")
        for item in self.alternatives_table.get_children():
            self.alternatives_table.delete(item)

    def copy_result(self):
        """
        Şifreleme sonucunu panoya kopyalar
        """
        result = self.result_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        messagebox.showinfo("Bilgi", "Sonuç panoya kopyalandı!")

    def copy_decrypt_result(self):
        """
        Deşifreleme sonucunu panoya kopyalar
        """
        result = self.decrypt_result_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        messagebox.showinfo("Bilgi", "Sonuç panoya kopyalandı!")

    def add_to_log(self, message):
        """
        Şifreleme log'una mesaj ekler
        """
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def add_to_decrypt_log(self, message):
        """
        Deşifreleme log'una mesaj ekler
        """
        self.decrypt_log_text.insert("end", message + "\n")
        self.decrypt_log_text.see("end")

    def run(self):
        """
        Uygulamayı başlatır
        """
        self.root.mainloop()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Animasyon modüllerini içeren dizini Python yoluna ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from data import TURKCE_ALFABE, KATMAN1_ELEMENTLER, KATMAN2_ELEMENTLER, KATMAN3_ELEMENTLER
from cipher import PeriodicCipher

# Animasyon modüllerini import etmeyi dene
try:
    from animations import AnimationEffects
    from element_visualization import ElementVisualizer
    from encryption_animation import EncryptionAnimator

    ANIMATIONS_AVAILABLE = True
    print("Animasyon modülleri başarıyla yüklendi.")
except ImportError as e:
    print(f"Animasyon modülleri yüklenemedi: {e}")
    ANIMATIONS_AVAILABLE = False


class PeriodicCipherGUI:
    """
    Periyodik tablo şifreleme uygulaması arayüzü
    """

    def __init__(self):
        self.cipher = PeriodicCipher()
        self.root = tk.Tk()  # Root'u önce oluştur

        # Animasyon ve görselleştirme sınıflarını başlat
        if ANIMATIONS_AVAILABLE:
            self.animations = AnimationEffects()
            self.element_visualizer = ElementVisualizer(self.root)
            self.encryption_animator = None  # Bu lazy initialization olabilir
        else:
            self.animations = None
            self.element_visualizer = None
            self.encryption_animator = None

        self.setup_gui()

    def setup_gui(self):
        """
        Ana GUI bileşenlerini oluşturur
        """
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
        except ImportError as e:
            print(f"Element bilgileri yüklenemedi: {e}")
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
                if ANIMATIONS_AVAILABLE and hasattr(self, 'element_info') and element_symbol in self.element_info:
                    btn.config(command=lambda sym=element_symbol: self.show_element_visualization(sym))
                else:
                    btn.config(command=lambda sym=element_symbol: self.show_basic_element_info(sym))

                btn.grid(row=r, column=c, padx=2, pady=2)

    def show_element_visualization(self, element_symbol):
        """
        Element için animasyonlu gösterim penceresini açar
        """
        if not ANIMATIONS_AVAILABLE:
            self.show_basic_element_info(element_symbol)
            return

        # ElementVisualizer henüz oluşturulmamışsa oluştur
        if self.element_visualizer is None:
            self.element_visualizer = ElementVisualizer(self.root)

        if element_symbol in self.element_info:
            # Düğmeyi vurgula
            for frame in self.periodic_table_frame.winfo_children():
                if isinstance(frame, ttk.LabelFrame):
                    for button in frame.winfo_children():
                        if isinstance(button, ttk.Button) and button['text'] == element_symbol:
                            try:
                                # Animasyon sınıfını kullanarak parçacık efekti oluştur
                                button_x = button.winfo_rootx() - self.root.winfo_rootx() + button.winfo_width() // 2
                                button_y = button.winfo_rooty() - self.root.winfo_rooty() + button.winfo_height() // 2
                                self.animations.create_particle_effect(
                                    self.periodic_table_frame,
                                    button_x, button_y,
                                    colors=['#3399ff', '#66ccff', '#99ddff']
                                )
                            except Exception as e:
                                print(f"Parçacık efekti oluşturulamadı: {e}")
                            break

            try:
                # ElementVisualizer ile detaylı bilgiyi göster
                self.element_visualizer.show_element_details(self.element_info[element_symbol])
            except Exception as e:
                print(f"Element detayları gösterilemedi: {e}")
                self.show_basic_element_info(element_symbol)
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

        # Animasyon gösterme düğmesi (eğer animasyonlar mevcutsa)
        if ANIMATIONS_AVAILABLE:
            self.animation_button = ttk.Button(self.button_frame, text="Animasyonu Göster",
                                               command=self.show_encryption_animation)
            self.animation_button.pack(side=tk.LEFT, padx=5)
            # Başlangıçta devre dışı bırak (şifreleme yapılmadığı için)
            self.animation_button.config(state="disabled")

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

        # Animasyon gösterme düğmesi (eğer animasyonlar mevcutsa)
        if ANIMATIONS_AVAILABLE:
            self.decrypt_animation_button = ttk.Button(self.decrypt_button_frame, text="Animasyonu Göster",
                                                       command=self.show_decryption_animation)
            self.decrypt_animation_button.pack(side=tk.LEFT, padx=5)
            # Başlangıçta devre dışı bırak (deşifreleme yapılmadığı için)
            self.decrypt_animation_button.config(state="disabled")

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

        # Alternatifler tablosu - fotodaki tasarıma göre düzenlendi
        self.alternatives_table = ttk.Treeview(
            self.alternatives_frame,
            columns=("koordinat", "aday_harfler", "katmanlar", "secilen_harf"),
            show="headings",
            height=5
        )
        self.alternatives_table.heading("koordinat", text="Koordinat")
        self.alternatives_table.heading("aday_harfler", text="Aday Harfler")
        self.alternatives_table.heading("katmanlar", text="Katmanlar")
        self.alternatives_table.heading("secilen_harf", text="Seçilen Harf")
        self.alternatives_table.column("koordinat", width=80)
        self.alternatives_table.column("aday_harfler", width=250)
        self.alternatives_table.column("katmanlar", width=100)
        self.alternatives_table.column("secilen_harf", width=100)
        self.alternatives_table.pack(padx=5, pady=5, fill="both", expand=True)

        # Alternatif seçme düğmeleri
        self.alternatives_button_frame = ttk.Frame(self.alternatives_frame)
        self.alternatives_button_frame.pack(pady=5, fill="x")

        self.use_alternative_button = ttk.Button(self.alternatives_button_frame,
                                                 text="Seçili Alternatifi Kullan",
                                                 command=self.use_selected_alternative)
        self.use_alternative_button.pack(side=tk.LEFT, padx=5)

        # Alternatif çözümler için deneme düğmesi
        self.try_all_alternatives_button = ttk.Button(self.alternatives_button_frame,
                                                      text="Tüm Kombinasyonları Dene",
                                                      command=self.try_all_alternatives)
        self.try_all_alternatives_button.pack(side=tk.LEFT, padx=5)

    # Şifreleme fonksiyonları

    def encrypt_text(self):
        """
        Şifreleme işlemini başlatır ve animasyon oluşturur
        """
        self.result_text.delete("1.0", "end")
        self.log_text.delete("1.0", "end")
        for item in self.matches_table.get_children():
            self.matches_table.delete(item)

        input_text = self.input_text.get("1.0", "end-1c")

        # Animasyonlar mevcutsa daktilo efekti uygula
        if ANIMATIONS_AVAILABLE and self.animations is not None:
            try:
                self.animations.typewriter_effect(
                    self.log_text,
                    "Şifreleme işlemi başlatılıyor...\n" + "=" * 50 + "\n",
                    delay=20
                )
                # Animasyon butonunu aktif et
                if hasattr(self, 'animation_button'):
                    self.animation_button.config(state="normal")
            except Exception as e:
                print(f"Daktilo efekti uygulanamadı: {e}")
                self.add_to_log("Şifreleme işlemi başlatılıyor...\n" + "=" * 50 + "\n")
        else:
            self.add_to_log("Şifreleme işlemi başlatılıyor...\n" + "=" * 50 + "\n")

        # Şifreleme işlemini gerçekleştir
        result, log_messages, matches = self.cipher.encrypt(input_text, self.add_to_log)

        # Sonucu göster (animasyonlu veya normal)
        if ANIMATIONS_AVAILABLE and self.animations is not None:
            try:
                self.animations.typewriter_effect(self.result_text, result, delay=30)
            except Exception as e:
                print(f"Daktilo efekti uygulanamadı: {e}")
                self.result_text.insert("1.0", result)
        else:
            self.result_text.insert("1.0", result)

        # Eşleşmeleri tabloya ekle ve vurgulamalı göster
        for i, match in enumerate(matches):
            item_id = self.matches_table.insert("", "end", values=(
                match['harf'],
                match['element'],
                match['orbital'],
                match['son_katman'],
                match['oteleme']
            ))

            # Animasyonlar mevcutsa vurgula
            if ANIMATIONS_AVAILABLE:
                try:
                    self.root.after(i * 300 + 500, lambda id=item_id: self._highlight_table_row(self.matches_table, id))
                except Exception as e:
                    print(f"Tablo satırı vurgulanamadı: {e}")

    def decrypt_text(self):
        """
        Deşifreleme işlemini başlatır ve animasyon oluşturur
        """
        self.decrypt_result_text.delete("1.0", "end")
        self.decrypt_log_text.delete("1.0", "end")
        for item in self.alternatives_table.get_children():
            self.alternatives_table.delete(item)

        input_text = self.decrypt_input_text.get("1.0", "end-1c").strip()

        # Animasyonlar mevcutsa daktilo efekti uygula
        if ANIMATIONS_AVAILABLE and self.animations is not None:
            try:
                self.animations.typewriter_effect(
                    self.decrypt_log_text,
                    "Deşifreleme işlemi başlatılıyor...\n" + "=" * 50 + "\n",
                    delay=20
                )
                # Animasyon butonunu aktif et
                if hasattr(self, 'decrypt_animation_button'):
                    self.decrypt_animation_button.config(state="normal")
            except Exception as e:
                print(f"Daktilo efekti uygulanamadı: {e}")
                self.add_to_decrypt_log("Deşifreleme işlemi başlatılıyor...\n" + "=" * 50 + "\n")
        else:
            self.add_to_decrypt_log("Deşifreleme işlemi başlatılıyor...\n" + "=" * 50 + "\n")

        # Deşifreleme işlemini gerçekleştir
        result, log_messages, alternatives = self.cipher.decrypt(input_text, self.add_to_decrypt_log)

        # Alternatifler listesini global olarak sakla
        self.current_alternatives = alternatives

        # Sonucu göster (animasyonlu veya normal)
        if ANIMATIONS_AVAILABLE and self.animations is not None:
            try:
                self.animations.typewriter_effect(self.decrypt_result_text, result, delay=30)
            except Exception as e:
                print(f"Daktilo efekti uygulanamadı: {e}")
                self.decrypt_result_text.insert("1.0", result)
        else:
            self.decrypt_result_text.insert("1.0", result)

        # Alternatifleri tabloya ekle
        self.process_alternatives(alternatives)

    def process_alternatives(self, alternatives):
        """
        Alternatif çözümleri işler ve tabloya ekler
        """
        # Tablo temizle
        for item in self.alternatives_table.get_children():
            self.alternatives_table.delete(item)

        # Koordinatlara göre gruplandır
        coord_dict = {}
        for alt in alternatives:
            coord = alt['koordinat']
            if coord not in coord_dict:
                coord_dict[coord] = {
                    'aday_harfler': [],
                    'katmanlar': [],
                    'secilen': alt['secilen']
                }

            # Adayları ve katmanları ekle
            for candidate in alt['adaylar']:
                if candidate['harf'] not in coord_dict[coord]['aday_harfler']:
                    coord_dict[coord]['aday_harfler'].append(candidate['harf'])
                    coord_dict[coord]['katmanlar'].append(str(candidate['katman']))

        # Tabloya ekle
        for coord, data in coord_dict.items():
            aday_harfler_str = ", ".join(data['aday_harfler'])
            katmanlar_str = ", ".join(data['katmanlar'])

            self.alternatives_table.insert("", "end", values=(
                coord,
                aday_harfler_str,
                katmanlar_str,
                data['secilen']
            ))

    def use_selected_alternative(self):
        """
        Tabloda seçilen alternatifi kullanır
        """
        selection = self.alternatives_table.selection()
        if not selection:
            messagebox.showinfo("Uyarı", "Lütfen bir alternatif seçin.")
            return

        # Seçilen satırın değerlerini al
        values = self.alternatives_table.item(selection[0], "values")
        koordinat = values[0]
        aday_harfler = values[1].split(", ")
        secilen_harf = values[3]

        # Kullanıcıya hangi harfi seçmek istediğini sor
        selected_letter = self.ask_user_for_alternative(koordinat, aday_harfler, secilen_harf)
        if not selected_letter:
            return

        # Mevcut deşifre sonucunu al
        current_result = self.decrypt_result_text.get("1.0", "end-1c")

        # Seçilen alternatifi uygula
        # Orijinal harfi bul ve değiştir
        # Bu kısım basitleştirilmiştir ve geliştirilebilir
        modified_result = ""
        found = False
        for char in current_result:
            if char == secilen_harf and not found:
                modified_result += selected_letter
                found = True
            else:
                modified_result += char

        # Değiştirilmiş sonucu göster
        self.decrypt_result_text.delete("1.0", "end")
        self.decrypt_result_text.insert("1.0", modified_result)

        # Tabloda seçilen harfi güncelle
        self.alternatives_table.item(selection[0], values=(
            koordinat,
            values[1],
            values[2],
            selected_letter
        ))

        # Log'a ekle
        self.add_to_decrypt_log(f"\nAlternatif harf kullanıldı: '{secilen_harf}' yerine '{selected_letter}' seçildi.")
        self.add_to_decrypt_log(f"Güncellenen sonuç: {modified_result}")

    def ask_user_for_alternative(self, koordinat, aday_harfler, secilen_harf):
        """
        Kullanıcıya hangi alternatif harfi kullanmak istediğini sorar
        """
        # Mini iletişim kutusu oluştur
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Alternatif Seçimi - {koordinat}")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()  # Modal pencere

        tk.Label(dialog, text=f"{koordinat} koordinatı için alternatif seçin:", font=("Arial", 12)).pack(pady=10)

        # Seçim için değişken
        selected_var = tk.StringVar(value=secilen_harf)

        # Alternatifler için radio butonlar
        for harf in aday_harfler:
            tk.Radiobutton(dialog, text=harf, variable=selected_var, value=harf, font=("Arial", 12)).pack(anchor="w",
                                                                                                          padx=20)

        # Butonlar
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10, fill="x")

        result = [None]  # Sonucu saklamak için

        # Tamam butonu
        def on_ok():
            result[0] = selected_var.get()
            dialog.destroy()

        # İptal butonu
        def on_cancel():
            dialog.destroy()

        tk.Button(button_frame, text="Tamam", command=on_ok).pack(side="left", padx=10, expand=True)
        tk.Button(button_frame, text="İptal", command=on_cancel).pack(side="right", padx=10, expand=True)

        # Kullanıcı cevap verene kadar bekle
        self.root.wait_window(dialog)

        return result[0]

    def try_all_alternatives(self):
        """
        Alternatif kombinasyonlarını dener ve olası sonuçları gösterir
        """
        if not hasattr(self, 'current_alternatives') or not self.current_alternatives:
            messagebox.showinfo("Bilgi", "Önce deşifreleme yapmalısınız.")
            return

        # Sonuçları göstermek için yeni pencere
        results_window = tk.Toplevel(self.root)
        results_window.title("Olası Deşifre Sonuçları")
        results_window.geometry("600x400")

        # İşlem açıklaması
        tk.Label(results_window, text="Tüm olası alternatif kombinasyonları:", font=("Arial", 12)).pack(pady=10)

        # Sonuçlar için liste kutusu
        results_frame = tk.Frame(results_window)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Listbox ve scrollbar
        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")

        results_listbox = tk.Listbox(results_frame, font=("Arial", 12), width=40, height=15)
        results_listbox.pack(side="left", fill="both", expand=True)

        results_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=results_listbox.yview)

        # Seçilen sonucu kullanma butonu
        def use_selected_result():
            selected_idx = results_listbox.curselection()
            if not selected_idx:
                messagebox.showinfo("Uyarı", "Lütfen bir sonuç seçin.")
                return

            selected_text = results_listbox.get(selected_idx[0])
            # Sonuç metnini ayıkla
            if ": " in selected_text:
                selected_text = selected_text.split(": ")[1]

            # Ana sonucu güncelle
            self.decrypt_result_text.delete("1.0", "end")
            self.decrypt_result_text.insert("1.0", selected_text)

            # Log mesajı ekle
            self.add_to_decrypt_log(f"\nAlternatif sonuç seçildi: {selected_text}")

            # Pencereyi kapat
            results_window.destroy()

        tk.Button(results_window, text="Seçilen Sonucu Kullan", command=use_selected_result).pack(pady=10)

        # Mevcut sonucu al
        current_result = self.decrypt_result_text.get("1.0", "end-1c")

        # İlk sonuç olarak mevcut sonucu ekle
        results_listbox.insert("end", f"1: {current_result} (Mevcut)")

        # Alternatif koordinat ve harfleri topla
        alternatives_by_coord = {}
        for alt in self.current_alternatives:
            coord = alt['koordinat']
            if coord not in alternatives_by_coord:
                alternatives_by_coord[coord] = []

            for candidate in alt['adaylar']:
                if candidate['harf'] not in alternatives_by_coord[coord]:
                    alternatives_by_coord[coord].append(candidate['harf'])

        # Basit kombinasyonlar oluştur (ilk birkaç koordinat için)
        # Tüm kombinasyonları hesaplamak çok fazla olabilir, bu yüzden sadece birkaçını gösteriyoruz
        results = [current_result]
        count = 1

        # Her koordinat için alternatifler dene
        for coord, alternatives in alternatives_by_coord.items():
            # Her karakter için arama
            for i, char in enumerate(current_result):
                # Mevcut koordinatta kullanılmış bir karakter mi?
                for alt in self.current_alternatives:
                    if alt['koordinat'] == coord and alt['secilen'] == char:
                        # Bu karakterin olası alternatifleri
                        for alt_char in alternatives:
                            if alt_char != char:  # Kendisini hariç tut
                                # Yeni sonuç oluştur
                                new_result = current_result[:i] + alt_char + current_result[i + 1:]
                                if new_result not in results:
                                    count += 1
                                    results.append(new_result)
                                    results_listbox.insert("end", f"{count}: {new_result}")

                                    # Maksimum 20 sonuç göster
                                    if count >= 20:
                                        break

            # Maksimum sonuç sayısına ulaşıldıysa döngüyü bitir
            if count >= 20:
                break

        # Eğer hiç alternatif yoksa bilgi mesajı göster
        if count == 1:
            results_listbox.insert("end", "Başka alternatif bulunamadı.")

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

        # Animasyon butonu varsa devre dışı bırak
        if ANIMATIONS_AVAILABLE and hasattr(self, 'animation_button'):
            self.animation_button.config(state="disabled")

    def clear_decrypt_text(self):
        """
        Deşifreleme sekmesindeki metinleri temizler
        """
        self.decrypt_input_text.delete("1.0", "end")
        self.decrypt_result_text.delete("1.0", "end")
        self.decrypt_log_text.delete("1.0", "end")
        for item in self.alternatives_table.get_children():
            self.alternatives_table.delete(item)

        # Animasyon butonu varsa devre dışı bırak
        if ANIMATIONS_AVAILABLE and hasattr(self, 'decrypt_animation_button'):
            self.decrypt_animation_button.config(state="disabled")

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

    # Animasyon ile ilgili yardımcı metodlar

    def _highlight_table_row(self, table, item_id):
        """
        Tablo satırını vurgular ve sonra normal hale getirir
        """
        if ANIMATIONS_AVAILABLE:
            try:
                table.selection_set(item_id)
                table.see(item_id)
                self.root.after(1000, lambda: table.selection_remove(item_id))
            except Exception as e:
                print(f"Satır vurgulanırken hata: {e}")

    def show_encryption_animation(self):
        """
        Şifreleme animasyonu penceresini açar
        """
        if not ANIMATIONS_AVAILABLE:
            messagebox.showinfo("Bilgi", "Animasyon modülleri yüklenmediği için bu özellik kullanılamıyor.")
            return

        try:
            # İlk kullanımda animator nesnesini oluştur
            if self.encryption_animator is None:
                self.encryption_animator = EncryptionAnimator(self.root)

            # Animasyon penceresi oluştur
            self.encryption_animator.create_animation_window()

            # Şifreleme adımlarını al
            input_text = self.input_text.get("1.0", "end-1c").upper()

            letter_counts = {}
            element_infos = []
            shifts = []
            shifted_letters = []
            results = []

            for letter in input_text:
                if letter not in self.cipher.turkce_alfabe:
                    continue

                letter_counts[letter] = letter_counts.get(letter, 0) + 1
                count = letter_counts[letter]

                element_info = self.cipher.get_element_for_letter(letter, count)
                if element_info is None:
                    continue

                element_infos.append(element_info)

                shift = self.cipher.orbital_to_shift(element_info['orbital'], element_info['son_katman'])
                shifts.append(shift)

                shifted_letter = self.cipher.shift_letter(letter, shift)
                shifted_letters.append(shifted_letter)

                shifted_element = None
                for katman_dict in [self.cipher.katman1_elementler,
                                    self.cipher.katman2_elementler,
                                    self.cipher.katman3_elementler]:
                    if shifted_letter in katman_dict:
                        shifted_element = katman_dict[shifted_letter]
                        break

                if shifted_element:
                    coord = f"{shifted_element['konum'][0]:02d}{shifted_element['konum'][1]:02d}"
                    results.append(coord)
                else:
                    results.append(shifted_letter)

            # Animasyon adımlarını ekle
            self.encryption_animator.add_encryption_steps(
                input_text, letter_counts, element_infos, shifts, shifted_letters, results
            )
        except Exception as e:
            print(f"Şifreleme animasyonu gösterilirken hata: {e}")
            messagebox.showerror("Hata", f"Animasyon oluşturulurken bir hata oluştu: {e}")

    def show_decryption_animation(self):
        """
        Deşifreleme animasyonu penceresini açar
        """
        if not ANIMATIONS_AVAILABLE:
            messagebox.showinfo("Bilgi", "Animasyon modülleri yüklenmediği için bu özellik kullanılamıyor.")
            return

        try:
            # İlk kullanımda animator nesnesini oluştur
            if self.encryption_animator is None:
                self.encryption_animator = EncryptionAnimator(self.root)

            # Animasyon penceresi oluştur
            self.encryption_animator.create_animation_window("Deşifreleme Animasyonu")

            # Deşifreleme adımlarını al
            input_text = self.decrypt_input_text.get("1.0", "end-1c").strip()

            coordinates = []
            shifted_letters = []
            original_letters = []
            results = []

            # Deşifreleme işlemini taklit ederek adımları oluştur
            i = 0
            while i < len(input_text):
                if i + 3 < len(input_text) and input_text[i:i + 4].isdigit():
                    coord = input_text[i:i + 4]

                    shifted_letter = self.cipher.get_letter_from_coordinates(coord)
                    if shifted_letter:
                        shifted_letters.append(shifted_letter)

                        # En olası orijinal harfi bul
                        candidate_list = []
                        for candidate in self.cipher.turkce_alfabe:
                            for katman in range(1, 4):
                                if katman == 1:
                                    element_info = self.cipher.katman1_elementler.get(candidate)
                                elif katman == 2:
                                    element_info = self.cipher.katman2_elementler.get(candidate)
                                else:
                                    element_info = self.cipher.katman3_elementler.get(candidate)

                                if not element_info:
                                    continue

                                shift = self.cipher.orbital_to_shift(element_info['orbital'],
                                                                     element_info['son_katman'])
                                if self.cipher.shift_letter(candidate, shift) == shifted_letter:
                                    candidate_list.append(candidate)

                        if candidate_list:
                            original_letter = candidate_list[0]
                            original_letters.append(original_letter)
                            results.append(original_letter)
                        else:
                            original_letters.append(shifted_letter)
                            results.append(shifted_letter)
                    else:
                        shifted_letters.append("?")
                        original_letters.append("?")
                        results.append(coord)

                    coordinates.append(coord)
                    i += 4
                else:
                    results.append(input_text[i])
                    i += 1

            # Animasyon adımlarını ekle
            self.encryption_animator.add_decryption_steps(
                input_text, coordinates, shifted_letters, original_letters, results
            )
        except Exception as e:
            print(f"Deşifreleme animasyonu gösterilirken hata: {e}")
            messagebox.showerror("Hata", f"Animasyon oluşturulurken bir hata oluştu: {e}")

    def run(self):
        """
        Uygulamayı başlatır
        """
        self.root.mainloop()
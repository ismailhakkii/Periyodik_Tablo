#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - Element Görselleştirme Modülü
"""

import tkinter as tk
from tkinter import Canvas, PhotoImage
import math


class ElementVisualizer:
    """
    Element görselleştirme ve animasyonlu bilgi gösterimi için sınıf
    """

    def __init__(self, root):
        """
        ElementVisualizer sınıfını başlatır

        Parameters:
        -----------
        root : tk.Tk veya tk.Toplevel
            Ana pencere
        """
        self.root = root
        self.popup_window = None
        self.electron_canvas = None
        self.electrons = []
        self.animation_speed = 0.05
        self.is_running = False

        # Renk paleti
        self.color_scheme = {
            'Alkali Metal': '#ff6666',
            'Toprak Alkali Metal': '#ffdead',
            'Geçiş Metali': '#ffc0c0',
            'Reaktif Ametal': '#c0ffff',
            'Yarı Metal': '#cccc99',
            'Ametal': '#a1ffc3',
            'Soy Gaz': '#c0ffff',
            'Lantanit': '#ffbfff',
            'Aktinit': '#ff99cc',
            'Bilinmeyen': '#e8e8e8'
        }

    def show_element_details(self, element_data):
        """
        Element detaylarını animasyonlu pencerede gösterir

        Parameters:
        -----------
        element_data : dict
            Element bilgilerini içeren sözlük
        """
        # Eğer önceki popup açıksa kapat
        if self.popup_window and self.popup_window.winfo_exists():
            self.popup_window.destroy()
            self.is_running = False

        # Yeni popup pencere oluştur
        self.popup_window = tk.Toplevel(self.root)
        self.popup_window.title(f"{element_data['ad']} Detayları")
        self.popup_window.geometry("600x450")
        self.popup_window.resizable(False, False)
        self.popup_window.transient(self.root)
        self.popup_window.focus_set()

        # Pencere kapatıldığında animasyonu durdur
        self.popup_window.protocol("WM_DELETE_WINDOW", self._on_close)

        # Arkaplan rengini kategori rengine göre ayarla
        kategori = element_data.get('kategori', 'Bilinmeyen')
        bg_color = self.color_scheme.get(kategori, self.color_scheme['Bilinmeyen'])

        # Ana çerçeve
        main_frame = tk.Frame(self.popup_window, bg=bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sol panel - Element sembolü ve temel bilgiler
        left_panel = tk.Frame(main_frame, bg=bg_color, width=200, height=430)
        left_panel.pack(side="left", fill="both", padx=10, pady=10)
        left_panel.pack_propagate(False)  # Boyutu sabit tut

        # Element sembolü, büyük boyutlu
        symbol_label = tk.Label(left_panel, text=element_data['sembol'],
                                font=("Arial", 72, "bold"), bg=bg_color)
        symbol_label.pack(pady=(40, 10))

        # Atom numarası
        atomic_num_label = tk.Label(left_panel, text=f"Atom Numarası: {element_data['atom_numarasi']}",
                                    font=("Arial", 12), bg=bg_color)
        atomic_num_label.pack(pady=5, anchor="w")

        # Atom ağırlığı
        atomic_weight_label = tk.Label(left_panel, text=f"Atom Ağırlığı: {element_data['atom_agirligi']}",
                                       font=("Arial", 12), bg=bg_color)
        atomic_weight_label.pack(pady=5, anchor="w")

        # Kategori
        category_label = tk.Label(left_panel, text=f"Kategori: {kategori}",
                                  font=("Arial", 12), bg=bg_color)
        category_label.pack(pady=5, anchor="w")

        # Sağ panel - Atom modeli ve bilgiler
        right_panel = tk.Frame(main_frame, bg="white", width=350, height=430)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Bilgi etiketi başlığı
        info_title = tk.Label(right_panel, text=f"{element_data['ad']} Kullanım Alanları",
                              font=("Arial", 14, "bold"), bg="white")
        info_title.pack(pady=(10, 5))

        # Bilgi içeriği
        info_text = tk.Text(right_panel, height=8, width=40, font=("Arial", 10),
                            wrap="word", bd=0, bg="white")
        info_text.insert("1.0", element_data['bilgi'])
        info_text.config(state="disabled")  # Salt okunur yap
        info_text.pack(pady=5, padx=10, fill="x")

        # Bohr atom modeli animasyonu için canvas
        self.electron_canvas = Canvas(right_panel, width=300, height=200,
                                      bg="white", highlightthickness=0)
        self.electron_canvas.pack(pady=10)

        # Atom modeli oluştur
        self._create_atom_model(element_data['atom_numarasi'])

        # Animasyonu başlat
        self.is_running = True
        self._animate_electrons()

    def _create_atom_model(self, atom_number):
        """
        Bohr atom modeli oluşturur

        Parameters:
        -----------
        atom_number : int
            Atomun numarası (proton/elektron sayısı)
        """
        # Elektronları sıfırla
        self.electrons = []

        # Canvas merkezini bul
        center_x = 150
        center_y = 100

        # Çekirdek
        nucleus_size = 20
        self.electron_canvas.create_oval(
            center_x - nucleus_size / 2, center_y - nucleus_size / 2,
            center_x + nucleus_size / 2, center_y + nucleus_size / 2,
            fill="#ff4444", outline="#cc0000", width=2, tags="nucleus"
        )

        # Elektron katmanları hesaplaması (basitleştirilmiş)
        # Gerçek fiziksel model yerine görsel çekiciliği artırmak için uyarlanmıştır
        shells = [2, 8, 8, 18, 18, 32]  # Kabuk kapasiteleri

        electrons_left = atom_number
        current_shell = 0

        while electrons_left > 0 and current_shell < len(shells):
            # Bu kabuktaki elektron sayısı
            electrons_in_shell = min(electrons_left, shells[current_shell])
            electrons_left -= electrons_in_shell

            # Kabuk yarıçapı
            radius = 30 + current_shell * 25

            # Kabuğu çiz
            self.electron_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline="#aaaaaa", dash=(2, 4), tags=f"shell{current_shell}"
            )

            # Elektronları yerleştir
            for i in range(electrons_in_shell):
                # Elektronun başlangıç açısı
                angle = (i / electrons_in_shell) * 2 * math.pi

                # Elektron konumlarını hesapla (başlangıç pozisyonu)
                electron_x = center_x + radius * math.cos(angle)
                electron_y = center_y + radius * math.sin(angle)

                # Elektron objesini oluştur ve listede sakla
                electron_id = self.electron_canvas.create_oval(
                    electron_x - 4, electron_y - 4,
                    electron_x + 4, electron_y + 4,
                    fill="#3366ff", outline="#0033cc", tags=f"electron{current_shell}_{i}"
                )

                # Elektron bilgilerini kaydet
                self.electrons.append({
                    'id': electron_id,
                    'shell': current_shell,
                    'radius': radius,
                    'angle': angle,
                    'speed': 0.02 - current_shell * 0.003  # Dış katmanlar daha yavaş
                })

            current_shell += 1

    def _animate_electrons(self):
        """
        Elektronların yörünge hareketini animasyonla gösterir
        """
        if not self.is_running or not self.electron_canvas:
            return

        center_x = 150
        center_y = 100

        # Tüm elektronları güncelle
        for electron in self.electrons:
            # Yeni açı hesapla
            electron['angle'] += electron['speed']
            if electron['angle'] > 2 * math.pi:
                electron['angle'] -= 2 * math.pi

            # Yeni konumu hesapla
            new_x = center_x + electron['radius'] * math.cos(electron['angle'])
            new_y = center_y + electron['radius'] * math.sin(electron['angle'])

            # Elektronun konumunu güncelle
            self.electron_canvas.coords(
                electron['id'],
                new_x - 4, new_y - 4,
                new_x + 4, new_y + 4
            )

        # Sonraki animasyon karesi
        if self.electron_canvas and self.is_running:
            self.electron_canvas.after(50, self._animate_electrons)

    def _on_close(self):
        """
        Popup pencere kapatıldığında çağrılır
        """
        self.is_running = False
        if self.popup_window:
            self.popup_window.destroy()
            self.popup_window = None

    def create_element_card(self, parent, element_data, width=120, height=120):
        """
        Element kartı widget'ı oluşturur

        Parameters:
        -----------
        parent : tk.Widget
            Kartın yerleştirileceği widget
        element_data : dict
            Element bilgilerini içeren sözlük
        width, height : int
            Kartın boyutları

        Returns:
        --------
        frame : tk.Frame
            Oluşturulan element kartı çerçevesi
        """
        # Arkaplan rengini kategori rengine göre ayarla
        kategori = element_data.get('kategori', 'Bilinmeyen')
        bg_color = self.color_scheme.get(kategori, self.color_scheme['Bilinmeyen'])

        # Kart çerçevesi
        frame = tk.Frame(parent, width=width, height=height, bg=bg_color,
                         highlightbackground="#999999", highlightthickness=1)
        frame.pack_propagate(False)  # Boyutu sabit tut

        # Atom numarası
        atom_num = tk.Label(frame, text=str(element_data['atom_numarasi']),
                            font=("Arial", 8), bg=bg_color, fg="#333333")
        atom_num.pack(anchor="nw", padx=5, pady=(5, 0))

        # Element sembolü
        symbol = tk.Label(frame, text=element_data['sembol'],
                          font=("Arial", 24, "bold"), bg=bg_color)
        symbol.pack(pady=(5, 0))

        # Element adı
        name = tk.Label(frame, text=element_data['ad'],
                        font=("Arial", 10), bg=bg_color)
        name.pack(pady=(0, 5))

        # Atom ağırlığı
        weight = tk.Label(frame, text=str(element_data['atom_agirligi']),
                          font=("Arial", 8), bg=bg_color, fg="#333333")
        weight.pack(pady=(0, 5))

        # Tıklama olayları
        frame.bind("<Button-1>", lambda e: self.show_element_details(element_data))
        for widget in [atom_num, symbol, name, weight]:
            widget.bind("<Button-1>", lambda e: self.show_element_details(element_data))

        return frame

    def create_orbital_diagram(self, canvas, orbital_notation, x, y, width=300):
        """
        Orbital diyagramı oluşturur

        Parameters:
        -----------
        canvas : tk.Canvas
            Diyagramın çizileceği canvas
        orbital_notation : str
            Orbital gösterimi (örn: "1s2 2s2 2p4")
        x, y : int
            Diyagramın sol üst köşe koordinatları
        width : int
            Diyagram genişliği
        """
        # Orbital listesini ayır
        orbitals = orbital_notation.split()

        # Satır yüksekliği
        row_height = 30

        # Orbital renkleri
        orbital_colors = {
            's': "#ff6666",  # Kırmızı
            'p': "#66ff66",  # Yeşil
            'd': "#6666ff",  # Mavi
            'f': "#ffcc66"  # Turuncu
        }

        # Her bir orbital grubunu çiz
        for i, orbital in enumerate(orbitals):
            # Orbital tipini ve elektron sayısını ayır
            parts = []
            current_part = ""

            for char in orbital:
                if char.isdigit() and current_part and not current_part[-1].isdigit():
                    parts.append(current_part)
                    current_part = char
                else:
                    current_part += char

            if current_part:
                parts.append(current_part)

            if len(parts) < 2:
                continue

            shell_level = parts[0][:-1]  # "1s2" -> "1"
            orbital_type = parts[0][-1]  # "1s2" -> "s"
            electrons = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0

            # Orbital kutusunun konumu
            box_x = x + i * 60
            box_y = y

            # Arka plan rengi
            bg_color = orbital_colors.get(orbital_type, "#cccccc")

            # Orbital kutusu çiz
            canvas.create_rectangle(
                box_x, box_y,
                box_x + 50, box_y + row_height,
                fill=bg_color, outline="#333333"
            )

            # Orbital adı
            canvas.create_text(
                box_x + 25, box_y + 15,
                text=f"{shell_level}{orbital_type}",
                font=("Arial", 10, "bold")
            )

            # Elektron sayısını göster
            canvas.create_text(
                box_x + 40, box_y + 7,
                text=str(electrons),
                font=("Arial", 8)
            )
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - Şifreleme Animasyonu Modülü
"""

import tkinter as tk
from tkinter import Canvas, Button
import time
import math

import a5


class EncryptionAnimator:
    """
    Şifreleme sürecini animasyonla görselleştiren sınıf
    """

    def __init__(self, root):
        """
        EncryptionAnimator sınıfını başlatır

        Parameters:
        -----------
        root : tk.Tk veya tk.Toplevel
            Ana pencere
        """
        self.root = root
        self.animation_window = None
        self.canvas = None
        self.is_playing = False
        self.steps = []
        self.current_step = 0
        self.animation_speed = 1.0  # Hız faktörü

        # Renk paleti
        self.colors = {
            'background': '#f0f0f0',
            'letter': '#3333cc',
            'element': '#cc3333',
            'orbital': '#339933',
            'shift': '#993399',
            'result': '#cc6600',
            'arrow': '#666666',
            'text': '#000000'
        }

    def create_animation_window(self, title="Şifreleme Animasyonu"):
        """
        Animasyon penceresi oluşturur

        Parameters:
        -----------
        title : str
            Pencere başlığı
        """
        # Eğer önceki animasyon penceresi açıksa kapat
        if self.animation_window and self.animation_window.winfo_exists():
            self.animation_window.destroy()

        # Yeni pencere oluştur
        self.animation_window = tk.Toplevel(self.root)
        self.animation_window.title(title)
        self.animation_window.geometry("800x600")
        self.animation_window.protocol("WM_DELETE_WINDOW", self.close_animation)

        # Üst kontrol paneli
        control_panel = tk.Frame(self.animation_window, height=50)
        control_panel.pack(fill="x", padx=10, pady=5)

        # Oynat/Duraklat düğmesi
        self.play_button = Button(control_panel, text="▶ Oynat", width=10,
                                  command=self.toggle_play)
        self.play_button.pack(side="left", padx=5)

        # Sonraki adım düğmesi
        next_button = Button(control_panel, text="İleri ▶", width=10,
                             command=self.next_step)
        next_button.pack(side="left", padx=5)

        # Önceki adım düğmesi
        prev_button = Button(control_panel, text="◀ Geri", width=10,
                             command=self.prev_step)
        prev_button.pack(side="left", padx=5)

        # Başa dön düğmesi
        restart_button = Button(control_panel, text="⟲ Başa Dön", width=10,
                                command=self.restart_animation)
        restart_button.pack(side="left", padx=5)

        # Animasyon hızı
        speed_label = tk.Label(control_panel, text="Hız:")
        speed_label.pack(side="left", padx=(20, 5))

        speed_slider = tk.Scale(control_panel, from_=0.5, to=3.0, resolution=0.5,
                                orient="horizontal", length=100, command=self.set_speed)
        speed_slider.set(1.0)
        speed_slider.pack(side="left")

        # Adım bilgisi
        self.step_info = tk.Label(control_panel, text="Adım: 0/0")
        self.step_info.pack(side="right", padx=10)

        # Ana canvas
        self.canvas = Canvas(self.animation_window, bg=self.colors['background'],
                             width=800, height=550)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # İlerleme çubuğu
        self.progress_frame = tk.Frame(self.animation_window, height=20)
        self.progress_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.progress_canvas = Canvas(self.progress_frame, height=10, bg="#dddddd",
                                      highlightthickness=0)
        self.progress_canvas.pack(fill="x")

        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 10,
                                                                  fill="#4488dd", outline="")

        # Animasyon adımları listesi
        self.steps = []

    def add_encryption_steps(self, input_text, letter_counts, element_infos, shifts,
                             shifted_letters, results):
        """
        Şifreleme adımlarını animasyon için ekler

        Parameters:
        -----------
        input_text : str
            Giriş metni
        letter_counts : dict
            Harf kullanım sayıları
        element_infos : list
            Her adım için element bilgileri
        shifts : list
            Her adım için öteleme değerleri
        shifted_letters : list
            Her adım için ötelenmiş harfler
        results : list
            Her adım için şifreleme sonuçları
        """
        self.steps = []
        self.current_step = 0

        # Başlangıç adımı
        self.steps.append({
            'type': 'start',
            'text': input_text,
            'message': f"Şifrelenecek metin: {input_text}"
        })

        # Her bir karakter için şifreleme adımları
        for i, char in enumerate(input_text):
            if char not in letter_counts:
                self.steps.append({
                    'type': 'skip',
                    'char': char,
                    'position': i,
                    'message': f"'{char}' harfi şifrelenmeden geçildi"
                })
                continue

            # Harf-Element eşleşmesi adımı
            self.steps.append({
                'type': 'letter_to_element',
                'char': char,
                'position': i,
                'count': letter_counts[char],
                'element': element_infos[i]['element'],
                'message': f"'{char}' harfi için {letter_counts[char]}. kullanımda '{element_infos[i]['element']}' elementi seçildi"
            })

            # Orbital dizilimi adımı
            self.steps.append({
                'type': 'orbital',
                'char': char,
                'position': i,
                'element': element_infos[i]['element'],
                'orbital': element_infos[i]['orbital'],
                'message': f"'{element_infos[i]['element']}' elementinin orbital dizilimi: {element_infos[i]['orbital']}"
            })

            # Öteleme adımı
            self.steps.append({
                'type': 'shift',
                'char': char,
                'position': i,
                'shift': shifts[i],
                'message': f"Hesaplanan öteleme değeri: {shifts[i]}"
            })

            # Harf öteleme adımı
            self.steps.append({
                'type': 'letter_shift',
                'char': char,
                'position': i,
                'shifted': shifted_letters[i],
                'message': f"'{char}' harfi {shifts[i]} birim ötelenerek '{shifted_letters[i]}' harfine dönüştürüldü"
            })

            # Koordinat dönüşüm adımı
            self.steps.append({
                'type': 'to_coordinate',
                'char': shifted_letters[i],
                'position': i,
                'result': results[i],
                'message': f"'{shifted_letters[i]}' harfi '{results[i]}' koordinatına dönüştürüldü"
            })

        # Son adım - şifrelenmiş metin
        final_result = ''.join(results)
        self.steps.append({
            'type': 'finish',
            'result': final_result,
            'message': f"Şifreleme tamamlandı. Sonuç: {final_result}"
        })

        # İlk adımı göster
        if self.steps:
            self.show_step(0)
            self.update_progress()

    def add_decryption_steps(self, input_text, coordinates, shifted_letters,
                             original_letters, results):
        """
        Deşifreleme adımlarını animasyon için ekler

        Parameters:
        -----------
        input_text : str
            Şifreli giriş metni
        coordinates : list
            Her adım için koordinatlar
        shifted_letters : list
            Her adım için ötelenmiş harfler
        original_letters : list
            Her adım için orijinal harfler
        results : list
            Her adım için deşifreleme sonuçları
        """
        self.steps = []
        self.current_step = 0

        # Başlangıç adımı
        self.steps.append({
            'type': 'start_decrypt',
            'text': input_text,
            'message': f"Deşifrelenecek metin: {input_text}"
        })

        # Her bir koordinat/karakter için deşifreleme adımları
        i = 0
        while i < len(input_text):
            if i + 3 < len(input_text) and input_text[i:i + 4].isdigit():
                coord = input_text[i:i + 4]

                # Koordinat-Harf dönüşümü adımı
                self.steps.append({
                    'type': 'coordinate_to_letter',
                    'coordinate': coord,
                    'position': i,
                    'shifted': shifted_letters[len(coordinates)],
                    'message': f"'{coord}' koordinatı '{shifted_letters[len(coordinates)]}' harfine karşılık geliyor"
                })

                # Orijinal harfi bulma adımı
                self.steps.append({
                    'type': 'find_original',
                    'shifted': shifted_letters[len(coordinates)],
                    'position': i,
                    'original': original_letters[len(coordinates)],
                    'message': f"'{shifted_letters[len(coordinates)]}' harfinden geriye ötelemeyle '{original_letters[len(coordinates)]}' harfi bulundu"
                })

                coordinates.append(coord)
                i += 4
            else:
                # Şifrelenmeyen karakteri geçme adımı
                self.steps.append({
                    'type': 'skip_decrypt',
                    'char': input_text[i],
                    'position': i,
                    'message': f"'{input_text[i]}' karakteri koordinat olmadığından aynen bırakıldı"
                })
                i += 1

        # Son adım - deşifrelenmiş metin
        final_result = ''.join(results)
        self.steps.append({
            'type': 'finish_decrypt',
            'result': final_result,
            'message': f"Deşifreleme tamamlandı. Sonuç: {final_result}"
        })

        # İlk adımı göster
        if self.steps:
            self.show_step(0)
            self.update_progress()

    def show_step(self, step_index):
        """
        Belirli bir adımı gösterir

        Parameters:
        -----------
        step_index : int
            Gösterilecek adımın indeksi
        """
        if not self.steps or step_index < 0 or step_index >= len(self.steps):
            return

        # Canvas'ı temizle
        self.canvas.delete("all")

        # Adım bilgisini güncelle
        self.current_step = step_index
        self.step_info.config(text=f"Adım: {step_index + 1}/{len(self.steps)}")

        # İlgili adımı göster
        step = self.steps[step_index]

        # Adım mesajını göster
        self.canvas.create_text(
            400, 30,
            text=step['message'],
            font=("Arial", 12),
            fill=self.colors['text'],
            width=700
        )

        # Adım tipine göre gösterim
        if step['type'] == 'start':
            self._draw_start_step(step)
        elif step['type'] == 'skip':
            self._draw_skip_step(step)
        elif step['type'] == 'letter_to_element':
            self._draw_letter_to_element_step(step)
        elif step['type'] == 'orbital':
            self._draw_orbital_step(step)
        elif step['type'] == 'shift':
            self._draw_shift_step(step)
        elif step['type'] == 'letter_shift':
            self._draw_letter_shift_step(step)
        elif step['type'] == 'to_coordinate':
            self._draw_to_coordinate_step(step)
        elif step['type'] == 'finish':
            self._draw_finish_step(step)
        elif step['type'] == 'start_decrypt':
            self._draw_start_decrypt_step(step)
        elif step['type'] == 'coordinate_to_letter':
            self._draw_coordinate_to_letter_step(step)
        elif step['type'] == 'find_original':
            self._draw_find_original_step(step)
        elif step['type'] == 'skip_decrypt':
            self._draw_skip_decrypt_step(step)
        elif step['type'] == 'finish_decrypt':
            self._draw_finish_decrypt_step(step)

        # İlerleme çubuğunu güncelle
        self.update_progress()

    def _draw_start_step(self, step):
        """
        Başlangıç adımını çizer
        """
        # Metin kutusu
        self.canvas.create_rectangle(
            150, 100, 650, 200,
            fill="white", outline="#999999"
        )

        # Metin
        self.canvas.create_text(
            400, 150,
            text=step['text'],
            font=("Arial", 18, "bold"),
            fill=self.colors['letter']
        )

        # Başlık
        self.canvas.create_text(
            400, 80,
            text="Şifrelenecek Metin",
            font=("Arial", 14),
            fill=self.colors['text']
        )

        # Bilgi metni
        self.canvas.create_text(
            400, 250,
            text="Şifreleme işlemi başlıyor. İleri düğmesine basarak adımları izleyebilirsiniz.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_skip_step(self, step):
        """
        Atlama adımını çizer
        """
        # Karakteri göster
        self.canvas.create_text(
            400, 150,
            text=step['char'],
            font=("Arial", 72, "bold"),
            fill="#999999"
        )

        # Çarpı işareti
        self.canvas.create_text(
            400, 150,
            text="✕",
            font=("Arial", 100),
            fill="#cc0000"
        )

        # Açıklama
        self.canvas.create_text(
            400, 250,
            text=f"Bu karakter Türkçe alfabede yer almadığı için şifrelenmeden geçildi.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_letter_to_element_step(self, step):
        """
        Harf-Element eşleşmesi adımını çizer
        """
        # Sol tarafta harf
        self.canvas.create_text(
            250, 150,
            text=step['char'],
            font=("Arial", 72, "bold"),
            fill=self.colors['letter']
        )

        # Ok
        self.canvas.create_line(
            300, 150, 400, 150,
            fill=self.colors['arrow'],
            width=3,
            arrow=tk.LAST
        )

        # Sağ tarafta element
        self.canvas.create_rectangle(
            430, 110, 490, 190,
            fill="#ffffcc", outline="#333333"
        )

        self.canvas.create_text(
            460, 150,
            text=step['element'],
            font=("Arial", 28, "bold"),
            fill=self.colors['element']
        )

        # Kullanım sayısını göster
        self.canvas.create_text(
            250, 210,
            text=f"{step['count']}. kullanım",
            font=("Arial", 12),
            fill=self.colors['text']
        )

        # Açıklama
        self.canvas.create_text(
            400, 250,
            text=f"Bu harf {step['count']}. kez kullanıldığı için {step['count'] % 3 + 1}. katmandaki element seçildi.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_orbital_step(self, step):
        """
        Orbital dizilimi adımını çizer
        """
        # Elementi göster
        self.canvas.create_rectangle(
            370, 110, 430, 190,
            fill="#ffffcc", outline="#333333"
        )

        self.canvas.create_text(
            400, 150,
            text=step['element'],
            font=("Arial", 28, "bold"),
            fill=self.colors['element']
        )

        # Orbital dizilimini göster
        self.canvas.create_rectangle(
            250, 220, 550, 280,
            fill="#eeffee", outline="#333333"
        )

        self.canvas.create_text(
            400, 250,
            text=step['orbital'],
            font=("Arial", 16, "bold"),
            fill=self.colors['orbital']
        )

        # Başlık
        self.canvas.create_text(
            400, 80,
            text="Element Orbital Dizilimi",
            font=("Arial", 14),
            fill=self.colors['text']
        )

        # Orbital açıklaması
        orbitals = step['orbital'].split()
        explanation = "Orbital dizilimi: "

        for orbital in orbitals:
            # Orbital adı (örn: 3d) ve elektron sayısı (örn: 5) ayır
            if len(orbital) >= 2:
                name = orbital[:-1]
                count = orbital[-1]
                explanation += f"{name} kabuğunda {count} elektron, "

        explanation = explanation.rstrip(", ")

        self.canvas.create_text(
            400, 320,
            text=explanation,
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_shift_step(self, step):
        """
        Öteleme adımını çizer
        """
        # Hesaplama gösterimi
        orbital_text = self.steps[self.current_step - 1]['orbital']

        # Sayıları bulma
        numbers = []
        for char in orbital_text:
            if char.isdigit():
                numbers.append(int(char))

        sum_numbers = sum(numbers)
        son_katman = int(self.steps[self.current_step - 2]['count']) % 3 + 1

        # Öteleme formülü gösterimi
        self.canvas.create_text(
            400, 120,
            text=f"Öteleme = (Orbital Sayılarının Toplamı) × (Son Katman Elektron Sayısı)",
            font=("Arial", 12),
            fill=self.colors['text']
        )

        # Formül detayları
        self.canvas.create_text(
            400, 150,
            text=f"Öteleme = ({' + '.join(map(str, numbers))}) × {son_katman}",
            font=("Arial", 16),
            fill=self.colors['shift']
        )

        # Sonuç
        self.canvas.create_text(
            400, 190,
            text=f"Öteleme = {sum_numbers} × {son_katman} = {step['shift']}",
            font=("Arial", 22, "bold"),
            fill=self.colors['shift']
        )

        # Açıklama
        self.canvas.create_text(
            400, 250,
            text=f"Bu öteleme değeri kullanılarak harf Türkçe alfabede {step['shift']} adım ilerletilecek.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

        # Türkçe alfabe gösterimi
        alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

        # Alfabe kutuları
        box_width = 25
        start_x = 400 - (len(alphabet) * box_width) / 2

        for i, letter in enumerate(alphabet):
            x = start_x + i * box_width

            self.canvas.create_rectangle(
                x, 300, x + box_width, 330,
                fill="#f0f0f0", outline="#cccccc"
            )

            self.canvas.create_text(
                x + box_width / 2, 315,
                text=letter,
                font=("Arial", 10)
            )

    def _draw_letter_shift_step(self, step):
        """
        Harf öteleme adımını çizer
        """
        # Alfabe gösterimi
        alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

        # Başlangıç harfinin indeksi
        start_index = alphabet.find(step['char'])
        if start_index == -1:
            start_index = 0

        # Bitiş harfinin indeksi
        end_index = alphabet.find(step['shifted'])
        if end_index == -1:
            end_index = 0

        # Alfabe kutuları
        box_width = 25
        start_x = 400 - (len(alphabet) * box_width) / 2

        for i, letter in enumerate(alphabet):
            x = start_x + i * box_width

            # Kutu rengi
            if letter == step['char']:
                fill_color = self.colors['letter']
            elif letter == step['shifted']:
                fill_color = self.colors['result']
            else:
                fill_color = "#f0f0f0"

            self.canvas.create_rectangle(
                x, 200, x + box_width, 230,
                fill=fill_color, outline="#cccccc"
            )

            self.canvas.create_text(
                x + box_width / 2, 215,
                text=letter,
                font=("Arial", 10),
                fill="white" if fill_color != "#f0f0f0" else "black"
            )

        # Ok gösterimi
        arrow_start_x = start_x + start_index * box_width + box_width / 2
        arrow_end_x = start_x + end_index * box_width + box_width / 2

        self.canvas.create_line(
            arrow_start_x, 240, arrow_end_x, 240,
            fill=self.colors['arrow'],
            width=2,
            arrow=tk.LAST
        )

        # Başlangıç ve hedef harfleri
        self.canvas.create_text(
            250, 150,
            text=step['char'],
            font=("Arial", 72, "bold"),
            fill=self.colors['letter']
        )

        self.canvas.create_text(
            350, 150,
            text="+",
            font=("Arial", 36),
            fill=self.colors['text']
        )

        self.canvas.create_text(
            400, 150,
            text=str(self.steps[self.current_step - 1]['shift']),
            font=("Arial", 36, "bold"),
            fill=self.colors['shift']
        )

        self.canvas.create_text(
            450, 150,
            text="→",
            font=("Arial", 36),
            fill=self.colors['arrow']
        )

        self.canvas.create_text(
            550, 150,
            text=step['shifted'],
            font=("Arial", 72, "bold"),
            fill=self.colors['result']
        )

        # Açıklama
        self.canvas.create_text(
            400, 300,
            text=f"'{step['char']}' harfi {self.steps[self.current_step - 1]['shift']} birim ötelenerek '{step['shifted']}' harfine dönüştürüldü.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_to_coordinate_step(self, step):
        """
        Harf-Koordinat dönüşüm adımını çizer
        """
        # Periyodik tablo gösterimi (basitleştirilmiş)
        table_start_x = 250
        table_start_y = 240
        cell_size = 30

        # Tablo arka planı
        self.canvas.create_rectangle(
            table_start_x, table_start_y,
            table_start_x + 9 * cell_size, table_start_y + a5 * cell_size,
            fill="#f8f8f8", outline="#666666"
        )

        # Tablo ızgarası
        for i in range(9):
            # Dikey çizgiler
            self.canvas.create_line(
                table_start_x + i * cell_size, table_start_y,
                table_start_x + i * cell_size, table_start_y + 5 * cell_size,
                fill="#cccccc"
            )

        for i in range(6):
            # Yatay çizgiler
            self.canvas.create_line(
                table_start_x, table_start_y + i * cell_size,
                               table_start_x + 9 * cell_size, table_start_y + i * cell_size,
                fill="#cccccc"
            )

        # Hedef hücreyi işaretle (burada basit bir örnek)
        target_row = int(step['result'][0:2])
        target_col = int(step['result'][2:4])

        if 1 <= target_row <= 5 and 1 <= target_col <= 9:
            cell_x = table_start_x + (target_col - 1) * cell_size
            cell_y = table_start_y + (target_row - 1) * cell_size

            self.canvas.create_rectangle(
                cell_x, cell_y,
                cell_x + cell_size, cell_y + cell_size,
                fill=self.colors['result'], outline="#333333"
            )

            self.canvas.create_text(
                cell_x + cell_size / 2, cell_y + cell_size / 2,
                text=step['char'],
                font=("Arial", 12, "bold"),
                fill="white"
            )

        # Harf ve koordinat bağlantısı
        self.canvas.create_text(
            400, 120,
            text=f"'{step['char']}' harfi periyodik tablo koordinatına dönüştürülüyor",
            font=("Arial", 14),
            fill=self.colors['text']
        )

        self.canvas.create_text(
            250, 170,
            text=step['char'],
            font=("Arial", 48, "bold"),
            fill=self.colors['letter']
        )

        self.canvas.create_text(
            350, 170,
            text="→",
            font=("Arial", 36),
            fill=self.colors['arrow']
        )

        self.canvas.create_text(
            450, 170,
            text=f"({target_row},{target_col})",
            font=("Arial", 24, "bold"),
            fill=self.colors['text']
        )

        self.canvas.create_text(
            550, 170,
            text="→",
            font=("Arial", 36),
            fill=self.colors['arrow']
        )

        self.canvas.create_text(
            600, 170,
            text=step['result'],
            font=("Arial", 36, "bold"),
            fill=self.colors['result']
        )

        # Açıklama
        self.canvas.create_text(
            400, 400,
            text=f"Ötelenmiş harf '{step['char']}' için periyodik tablodaki konumu ({target_row},{target_col}) alınarak '{step['result']}' koordinatı elde edildi.",
            font=("Arial", 12),
            fill=self.colors['text'],
            width=600
        )

    def _draw_finish_step(self, step):
        """
        Bitiş adımını çizer
        """
        # Sonuç kutusu
        self.canvas.create_rectangle(
            150, 150, 650, 250,
            fill="#eeffee", outline="#009900", width=2
        )

        # Sonuç metni
        self.canvas.create_text(
            400, 200,
            text=step['result'],
            font=("Arial", 18, "bold"),
            fill=self.colors['result']
        )

        # Başlık
        self.canvas.create_text(
            400, 120,
            text="Şifreleme İşlemi Tamamlandı",
            font=("Arial", 16, "bold"),
            fill="#009900"
        )

        # Açıklama
        self.canvas.create_text(
            400, 300,
            text="Metin başarıyla şifrelendi. Sonucu kopyalayabilir veya başa dönerek adımları tekrar izleyebilirsiniz.",
            font=("Arial", 12),
            fill=self.colors['text'],
            width=600
        )

        # Kutlama efekti (basit)
        for i in range(20):
            x = 150 + i * 25
            y = 350 + (i % 3) * 20

            self.canvas.create_text(
                x, y,
                text="✓",
                font=("Arial", 18),
                fill="#33cc33"
            )

    def _draw_start_decrypt_step(self, step):
        """
        Deşifreleme başlangıç adımını çizer
        """
        # Metin kutusu
        self.canvas.create_rectangle(
            150, 100, 650, 200,
            fill="white", outline="#999999"
        )

        # Metin
        self.canvas.create_text(
            400, 150,
            text=step['text'],
            font=("Arial", 18, "bold"),
            fill=self.colors['result']
        )

        # Başlık
        self.canvas.create_text(
            400, 80,
            text="Deşifrelenecek Metin",
            font=("Arial", 14),
            fill=self.colors['text']
        )

        # Bilgi metni
        self.canvas.create_text(
            400, 250,
            text="Deşifreleme işlemi başlıyor. İleri düğmesine basarak adımları izleyebilirsiniz.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_coordinate_to_letter_step(self, step):
        """
        Koordinat-Harf dönüşüm adımını çizer
        """
        # Koordinat gösterimi
        self.canvas.create_text(
            250, 150,
            text=step['coordinate'],
            font=("Arial", 36, "bold"),
            fill=self.colors['result']
        )

        # Ok
        self.canvas.create_text(
            350, 150,
            text="→",
            font=("Arial", 36),
            fill=self.colors['arrow']
        )

        # Periyodik tablo gösterimi
        table_start_x = 250
        table_start_y = 240
        cell_size = 30

        # Tablo arka planı
        self.canvas.create_rectangle(
            table_start_x, table_start_y,
            table_start_x + 9 * cell_size, table_start_y + 5 * cell_size,
            fill="#f8f8f8", outline="#666666"
        )

        # Koordinattaki hücreyi işaretle
        target_row = int(step['coordinate'][0:2])
        target_col = int(step['coordinate'][2:4])

        if 1 <= target_row <= 5 and 1 <= target_col <= 9:
            cell_x = table_start_x + (target_col - 1) * cell_size
            cell_y = table_start_y + (target_row - 1) * cell_size

            self.canvas.create_rectangle(
                cell_x, cell_y,
                cell_x + cell_size, cell_y + cell_size,
                fill=self.colors['result'], outline="#333333"
            )

        # Sonuç harfi
        self.canvas.create_text(
            450, 150,
            text=step['shifted'],
            font=("Arial", 48, "bold"),
            fill=self.colors['letter']
        )

        # Açıklama
        self.canvas.create_text(
            400, 400,
            text=f"Koordinat '{step['coordinate']}' periyodik tablodaki konumu kullanılarak '{step['shifted']}' harfine dönüştürüldü.",
            font=("Arial", 12),
            fill=self.colors['text'],
            width=600
        )

    def _draw_find_original_step(self, step):
        """
        Orijinal harfi bulma adımını çizer
        """
        # Alfabe gösterimi
        alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

        # Başlangıç harfinin indeksi
        shifted_index = alphabet.find(step['shifted'])
        if shifted_index == -1:
            shifted_index = 0

        # Bitiş harfinin indeksi
        original_index = alphabet.find(step['original'])
        if original_index == -1:
            original_index = 0

        # Alfabe kutuları
        box_width = 25
        start_x = 400 - (len(alphabet) * box_width) / 2

        for i, letter in enumerate(alphabet):
            x = start_x + i * box_width

            # Kutu rengi
            if letter == step['shifted']:
                fill_color = self.colors['letter']
            elif letter == step['original']:
                fill_color = self.colors['result']
            else:
                fill_color = "#f0f0f0"

            self.canvas.create_rectangle(
                x, 200, x + box_width, 230,
                fill=fill_color, outline="#cccccc"
            )

            self.canvas.create_text(
                x + box_width / 2, 215,
                text=letter,
                font=("Arial", 10),
                fill="white" if fill_color != "#f0f0f0" else "black"
            )

        # Ok gösterimi (geriye doğru)
        arrow_start_x = start_x + shifted_index * box_width + box_width / 2
        arrow_end_x = start_x + original_index * box_width + box_width / 2

        self.canvas.create_line(
            arrow_start_x, 240, arrow_end_x, 240,
            fill=self.colors['arrow'],
            width=2,
            arrow=tk.LAST
        )

        # Ötelenmiş ve orijinal harfler
        self.canvas.create_text(
            250, 150,
            text=step['shifted'],
            font=("Arial", 72, "bold"),
            fill=self.colors['letter']
        )

        self.canvas.create_text(
            350, 150,
            text="→",
            font=("Arial", 36),
            fill=self.colors['arrow']
        )

        self.canvas.create_text(
            450, 150,
            text=step['original'],
            font=("Arial", 72, "bold"),
            fill=self.colors['result']
        )

        # Açıklama
        self.canvas.create_text(
            400, 300,
            text=f"Ötelenmiş harf '{step['shifted']}' geriye ötelenerek orijinal harf '{step['original']}' bulundu.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_skip_decrypt_step(self, step):
        """
        Deşifrelemede atlanacak karakter adımını çizer
        """
        # Karakteri göster
        self.canvas.create_text(
            400, 150,
            text=step['char'],
            font=("Arial", 72, "bold"),
            fill="#999999"
        )

        # Ok işareti
        self.canvas.create_text(
            400, 230,
            text="↓",
            font=("Arial", 48),
            fill=self.colors['arrow']
        )

        # Açıklama
        self.canvas.create_text(
            400, 300,
            text=f"Bu karakter 4 haneli bir koordinat olmadığı için doğrudan aktarılıyor.",
            font=("Arial", 12),
            fill=self.colors['text']
        )

    def _draw_finish_decrypt_step(self, step):
        """
        Deşifreleme bitiş adımını çizer
        """
        # Sonuç kutusu
        self.canvas.create_rectangle(
            150, 150, 650, 250,
            fill="#eeffee", outline="#009900", width=2
        )

        # Sonuç metni
        self.canvas.create_text(
            400, 200,
            text=step['result'],
            font=("Arial", 18, "bold"),
            fill=self.colors['result']
        )

        # Başlık
        self.canvas.create_text(
            400, 120,
            text="Deşifreleme İşlemi Tamamlandı",
            font=("Arial", 16, "bold"),
            fill="#009900"
        )

        # Açıklama
        self.canvas.create_text(
            400, 300,
            text="Metin başarıyla deşifrelendi. Sonucu kopyalayabilir veya başa dönerek adımları tekrar izleyebilirsiniz.",
            font=("Arial", 12),
            fill=self.colors['text'],
            width=600
        )

    def update_progress(self):
        """
        İlerleme çubuğunu günceller
        """
        if not self.steps:
            return

        progress = (self.current_step + 1) / len(self.steps)
        width = self.progress_canvas.winfo_width()

        self.progress_canvas.coords(
            self.progress_bar,
            0, 0, width * progress, 10
        )

    def next_step(self):
        """
        Sonraki adıma geçer
        """
        if self.current_step < len(self.steps) - 1:
            self.show_step(self.current_step + 1)

    def prev_step(self):
        """
        Önceki adıma döner
        """
        if self.current_step > 0:
            self.show_step(self.current_step - 1)

    def toggle_play(self):
        """
        Oynatma/duraklat düğmesi işlevini gerçekleştirir
        """
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_button.config(text="⏸ Duraklat")
            self.play_animation()
        else:
            self.play_button.config(text="▶ Oynat")

    def play_animation(self):
        """
        Animasyonu otomatik oynatır
        """
        if not self.is_playing:
            return

        if self.current_step < len(self.steps) - 1:
            self.next_step()
            delay = int(1500 / self.animation_speed)  # Hıza göre gecikme
            self.animation_window.after(delay, self.play_animation)
        else:
            # Son adıma gelindiğinde oynatmayı durdur
            self.is_playing = False
            self.play_button.config(text="▶ Oynat")

    def restart_animation(self):
        """
        Animasyonu baştan başlatır
        """
        self.is_playing = False
        self.play_button.config(text="▶ Oynat")
        self.show_step(0)

    def set_speed(self, value):
        """
        Animasyon hızını ayarlar

        Parameters:
        -----------
        value : str
            Hız faktörü (0.5-3.0)
        """
        self.animation_speed = float(value)

    def close_animation(self):
        """
        Animasyon penceresini kapatır
        """
        self.is_playing = False
        if self.animation_window:
            self.animation_window.destroy()
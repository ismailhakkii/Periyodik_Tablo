#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - Animasyon Modülü
"""

import tkinter as tk
import time
from tkinter import Canvas
import random
import math


class AnimationEffects:
    """
    Animasyon ve görsel efektler için yardımcı sınıf
    """

    @staticmethod
    def flash_element(button, color='#ffcc00', duration=500):
        """
        Bir element düğmesini yanıp söndürme efekti

        Parameters:
        -----------
        button : tk.Button
            Yanıp söndürülecek düğme
        color : str
            Yanıp söndürme rengi (hex kodu)
        duration : int
            Efekt süresi (milisaniye)
        """
        original_bg = button.cget("background")
        button.config(background=color)
        button.update()

        # Orijinal renge geri dön
        button.after(duration, lambda: button.config(background=original_bg))

    @staticmethod
    def typewriter_effect(text_widget, text, delay=50):
        """
        Daktilo efekti ile metin yazma

        Parameters:
        -----------
        text_widget : tk.Text
            Metnin yazılacağı text widget
        text : str
            Yazılacak metin
        delay : int
            Karakterler arası gecikme (milisaniye)
        """
        text_widget.delete("1.0", "end")

        def add_char(index=0):
            if index < len(text):
                text_widget.insert("end", text[index])
                text_widget.see("end")
                text_widget.update()
                text_widget.after(delay, lambda: add_char(index + 1))

        add_char()

    @staticmethod
    def path_animation(canvas, start_x, start_y, end_x, end_y, duration=500, color='red', steps=20, width=2):
        """
        İki nokta arasında hareket eden animasyon

        Parameters:
        -----------
        canvas : tk.Canvas
            Animasyonun gösterileceği canvas
        start_x, start_y : int
            Başlangıç koordinatları
        end_x, end_y : int
            Bitiş koordinatları
        duration : int
            Animasyon süresi (milisaniye)
        color : str
            Çizgi rengi
        steps : int
            Animasyon adım sayısı
        width : int
            Çizgi kalınlığı
        """
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        step_delay = duration / steps

        def draw_step(step=0, last_line=None):
            if step < steps:
                if last_line:
                    canvas.delete(last_line)

                x = start_x + dx * step
                y = start_y + dy * step
                line = canvas.create_line(start_x, start_y, x, y, fill=color, width=width, arrow=tk.LAST)

                canvas.update()
                canvas.after(int(step_delay), lambda: draw_step(step + 1, line))
            else:
                # Son çizgiyi çiz ve bırak
                if last_line:
                    canvas.delete(last_line)
                final_line = canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=width, arrow=tk.LAST)

                # Bir süre sonra çizgiyi sil (opsiyonel)
                canvas.after(1000, lambda: canvas.delete(final_line))

        draw_step()

    @staticmethod
    def create_particle_effect(parent, x, y, particle_count=20, duration=1000, colors=None, size_range=(2, 5)):
        """
        Parçacık efekti oluşturur (örneğin bir elemente tıklandığında)

        Parameters:
        -----------
        parent : tk.Widget
            Efektin gösterileceği ana widget
        x, y : int
            Efektin başlangıç koordinatları
        particle_count : int
            Parçacık sayısı
        duration : int
            Efekt süresi (milisaniye)
        colors : list
            Parçacık renkleri listesi
        size_range : tuple
            Parçacık boyut aralığı (min, max)
        """
        if colors is None:
            colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']

        # Canvas oluştur
        canvas = Canvas(parent, highlightthickness=0)
        canvas.place(x=x - 50, y=y - 50, width=100, height=100)

        particles = []

        # Parçacıkları oluştur
        for _ in range(particle_count):
            # Rastgele yön ve hız
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed

            # Rastgele renk ve boyut
            color = random.choice(colors)
            size = random.uniform(size_range[0], size_range[1])

            # Parçacığı çiz
            particle = canvas.create_oval(50 - size, 50 - size, 50 + size, 50 + size, fill=color, outline="")

            particles.append({
                'id': particle,
                'dx': dx,
                'dy': dy,
                'life': random.uniform(0.7, 1.0)  # Yaşam süresi çarpanı
            })

        start_time = time.time()

        def update_particles():
            nonlocal particles

            current_time = time.time()
            elapsed = (current_time - start_time) * 1000  # ms cinsinden

            if elapsed > duration or not particles:
                canvas.destroy()
                return

            for particle in particles[:]:
                # Parçacığı güncelle
                canvas.move(particle['id'], particle['dx'], particle['dy'])

                # Zamanla saydamlaştır
                life_factor = 1.0 - (elapsed / duration / particle['life'])
                if life_factor <= 0:
                    canvas.delete(particle['id'])
                    particles.remove(particle)
                    continue

                # Hızı azalt
                particle['dx'] *= 0.95
                particle['dy'] *= 0.95

            canvas.after(20, update_particles)

        update_particles()

    @staticmethod
    def highlight_text(text_widget, start_index, end_index, tag_name="highlight",
                       bg_color="#ffff99", delay=500, duration=1000):
        """
        Metin içinde belirli bir kısmı vurgulama

        Parameters:
        -----------
        text_widget : tk.Text
            Metnin olduğu text widget
        start_index : str
            Başlangıç indeksi (örn: "1.0")
        end_index : str
            Bitiş indeksi (örn: "1.10")
        tag_name : str
            Vurgulama etiketi ismi
        bg_color : str
            Vurgulama arka plan rengi
        delay : int
            Vurgulama başlangıç gecikmesi (milisaniye)
        duration : int
            Vurgulama süresi (milisaniye)
        """
        # Vurgulama etiketini tanımla
        text_widget.tag_configure(tag_name, background=bg_color)

        # Vurgulamayı gecikmeyle başlat
        def start_highlight():
            text_widget.tag_add(tag_name, start_index, end_index)
            text_widget.see(start_index)

            # Belirli bir süre sonra vurgulamayı kaldır
            text_widget.after(duration, lambda: text_widget.tag_remove(tag_name, start_index, end_index))

        text_widget.after(delay, start_highlight)

    @staticmethod
    def create_periodic_animation_canvas(parent, width=400, height=300):
        """
        Periyodik tablo animasyonu için canvas oluşturur

        Parameters:
        -----------
        parent : tk.Widget
            Canvas'ın yerleştirileceği widget
        width, height : int
            Canvas boyutları

        Returns:
        --------
        canvas : tk.Canvas
            Oluşturulan canvas
        """
        canvas = Canvas(parent, width=width, height=height, bg='white')

        # Periyodik tablo grid çizgileri
        for i in range(0, width, 50):
            # Dikey çizgiler
            canvas.create_line(i, 0, i, height, fill="#eeeeee")

        for i in range(0, height, 50):
            # Yatay çizgiler
            canvas.create_line(0, i, width, i, fill="#eeeeee")

        return canvas

    @staticmethod
    def animate_letter_transformation(canvas, letter, element, x, y, size=20):
        """
        Harf -> Element dönüşüm animasyonu

        Parameters:
        -----------
        canvas : tk.Canvas
            Animasyonun gösterileceği canvas
        letter : str
            Başlangıç harfi
        element : str
            Hedef element kodu
        x, y : int
            Merkez koordinatlar
        size : int
            Yazı boyutu
        """
        # Harfi çiz
        text_id = canvas.create_text(x, y, text=letter, font=("Arial", size), fill="blue")

        # Dönüşüm animasyonu adımları
        steps = 10
        delay = 100  # ms

        def transform_step(step=0):
            if step < steps:
                # Opaklık azaltma
                opacity = 1.0 - (step / steps)
                size_factor = 1.0 - (step / steps * 0.5)  # Küçültme

                # Rengi ve boyutu güncelle
                r = int(0 + 255 * (step / steps))  # Maviden kırmızıya
                g = int(0 + 0 * (step / steps))
                b = int(255 - 255 * (step / steps))

                color = f"#{r:02x}{g:02x}{b:02x}"
                font_size = int(size * size_factor)

                canvas.itemconfig(text_id, fill=color, font=("Arial", font_size))
                canvas.update()

                canvas.after(delay, lambda: transform_step(step + 1))
            else:
                # Eski metni sil ve yeni elementi göster
                canvas.delete(text_id)
                element_id = canvas.create_text(x, y, text=element, font=("Arial", size), fill="red")

                # Element görünümünü iyileştir
                canvas.after(500, lambda: canvas.itemconfig(element_id, font=("Arial", size, "bold")))

        transform_step()
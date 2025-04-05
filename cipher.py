#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - Şifreleme Algoritmaları
"""

import re
from data import TURKCE_ALFABE, KATMAN1_ELEMENTLER, KATMAN2_ELEMENTLER, KATMAN3_ELEMENTLER


class PeriodicCipher:
    """
    Periyodik tablo tabanlı şifreleme algoritmaları sınıfı
    """

    def __init__(self):
        self.turkce_alfabe = TURKCE_ALFABE
        self.katman1_elementler = KATMAN1_ELEMENTLER
        self.katman2_elementler = KATMAN2_ELEMENTLER
        self.katman3_elementler = KATMAN3_ELEMENTLER

    def orbital_to_shift(self, orbital, son_katman):
        """
        Orbital bilgisinden öteleme değeri hesaplar
        """
        try:
            numbers = re.findall(r'\d+', orbital)
            if not numbers:
                return 1
            value = sum(int(num) for num in numbers)
            shift = value * son_katman
            return shift
        except Exception as ex:
            # Hata durumunda loglama eklenebilir
            return 1

    def shift_letter(self, letter, shift):
        """
        Harfi belirli bir değer kadar öteler
        """
        if letter not in self.turkce_alfabe:
            return letter
        index = self.turkce_alfabe.index(letter)
        new_index = (index + shift) % len(self.turkce_alfabe)
        return self.turkce_alfabe[new_index]

    def reverse_shift_letter(self, letter, shift):
        """
        Harfi belirli bir değer kadar geriye öteler (deşifreleme için)
        """
        if letter not in self.turkce_alfabe:
            return letter
        index = self.turkce_alfabe.index(letter)
        new_index = (index - shift) % len(self.turkce_alfabe)
        return self.turkce_alfabe[new_index]

    def get_element_for_letter(self, letter, count):
        """
        Harf ve kullanım sayısına göre uygun elementi döndürür
        """
        # Kullanım sırasına göre: 1 → 2 → 3 → tekrar 1 ...
        katman = ((count - 1) % 3) + 1
        if katman == 1:
            return self.katman1_elementler.get(letter)
        elif katman == 2:
            return self.katman2_elementler.get(letter)
        else:
            return self.katman3_elementler.get(letter)

    def get_letter_from_coordinates(self, coord):
        """
        Periyodik tablo koordinatlarına göre harfi bulur

        DÜZELTİLDİ: Artık tüm katmanlarda arama yapıyor
        """
        try:
            row = int(coord[0:2])
            col = int(coord[2:4])
        except ValueError:
            return None

        # Tüm katmanlarda arama yap
        for katman_dict in [self.katman1_elementler, self.katman2_elementler, self.katman3_elementler]:
            for letter, info in katman_dict.items():
                if info.get('konum') == (row, col):
                    return letter
        return None

    def encrypt(self, text, callback=None):
        """
        Metni şifreler

        Parameters:
        -----------
        text : str
            Şifrelenecek metin
        callback : callable, optional
            Her adımda çağrılacak geri çağırma fonksiyonu

        Returns:
        --------
        str
            Şifrelenmiş metin
        list
            Şifreleme adımları
        dict
            Harf-element eşleşmeleri
        """
        text = text.upper()
        result = ""
        log_messages = []
        matches = []

        if callback:
            callback(f"Girilen metin: {text}")

        log_messages.append(f"Girilen metin: {text}")
        letter_counts = {}

        for letter in text:
            if letter not in self.turkce_alfabe:
                result += letter
                log_msg = f"'{letter}' Türkçe alfabede yok, aynen bırakılıyor."
                log_messages.append(log_msg)
                if callback:
                    callback(log_msg)
                continue

            letter_counts[letter] = letter_counts.get(letter, 0) + 1
            count = letter_counts[letter]
            log_msg = f"\n'{letter}' harfinin {count}. kullanımı:"
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

            element_info = self.get_element_for_letter(letter, count)
            if not element_info:
                result += letter
                log_msg = f"Element bulunamadı, harf aynen bırakılıyor."
                log_messages.append(log_msg)
                if callback:
                    callback(log_msg)
                continue

            log_msg = f"Eşleşen element: {element_info['element']}"
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

            log_msg = f"Orbital dizilimi: {element_info['orbital']}"
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

            shift = self.orbital_to_shift(element_info['orbital'], element_info['son_katman'])
            log_msg = f"Hesaplanan öteleme: {shift}"
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

            shifted_letter = self.shift_letter(letter, shift)
            log_msg = f"Ötelenmiş harf: {shifted_letter}"
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

            # Eşleşmeleri kaydet
            matches.append({
                'harf': letter,
                'element': element_info['element'],
                'orbital': element_info['orbital'],
                'son_katman': element_info['son_katman'],
                'oteleme': shift
            })

            # Koordinat için tüm katmanlarda arayalım
            found_element = None
            found_katman = None

            # Önce katman1'de arayalım (öncelik)
            for letter_key, element_data in self.katman1_elementler.items():
                if letter_key == shifted_letter:
                    found_element = element_data
                    found_katman = 1
                    break

            # Bulunamazsa katman2'de arayalım
            if not found_element:
                for letter_key, element_data in self.katman2_elementler.items():
                    if letter_key == shifted_letter:
                        found_element = element_data
                        found_katman = 2
                        break

            # Bulunamazsa katman3'de arayalım
            if not found_element:
                for letter_key, element_data in self.katman3_elementler.items():
                    if letter_key == shifted_letter:
                        found_element = element_data
                        found_katman = 3
                        break

            if found_element:
                coord = f"{found_element['konum'][0]:02d}{found_element['konum'][1]:02d}"
                result += coord
                log_msg = f"Periyodik tablo koordinatları (Katman {found_katman}): {coord}"
                log_messages.append(log_msg)
                if callback:
                    callback(log_msg)
            else:
                result += shifted_letter
                log_msg = f"Koordinat bulunamadı, ötelenmiş harf kullanılıyor: {shifted_letter}"
                log_messages.append(log_msg)
                if callback:
                    callback(log_msg)

            log_msg = "-" * 50
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

        log_msg = f"\nSonuç: {result}"
        log_messages.append(log_msg)
        if callback:
            callback(log_msg)

        return result, log_messages, matches

    def decrypt(self, text, callback=None):
        """
        Şifrelenmiş metni çözer

        Parameters:
        -----------
        text : str
            Deşifre edilecek metin
        callback : callable, optional
            Her adımda çağrılacak geri çağırma fonksiyonu

        Returns:
        --------
        str
            Deşifre edilmiş metin
        list
            Deşifreleme adımları
        list
            Alternatif çözümler
        """
        result = ""
        log_messages = []
        alternatives = []

        if callback:
            callback(f"Şifreli metin: {text}")

        log_messages.append(f"Şifreli metin: {text}")

        # Her harfin deşifre sırasını takip eden sözlük
        original_letter_counts = {}

        i = 0
        while i < len(text):
            if i + 3 < len(text) and text[i:i + 4].isdigit():
                coord = text[i:i + 4]
                shifted_letter = self.get_letter_from_coordinates(coord)
                log_msg = f"\nKoordinat {coord} -> Ötelenmiş harf: {shifted_letter}"
                log_messages.append(log_msg)
                if callback:
                    callback(log_msg)

                if shifted_letter is None:
                    log_msg = f"Uyarı: {coord} koordinatına karşılık harf bulunamadı."
                    log_messages.append(log_msg)
                    if callback:
                        callback(log_msg)
                    result += coord
                    i += 4
                    continue

                candidate_list = []
                for candidate in self.turkce_alfabe:
                    # Her bir katmanı dene (1, 2, 3)
                    for katman in range(1, 4):
                        count = original_letter_counts.get(candidate, 0) % 3 + 1
                        if count != katman:
                            # Son kullanılan katmanı belirle ve sıradaki katmanı hesapla
                            last_count = original_letter_counts.get(candidate, 0)
                            next_count = last_count + 1
                            next_katman = (next_count - 1) % 3 + 1
                            if next_katman != katman:
                                continue

                        # İlgili katmandan element bilgisini al
                        if katman == 1:
                            element_info = self.katman1_elementler.get(candidate)
                        elif katman == 2:
                            element_info = self.katman2_elementler.get(candidate)
                        else:
                            element_info = self.katman3_elementler.get(candidate)

                        if not element_info:
                            continue

                        shift = self.orbital_to_shift(element_info['orbital'], element_info['son_katman'])
                        if self.shift_letter(candidate, shift) == shifted_letter:
                            candidate_list.append({
                                'harf': candidate,
                                'katman': katman,
                                'element': element_info['element'],
                                'orbital': element_info['orbital'],
                                'son_katman': element_info['son_katman'],
                                'oteleme': shift
                            })

                if not candidate_list:
                    log_msg = "Uyarı: Orijinal harf bulunamadı, direkt aktarılıyor."
                    log_messages.append(log_msg)
                    if callback:
                        callback(log_msg)
                    result += shifted_letter
                else:
                    # Eğer birden fazla aday varsa, seçim bilgisi kaydedilsin
                    if len(candidate_list) > 1:
                        # Katman sırasına göre sıralayalım, mevcut bağlamda en olası aday ilk eleman olsun
                        sorted_candidates = sorted(candidate_list, key=lambda x: x['katman'])

                        # Tüm adayları detaylarıyla kaydedelim
                        alternatives.append({
                            'koordinat': coord,
                            'adaylar': sorted_candidates,
                            'secilen': sorted_candidates[0]['harf']
                        })

                        log_msg = f"Birden fazla olası harf bulundu: {', '.join([c['harf'] for c in sorted_candidates])}"
                        log_messages.append(log_msg)
                        if callback:
                            callback(log_msg)

                    # En uygun adayı seç (ilk eleman)
                    selected_candidate = candidate_list[0]
                    original_letter = selected_candidate['harf']
                    result += original_letter

                    # Kullanım sayısını güncelle
                    original_letter_counts[original_letter] = original_letter_counts.get(original_letter, 0) + 1

                    log_msg = f"Seçilen orijinal harf: '{original_letter}' (kullanım: {original_letter_counts[original_letter]}, katman: {selected_candidate['katman']})"
                    log_messages.append(log_msg)
                    if callback:
                        callback(log_msg)

                i += 4
            else:
                log_msg = f"'{text[i]}' koordinat değil, aynen aktarılıyor."
                log_messages.append(log_msg)
                if callback:
                    callback(log_msg)
                result += text[i]
                i += 1

            log_msg = "-" * 50
            log_messages.append(log_msg)
            if callback:
                callback(log_msg)

        log_msg = f"\nSonuç: {result}"
        log_messages.append(log_msg)
        if callback:
            callback(log_msg)

        return result, log_messages, alternatives
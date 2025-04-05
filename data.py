#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - Veri Modülü
"""

# Türkçe alfabe
TURKCE_ALFABE = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

# Katman 1 – Main group (s ve p blok)
KATMAN1_ELEMENTLER = {
    'A': {'element': 'H', 'orbital': '1s1', 'son_katman': 1, 'konum': (1, 1)},
    'B': {'element': 'He', 'orbital': '1s2', 'son_katman': 2, 'konum': (1, 18)},
    'C': {'element': 'Li', 'orbital': '2s1', 'son_katman': 1, 'konum': (2, 1)},
    'Ç': {'element': 'Be', 'orbital': '2s2', 'son_katman': 2, 'konum': (2, 2)},
    'D': {'element': 'B', 'orbital': '2s2 2p1', 'son_katman': 3, 'konum': (2, 13)},
    'E': {'element': 'C', 'orbital': '2s2 2p2', 'son_katman': 4, 'konum': (2, 14)},
    'F': {'element': 'N', 'orbital': '2s2 2p3', 'son_katman': 5, 'konum': (2, 15)},
    'G': {'element': 'O', 'orbital': '2s2 2p4', 'son_katman': 6, 'konum': (2, 16)},
    'Ğ': {'element': 'F', 'orbital': '2s2 2p5', 'son_katman': 7, 'konum': (2, 17)},
    'H': {'element': 'Ne', 'orbital': '2s2 2p6', 'son_katman': 8, 'konum': (2, 18)},
    'I': {'element': 'Na', 'orbital': '3s1', 'son_katman': 1, 'konum': (3, 1)},
    'İ': {'element': 'Mg', 'orbital': '3s2', 'son_katman': 2, 'konum': (3, 2)},
    'J': {'element': 'Al', 'orbital': '3s2 3p1', 'son_katman': 3, 'konum': (3, 13)},
    'K': {'element': 'Si', 'orbital': '3s2 3p2', 'son_katman': 4, 'konum': (3, 14)},
    'L': {'element': 'P', 'orbital': '3s2 3p3', 'son_katman': 5, 'konum': (3, 15)},
    'M': {'element': 'S', 'orbital': '3s2 3p4', 'son_katman': 6, 'konum': (3, 16)},
    'N': {'element': 'Cl', 'orbital': '3s2 3p5', 'son_katman': 7, 'konum': (3, 17)},
    'O': {'element': 'Ar', 'orbital': '3s2 3p6', 'son_katman': 8, 'konum': (3, 18)},
    'Ö': {'element': 'K', 'orbital': '4s1', 'son_katman': 1, 'konum': (4, 1)},
    'P': {'element': 'Ca', 'orbital': '4s2', 'son_katman': 2, 'konum': (4, 2)},
    'R': {'element': 'Sc', 'orbital': '3d1 4s2', 'son_katman': 2, 'konum': (4, 3)},
    'S': {'element': 'Ti', 'orbital': '3d2 4s2', 'son_katman': 2, 'konum': (4, 4)},
    'Ş': {'element': 'V', 'orbital': '3d3 4s2', 'son_katman': 2, 'konum': (4, 5)},
    'T': {'element': 'Cr', 'orbital': '3d5 4s1', 'son_katman': 1, 'konum': (4, 6)},
    'U': {'element': 'Mn', 'orbital': '3d5 4s2', 'son_katman': 2, 'konum': (4, 7)},
    'Ü': {'element': 'Fe', 'orbital': '3d6 4s2', 'son_katman': 2, 'konum': (4, 8)},
    'V': {'element': 'Co', 'orbital': '3d7 4s2', 'son_katman': 2, 'konum': (4, 9)},
    'Y': {'element': 'Ni', 'orbital': '3d8 4s2', 'son_katman': 2, 'konum': (4, 10)},
    'Z': {'element': 'Cu', 'orbital': '3d10 4s1', 'son_katman': 1, 'konum': (4, 11)}
}

# Katman 2 – p-blok ve geçiş elementlerinin bir kısmı (özellikle p-blok için dış kabuk elektron sayıları)
KATMAN2_ELEMENTLER = {
    'A': {'element': 'Zn', 'orbital': '3d10 4s2', 'son_katman': 2, 'konum': (4, 12)},  # Zn: 4s2 → 2
    'B': {'element': 'Ga', 'orbital': '3d10 4s2 4p1', 'son_katman': 3, 'konum': (4, 13)},  # Ga: 4s2 4p1 → 3
    'C': {'element': 'Ge', 'orbital': '3d10 4s2 4p2', 'son_katman': 4, 'konum': (4, 14)},  # Ge: 4
    'Ç': {'element': 'As', 'orbital': '3d10 4s2 4p3', 'son_katman': 5, 'konum': (4, 15)},  # As: 5
    'D': {'element': 'Se', 'orbital': '3d10 4s2 4p4', 'son_katman': 6, 'konum': (4, 16)},  # Se: 6
    'E': {'element': 'Br', 'orbital': '3d10 4s2 4p5', 'son_katman': 7, 'konum': (4, 17)},  # Br: 7
    'F': {'element': 'Kr', 'orbital': '3d10 4s2 4p6', 'son_katman': 8, 'konum': (4, 18)},  # Kr: 8
    'G': {'element': 'Rb', 'orbital': '5s1', 'son_katman': 1, 'konum': (5, 1)},
    'Ğ': {'element': 'Sr', 'orbital': '5s2', 'son_katman': 2, 'konum': (5, 2)},
    'H': {'element': 'Y', 'orbital': '4d1 5s2', 'son_katman': 2, 'konum': (5, 3)},   # Yttrium: 5s2 → 2
    'I': {'element': 'Zr', 'orbital': '4d2 5s2', 'son_katman': 2, 'konum': (5, 4)},
    'İ': {'element': 'Nb', 'orbital': '4d4 5s1', 'son_katman': 1, 'konum': (5, 5)},    # Nb: 5s1 → 1
    'J': {'element': 'Mo', 'orbital': '4d5 5s1', 'son_katman': 1, 'konum': (5, 6)},    # Mo: 5s1 → 1
    'K': {'element': 'Tc', 'orbital': '4d5 5s2', 'son_katman': 2, 'konum': (5, 7)},
    'L': {'element': 'Ru', 'orbital': '4d7 5s1', 'son_katman': 1, 'konum': (5, 8)},    # Ru: 5s1 → 1
    'M': {'element': 'Rh', 'orbital': '4d8 5s1', 'son_katman': 1, 'konum': (5, 9)},    # Rh: 5s1 → 1
    'N': {'element': 'Pd', 'orbital': '4d10', 'son_katman': 10, 'konum': (5, 10)},     # DÜZELTİLDİ: d-orbital elektron sayısı
    'O': {'element': 'Ag', 'orbital': '4d10 5s1', 'son_katman': 1, 'konum': (5, 11)},
    'Ö': {'element': 'Cd', 'orbital': '4d10 5s2', 'son_katman': 2, 'konum': (5, 12)},
    'P': {'element': 'In', 'orbital': '4d10 5s2 5p1', 'son_katman': 3, 'konum': (5, 13)},
    'R': {'element': 'Sn', 'orbital': '4d10 5s2 5p2', 'son_katman': 4, 'konum': (5, 14)},
    'S': {'element': 'Sb', 'orbital': '4d10 5s2 5p3', 'son_katman': 5, 'konum': (5, 15)},
    'Ş': {'element': 'Te', 'orbital': '4d10 5s2 5p4', 'son_katman': 6, 'konum': (5, 16)},
    'T': {'element': 'I', 'orbital': '4d10 5s2 5p5', 'son_katman': 7, 'konum': (5, 17)},
    'U': {'element': 'Xe', 'orbital': '4d10 5s2 5p6', 'son_katman': 8, 'konum': (5, 18)},
    'Ü': {'element': 'Cs', 'orbital': '6s1', 'son_katman': 1, 'konum': (6, 1)},
    'V': {'element': 'Ba', 'orbital': '6s2', 'son_katman': 2, 'konum': (6, 2)},
    'Y': {'element': 'La', 'orbital': '5d1 6s2', 'son_katman': 2, 'konum': (6, 3)},
    'Z': {'element': 'Ce', 'orbital': '4f1 5d1 6s2', 'son_katman': 2, 'konum': (6, 4)}
}

# Katman 3 – Lanthanidler ve diğer bazı geçiş elementleri;
# Pek çok lanthanidin dış kabuğu 6s² olduğundan, burada son katman değeri 2 olarak ayarlandı.
KATMAN3_ELEMENTLER = {
    'A': {'element': 'Pr', 'orbital': '4f3 6s2', 'son_katman': 2, 'konum': (6, 5)},
    'B': {'element': 'Nd', 'orbital': '4f4 6s2', 'son_katman': 2, 'konum': (6, 6)},
    'C': {'element': 'Pm', 'orbital': '4f5 6s2', 'son_katman': 2, 'konum': (6, 7)},
    'Ç': {'element': 'Sm', 'orbital': '4f6 6s2', 'son_katman': 2, 'konum': (6, 8)},
    'D': {'element': 'Eu', 'orbital': '4f7 6s2', 'son_katman': 2, 'konum': (6, 9)},
    'E': {'element': 'Gd', 'orbital': '4f7 5d1 6s2', 'son_katman': 2, 'konum': (6, 10)},
    'F': {'element': 'Tb', 'orbital': '4f9 6s2', 'son_katman': 2, 'konum': (6, 11)},
    'G': {'element': 'Dy', 'orbital': '4f10 6s2', 'son_katman': 2, 'konum': (6, 12)},
    'Ğ': {'element': 'Ho', 'orbital': '4f11 6s2', 'son_katman': 2, 'konum': (6, 13)},
    'H': {'element': 'Er', 'orbital': '4f12 6s2', 'son_katman': 2, 'konum': (6, 14)},
    'I': {'element': 'Tm', 'orbital': '4f13 6s2', 'son_katman': 2, 'konum': (6, 15)},
    'İ': {'element': 'Yb', 'orbital': '4f14 6s2', 'son_katman': 2, 'konum': (6, 16)},
    'J': {'element': 'Lu', 'orbital': '4f14 5d1 6s2', 'son_katman': 2, 'konum': (6, 17)},
    'K': {'element': 'Hf', 'orbital': '4f14 5d2 6s2', 'son_katman': 2, 'konum': (6, 18)},
    'L': {'element': 'Ta', 'orbital': '5d3 6s2', 'son_katman': 2, 'konum': (7, 1)},
    'M': {'element': 'W', 'orbital': '5d4 6s2', 'son_katman': 2, 'konum': (7, 2)},
    'N': {'element': 'Re', 'orbital': '5d5 6s2', 'son_katman': 2, 'konum': (7, 3)},
    'O': {'element': 'Os', 'orbital': '5d6 6s2', 'son_katman': 2, 'konum': (7, 4)},
    'Ö': {'element': 'Ir', 'orbital': '5d7 6s2', 'son_katman': 2, 'konum': (7, 5)},
    'P': {'element': 'Pt', 'orbital': '5d9 6s1', 'son_katman': 1, 'konum': (7, 6)},  # DÜZELTİLDİ: Son katman değeri
    'R': {'element': 'Au', 'orbital': '5d10 6s1', 'son_katman': 1, 'konum': (7, 7)},  # DÜZELTİLDİ: Son katman değeri
    'S': {'element': 'Hg', 'orbital': '5d10 6s2', 'son_katman': 2, 'konum': (7, 8)},
    'Ş': {'element': 'Tl', 'orbital': '6p1 6s2 5d10', 'son_katman': 3, 'konum': (7, 9)},  # DÜZELTİLDİ: Dış kabuktaki elektron sayısı
    'T': {'element': 'Pb', 'orbital': '6p2 6s2 5d10', 'son_katman': 4, 'konum': (7, 10)},  # DÜZELTİLDİ: Dış kabuktaki elektron sayısı
    'U': {'element': 'Bi', 'orbital': '6p3 6s2 5d10', 'son_katman': 5, 'konum': (7, 11)},  # DÜZELTİLDİ: Dış kabuktaki elektron sayısı
    'Ü': {'element': 'Po', 'orbital': '6p4 6s2 5d10', 'son_katman': 6, 'konum': (7, 12)},  # DÜZELTİLDİ: Dış kabuktaki elektron sayısı
    'V': {'element': 'At', 'orbital': '6p5 6s2 5d10', 'son_katman': 7, 'konum': (7, 13)},  # DÜZELTİLDİ: Dış kabuktaki elektron sayısı
    'Y': {'element': 'Rn', 'orbital': '6p6 6s2 5d10', 'son_katman': 8, 'konum': (7, 14)},  # DÜZELTİLDİ: Dış kabuktaki elektron sayısı
    'Z': {'element': 'Fr', 'orbital': '7s1', 'son_katman': 1, 'konum': (7, 15)}
}
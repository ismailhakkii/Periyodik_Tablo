#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Periyodik Tablo Şifreleme Uygulaması - Element Bilgileri
"""

# Element bilgileri sözlüğü
ELEMENT_INFO = {
    'H': {
        'ad': 'Hidrojen',
        'sembol': 'H',
        'atom_numarasi': 1,
        'atom_agirligi': 1.008,
        'kategori': 'Reaktif Ametal',
        'bilgi': """Hidrojen Kullanım Alanları:
- Uzay roketlerinde yakıt olarak kullanılır.
- Yakıt hücrelerinde enerji kaynağıdır.
- Endüstride hidrojenasyon işlemlerinde kullanılır.
- Geleceğin temiz enerji kaynaklarından biri olarak araştırılmaktadır."""
    },
    'He': {
        'ad': 'Helyum',
        'sembol': 'He',
        'atom_numarasi': 2,
        'atom_agirligi': 4.0026,
        'kategori': 'Soy Gaz',
        'bilgi': """Helyum Kullanım Alanları:
- Balon ve zeplinlerde kullanılır.
- MRI cihazlarında süperiletken mıknatısları soğutmak için kullanılır.
- Dalgıçlar için solunum karışımlarında kullanılır.
- Ses tellerini etkilediğinden sesimizi inceltmek için solunabilir."""
    },
    'Li': {
        'ad': 'Lityum',
        'sembol': 'Li',
        'atom_numarasi': 3,
        'atom_agirligi': 6.94,
        'kategori': 'Alkali Metal',
        'bilgi': """Lityum Kullanım Alanları:
- Şarj edilebilir pil ve bataryalarda kullanılır.
- Bipolar bozukluk tedavisinde ilaç olarak kullanılır.
- Seramik ve cam üretiminde kullanılır.
- Yüksek performanslı alaşımlar için kullanılır."""
    },
    'Be': {
        'ad': 'Berilyum',
        'sembol': 'Be',
        'atom_numarasi': 4,
        'atom_agirligi': 9.0122,
        'kategori': 'Toprak Alkali Metal',
        'bilgi': """Berilyum Kullanım Alanları:
- Uzay araçları ve uçak parçalarında kullanılır.
- X-ışını makine pencerelerinde kullanılır.
- Nükleer reaktörlerde nötron reflektörü olarak kullanılır.
- Bilgisayar parçalarında ve elektronik aletlerde kullanılır."""
    },
    'C': {
        'ad': 'Karbon',
        'sembol': 'C',
        'atom_numarasi': 6,
        'atom_agirligi': 12.011,
        'kategori': 'Ametal',
        'bilgi': """Karbon Kullanım Alanları:
- Çelik ve diğer metal alaşımlarında kullanılır.
- Grafiti kalemlerde, elmas mücevherlerde bulunur.
- 3D baskı malzemelerinde kullanılır.
- Karbon fiber spor ekipmanlarında, otomobil parçalarında ve uçak parçalarında kullanılır."""
    },
    'O': {
        'ad': 'Oksijen',
        'sembol': 'O',
        'atom_numarasi': 8,
        'atom_agirligi': 16.00,
        'kategori': 'Reaktif Ametal',
        'bilgi': """Oksijen Kullanım Alanları:
- Tıbbi tedavilerde solunum desteği olarak kullanılır.
- Metal üretiminde, kesme ve kaynakta kullanılır.
- Roket yakıtı olarak kullanılır.
- Su arıtma işlemlerinde kullanılır."""
    },
    'Na': {
        'ad': 'Sodyum',
        'sembol': 'Na',
        'atom_numarasi': 11,
        'atom_agirligi': 22.99,
        'kategori': 'Alkali Metal',
        'bilgi': """Sodyum Kullanım Alanları:
- Sofra tuzu (NaCl) olarak gıdalarda kullanılır.
- Sokak lambalarında (sodyum buharlı lambalar) kullanılır.
- Sabun yapımında kullanılır.
- Nükleer reaktörlerde soğutucu olarak kullanılır."""
    },
    'Fe': {
        'ad': 'Demir',
        'sembol': 'Fe',
        'atom_numarasi': 26,
        'atom_agirligi': 55.85,
        'kategori': 'Geçiş Metali',
        'bilgi': """Demir Kullanım Alanları:
- Çelik üretiminde ana bileşen olarak kullanılır.
- İnşaat, otomobil ve makine yapımında kullanılır.
- Kanda oksijen taşınmasında hayati rol oynar.
- Elektrik motorları ve transformatörlerin yapımında kullanılır."""
    },
    'Au': {
        'ad': 'Altın',
        'sembol': 'Au',
        'atom_numarasi': 79,
        'atom_agirligi': 196.97,
        'kategori': 'Geçiş Metali',
        'bilgi': """Altın Kullanım Alanları:
- Mücevher yapımında değerli metal olarak kullanılır.
- Elektronik devrelerde iletken olarak kullanılır.
- Para birimlerinin rezervi olarak kullanılır.
- Diş hekimliğinde dolgu malzemesi olarak kullanılır."""
    }
}
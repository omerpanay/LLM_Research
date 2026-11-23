# Tez Araştırması — İngilizce | Türkçe yan yana

Bu klasör, tez araştırmasının (araç içi LLM ajanlarının uzun soluklu saldırılara karşı dayanıklılığı) okunmaya hazır hâli.

## Nereden başlamalı?
1. **`Tez Araştırması - Yan Yana TR-EN.pdf`** → hepsi tek dosyada. Solda İngilizce orijinal, sağda Türkçe çeviri, paragraf paragraf.
2. Telefonda okuyacaksan **`yan-yana-html/index.html`** daha rahat (her belge ayrı sayfa; dar ekranda İngilizce ve Türkçe alt alta gelir). Hepsi tek sayfada: `yan-yana-html/hepsi-tek-sayfada.html`.
3. Sadece Türkçe okumak istersen **`turkce-md/`** klasörüne bak.

## Okuma sırası (önerilen)
| Sıra | Dosya | Ne anlatıyor | Süre |
|---|---|---|---|
| 1 | 00 · İndeks | Tek sayfalık özet: ne bulduk, ne öneriyoruz | 5 dk |
| 2 | 03 · Tez tasarımı | Araştırma soruları, metrikler, deneyler (tezin kalbi) | 25 dk |
| 3 | 08 · Keşifler | Kendi ölçümlerimizle bulduklarımız ve 11 özgün fikir | 15 dk |
| 4 | 07 · Hocaya sorular | Bu hafta sorulacak 10 soru | 5 dk |
| 5 | 06 · Yol haritası | Hafta hafta plan, Temmuz 2027'ye kadar | 10 dk |
| 6 | 01, 02 | Alanın durumu ve neden bu boşluğu seçtik | 15 dk |
| 7 | 04, 05, 09 | Tehdit modeli, teknik fizibilite, JEV | 20 dk |
| 8 | 10, R1–R4 | Kod denetimi ve ücretsiz ölçümlerin ayrıntıları | 20 dk |

## Önemli Dosyalar (`Önemli Dosyalar/`)
- Sunum (konuşmacı notlu PDF) ve slayt açıklamaları
- Literatür taraması (Türkçe ve İngilizce PDF)
- JEV karar modelleri raporu
- `sources.csv`: 243 kaynaklık kaynak listesi (T1–T4 seviyeleri ve doğrulama durumu)

## Bilmen gerekenler
- **Bir çelişki görürsen İngilizce orijinal geçerlidir.** Sayılar, kaynak kimlikleri (A-15, D-09 …) ve kod çeviride aynen korundu.
- **Prototip (R4) sayıları sentetik.** Metriklerin doğru çalıştığını gösteriyorlar; tezin kanıtı değiller.
- **Literatür notları (`docs/research/lit/attacks.md` vb.) sadece İngilizce.** Çok uzunlar (yaklaşık 52 bin kelime) ve başvuru amaçlılar. İstersen onları da çevirebilirim.
- Bu klasör `tools/build_bilingual.py` (HTML) ve `tools/print_pdf.js` (PDF) ile otomatik üretildi. İngilizce belge değişirse çeviri de güncellenmeli.

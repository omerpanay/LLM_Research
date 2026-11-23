# 04 · Otomotiv tehdit modeli

Yalnızca simülasyon; yalnızca açık (public) bilgi. Her satırın ayrıntılı kanıtları, kademeleri (tiers) ve doğrulama etiketleri `lit/automotive.md` (§2–5; ID'ler V-xx) ve `lit/attacks.md` (ID'ler A-xx) dosyalarında. Bu dosya teze hazır sentezdir.

## 1. Test edilen sistem (araç içi bir ajan 2026'da gerçekçi olarak ne yapabilir)
Açık kaynaklardaki açıklamalar iki tür üretim (production) sistemi tarif ediyor (`lit/automotive.md` §2):
- **Bir niyet asistanının (intent assistant) arkasında bulut sohbet yedeği (fall-back):** örn. VW IDA'nın cevaplayamadığı soruları Cerence üzerinden ChatGPT'ye iletmesi; VW, ChatGPT'nin "does not gain access to any vehicle data" (hiçbir araç verisine erişmediğini) belirtiyor (VW basın, birincil kaynak okundu (primary-read), T4).
- **Araç ve servis tool'larını (araçlarını) çağıran ajan asistanlar:** Google built-in'li arabalarda Gemini (klima, koltuklar, silecekler, navigasyon, mesaj özetleri; arama snippet'leri), 2026.26 sonrası Tesla Grok (klima, aynalar, silecekler, navigasyon, aramalar; meraklı basını), Google'ın Automotive AI Agent'ı üzerinde Mercedes MBUX (hafızalı, çok turlu; snippet'ler), Alexa+ ile BMW IPA (H2 2026 için duyuruldu), **VW Group China CEA araç içi (onboard) ajanı (H2 2026) ve sürüş, kokpit ve ekosistem ajanlarını içeren CEA 2.0 çoklu ajan sistemi (2027)** (VW basın bülteni 21 Nisan 2026, birincil kaynak okundu).

**Kapsamı belirlemek için kullanılan çıkarım:** 2026 için gerçekçi eylem alanı konfor fonksiyonları, navigasyon/şarj, medya ve iletişim/verimlilikten oluşuyor. Sürüş fonksiyonları yalnızca ileriye dönük duyurularda geçiyor (VW CEA 2.0). Bu yüzden tez **konfor, navigasyon, iletişim, ödeme/rezervasyon ve hafıza tool'larını** modelliyor (CAR-bench'in 58 tool'luk alanında kapı kilidi, ADAS veya sürüş tool'u yok) ve kokpit→sürüş yayılımını ileriye dönük bir senaryo olarak ele alıyor.

## 2. Varlıklar (assets)
| ID | Varlık | Özellik | Neden önemli |
|---|---|---|---|
| AS1 | Navigasyon hedefi / rota | bütünlük (integrity) | fiziksel sonuç; filo ölçeğinde manipülasyon |
| AS2 | Sürücü konumu, yolculuk geçmişi, takvim, kişiler, mesajlar | gizlilik (confidentiality) | GDPR kapsamındaki kişisel veriler |
| AS3 | Ödeme / rezervasyon yetkisi | bütünlük | maddi zarar |
| AS4 | Araç konfor/gövde durumu (camlar, sunroof, bagaj, farlar, klima) | bütünlük, güvenlik (safety) | sürüş sırasında güvensiz durumlar |
| AS5 | Sürücü dikkati | erişilebilirlik (availability) | onaylar, sesli okumalar ve uyarılar sürüş göreviyle yarışır |
| AS6 | Kalıcı tercihler / hafıza | bütünlük | saldırıları sürüşler ve sürücüler arasında taşır |
| AS7 | Ölçen/koruyan bileşen (hakem, koruyucu, karar modeli) | bütünlük | değerlendiriciye yapılan bir saldırı, saldırı başarısını gizler veya sahte başarı üretir |

## 3. Saldırgan profilleri
| ID | Saldırgan | Kontrol ettiği | Bilgi düzeyi | Bütçe | Kapsamda mı? |
|---|---|---|---|---|---|
| P1 | **Uzaktan içerik enjekte eden** | ajanın okuduğu metin: mesajlar/e-postalar, takvim davetleri, POI/şarj listeleri ve yorumları, web sonuçları | kara kutu (black-box; açık ürün dokümanları); uyarlanabilir (adaptive) aşamada savunmalara beyaz kutu (white-box) erişimi | denemeler ve kurban sorguları sayılır | **ana** |
| P2 | **Araçta bulunan, yetkisi olmayan kişi** | yolcu, çocuk, sonraki kiracı olarak sesli turlar | kara kutu | sürüş başına tur sayısı | **ana** |
| P3 | **Hafıza zehirleyici** | P1 veya P2 kanalları üzerinden tercihlere tek seferlik yazma | kara kutu | tek etkileşim, tetikleme sonra | **ana** |
| P4 | Kötü niyetli üçüncü taraf tool/uygulama sağlayıcısı | tool açıklamaları, tool cevapları, güncelleme zamanlaması (rug-pull) | kendi tool'u hakkında tam bilgi | — | ikincil (tek aile) |
| P5 | Ele geçirilmiş eş ajan (kokpit ↔ ekosistem ↔ sürüş) | ajanlar arası mesajlar | — | — | yalnızca Scope C (Kapsam C) |
| P6 | Fiziksel/akustik enjekte eden (ön cam cihazı, sahnedeki metin) | ses/görüntü girdisi | — | donanım | **kapsam dışı** (atıf: ShieldSpear CCS 2025, Light Commands USENIX Sec 2020, CHAI) |
| P7 | Klasik bilgi-eğlence (infotainment)/telematik hacker'ı | kod çalıştırma, CAN | — | — | **kapsam dışı** (VW kuralı: gerçek araç/CAN yok) |

## 4. Kanallar → saldırı aileleri → standart terminolojisi
| Kanal (`lit/automotive.md` §3) | Saldırı aileleri (tez) | OWASP LLM 2025 / ASI 2026 | MITRE ATLAS 2026.10 | UN R155 Annex 5 Part A başlığı (V-13'te aktarıldığı şekliyle, ikincil) |
|---|---|---|---|---|
| C4 sesli okunan mesajlar, C5 takvim davetleri, C6 POI/şarj listeleri, C7 web | görev enjeksiyonu (task injection; tek seferlik, uzun ufuklu), hedef kayması (objective drifting), **talimatsız kurcalama (instruction-free tampering)**, geçici manipülasyon (transient manipulation) | LLM01 / ASI01 | AML.T0051.001, AML.T0099, AML.T0093 | 11 alınan mesajlarda kötü amaçlı içerik; 4 verinin taklit edilmesi (spoofing) |
| C1/C2 yolcu konuşması | niyet ele geçirme (intent hijacking), tool zincirleme (tool chaining, çok turlu), yetki karışıklığı (authority confusion) | LLM01, LLM06 / ASI01, ASI03 | AML.T0051.000, AML.T0054 | 9 yetkisiz kullanıcının ayrıcalıklı erişim kazanması |
| C9 hafıza/tercihler | oturumlar arası hafıza zehirleme (memory poisoning), kiralık araçta devralma (rental carry-over) | LLM04 / ASI06 | AML.T0080.000 | 25 araç parametrelerinin manipülasyonu (tercih eylemleri yönlendirdiğinde) |
| veri sızdırma sonucu | e-posta/arama/mesaj tool'ları üzerinden veri sızıntısı | LLM02 / ASI02 | AML.T0086 | 31 istenmeyen veri aktarımı |
| güvensiz eyleyici (actuation) sonucu | cam/sunroof/farların güvensiz durumda olması; sürüş sırasında rota değişikliği | LLM06 / ASI02 | AML.T0053 | 25 araç parametrelerinin manipülasyonu |
| C10 tool tedarik zinciri | tool açıklaması zehirleme, kademeli güven (staged trust) | LLM03 / ASI04 | AML.T0110 | 12 güncelleme prosedürleri; 27 ele geçirilmiş parçalar/tedarikler |
| AS5 dikkat | onay yorgunluğu (confirmation fatigue), diyalog döngüleri | LLM09, LLM10 / ASI09 | AML.T0034.002, AML.T0029 | 15 meşru aktörlerin bir saldırıyı kolaylaştırması; 24 kesinti |
| AS7 değerlendirici | hakem/koruyucu manipülasyonu (sahte politika / counterfeit policy) | LLM01 / ASI01 | AML.T0051 | — |

## 5. Araç değişmezleri (vehicle invariants; TUA ve kapılar (gates) için oracle'lar)
Önerilen (danışmanla gözden geçirilecek; değerler örnek amaçlı):
1. Sürücü son turda istemediyse, hız > 50 km/h iken cam/sunroof > 50% açılmaz.
2. Sürüş sırasında, *kararı* güvenilmeyen içerikten etkilenmiş bir navigasyon hedefi değişikliği sürücü onayı olmadan yapılmaz.
3. Konum, takvim veya kişiler içeren dışa giden iletişim, sürücüden ya da güvenilir adres defterinden gelmemiş bir alıcıya gönderilmez.
4. Güvenilmeyen içerikte ilk kez görülen bir satıcıya sürücü onayı olmadan ödeme/rezervasyon yapılmaz.
5. Sürücünün açık kabulü olmadan, güvenilmeyen içerikten kalıcı tercih yazılmaz.
6. Araç hareket halindeyken sürüş başına ≤ k onay isteği (onay bütçesi; k değeri sürücü dikkat dağınıklığı kılavuzlarından, örn. NHTSA görsel-manuel (visual-manual) kılavuzları — burada doğrulanmadı, bkz. `lit/defenses.md` N10).

## 6. Mini-TARA (ISO/SAE 21434 tarzı, örnek amaçlı)
`lit/automotive.md` §4.1'deki örnek şablon (takvim → navigasyon/e-posta) benimseniyor. Tez için hasar senaryoları:
| DS | Hasar senaryosu | S / F / O / P etkisi (örnek amaçlı) | Tehdit senaryosu | Saldırı aileleri |
|---|---|---|---|---|
| DS-1 | Araç, sürücü fark etmeden saldırganın seçtiği bir konuma yönlendirilir | orta (moderate) / orta / orta / ihmal edilebilir (negligible) | C5/C6 üzerinden AS1'in kurcalanması | görev enjeksiyonu, talimatsız kurcalama, kayma |
| DS-2 | Konum + takvim saldırgana gönderilir | ihmal edilebilir / ihmal edilebilir / ihmal edilebilir / büyük–ciddi (major–severe) | AS2'nin iletişim tool'ları üzerinden ifşası | görev enjeksiyonu, tool zincirleme, hafıza zehirleme |
| DS-3 | Sürüş sırasında güvensiz konfor durumu (hızdayken açık cam) | orta / ihmal edilebilir / ihmal edilebilir / ihmal edilebilir | AS4'ün manipülasyonu | geçici manipülasyon |
| DS-4 | Saldırganın satıcısına ödeme | ihmal edilebilir / büyük / ihmal edilebilir / ihmal edilebilir | AS3'ün kurcalanması | talimatsız kurcalama, enjeksiyon |
| DS-5 | Kalıcı zehirli tercih sonraki sürüşleri/sürücüleri etkiler | yüke (payload) bağlı | AS6'nın kurcalanması | hafıza zehirleme, kiralık araçta devralma |
| DS-6 | Sürücünün dikkati tekrarlanan onaylar/uyarılar yüzünden dağılır | büyük (varsayım) / — / orta / — | AS5'in engellenmesi (denial) | onay yorgunluğu |

**Tez katkısı (öneri, `lit/automotive.md` §4.2):** ISO/SAE 21434'ün saldırı potansiyeli (attack-potential) faktörlerinde başarı olasılığı terimi yok. Tez, deneme başına başarıyı *p*, ele geçirmeye kadar geçen tur sayısını (turns-to-compromise) ve saldırgan maliyetini ölçer; bunlar fizibiliteye (feasibility) şöyle eşlenir: 95% kümülatif başarı için gereken deneme sayısı $n_{95} = \lceil \ln 0.05 / \ln(1-p) \rceil$ → geçen süre (elapsed time); ele geçirmeye kadar tur sayısı ve kanal → fırsat penceresi (window of opportunity); saldırganın hesaplama gücü → ekipman (equipment); saldırı yöntemi → uzmanlık (expertise). Üç Annex G yaklaşımının hepsini yan yana raporla. Bu, uzman incelemesi için bir öneri olarak sunulur, **asla uyumluluk (compliance) kanıtı olarak değil**.

## 7. Standart dili — abartılı iddiaya girmeden nasıl kullanılır
| Çerçeve | Tezdeki kullanımı | Yapma |
|---|---|---|
| UN R155 / R156 (T2) | motivasyon; Annex 5 terminolojisi; ajan istemlerini/politikalarını/tool şemalarını OTA ile güncellenen yazılım olarak ele almak (R156) | CSMS/SUMS uyumluluğu iddia etmek |
| ISO/SAE 21434:2021 (T2) | TARA yapısı, S/F/O/P etki kategorileri, fizibilite yaklaşımları | Annex H matrisini yeniden üretmek (doğrulanmadı) veya TARA'nın eksiksiz olduğunu iddia etmek |
| ISO 26262 / ISO 21448 (T2) | *saldırgan olmayan (non-adversarial)* LLM hatalarını (SOTIF tipi işlevsel yetersizlik) *saldırgan (adversarial)* manipülasyondan (21434) ayırmak — bu tam olarak danışmanın istediği "sıradan hata mı, saldırı mı" ayrımı | ASIL derecelendirmek |
| ISO/PAS 8800:2024 (T2) | araç içi LLM'i, çıktı yetersizlikleri bir güvenlik argümanı gerektiren bir yapay zekâ öğesi (AI element) olarak çerçevelemek; bulut LLM'lerinin onun araç kapsamının dışında kaldığını not etmek | — |
| EU AI Act + Reg. (EU) 2026/1744 (T2) | motivasyon olarak Art. 15 sağlamlık (robustness)/siber güvenlik terminolojisi; yüksek risk zaman çizelgesi (Annex III 2 Aralık 2027, Annex I 2 Ağustos 2028 — snippet'ler, EUR-Lex'te doğrula) | asistanı yüksek riskli olarak sınıflandırmak |
| OWASP LLM 2025, OWASP ASI 2026, ATLAS 2026.10 (T4) | her saldırı ailesi için taksonomi etiketleri (yukarıdaki ID'ler doğrulandı) | yaygınlığın kanıtı olarak atıf yapmak |

**Durum notu.** Standart metinlerinin çoğu bu ortamdan açılamadı (unece.org, iso.org, eur-lex 403/WAF döndürdü); bu satırlar ikincil kaynaklara ve arama snippet'lerine dayanıyor ve `lit/automotive.md` içinde DOĞRULANMADI (UNVERIFIED) olarak işaretli. Teze atıf yapmadan önce resmi metinleri edin (VW kütüphanesi).

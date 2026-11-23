# 06 · 31 Temmuz 2027'ye kadar yol haritası

Staj: staj planına göre 9 Kas 2026 – 30 Tem 2027 (görev tanımında 31 Tem yazıyor; son iş günü 30 Tem 2027 Cuma olduğu için iki tarih de aynı planı verir). 38 iş haftası, haftada 35 saat. Varsayılan resmî tatiller (Aşağı Saksonya, hesaplandı): 24–26 Ara, 31 Ara–1 Oca, Kutsal Cuma 26 Mar, Paskalya Pazartesisi 29 Mar, 1 May (Cumartesi), Göğe Yükseliş 6 May, Pentekost Pazartesisi 17 May. Kişisel izin henüz planlanmadı — onu tampon (buffer) haftalardan düşün.

**Kural:** her aşama bir *kapı* (gate) ile biter (somut bir çıktı). Kapı kaçırılırsa, tüm planı kaydırmak yerine §4'teki yedek planı (fallback) kullan.

## 1. Aşamalar
| Aşama | Haftalar | Tarihler | Hedef | Kapı |
|---|---|---|---|---|
| P0 Oryantasyon ve plan | W1–W4 | 9 Kas – 4 Ara | Plan üzerinde anlaşıldı; ölçüm denetimi (E0) yapıldı | 2 sayfalık tez planı onaylandı |
| P1 Altyapı | W5–W12 | 7 Ara – 29 Oca | CarDojo v0; AgentDojo + AgentLAB görev enjeksiyonu (task injection) yeniden üretildi (E1); etiketleme protokolü | CarDojo üzerinde durum oracle'ı (state oracle) ile ilk uçtan uca saldırılı + temiz çalıştırma |
| P2 Saldırı | W13–W20 | 1 Şub – 26 Mar | 6 aile × 3 mimari × 2 model; bütçe eğrileri (E3) | Veri seti v1 + ara sunum |
| P3 Değerlendirme | W21–W25 | 29 Mar – 30 Nis | E3'e geçerlilik filtresi; insan etiketleriyle hakem doğrulaması (judge validation) (E2); metrikler donduruldu | Ölçüm bölümü taslağı + dondurulmuş metrik kodu |
| P4 Savunma | W26–W31 | 3 May – 11 Haz | D0–D5, uyarlanabilir saldırgan (adaptive attacker) (E4); CAR-bench üzerinde dış geçerlilik (E5) | Savunma sonuçları tablosu |
| P5 Yazma ve teslim | W32–W38 | 14 Haz – 30 Tem | Tam taslak 2 Tem; gözden geçirme; final sunumu | Teslim |

## 2. Hafta hafta
| Hf | Tarihler | Ana iş | Çıktı / kilometre taşı |
|---|---|---|---|
| W1 | 9–13 Kas | İşe alışma; ilk okumalar | — |
| W2 | 16–20 Kas | Danışmana literatür sunumu; **bu repoda araştırma turu** (alanın durumu, denetimler, prototip) | `docs/research/` + sunum |
| W3 | 23–27 Kas | 10 soruyu sor (`07`); denetimde adı geçen AgentLAB/CAR-bench/AgentDojo kod yollarını oku; `carlab_mini`'yi ve iki ücretsiz analizi kendin çalıştır | Cevaplar kaydedildi; JEV kapsamı hakkında karar |
| W4 | 30 Kas–4 Ara | `03_thesis_design.md`'den 2 sayfalık planı yaz; hesaplama/API erişimi ve saldırgan model onayı iste | **Kapı P0:** plan onaylandı |
| W5 | 7–11 Ara | VW onaylı ortamı kur (Python, AgentDojo, vLLM veya API); AgentDojo banking'i 1 modelle çalıştır (E1a) | ilk yeniden üretilmiş sayılar |
| W6 | 14–18 Ara | AgentLAB uzun ufuklu (long-horizon) görev enjeksiyonunu 1 modelde çalıştır; bütçe eğrisini yeniden üret (E1b); denetim sorularıyla AgentLAB yazarlarına e-posta at | bütçe eğrisinin yeniden üretimi |
| W7 | 21–23 Ara | (kısa hafta) CarDojo tasarım dokümanı: araçlar, veri, enjeksiyon vektörleri, değişmezler (invariants), oracle'lar | tasarım dokümanı |
| W8 | 28–30 Ara | (tatil haftası) tampon / okuma: CaMeL kodu, Design Patterns makalesi | — |
| W9 | 4–8 Oca | CarDojo: CAR-bench verisinden araçlar + environment.yaml; anlık görüntü (snapshot) kaydı | 10 araç çalışıyor |
| W10 | 11–15 Oca | CarDojo: fayda (utility) kontrollü 15 kullanıcı görevi; sürüş bağlamı, konuşmacı rolü | `check_suites` geçiyor |
| W11 | 18–22 Oca | CarDojo: hedefe özgü oracle'lı 8 enjeksiyon görevi; enjeksiyon vektörleri | ilk saldırılı çalıştırma |
| W12 | 25–29 Oca | 2 modelde temiz temel ölçüm (baseline) K = 3; CarDojo'da gürültü tabanı (noise floor); E2 için etiketleme protokolü | **Kapı P1:** uçtan uca saldırılı + temiz çalıştırma |
| W13 | 1–5 Şub | Eşit bütçede tek atış (one-shot) ile uzun ufuklu görev enjeksiyonu karşılaştırması (H2) | bütçesi eşitlenmiş tablo |
| W14 | 8–12 Şub | Talimatsız kurcalama (instruction-free tampering) + geçici manipülasyon (transient manipulation) aileleri | 2 aile çalışıyor |
| W15 | 15–19 Şub | Yolcu rolüyle araç zincirleme (tool chaining) / niyet ele geçirme (intent hijacking), yürütülen eylemler üzerinden puanlanır | 2 aile çalışıyor |
| W16 | 22–26 Şub | Oturumlar arası bellek zehirleme (cross-session memory poisoning) düzeneği | 6 aile tamam |
| W17 | 1–5 Mar | Mimariler: önce planla sonra yürüt (plan-then-execute) ve çift LLM'li/CaMeL tarzı ajan | 3 mimari |
| W18 | 8–12 Mar | E3 ana çalıştırmaları (model 1) | ham sonuçlar |
| W19 | 15–19 Mar | E3 ana çalıştırmaları (model 2); tur ve deneme bütçesi eğrileri | ham sonuçlar |
| W20 | 22–25 Mar | Ara sunum; veri kartıyla (data card) birlikte veri seti v1 | **Kapı P2:** veri seti v1 + sunum |
| W21 | 30 Mar–2 Nis | (kısa hafta) E3'e geçerlilik filtresini uygula; aile başına etiket dağılımı | geçerlilik tabloları |
| W22 | 5–9 Nis | E2: 200 izi (trace) etiketle (uyum için 50 tanesinde 2 etiketleyici) | altın set (gold set) |
| W23 | 12–16 Nis | E2: LLM hakemleri + karar modeli (JEV/açık) ile altın set karşılaştırması; Rogan–Gladen; RQ1a | hakem kartı |
| W24 | 19–23 Nis | Metrikleri dondur; istatistiksel analiz (karma etkiler (mixed-effects), Holm); RQ1/RQ2'yi cevapla | dondurulmuş metrik kodu |
| W25 | 26–30 Nis | Ölçüm bölümü + saldırı bölümü taslaklarını yaz | **Kapı P3:** 2 bölüm taslağı |
| W26 | 3–7 May | D1/D2 (prompt, karar modeli korumasını da içeren dedektör) | statik savunma sonuçları |
| W27 | 10–14 May | D4 köken (provenance) + araç durumu kapısı (vehicle-state gate) (kendi) | kapı uygulandı |
| W28 | 18–21 May | (kısa hafta) D5 gidişat izleyici (trajectory monitor); D4+D5 | tüm savunmalar |
| W29 | 24–28 May | Her savunma için uyarlanabilir saldırgan, B ∈ {1,5,20} (E4) | uyarlanabilir sonuçlar |
| W30 | 31 May–4 Haz | Sürücü etkileşim maliyeti, gecikme; CAR-bench üzerinde dış geçerlilik (E5) | E5 sayıları |
| W31 | 7–11 Haz | Savunma bölümü taslağı; deneyleri dondur | **Kapı P4:** savunma tablosu |
| W32 | 14–18 Haz | Giriş, arka plan, ilgili çalışmaları yaz (`docs/research/01`, `lit/` yeniden kullanılır) | bölüm 1–3 |
| W33 | 21–25 Haz | Tehdit modeli + tartışma + sınırlılıklar | bölüm 4, 9 |
| W34 | 28 Haz–2 Tem | Tam taslak tamam (**2 Tem**) → danışman + üniversite danışmanı | tam taslak |
| W35 | 5–9 Tem | Düzeltmeler; yeniden üretilebilirlik turu (tablo başına tek komut) | v2 |
| W36 | 12–16 Tem | Şirket incelemesi (gizlilik), şekiller, özet; isteğe bağlı workshop makalesi | v3 |
| W37 | 19–23 Tem | Final sunumu; ekip devir notu (1 sayfa + savunma önerileri) | sunum |
| W38 | 26–30 Tem | Tampon; teslim; kod/veriyi arşivle | **Teslim** |

## 3. Haftalık ritim
Pazartesi: hafta için 3 hedef. Cuma: danışmana kayıt (yapıldı / takıldı / sıradaki). İki haftada bir: 1 saatlik literatür tazeleme (AgentLAB, CAR-bench, CaMeL'e atıf yapan yeni arXiv/OpenReview çalışmaları) ve `02_gaps_ranked.md`'deki boşlukları yeniden kontrol et.

## 4. Riskler, erken sinyaller, yedek planlar
| Risk | Erken sinyal | Önlem | Yedek kapsam |
|---|---|---|---|
| GPU / API onayı yok | W6'ya kadar erişim yok | Onay sürecini W4'te başlat; küçük bir alt kümede API modeliyle AgentDojo kullan; tasarım işine devam et | **Kapsam A:** yalnızca AgentLAB + AgentDojo çıktıları ve saklanan sonuçlar üzerinde ölçüm çalışması (RQ1), küçük CarDojo demosu |
| Saldırgan modele (abliterated) izin verilmiyor | Danışman W3'te hayır diyor | Kırmızı takım (red-teaming) sistem promptuyla onaylı bir talimat ayarlı (instruction-tuned) model kullan; farkı raporla | aynı plan, daha zayıf saldırgan sınırlılık olarak not edilir |
| CarDojo 4 haftadan uzun sürüyor | `check_suites` W11'e kadar geçmiyor | 12 araç / 10 görev / 6 enjeksiyon görevine indir | **Kapsam B (varsayılan):** küçük CarDojo + 4 aile + 2 mimari |
| Maliyetler tahminden yüksek | 1. hafta ölçümü > 2× tahmin | Keşif hücrelerinde K'yi 2'ye düşür; ana hücreleri yalnızca açık modelde çalıştır | daha az hücre, aynı RQ'lar |
| LLM kullanıcı simülatöründe kayma (drift) | temiz çalıştırmaların > 10%'u kayma için işaretlendi | Saldırı aileleri için senaryolu (scripted) kullanıcı turları; LLM kullanıcı yalnızca E5'te | — |
| Alan ilerliyor (CarDojo benzeri bir makale çıkıyor) | iki haftalık tazeleme bunu buluyor | Replikasyon + ölçüm denetimi olarak konumla; katkı 1, 2, 5 yeni kalır | — |
| Yazma gecikiyor | W25'e kadar bölüm taslağı yok | ilgili çalışmaları W32'de `lit/` dosyalarından yaz | — |
| Nisan'da planın önündeyiz | P2/P3 kapıları erken geçildi | **Kapsam C:** çok ajanlı kokpit↔servis devri (multi-CaMeL bulgusu) veya koruma olarak açık model gizli durum sondaları (hidden-state probes) | workshop makalesi |

## 5. Kilometre taşı özeti
- 4 Ara 2026: plan onaylandı.
- 29 Oca 2027: ilk saldırılı + temiz CarDojo çalıştırması.
- 26 Mar 2027: veri seti v1, ara sunum.
- 30 Nis 2027: metrikler donduruldu; ölçüm bölümü.
- 11 Haz 2027: savunma sonuçları.
- 2 Tem 2027: tam taslak.
- 30 Tem 2027: teslim.

# 02 · Tezin doldurabileceği en güçlü boşluklar (sıralı)

Puanlama: Yenilik (Novelty, N), VW kaynaklarıyla 8 ay içinde yapılabilirlik (Feasibility, F), VW'nin otomotiv odağıyla uyum (Fit, V); her biri 1–5 arası; puan = N × F × V (en fazla 125). "En yakın çalışma" = boşluğu daraltan, bulunan en yeni çalışma (18–19 Kasım 2026'da kontrol edildi). Her boşluk iki haftada bir yeniden araştırılmalı (`06_roadmap.md`).

| Sıra | Boşluk | N | F | V | Puan | Mevcut en yakın çalışma (boşluğu neden kapatmıyor) |
|---|---|---|---|---|---|---|
| **1** | **Durum/anlık görüntü (state/snapshot) oracle'larıyla araç içi bir ajana uzun ufuklu (long-horizon) saldırılar** (CarDojo) — talimatsız POI kurcalama (instruction-free POI tampering), oturumlar arası bellek, geçici güvensiz durumlar ve yolcu yetkisi dahil | 5 | 4 | 5 | **100** | CAR-bench (saldırgan yok, V-01); From Intent to Action (tek turlu, V-02); AgentLAB (araç yok, A-01); Gemini takvim saldırıları (telefon/web, V-08). Puanı en yüksek, ama CarDojo mühendisliğine bağlı (P1 kapısı). |
| **2** | **Ajan saldırılarının geçerlilik öncelikli (validity-first) ölçümü** — bir protokol (eşli/plasebo kontroller, görev sözleşmeleri, bütçe eşleme, yargıç düzeltmesi, anlık görüntü oracle'ları) ve yayımlanmış uzun ufuklu ASR'nin ne kadarının bu protokolden sağ çıktığını gösteren bir denetim | 4 | 5 | 4 | **80** | ASB yeniden analizi (E-01, tek benchmark, tek artefakt); çalıştırılabilir görev sözleşmeleri (E-45, pertürbasyon görevleri); yargıçlar için Rogan–Gladen (E-25, ICML 2026, sohbet botu yargıları); Coin Flip (E-16, jailbreak yargıçları). Hiçbiri AgentLAB'i denetlemiyor; hiçbiri bu kontrolleri çok turlu ajan saldırıları için birleştirmiyor. Kendi ölçümlerimiz etkiyi zaten gösteriyor (`results/`). |
| **3** | **Tek atışlık (one-shot) ve uzun ufuklu saldırıların bütçe eşlemeli karşılaştırması** (denemeler, turlar, sorgular) ve oturum semantiği (taze ve kalıcı oturum) | 4 | 5 | 3 | **60** | Adaptive Adversaries (A-05: taze oturumlu savunucu, 15 tur); AgentLAB (A-01: tur eğrileri var, ama N-denemelik birleştirme). Kısmen AgentLAB'in saklanan sonuçlarından ücretsiz yapılabilir; tam sürümü için çalıştırma gerekir. |
| **4** | **Uyarlanabilir (adaptive) + uzun ufuklu saldırı altında, sürücü etkileşimiyle fiyatlandırılmış, araç durumunu bilen köken kapısı (provenance gate)** | 4 | 3 | 5 | **60** | CaMeL/ROPE/Progent (araç durumu yok; güçlü uyarlanabilir uzun ufuklu test yok, D-01/D-09/D-19); AgentSpec AV kuralları (D-24, saldırı yok); ideal onaylayıcı varsayan SPIDES onayları (D-07). Yeni kombinasyon: araç durumu + karar kökeni + onay bütçesi. |
| **5** | **Uzun ajan izlerinde yargıç ve koruyucu (judge/guard) güvenilirliği — karar modelleri (JEV) dahil** ve yargıcın kendisine yönelik saldırılar | 3 | 5 | 3 | **45** | JEV iz çalışması (E-40: geriye dönük sınıflandırma, saldırı altındaki bir döngünün içinde değil); Datadog sahte politika (E-41, satıcı); R-Judge/AgentAuditor (kısa izler). Küçük, sınırları belli bir alt soru (RQ1a). |

## Öneri
Tezi çekirdek olarak **sıra 1 + 2** üzerine kur (yeni bir araç içi uzun ufuklu saldırı paketine uygulanan geçerlilik öncelikli ölçüm protokolü). **Sıra 4** (araç durumunu bilen kapı) Savunma (Defense) bölümü olsun. **Sıra 3 ve 5** (bütçe eşleme; yargıç/JEV güvenilirliği) Değerlendirme (Evaluate) bölümünün içinde sınırlı alt sorular olsun. Bu plan ana riske karşı sağlamdır: CarDojo gecikirse (sıra 1), ölçüm protokolü (sıra 2) ve bütçe eşleme (sıra 3) yine de mevcut artefaktlar üzerinde yayımlanabilir bir ölçüm çalışması çıkarır (`06_roadmap.md` içindeki Scope A). Eşit puanlar yapılabilirliğe göre sıralanır.

## Değerlendirilen ama öncelik verilmeyen boşluklar
| Boşluk | Neden (şimdilik) değil |
|---|---|
| Araç içi ajanlara fiziksel/akustik enjeksiyon | kapsam dışı (gerçek araç yok); simülasyon ikna edici olmaz (V-07, A-48 donanım sonuçları) |
| Kokpit → sürüş ajanı zincirleme etkileri (VW CEA 2.0) | VW için çok önemli ama inandırıcı, iki alanlı bir test ortamı gerekir; Scope C uzantısı |
| Model düzeyinde eğitim savunmaları (SecAlign tarzı) | GPU eğitim bütçesi gerekir; uyarlanabilir saldırılarla defalarca kırıldı (D-39–D-42) |
| Yeni jailbreak teknikleri | çok kalabalık bir alan; ajana özgü değil |
| Koruyucu olarak gizli durum yoklamaları (hidden-state probes) (D-34) | yalnızca açık modeller; GPU varsa iyi bir isteğe bağlı uzantı |

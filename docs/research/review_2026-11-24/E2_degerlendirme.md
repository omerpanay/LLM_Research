# E2 — "Bu gerçekten saldırı mı?" Değerlendirme iddialarının kaynaktan doğrulanması

*Ömer için hazırlandı, 24 Kasım 2026. Konu: `docs/research/lit/evaluation.md` §1–§2'deki sayılar gerçek mi, hangi deneyden geliyor, yazarlar ne yaptı?*

## 0. Bunu nasıl kontrol ettim?

- **Makaleyi açtım.** Her makalenin PDF'ini arXiv'den indirdim (bazıları scratchpad'de zaten vardı), `pdftotext` ile metne çevirdim. Sayıyı, tabloyu ve cümleyi metin içinde aradım, çevresindeki paragrafı okudum. Gerekirse sayfayı görüntü olarak açtım (Lee et al. Figure 3).
- **Yayın yeri (venue).** OpenReview API'sinden `venue` alanına baktım (24.11.2026). Bulamadıysam arXiv sayfasındaki bilgiye baktım.
  - T1: Üst düzey konferansın hakemli ana programı.
  - T2: Hakemli workshop veya dergi.
  - T3: Hakemden geçmemiş ön baskı ya da reddedilmiş makale.
  - T4: Blog.
- **Kodu açtım.** AgentDojo'nun "brittle oracle" örneğini doğrudan AgentDojo kaynak kodunda kontrol ettim. Kullandığım kopya `agentdojo-inspect` reposu, v1 Slack görevleri.
- **Hesabı kendim yaptım.** Etiket sayısı hesaplarını Python ile kendim yaptım. Bunlar "**Hesap:**" diye işaretli. Scriptler şurada: `/tmp/claude-0/-home-user-LLM-Research/7b4b409f-0a1f-514a-ac3c-eb445351057c/scratchpad/scripts_e2/`.
- **Etiketler.**
  - DOĞRULANDI: Sayı, yer ve koşul kaynakla birebir tutuyor.
  - KISMEN: Sayı doğru ama koşulu daha dar, ya da yorum fazla genellenmiş.
  - YANLIŞ: Sayı ya da iddia kaynakla tutmuyor.
  - AÇILAMADI: Tam metne ulaşamadım.
- **Benim yorumum.** "**Çıkarım:**" diye başlayan satırlar kaynaktan değil, benim yorumum.
- **Alıntı kuralı.** Yazar alıntısını yalnızca yazar onu bir deneyle destekliyorsa alıyorum. Desteklemiyorsa bunu açıkça yazıyorum.

## Özet tablo

| # | İddia | Hüküm | Kaynak / tier |
|---|---|---|---|
| 1 | ASB GPT-4o ASR 73.58 → 9.25; "most of the original attack success…"; AgentDojo verinin üzerine yazıyor; UA 60.87 → 72.19; "exactly one more message" | **KISMEN.** Sayılar tabloda var. Ama 73.58 aslında *delimiters savunmalı* satır. Savunmasız satır 67.50. Llama-3.3-70B'de düşüş küçük (62.58 → 52.92), yani alıntıdaki genelleme yalnızca GPT-4o için deneyle destekli. | E-01, T2 (NeurIPS'25 Lock-LLM workshop; ICLR'26 reddedildi; TMLR'de inceleniyor) |
| 2 | "Mistral appeared vulnerable on all 64 tasks, but only 26…"; %75–100 | **KISMEN.** Sayılar doğru. Ama 26, *sözleşme + eşik* kuralının birlikte sonucu. Yalnızca sözleşmeyle Mistral 48/64 görevde gerçekten kırılıyor. | E-45, T3 (arXiv) |
| 3 | Hakemler "near random chance"a düşüyor | **DOĞRULANDI** (koşullu): sohbet jailbreak'i, 4 sınıflandırıcı hakem, dengelenmiş alt küme | E-16, T1 (ICML 2026) |
| 4 | Zararsız sarmalayıcılar LLM hakemini %57–100 çeviriyor | **DOĞRULANDI** (dar koşul: 3 küçük açık model, 4-bit) | E-46, T3 (tek yazar, ön baskı) |
| 5 | WASP %17–86 ara başarı, ≤%16 uçtan uca | **DOĞRULANDI.** Not: ara başarıyı GPT-4o hakemi ölçüyor ve bu hakemin doğrulandığını metinde bulamadım. | E-02, T1 (NeurIPS'25 D&B) |
| 6 | Düşük ASR çoğunlukla "görmezden gelme" (%76–80) | **DOĞRULANDI** (2–14B açık modeller) | E-44, T3 (ACL ARR Ekim 2026 başvurusu) |
| 7 | Sıcaklık 0'da jitter %5.0 / %6.8; rubrik yeniden yazımı %9.1'e kadar çeviriyor | **DOĞRULANDI.** Küçük not: aynı tabloda Gemini T1 için %10.4 var. | E-18, **T1** (NeurIPS 2026 E&D spotlight; OpenReview'da artık doğrulandı) |
| 8 | GPT-4o-mini %45.7 FPR; test-retest %3–15 | **DOĞRULANDI (yalnızca özet).** PDF açılmadı. | E-21, T2 (NeurIPS'26 JUDGe workshop oral) |
| 9 | En iyi BIPIA dedektörü AgentDojo'da %2.1 yakalıyor (FPR %1'de); FPR "none to over 90%" | **DOĞRULANDI** | E-12, T3 |
| 10 | Rogan–Gladen düzeltmesi (ICML 2026) | **DOĞRULANDI.** Ama "m≈200 yeter" cümlesi uç bir örneğe ait, genellenemez (bkz. §10). E-26 da artık **T1** (ICML 2026), `sources.csv`'deki T3 yanlış. | E-25 T1, E-26 T1 |
| 11 | "Plasebo kolu" | Literatürde bu adla **bulunamadı**. Tezin kendi önerisi (evaluation.md M1). Destekleyen ve motive eden kaynaklar §11'de. | — |

---

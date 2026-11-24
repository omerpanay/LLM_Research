# JEV: nerede iyi, nerede kötü? Hakem mi, bekçi mi, başka bir şey mi?

*Hazırlayan: araştırma alt-ajanı, 24 Kasım 2026. Tez: araç içi LLM ajanlarının uzun ufuklu saldırılara dayanıklılığı. Hocanın sorusu: "JEV hangi durumlarda iyi, hangilerinde kötü; judge olarak mı, guard olarak mı, başka bir şey olarak mı kullanalım?"*

**Okuma kuralları**
- Her sayının yanında kaynak yeri (tablo/bölüm) ve tier var. T1 = hakemli üst konferans/dergi, T2 = workshop, T3 = preprint (arXiv), T4 = blog/üretici/GitHub.
- **Önemli:** JEV hakkında okuduğum çalışmaların **hiçbiri hakemli değil.** Akademik olanların hepsi arXiv preprint (T3). Geri kalanı üretici, şirket blogu veya GitHub (T4). T1/T2 kanıt yok.
- "Çıkarım:" ile başlayan cümleler benim yorumum. Kaynağın söylediği şey değil.
- Bir makale yalnızca accuracy veriyorsa öyle yazdım. Precision/recall'u yalnızca karışıklık sayıları (TP/FP/TN/FN) yayımlanmışsa kendim hesapladım ve hesabı gösterdim.
- Bütün akademik çalışmalar `jev-1.13.0` ya da `jev-1.14.0` sürümünü test ediyor. Sürüm her satırda belirtildi.

---

## 0. Kısa cevap (60 saniyede)

1. **Okunabilen kararlarda iyi, türetilmesi gereken kararlarda kötü.** Cevap metinden doğrudan okunabiliyorsa JEV, GPT-6'ya 3 puan içinde yaklaşıyor. Bunu GPT-6 ücretinin %0,36'sına ve 0,15 s medyan gecikmeyle yapıyor. Matematik, kod, mantık ve uzman bilgisinde 7–28 puan geride kalıyor (CMU, T3).
2. **Ajan izlerinde iyi bir ön eleyici (screener), tek başına hakem değil.** 5.219 izde ortalama F1 77,8, en iyi üretken hakem GLM-5.2 74,1. Ama JEV'in ortalama precision'ı 77,1, GLM'inki 91,9. JEV daha çok yanlış alarm veriyor; MCPHunt'ta FPR %16,6, GLM'de %2,1 (USTC, T3; FPR'yi karışıklık sayılarından ben hesapladım).
3. **Saldırıya karşı zayıf, özellikle kendi karar formatına yazılmış saldırılara.** Sahte politika ("counterfeit policy") eklenince prompt-injection tespitinde recall %82,90'dan %3,88'e, F1 %90,51'den %7,46'ya düşüyor (Datadog, T4). Sıradan "ignore previous instructions" türü saldırılar ise JEV'e genelde işlemiyor. Yani **zayıf saldırılarla test edilen JEV yanıltıcı biçimde sağlam görünür.** Sonraki çalışmalar bunu doğruluyor: kanıt yarıştırma saldırısı R-Judge'da jev-1.14'e karşı %65,13 ASR (S1-EC, T3). Hakeme yazılmış "değerlendiriciye not" jev-1.14'ün doğru kararlarının %23,3'ünü çeviriyor; üretken hakemlerde bu oran %0,4–2,3 (Scale AI, T3).
4. **Pahalı hakeme yönlendiren bir ilk aşama (router/cascade) olarak iyi.** Önceden dondurulmuş eşikle, GPT-6'dan 0,93 puan daha doğru, GPT-6 ücretinin %41,4'ü (CMU Tablo 4, T3). Ama kazanç sınırlı, çünkü JEV ile LLM hakemler aynı yerlerde yanılıyor: JEV'in en emin hatalarında LLM kararlarının %96,0'ı aynı yanlış cevabı veriyor (UPenn, T3).
5. **Tavsiye.** JEV'i (a) **izleri önceliklendirme ve insan etiketlemesine ön-etiket** aracı, (b) **cascade'in ucuz ilk aşaması** olarak kullan. ASR'nin nihai hakemi yapma; o iş **durum kâhini (state oracle)** veya insanın. Online **bekçi (guard)** olarak yalnızca savunma katmanlarından biri olabilir. Tek başına bekçi olmamalı, ve önce politika şeklindeki yüklerle (policy-shaped payloads) red-team edilmeli.

---

## 1. Kaynak listesi ve okuma durumu

| ID | Kaynak | Tür / tarih | Tier | Bu çalışmada okuma durumu |
|---|---|---|---|---|
| S1 | Li, Miao, Krishnan, Padman (CMU), *JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*, arXiv 2609.26550 v6 | Preprint, 29 Eki 2026 | T3 | Tam metin, ana gövde §1–10 ve Ek A (Tablo 6) okundu. Diğer ekler hedefli okundu. |
| S2 | Rao, Callison-Burch (UPenn), *Decision Models vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places*, arXiv 2609.29769 v3 | Preprint, 13 Eki 2026 | T3 | Ana gövde, Limitations, Tablo 2–3 okundu. Ekler (A–R) okunmadı. |
| S3 | Wang, Gao (USTC), *JEV as a Judge for Agent Trace Security*, arXiv 2609.34862 v1 | Preprint, 28 Eyl 2026 | T3 | **Tam PDF indirildi ve okundu**, Ek A–G dahil. |
| S4 | Deußer, Ramamurthy, Sparrenberg, Sifa, *Evaluating and Benchmarking the System One Model Jev*, arXiv 2609.37647 v2 | Preprint, 29 Eki 2026 | T3 | Tablo 2, 3 ve §4.1.3 okundu (moderasyon, injection, eşik). Ardışık görevler §5 okundu. |
| S5 | Lan, Liu vd. (Penn State), *DecisionRobust*, arXiv 2610.19118 v1 | Preprint, 13 Eki 2026 | T3 | §1–3, Tablo 3, Tablo 4, Tablo A4 okundu. |
| S6 | Wang, Zhu vd., *Hidden Risks of Jev: An Empirical Study of Security, Privacy, and Dual Use*, arXiv 2610.04985 v1 | Preprint, 4 Eki 2026 (IEEE şablonu, yayın yeri "TBD") | T3 | §IV-A (Tablo I) ve §V (tespit, Şekil 8) okundu. Gizlilik bölümleri göz atıldı. |
| S7 | Wu, Lim (NTU), *Decision Hijacking: Prompt Injection Attacks on Jev's Typed Probabilistic Decisions*, arXiv 2609.28613 v1 | Preprint, 23 Eyl 2026 | T3 | §1–5 ve Tablo 1–2 okundu. **Yeni kaynak**, önceki notlarda yok. |
| S8 | Hu, Zhang vd., *JevAdvBench*, arXiv 2609.31142 v2 | Preprint, 26 Eki 2026 | T3 | Yalnızca özet ve §1. **Yeni kaynak.** |
| S9 | Wang, Li vd., *S1-EC: Offline Experience-Guided Evidence Competition Attacks on Typed System-1 Decision Models*, arXiv 2611.16937 v2 | Preprint, 13 Kas 2026 | T3 | §1–5, Tablo 1, 2, 4, 7 okundu. **Yeni kaynak.** (Arama sonucu başlığı "S1-Evo" diyordu; PDF'teki başlık "S1-EC".) |
| S10 | Subramanian (Scale AI), *To Jev or Not to Jev: When Can System-1 Decision Models Replace LLM Judges?*, arXiv 2611.00505 v1 | Preprint, 31 Eki 2026 | T3 | Özet, §2–3, Tablo 1, Ek E.5, Tablo 21 okundu. **Yeni kaynak.** |
| S11 | Ghadamyari, Habibi, *Decision Models as Retrieval Gates Against Injection and Pollution*, arXiv 2611.08325 v1 | Preprint, 5 Kas 2026 | T3 | Tam metin, kısa makale. **Yeni kaynak.** Konusu Kev, JEV değil. |
| S12 | Liu, Fan, Fu, *Is Jev a Good Multilingual Judge?*, arXiv 2611.14861 v1 | Preprint, 11 Kas 2026 | T3 | **Yalnızca özet.** **Yeni kaynak.** |
| V1 | TypeSafe: lansman yazısı, *Model jaggedness*, *Models*, *Changelog*, *Legal*, *Enterprise*, *Guardrails for LLMs* cookbook | Üretici, Eyl–Kas 2026 | T4 | Sayfalar curl ile çekilip okundu (24 Kas 2026). Enterprise SSS cevapları açılır kutuda olduğu için okunamadı. |
| V2 | Frichette, Al-Kassar (Datadog Security Labs), *Jev as a judge: How counterfeit policy steers Jev* | Şirket araştırma blogu, 15 Eki 2026 | T4 | Tam metin okundu, tüm tablolar dahil. |
| V3 | LangChain, *Building a Harness with Jev* (17 Eyl) ve *Building Prod with Jev and LangGraph* | Şirket blogu | T4 | Tam metin okundu. |
| V4 | Ruchith1018, *jev-guardrail-evaluation* (GitHub README) | Bağımsız, hakemsiz | T4 | Yalnızca README. Rakamlar doğrulanmadı. **Yeni kaynak.** |

**Kapsama notu.** Görevdeki "CMU çalışması E-35" = S1. "İz çalışması E-40" = S3. "DecisionRobust E-37" = S5. "Datadog E-41" = V2. "LangChain E-42" = V3. "TypeSafe E-34" = V1.

---
## 2. Kanıt dökümü: kaynak kaynak, sayılar aynen

### 2.1 S1: CMU, JEV-as-a-Judge (T3, jev-1.13.0)
**Kurulum.** JEV, 16 başka hakemle (14 üretken LLM, 2 reward model) karşılaştırılıyor. Toplam 5.172 temel yargı var:
- 1.500 RewardBench çifti,
- 350 JudgeBench çifti,
- 3.000 HaluEval cevabı,
- 150 nihai cevap.

Üretken hakemler de JEV'in çıktı sözleşmesiyle cevap veriyor: bir karar ve etiket olasılıkları, gerekçe yok. Etiketlerin sorunlu olabileceği yerlerde 183 kör insan değerlendirmesi (adjudication) yapılmış. Metrik **accuracy**. Sadece nihai-cevap setinde ayrıca macro-F1 var. Precision/recall raporlanmıyor.

| Ne | Sayı | Yer |
|---|---|---|
| RewardBench accuracy | JEV 92,5 / GPT-6 92,5. Fark 0,0 [−1,4; 1,4] | §5, Tablo 1 |
| HaluEval accuracy | 87,3 / 88,4. Fark −1,1 [−1,9; −0,3] | §5, Tablo 1 |
| Nihai cevap | 94,0 / 96,7. Macro-F1 0,923 / 0,947 | §5 |
| JudgeBench (zor doğruluk) | 78,6 / 93,1. Eşleştirilmiş fark −14,6 [−18,9; −10,3]. İnsan değerlendirmesiyle −16,0 [−20,0; −12,3] | §5, Tablo 2 |
| Beceri bazında (okunan kararlar) | Sohbet kalitesi 86,1 / 83,9. Zararlı isteği reddetme 96,5 / 94,5. Uyması gereken istek 88,3 / 89,9. Kanıta dayalı doğruluk 87,3 / 88,4 | §6, Şekil 4a |
| Beceri bazında (türetilen kararlar) | Uzman bilgi −7,0. Kod −12,9. Matematik −14,3. Mantık bulmacası −27,6 (68,4 / 95,9) | §6 |
| Stil-çelişkili çiftler (RM-Bench hard) | 76,6 / 90,1. Fark −13,5 [−16,2; −10,9] | Tablo 2 |
| Referanssız düzyazı | 53,5 (GPT-5.4: 56,0). "Not supported". Hata tespiti AUROC 0,498 | §6, Tablo 2 |
| Maliyet / gecikme | $0,044 / 1.000 yargı. GPT-6 $12,182. Medyan 0,15 s, GPT-6 1,89 s. p95 0,24 s, GPT-6 3,86 s | §5, Tablo 1, Şekil 3 |
| Genel sıralama | 4.850 kamu yargısında 15 LLM hakem içinde 8. sırada. GPT-6'nın 1,7 puan gerisinde | §5 |
| Güven = hata işareti | q ≥ 0,9 olan 3.744 maddede JEV 94,7, GPT-6 94,4. q < 0,9 olan 1.106 maddede 67,7 / 75,0. Görev içi hata AUROC'u RewardBench 0,875, JudgeBench 0,745, HaluEval 0,827. GPT-6: 0,894 / 0,907 / 0,831 | §7 |
| Emin hatalar (q ≥ 0,9, tek çağrı) | RewardBench %2,1 (24/1.155), JudgeBench %6,5 (9/138). GPT-6: %3,5 / %2,0 | §6 sonu |
| Kalibrasyon (Brier) | JEV 0,113 / 0,297 / 0,196. GPT-6 0,115 / 0,095 / 0,213 (RB / JB / HaluEval) | §7 |
| Sıcaklık ölçekleme (temperature scaling) | Pilot sette fit edilince bir görevde iyileştiriyor, ikisinde kötüleştiriyor. Bulunan sıcaklıklar 0,65 / 2,15 / 4,45 | §7, Tablo 28 |
| Sıra hassasiyeti | Çiftin sırası değişince karar değişme oranı: RewardBench %3,7, JudgeBench %11,1 (GPT-6 %1,5 / %0,9). q ≥ 0,9 olan 1.293 çiftten yalnız 3'ü değişiyor | §7.3 |
| Tekrar / parafraz | 96 tekrar istekte 0 karar değişikliği. 48 parafrazda 4 değişiklik | §7 |
| **Cascade, dondurulmuş politika (τ = 0,9)** | 1.610 tutulmuş çift. %31,5'i yükseltiliyor ve bu küme JEV hatalarının %85'ini içeriyor. **Doğruluk 93,4, GPT-6 92,5 (+0,93 [0,24; 1,66]), maliyet GPT-6 ücretinin %41,4'ü** (muhafazakâr hesapla %44,0) | §8, Tablo 3–4 |
| Cascade, benchmark ayrımı | RewardBench: %25 yükseltme, +1,27, ücretin %26,7'si. JudgeBench: %65 yükseltme, 92,2 / 93,0 (−0,74), ücretin ~2/3'ü | §8 |
| Canlı tekrar | 510 çift. 92,5 / 93,1 (−0,59 [−1,95; 0,59]), ücretin %57,2'si. Medyan 0,27 s, GPT-6 tek başına 2,10 s | §8 |
| İleriye dönük canlı test | 2 yeni iş yükü, 570 çift. Doğruluk GPT-6 ile birebir aynı (PPE 88,2, JudgeBench-Claude 94,7). %68 ve %89 yükseltme. Ücretin %75,5'i | §9, Tablo 5 |
| Eşik için gereken etiket | Nokta kuralıyla, seçilen politika denemelerin %40–50'sinde 2 puandan fazla kaybediyor. Alt güven sınırı kuralıyla 96 veya 192 etikette ~%5. İş yükü başına ayrı eşikle 96 etikette %0,6 | §8, Tablo 32 |
| Açık karar modelleri | 6 açık model JEV'in havuz doğruluğu (88,3) ile istatistiksel olarak ayırt edilemiyor. **Perplexity Decider v1.1 27B 89,0 (+0,8 [0,0; +1,5])**, hata AUROC 0,841, 84 ms. **Kev 27B 86,5 (−1,7 [−2,5; −1,0])**, AUROC 0,816, 77 ms. JEV AUROC 0,822, 152 ms (barındırılan API). Açık modeller tek H100'de koşuyor | Ek A, Tablo 6 |
| Sınırlar (yazarlar) | "Whether its decisions and confidence are as useful inside an agent ... is not tested here". "we cannot rule out that benchmark items were seen in training". "Confident errors ... argue against using any automated judge as the sole arbiter of consequential decisions" | Limitations, Ethics |

**Düzeltme.** Öğretici rapordaki (PDF) "JudgeBench'te 14,5 puan geride" ham farktır (93,1 − 78,6). Makalenin raporladığı eşleştirilmiş fark −14,6.

### 2.2 S2: UPenn, Rubric Judges (T3, jev-1.13.0 ve Perplexity Decider v1.1)
**Kurulum.** Dokuz panel, yedi benchmark, 5.003 çift. Rakipler üç "flash" seviye LLM hakem: GPT-5.6 Luna, Gemini 3.8 Flash ve DeepSeek V4.1 Flash. Metrikler: verdict accuracy ve exact accuracy, QWK, Cohen κ, AUROC, ECE. P/R/F1 yok.

| Ne | Sayı | Yer |
|---|---|---|
| Maliyet / süre | LLM hakemler JEV'den 16–325 kat pahalı, 28–350 kat yavaş. Decider'dan 18–357 kat pahalı, 5,4–67,5 kat yavaş | Özet, §4 |
| Doğruluk | JEV Choice 27 karşılaştırmanın 8'inde anlamlı fark gösteriyor (4 önde, 4 geride). 8'inde eşitlik, 11'i belirsiz. Önde olduğu yerler ikili panellerde, geride olduğu yerlerin hepsi sıralı (ordinal) panellerde | §4 |
| **Aynı yerde yanılma** | "For Jev, 242 of the 252 LLM verdicts on these 84 pairs (96.0%) repeat its answer, against 50.3% expected." Decider için 218/252 = %86,5 (beklenen %47,9) | §5.2, Tablo 2 |
| Güven → hata sıralaması | Altı sıralı panelde AUROC 0,57–0,70. ELLIPSE'te 0,49. İkili panellerde P(MET) AUROC 0,80–0,86, ECE 0,056–0,096 | §6.1 |
| Cascade kazancı | Kehanet (oracle) eşiklerle bile flash fallback'lerle en fazla +2,7 puan. Çapraz-fit eşiklerle en fazla +1,5. Üst seviye fallback'lerle en fazla +1,7 | Özet, §6, Tablo 3 |
| Kararlılık | RiceChem üzerinde 5 geçişte JEV çiftlerinin ~%3'ü en az bir kez karar değiştirdi | Limitations |
| Decider lisans/veri | "fine-tune of Qwen3.8-27B with Apache-2.0 open weights". 626.033 eğitim satırının 530.103'ü tasksource'tan, aralarında HelpSteer2 etiketleri de var. Sentetik satırlar gpt-5.6-sol ile etiketlenmiş | Limitations |

**Düzeltme.** Sunum paketi §7.3 "LLM verdicts repeat 242 of JEV's 252 most confident errors" diyor. Doğrusu şu: JEV'in en emin 84 hatalı çiftinde, üç LLM hakemin toplam **252 kararından 242'si** JEV ile aynı yanlış cevabı veriyor. Yani 252 "hata" değil, 252 "LLM kararı".

### 2.3 S3: USTC, ajan izlerinde güvenlik hakemi (T3, JEV sürümü makalede açıkça yazılmıyor)
**Kurulum.** Dört koleksiyondan 5.219 iz: R-Judge 564, ATBench500 500, TraceSafe alt kümesi 540, MCPHunt 3.615. Her hakem 1–5 risk puanı veriyor ve **s ≥ 3 pozitif** sayılıyor. JEV tek istekte dört tipli soru alıyor: risk Score, authorization Choice, safety Choice, severity Score. Rakipler dört üretken hakem: GLM-5.2, DS-V4-Flash, DS-V4-Pro, Qwen3-Next. Metrikler pozitif sınıf P/R/F1 ve accuracy, her hakemin kendi geçerli cevapları üzerinde. Ayrıca kapsama (coverage) ve doğru karar verimi (yield) var. **TraceSafe ve MCPHunt'ta yazarların revize ettiği etiketler kullanılıyor** (§4.1).

Dört benchmark ortalaması (Tablo 2):

| Hakem | Geçerli | Kapsama | Ort. P | Ort. R | Ort. F1 | Ort. Acc |
|---|---|---|---|---|---|---|
| JEV | 4.982 | %95,5 | 77,1 | 79,2 | **77,8** | 82,8 |
| GLM-5.2 | 4.927 | %94,4 | 91,9 | 64,1 | 74,1 | 86,5 |
| DS-V4-Flash | 5.214 | %99,9 | 51,6 | 75,6 | 61,0 | 61,5 |
| DS-V4-Pro | 3.070 | %58,8 | 93,3 | 49,4 | 56,3 | 92,1 |
| Qwen3-Next | 4.926 | %94,4 | 92,0 | 37,2 | 49,4 | 76,4 |

Benchmark bazında, JEV ve GLM-5.2 (Tablo 3; karışıklık sayıları Tablo 8). **Karışıklık sayıları yayımlandığı için P, R ve FPR'yi kendim yeniden hesapladım.** P ve R makaleyle birebir tutuyor. FPR makalede yok, onu ben ekledim.

| Benchmark | Hakem | TP / FP / TN / FN | P = TP/(TP+FP) | R = TP/(TP+FN) | F1 | **FPR = FP/(FP+TN)** (hesap) |
|---|---|---|---|---|---|---|
| R-Judge | JEV | 250 / 20 / 246 / 45 | 250/270 = 92,6 | 250/295 = 84,7 | 88,5 | 20/266 = **%7,5** |
| R-Judge | GLM | 255 / 2 / 262 / 34 | 99,2 | 88,2 | **93,4** | 2/264 = %0,8 |
| ATBench500 | JEV | 241 / 30 / 218 / 2 | 241/271 = 88,9 | 241/243 = 99,2 | **93,8** | 30/248 = **%12,1** |
| ATBench500 | GLM | 140 / 5 / 232 / 41 | 96,6 | 77,3 | 85,9 | 5/237 = %2,1 |
| TraceSafe | JEV | 166 / 64 / 191 / 94 | 166/230 = 72,2 | 166/260 = 63,8 | 67,8 | 64/255 = **%25,1** |
| TraceSafe | GLM | 130 / 11 / 250 / 88 | 92,2 | 59,6 | **72,4** | 11/261 = %4,2 |
| MCPHunt | JEV | 531 / 439 / 2.207 / 238 | 531/970 = 54,7 | 531/769 = 69,1 | **61,1** | 439/2.646 = **%16,6** |
| MCPHunt | GLM | 225 / 57 / 2.699 / 496 | 79,8 | 31,2 | 44,9 | 57/2.756 = %2,1 |

Diğer sonuçlar:
- **Ortak geçerli örneklerde** JEV ile GLM: 76,8 / 74,1, fark +2,7, keşif amaçlı bootstrap aralığı [0,5; 4,8] (Ek B, Tablo 6). Benchmark bazında: R-Judge −5,0, ATBench +8,6, TraceSafe −7,1, MCPHunt +14,2.
- **Maliyet ve gecikme** (Tablo 4): JEV medyan 0,99 s, p95 2,02 s, $0,000195 / geçerli karar. GLM medyan 33,29 s, $0,014887.
- **İz uzunluğu** (Ek E, Tablo 9): adım sayısı > 16 olan izlerde JEV F1 57,5, GLM 50,6. ≥ 8k token izlerde 62,8 / 48,7. **Ama** MCPHunt çıkarılınca uzun kovalarda GLM önde: > 16 adımda 70,0 / 73,1, ≥ 8k token'da 69,6 / 73,2 (Tablo 11). Yazarlar da uzunluk eğiliminin benchmark bileşimine duyarlı olduğunu söylüyor.
- **Yazarların önerdiği rol:** "economical screening signal"; "screening-and-escalation pipeline in which compact judgments prioritize traces for further investigation" (Özet, §6).
- **Sınırlar:** revize edilmiş etiketler, tek eşik, eksik çıktılar. "Future studies could use independently reviewed labels" (§6). Hakeme yönelik saldırı **test edilmemiş**.

Çıkarım: JEV'in F1 üstünlüğü yüksek recall'dan geliyor, bedeli yüksek FPR. Önceliklendirme ve ön eleme için bu iyi, çünkü kaçırmak pahalı ve fazla işaret insan tarafından ayıklanır. Otomatik engelleme veya nihai ASR için kötü: TraceSafe'de güvenli izlerin dörtte biri "riskli" işaretleniyor.

### 2.4 S4: Deußer vd., 37 veri seti (T3, jev-1.13.0)
Tablo 2 ve ek tablo, sabit 0,5 eşik:

| Görev | Sayı |
|---|---|
| deepset/prompt-injections (116 örnek, Noul) | Accuracy **0,741**, %95 GA [0,664; 0,828], **ECE 0,236**. Qwen3.8-27B 0,767 (ECE 0,248). Gemma-4-E4B 0,664 (ECE 0,322) |
| Aynı set, metinde (§4.1.3) | "precision is perfect but recall is only 50%, although the AUROC is 0.982" |
| ToxicChat jailbreak F1 | 0,5 eşikte 0,717. Ayarlanmış eşikte 0,833 (Tablo 3; eşik 0,85'e çıkıyor) |
| Zararlı içerik AUROC | ToxiGen 0,949. ToxicChat 0,989 (toxicity) ve 0,994 (jailbreak). OpenAI moderation ort. 0,972 |
| Ardışık karar (ALFWorld) | Başarı %35,1 (uzman %90,3). Adım doğruluğu %17,9. Ortalama en üst olasılık 0,43, ECE 0,247: tek adımlı Choice'a göre aşırı emin |

Çıkarım: Sıralama iyi (AUROC yüksek), ama sabit 0,5 eşik injection'da recall'u yarıya indiriyor. **Eşik yerel veriyle ayarlanmadan JEV bir guard olarak kullanılmamalı.** Çok adımlı ajan döngüsünün kendisinde JEV zayıf (ALFWorld).

### 2.5 V2: Datadog, sahte politika (counterfeit policy) (T4, Eki 2026; JEV sürümü belirtilmemiş)
**Kurulum.** Dört kamu prompt-injection veri seti, toplam 12.295 örnek: 4.643 saldırı, 7.652 iyi niyetli. JEV'e iki soru soruluyor: Noul `has_prompt_injection` (0,5 eşik) ve Choice `attack_category`. "Counterfeit policy" mesajın başına ekleniyor. Bu politika istenen cevabı veriyor, orijinal mesajı "istisna" ilan ediyor ve saldırı kategorilerini alakasız şeylere yeniden tanımlıyor ("credential access" = kapı anahtarı sormak gibi).

Noul (has_prompt_injection), yazının tablosundan aynen:

| Girdi | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| Ham | 3.849 | 13 | 794 | **99,66%** | **82,90%** | **90,51%** |
| Sahte politika eklenmiş | 180 | 0 | 4.463 | 100,00% | **3,88%** | **7,46%** |

**Doğrulama:** 3.849 / (3.849 + 13) = %99,66. 3.849 / 4.643 = %82,90. 180 / 4.643 = %3,88. Hepsi tutuyor.

FPR: yazı TN vermiyor. Benign toplam 7.652 ve her örnek geçerli cevap aldıysa FPR = 13 / 7.652 = **%0,17**. Bu benim hesabım ve "her örnek cevap aldı" varsayımına dayanıyor.

Choice (attack_category): ham P 99,45%, R 85,46%, F1 91,93%. Sahte politikayla P 99,56%, R 9,69%, F1 17,66%.

Veri seti bazında (Noul): zachz ve Yanismiraoui setlerinde recall %0. DeepSet F1 72,46 → 5,19. xTRam1 F1 90,40 → 10,42.

**Araç-çağrısı engelleme senaryosu (LangChain tool-risk gating, `is_risky ≥ 0,5` ise engelle).** Kullanıcı yetkisiz: `can_edit: false`, viewer. 40 koşuda ortalama is_risky **0,893**, 40'ının 40'ı engellendi. Kullanıcının düzenleyebildiği `profile_description` alanına sahte `is_risky` tanımı konunca ortalama **0,290**, eşiğin altında. Sahte system/assistant mesajlı düz prompt injection ise ortalama **0,905** verdi, yani taban çizgisinden yüksek. "hundreds of additional prompt injection attempts" sonucunda da ortalama tabana yakın kaldı.

Not: Yazı Datadog'un kendi AI Guard ürününü tanıtan bir bölüm içeriyor. Çıkar çatışması olabilir, bu da T4 olmasının bir sebebi.

### 2.6 S5: DecisionRobust (T3, jev-1.13.0; saldırılar Jev üzerinde inşa edilmiş)
- **Tablo 3.** Bozulma (perturbation) saldırıları Jev'in olasılıkları kullanılarak Jev üzerinde inşa edilmiş, yani Jev'e karşı en iyimser saldırgan durumu. Tüm veri setlerinde (1.332 örnek) birleşik ASR: **ham 69,7, etiket-kontrollü 36,6**. Etiket kontrolü şu demek: iki dış LLM bozulmuş girdide de doğru cevabı bulabiliyor olmalı, yoksa "saldırı" aslında doğru cevabı değiştirmiş sayılır. Transfer hedeflerinde kontrollü ASR: KEV 20,0, AutoTrust 12,5, OpenJEV 12,8, Bosun 22,5, Liquid D1 19,5.
- **Injection tespit görevi olarak PromptShield'de** Jev Choice ham 95,5 / kontrollü **77,3**, Noul 95,6 / **60,0** (Tablo 3). Çıkarım: JEV bir injection dedektörü olarak kullanılırsa, anlamı koruyan küçük metin oynamalarıyla bile çoğu doğru karar çevrilebiliyor. Bu sonuç beyaz kutuya yakın, skor erişimli bir saldırganla elde edildi.
- **Agent traces** satırı (N = 13–14, çok küçük): Choice 0,0 / 0,0. Score 91,7 / 58,3.
- **Tablo 4 / A4, prompt injection.** Tüm veride, iki konum birlikte, flip/target ASR: **Jev 54,4 / 49,6**, KEV 22,5 / 18,3, AutoTrust 64,6 / 60,7, OpenJEV 86,3 / 82,5, Bosun 47,9 / 41,1, Liquid D1 28,7 / 23,2.
- Araç seçimi (BFCL, Choice), Jev injection flip/target: **96,7 / 96,7** (Tablo A4). Skill Router 12,5 / 12,5. Agent traces Score 75,0 / 33,3 (N = 13).
- "Target ASR is always below flip ASR, so a wrong decision need not match the attacker target" (§3.2.2).
- Perplexity Decider v1.1-27B (görsel setlerde): bozulma ASR'si en düşük (%3,2), ama talimat injection'da hedef ASR %45,7 (§3.3). Yazarların yorumu: "resistance to perturbations need not extend to injection".

### 2.7 S6: Hidden Risks of Jev (T3, resmi Jev API)
**Tablo I.** Karar katmanı olarak Jev. Üç görev: destek yönlendirme (Choice), abonelik iptali (Noul), sorun ciddiyeti (Score). Her görevde GPT-4o ile üretilmiş 200 durum, her değerlendirme 3 kez tekrar edilmiş. Temiz accuracy üç görevde de %100, temiz ASR %0.

| Saldırı (Jev) | Yönlendirme ASR | İptal ASR | Ciddiyet ASR |
|---|---|---|---|
| Context ignoring | 96,5 | 100,0 | 47,0 |
| Fake completion | 2,5 | 88,5 | 18,8 |
| Role spoofing | 93,5 | **0,0** | 86,7 |
| Persuasive appeals | 59,3 | 100,0 | 1,7 |
| Jev-specific injection (durum "eski/yanlış" + sahte kanıt) | 100,0 | 100,0 | 97,2 |
| Universal suffix | 100,0 | 100,0 | 97,0 |

**Şekil 8.** Jev tespit aracı olarak, 8 benchmark: ROC-AUC **0,95–1,0**, kalibre edilmiş eşikle 6 güvenlik benchmark'ında **accuracy %87–99**. Prompt injection için Tensor Trust (500/500) ve BIPIA (180/180) kullanılmış. **Yalnızca accuracy ve ROC-AUC raporlanıyor.** Benchmark bazında kesin değerler yalnız şekilde, metinde aralık var. Precision/recall yok.

Önerilen azaltımlar (§VI-A): güvenilir bağlamı güvenilmez içerikten ayırmak, ama "field separation alone does not guarantee this behavior". Güvenlik açısından hassas eylemlerde Jev'in kararını güvenilir veriyle doğrulamak ve yürütmeden önce yetkiyi zorunlu kılmak.

### 2.8 S7: Decision Hijacking (T3, jev-1.13.0) — yeni
**Kurulum.** InjecAgent'in doğrudan zarar bölümünden 510 vaka yeniden kurulmuş. Burada JEV **bekçi değil, ajanın eylem seçicisi**: zararlı içeriği okuduktan sonraki ilk güvenlik-kritik kararı veriyor. Seçenekler: görevi bitir / kullanıcı aracı / saldırganın aracı. Ana çalışmada 54.060 çağrı var.

| Ne | Sayı | Yer |
|---|---|---|
| Orijinal saldırı | ASR **%1,8** (9/510). Saldırganın olasılığı ortalama +0,043 | §5.1, Tablo 2 |
| "IMPORTANT!!! Ignore all previous instructions" eklenince | ASR **%0**. Olasılık etkisi −0,034 [−0,062; −0,015] | §5.1 |
| Uyarlamalı saldırı, skor erişimli, 24 sorgu | Doğrulanmış ASR %1,8 → **%3,5** [0,0; 10,0]. Güvenle (≥ 0,7) ele geçirme oranı %0,2 | §5.4 |
| Başarı koşulu | Sınıra yakın gömülü vakalarda 12/12 başarı. Sınırdan uzak gömülü vakalarda 1/468 | §5.5 |

Çıkarım: Generic injection'lar JEV'in seçimini nadiren çeviriyor. Bu Datadog'un "düz injection işe yaramadı" gözlemiyle tutarlı. Ama aynı JEV, kendi sözleşmesine yazılmış saldırılara (S6, S9, V2) karşı çok zayıf. **Saldırı ailesi sonucu belirliyor.** Bir tezde "JEV injection'a dayanıklı" demek için generic saldırılar yetmez.

### 2.9 S8: JevAdvBench (T3, jev-1.13.0) — yeni, yalnızca özet okundu
Özetten aynen:
- "The attacks flip 46.3% of Jev's correct decisions, while identical re-runs flip only 0.17%."
- "A flawed argument without a command flips 77.2%, close to direct prompt injection at 92.0%."
- "The same variants flip 34.0% to 51.7% of correct decisions on eight open TDMs."
- "At a 0.8 threshold, 23.5% of the decisions that the service still executes are wrong."
- "On Agentgateway, the Jev guardrail rejects a jailbreak request but accepts it with an inserted argument."

Veri: 862 soru ve 5.586 cevabı koruyan varyant.

### 2.10 S9: S1-EC, kanıt yarıştırma saldırısı (T3, jev-1.14 / jev-1.13 / kev-4B) — yeni
**Kurulum.** Saldırgan komut yazmıyor. Güvenilmez alana, doğru seçenekle yarışan "kanıt" ekliyor. Saldırılar önce ayrı seed görevlerde çevrimdışı öğreniliyor, sonra yeni görevlere sorgusuz uygulanıyor.

| Ne | Sayı | Yer |
|---|---|---|
| jev-1.14, 4 benchmark ortalaması | ASR **%71,99**. Yüksek güvenli ASR %57,47. Ortalama accuracy 92,02 → 20,28 | Özet, §5.2 |
| **R-Judge (ajan risk yargısı)**, jev-1.14 | Accuracy 83,08 → 17,95. **ASR %65,13**, HC-ASR %41,54 | Tablo 1–2 |
| R-Judge, jev-1.13 | ASR %68,72 | Tablo 2 |
| R-Judge, kev-4B | ASR %65,64 | Tablo 2 |
| R-Judge, **üretken Qwen-3.8-flash** | ASR **%2,05** (DecisionRobust'ta %4,00) | Tablo 2 |
| WildGuardTest (Score, güvenlik moderasyonu), jev-1.14 | ASR %65,00 | Tablo 1 |
| InjecAgent, jev-1.14 | S1-EC %87,33. Gramer tabanlı DH-72 %95,67 | Tablo 1 |
| Uçtan uca Guardrail ajanı (τ-bench uyarlaması; S1 allow/block/escalate) | Accuracy 98,00 → 80,67. S1 ASR %45,33, **E2E ihlal %17,33** | Tablo 4 |
| Uçtan uca Tool Router ajanı (AgentDojo uyarlaması) | S1 ASR %58,67, **E2E ihlal %24,00** | Tablo 4 |
| Savunmalar (jev-1.14) | Rule Reminder: DR ASR 70,5 → 43,5, WG 65,0 → 27,0. **Label Anonymization** (safe/unsafe yerine OPT_A/OPT_B): DR 38,0, WG 18,5 | Tablo 7 |

Çıkarım: Bu, **JEV'i ajan izi hakemi ya da guard olarak kullanmaya karşı en doğrudan kanıt.** Saldırıya özel kurulmuş bir girdiyle R-Judge doğruluğu 83'ten 18'e düşüyor. Aynı saldırı üretken bir modelde neredeyse hiç işlemiyor. Ek önemli nokta: bir S1 flip'inin hepsi ihlale dönüşmüyor (%38–41). Yani sistem düzeyinde başka katmanlar zararı kısmen yutuyor.

### 2.11 S10: Scale AI, "To Jev or Not to Jev" (T3, jev-1.14) — yeni
| Ne | Sayı | Yer |
|---|---|---|
| Kalibrasyon | Jev 1.14 ECE **0,019**, tüm hakemler içinde en iyi. Üretken hakemler 0,038–0,087 | Tablo 1, §3 |
| Hakem metnine gömülü "değerlendiriciye not" (evaluator note) | Jev 1.14 doğru Choice kararlarının **%23,3**'ünü çeviriyor. pplx-decider 1.2 %4,7. Kev-4B %32,2. Mercury-Decide %49,0. Üretken hakemler %0,4–2,3 (Opus 5.5 think 0,4, GPT-5.6 2,3, Haiku 5.5 2,3). Aynı boyuttaki üretken Qwen3.5-4B %77,3 | Tablo 1, Ek E.5 |
| JudgeBench (Choice, iki sıra ortalaması) | Jev 1.14 82,3. Referansla 91,4. GPT-5.6 think 93,1. Opus 5.5 think 94,7 | Tablo 1 |
| Routing (Jev veya pplx-decider → Opus) | LLMBar: %17 yükseltmeyle 91,7, Opus tek başına 91,7. Hata AUROC 0,71–0,90 | §3 |
| **AgentRewardBench (web ajanı izleri, n = 292), başarı tespiti, 0,5 eşik** | **Jev 1.14: P 87,5, R 53,3, F1 66,2, AUROC 0,895.** Yan etki F1 35,3, döngü F1 82,0. pplx-decider 1.2: P 77,4, R 70,7, F1 73,9, AUROC 0,921. Kev-4B: P 65,3, R 88,0, F1 75,0. GPT-5.6 think F1 72,3. Opus 5.5 think F1 67,6, AUROC 0,933 | Ek, Tablo 21 |

Yazarın sonucu: "Robustness to instructions injected into the judged response is a property of the individual model rather than of the System-1 design" (Özet).

Not: Enjeksiyon yükleri yazarın kendi JudgeBench/LLMBar pertürbasyonu, yerleşik bir injection benchmark'ı değil (§Limitations).

### 2.12 S11: Kev-4B retrieval bekçisi (T3) — yeni, JEV değil ama açık-model alternatifi için önemli
- **Kurulum.** 1.000 sorgu, gizli talimatlı forum sayfaları. Kev-4B her pasaja üç soru soruyor. Kev açık ağırlıklı, tek GPU'da koşuyor.
- **ASR (Llama-3.1-8B üretici):** savunmasız %27,9 → yayımlanmış azaltımlar %13,6 → **+Kev bekçisi %5,7**.
- **FPR** (insanlara yönelik talimat içeren iyi niyetli sayfalar): Kev **%2,2 (4/186)**. 70B LLM hakem %18,3.
- **Q1 AUROC** (HTML): Kev 0,94. Llama-3.3-70B 0,99. DeepSeek V4.1 Flash 1,00. Kev 76 ms ve $0,015 / 1.000 pasaj; büyük hakemler ~$0,15 ve 0,65–1,15 s (Tablo 1).
- **Bekçinin skorunu gören uyarlamalı saldırgan:** her sayfa 0,35'in altına indi, ama ASR %3,5 kaldı. Yazarların açıklaması: "Rewrites that stop addressing the AI also stop being obeyed".

### 2.13 S12: Çok dilli hakem (T3, jev-1.13.0) — yalnız özet
Özetten: JEV, GPT-6.1 maliyetinin yaklaşık 1/31 ile 1/61'i arasında bir maliyetle çoğu çok dilli hakem görevinde rekabetçi. Bilgi yoğun cevap doğrulamada geride. "Jev is more likely to accept incorrect answers in low-resource languages than in English." Almanca için ayrı sayı okunmadı.

### 2.14 Üretici ve sektör (T4)
**TypeSafe "Model jaggedness" sayfası** 9 hata modu listeliyor. Bizim için önemli olanlar:
- #1 Literal okuma.
- #4 Dolaylılık (indirection).
- #5 "Large state full of irrelevant detail". Ayrıca "Jev suffers from context rot".
- #6 Adversarial content: "State is data, and Jev does not treat it as hostile by default. Content written to adversarially steer the model, whether that is an injected instruction, a deliberately misleading framing, or text that argues for its own classification, can move the answer." Önerilen önlem: "be explicit in the criteria. Test your integration thoroughly before deploying it".
- #8 Seçenek sırası ("leans toward the option that comes first").

**Lansman yazısı (15 Eyl 2026)** kullanım alanları arasında açıkça "Score, judge, verify, guardrail, and detect jailbreaks" sayıyor. Diğer iddialar:
- Kamu benchmark'ı yayımlamama tercihi: "deliberately chose *not* to publish performance against *public* benchmarks".
- Veri: "We make all the data ourselves".
- "can't hallucinate", yani tip-güvenliği anlamında.
- Konum: "our published evals are generally run from our laptops on the West Coast (this is where our service is currently based)".

**Models sayfası:**
- jev-1.14.0 ve jev-1.13.0 ikisi de $0,042 / M girdi token, çıktı ücretsiz.
- Bağlam: 64k istek başına, 32k soru başına.
- Uzun bağlam başlığıyla 262k, ama "slower and less accurate".

**Legal / Enterprise:**
- "commitment not to train models on user data".
- "Zero data retention is available for enterprise customers".
- SOC 2 Type II raporu talep üzerine.
- "Can we run Jev in our own VPC or on-premises?" ve "Where is our data processed?" soruları sayfada var, ama **cevapları okunamadı** (açılır kutu).

**Erişim yolları:** TypeSafe API (`api.typesafe.ai/v1/systemone`). Ayrıca OpenRouter "decisions API": GitHub değerlendirmesi `typesafe/jev-1.13-20260917` kullanıyor, Scale AI makalesi Tablo 2'de `typesafe/jev-1.14`.

**LangChain (17 Eyl):**
- "`AutoModeMiddleware` uses Jev to check tool calls for risky decisions it may take, and block calls before the tool executes."
- `ModelRouterMiddleware` model yönlendirme yapıyor.
- 25 Eyl yazısı: "In an early Jev-as-a-judge experiment, its scores barely moved across 100 repeated runs, far less than any LLM judge we tested". **Veri verilmemiş, kanıt sayılmamalı.**
- Browserbase vakası: 0,7 güven eşiğinin altı LLM'e düşüyor. Medyan act() gecikmesi 1,97 s → 0,46 s.

**TypeSafe "Guardrails for LLMs" cookbook:**
- İki eşikli politika öneriyor: review ve action. Örnek değerler: strict 0,35/0,70, permissive 0,70/0,85.
- Birkaç örnekle demo var. Metrik yok.

**GitHub bağımsız değerlendirme (V4), README'den, doğrulanmadı:**
- 6.991 çağrı.
- deepset'te AUC 0,986. ProtectAI 0,882, DeepSeek Flash 0,910.
- 0,5 eşikte saldırıların %58,6'sı yakalanıyor, 399 güvenli istemin 0'ı engelleniyor.
- deepset'in yarısında ayarlanmış 0,12 eşik diğer yarıda %81,7 yakalıyor. Ama aynı eşik belge sorusunda temiz belgelerin %74,7'sini engelliyor.
- NotInject: güvenli istemlerin %0,6'sı işaretleniyor (ProtectAI %43,4).
- Zayıf alanlar: ROT13 %39, ters metin %32, Hintçe %33.
- 3 tekrarda 100 istemin 77'si birebir aynı skoru aldı.

---
## 3. Ana tablo: Görev tipi → JEV iyi mi kötü mü → kanıt → kaynak (tier)

| Görev tipi | Karar | Kanıt (metrik aynen; yoksa "yalnız accuracy" notu) | Kaynak (tier) |
|---|---|---|---|
| **Tek adımlı, cevabın metinden okunabildiği yargılar** (politika kontrolü, ret/uyma, kanıta dayalı doğruluk, sıradan tercih) | **İyi** | RewardBench 92,5 / GPT-6 92,5 (fark 0,0). HaluEval 87,3 / 88,4. Ret 96,5 / 94,5. **Yalnız accuracy.** Maliyet GPT-6'nın %0,36'sı, medyan 0,15 s | S1 §5–6, Tablo 1–2 (T3) |
| Rubrik puanlama (ikili panel) | İyi | P(MET) AUROC 0,80–0,86, ECE 0,056–0,096. 27 karşılaştırmanın en fazla 6'sında anlamlı geride (özet) | S2 §6.1 (T3) |
| Rubrik puanlama (sıralı/ordinal panel) | Orta/kötü | Hiçbir sıralı panelde en doğru eşleşik hakem değil. Güven AUROC 0,57–0,70 (ELLIPSE 0,49) | S2 §4, §6.1 (T3) |
| **Çok adımlı akıl yürütme / türetilen karar** (JudgeBench, matematik, kod, mantık) | **Kötü** | JudgeBench 78,6 / 93,1 (−14,6 [−18,9; −10,3]). Mantık −27,6, matematik −14,3, kod −12,9. **Yalnız accuracy.** jev-1.14 için JudgeBench 82,3 / GPT-5.6 think 93,1 | S1 Tablo 2 (T3); S10 Tablo 1 (T3) |
| Stil-çelişkili çiftler (yanlış cevap daha süslü) | Kötü | 76,6 / 90,1 (−13,5). Bu çiftlerde güven AUROC'u 0,764 (stil-eşik çiftlerde 0,839) | S1 Tablo 2, §7 (T3) |
| Referanssız uzun düzyazı | Kullanılamaz (diğer hakemler de) | 53,5, hata AUROC 0,498 | S1 §6 (T3) |
| **Ajan izi güvenlik sınıflandırması, ortalama** | **Ön eleyici olarak iyi, hakem olarak orta** | Ort. F1 77,8 (P 77,1, R 79,2, Acc 82,8, kapsama %95,5). GLM-5.2: F1 74,1 (P 91,9, R 64,1, Acc 86,5) | S3 Tablo 2 (T3) |
| — R-Judge | GLM daha iyi | JEV P 92,6 / R 84,7 / **F1 88,5** / FPR %7,5 (hesap). GLM P 99,2 / R 88,2 / F1 93,4 / FPR %0,8 | S3 Tablo 3, 8 (T3) |
| — ATBench500 | JEV daha iyi | JEV P 88,9 / R 99,2 / **F1 93,8** / FPR %12,1. GLM P 96,6 / R 77,3 / F1 85,9 / FPR %2,1 | S3 Tablo 3, 8 (T3) |
| — MCPHunt | JEV daha iyi (F1), ama FPR yüksek | JEV P 54,7 / R 69,1 / **F1 61,1** / FPR %16,6. GLM P 79,8 / R 31,2 / F1 44,9 / FPR %2,1 | S3 Tablo 3, 8 (T3) |
| — TraceSafe | GLM daha iyi | JEV P 72,2 / R 63,8 / **F1 67,8** / FPR %25,1. GLM P 92,2 / R 59,6 / F1 72,4 / FPR %4,2 | S3 Tablo 3, 8 (T3) |
| — Web ajanı başarı yargısı (AgentRewardBench) | Orta, düşük recall | Jev 1.14: P 87,5 / R 53,3 / F1 66,2 / AUROC 0,895. pplx-decider F1 73,9. GPT-5.6 think 72,3 | S10 Tablo 21 (T3) |
| — İz hakemine saldırı (R-Judge + kanıt yarıştırma) | **Çok kötü** | jev-1.14 accuracy 83,08 → 17,95. ASR %65,13. Üretken Qwen-3.8-flash'ta ASR %2,05 | S9 Tablo 2 (T3) |
| **Prompt-injection tespiti, temiz/generic veri** | İyi sıralama, eşik ayarı şart | Datadog: P 99,66 / R 82,90 / F1 90,51 (12.295 örnek). Deußer deepset: Acc 0,741, ECE 0,236, "precision perfect, recall 50%", AUROC 0,982. Hidden Risks: ROC-AUC 0,95–1,0, kalibre accuracy %87–99 (**yalnız accuracy + AUROC**). GitHub: deepset AUC 0,986 (T4) | V2 (T4); S4 Tablo 2, §4.1.3 (T3); S6 Şekil 8 (T3); V4 (T4) |
| **Prompt-injection tespiti, uyarlamalı / dedektöre yazılmış saldırı** | **Kötü** | Sahte politika: R 82,90 → **3,88**, F1 90,51 → **7,46** (P 100). Choice: F1 91,93 → 17,66. PromptShield'de anlam koruyan bozulmalar: kontrollü ASR Choice %77,3, Noul %60,0 | V2 (T4); S5 Tablo 3 (T3) |
| **Araç-çağrısı risk kapısı (online guard)** | **Kötü** (tek başına) | LangChain is_risky ortalaması 0,893 → 0,290 (40 koşu). Guardrail ajanında S1 ASR %45,33, E2E ihlal %17,33. Agentgateway guardrail'i "inserted argument" ile aşılıyor | V2 (T4); S9 Tablo 4 (T3); S8 özet (T3) |
| JEV'in kendisi ajanın eylem seçicisi olduğunda (generic injection) | Şaşırtıcı biçimde sağlam | InjecAgent ASR %1,8. "Ignore previous" ile %0. Skor erişimli uyarlamalı saldırı %3,5 | S7 Tablo 2 (T3) |
| Aynı rol, araç seçimi (BFCL), şablon injection | Kötü | Flip/target **96,7 / 96,7** | S5 Tablo A4 (T3) |
| Karar katmanı (yönlendirme/iptal/ciddiyet), JEV'e özel injection | Kötü | Temiz acc %100. JEV'e özel injection ASR 100 / 100 / 97,2. Universal suffix 100 / 100 / 97,0 | S6 Tablo I (T3) |
| Hakeme gömülü "not" (grader-directed text) | Kötü (jev-1.14) | %23,3 doğru karar çevriliyor. Üretken hakemler %0,4–2,3. pplx-decider %4,7 | S10 Tablo 1, E.5 (T3) |
| **Cascade / yönlendirme (router)** | **İyi** (maliyet için) | Dondurulmuş τ = 0,9: 93,4 / 92,5 (**+0,93** [0,24; 1,66]), ücretin **%41,4**'ü. Canlı yeni iş yükünde doğruluk birebir, ücretin %75,5'i | S1 §8–9, Tablo 4–5 (T3) |
| Cascade'in doğruluk tavanı | Sınırlı | Kehanet eşikle bile en fazla +2,7 puan (flash fallback), +1,7 (üst seviye) | S2 Özet, §6 (T3) |
| **LLM hakemlerle hata korelasyonu** | Bağımsız ikinci görüş **değil** | JEV'in en emin hatalarında LLM kararlarının 242/252'si (%96,0) aynı cevap. Beklenen %50,3 | S2 §5.2 (T3) |
| **Kalibrasyon / güven** | Görev ve sürüme bağlı | jev-1.14 ECE 0,019 (pairwise judge benchmark'ları; en iyi). jev-1.13 deepset injection ECE 0,236. ALFWorld ardışık adımda ECE 0,247. Sıcaklık ölçekleme görevler arası taşınmıyor. Güven ≥ 0,9'da hata %2,1 (RB) / %6,5 (JB) | S10 Tablo 1; S4 Tablo 2, §5; S1 §6–7, Tablo 28 (T3) |
| Eşik taşınabilirliği | Kötü | Ayarlanmış eşik iki kat recall veriyor ama başka girdi tipinde temiz belgelerin %74,7'sini engelliyor. Sabit 0,5 eşikte injection recall %50 | V4 (T4); S4 §4.1.3 (T3) |
| Sıra / tekrar kararlılığı | Çoğunlukla iyi | Tekrarda 96/96 aynı. Sıra değişince %3,7 (RB) / %11,1 (JB) karar değişiyor. 5 geçişte ~%3 çift en az bir kez değişiyor. Üretici seçenek-sırası yanlılığını kabul ediyor | S1 §7.3; S2 Limitations (T3); V1 #8 (T4) |
| Uzun iz / büyük durum | Belirsiz | > 16 adımda F1 57,5 / GLM 50,6, ama MCPHunt hariç tutulunca GLM önde. Üretici "context rot" diyor | S3 Tablo 9, 11 (T3); V1 #5 (T4) |
| Çok dilli | Orta | Düşük kaynaklı dillerde yanlış cevabı kabul etme eğilimi daha yüksek (yalnız özet) | S12 (T3) |
| **Kirlenme (contamination)** | Bilinmiyor, risk var | "we cannot rule out that benchmark items were seen in training". Eğitim verisi açıklanmıyor ("We make all the data ourselves"). Decider'ın eğitiminde HelpSteer2 etiketleri var (UPenn'in test panellerinden biri) | S1 Limitations; S2 Limitations (T3); V1 (T4) |

**Tablodan üç genel ders**

1. **"İyi mi kötü mü" sorusunun cevabını görev tipinden çok saldırganın olup olmaması belirliyor.** Temiz veride JEV hakem olarak üretken LLM'lerle yarışıyor, injection tespitinde de AUROC yüksek. Saldırgan kendi karar formatını hedef aldığında ise (sahte politika, kanıt yarıştırma, değerlendiriciye not) doğruluk 80'lerden 10–20'lere iniyor. Aynı saldırılar üretken hakemlerde çoğunlukla işlemiyor (S9: %2,05; S10: %0,4–2,3).
2. **Generic injection testleri yanıltır.** "Ignore previous instructions" JEV'de ASR'yi düşürüyor bile (S7: %1,8 → %0; V2: is_risky 0,893 → 0,905). Bir tezin "JEV-guard injection'ı durdurdu" sonucu, JEV'e özel saldırılarla test edilmediyse geçersizdir.
3. **JEV'in değeri doğrulukta değil, maliyet × güven sinyalinde.** Ucuz, hızlı ve hatalarının çoğunu düşük güvenle veriyor (S1 §7). Bu yüzden "kime bakalım?" sorusunu cevaplamakta iyi, "son karar ne?" sorusunu cevaplamakta değil.

---

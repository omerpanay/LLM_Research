# 09 · "JEV modelleri" ne anlama geliyor?

Ömer'in özeti: *"Benden 'JEV modelleri'ni araştırmamı istedi. [ÖMER: bunun ne anlama geldiğini teyit et.]"*

## En olası anlam (yüksek güven, ama kesin değil)
**JEV, TypeSafe AI'ın 15 Eylül 2026'da yayımladığı bir "karar modeli"dir (decision model).** Metin üretmez. Bir durum (metin) ve tipli sorular verildiğinde, tek bir ileri geçişte (forward pass) izin verilen her cevap için bir olasılık döndürür. Soru tipleri Noul (evet/hayır), Choice (en fazla 255 seçenekten biri) ve Score (sıralı seviye). Şirket bu model sınıfına "System One" modelleri diyor. Sloganı: "Jev makes judgments, code makes decisions." (Jev yargılar, kod karar verir.) Kaynaklar: TypeSafe dokümanları ve blogu (T4, vendor), 16 Kasım 2026'da kontrol edilen alıntılar için bkz. `../../Sunum Bilgi Paketi - Saldırılar, Değerlendirme, Savunmalar + JEV (TR-EN).md` §5–6.

Bunun neden en olası anlam olduğu:
1. "JEV models", TypeSafe'in kendi ifadeleriyle ("decision models", "System One models") ve ürün adıyla örtüşüyor.
2. Zamanlama uyuyor: model stajdan iki ay önce çıktı ve Eyl–Kas 2026'da arka arkaya birkaç değerlendirme yayımlandı.
3. Ömer bu hafta danışmana bu yoruma dayanarak "Agent Security and JEV" (Ajan Güvenliği ve JEV) sunumunu yaptı. Danışman başka bir şey kastettiyse bunu orada belirtmesi beklenirdi — **açıkça teyit et** (`07_supervisor_questions.md` içindeki 1. soru).

## JEV'in hakem (judge) veya koruyucu (guard) olarak kanıtlanmış yönleri (kademeler / tiers)
| İddia | Kaynak | Kademe | Durum |
|---|---|---|---|
| Kararın metinde görünür olduğu durumlarda öncü (frontier) LLM hakemlerine yakın (RewardBench 92.5, GPT-6 ise 92.5), JudgeBench'te ise çok geride (78.6'ya karşı 93.1) | JEV-as-a-Judge, CMU, arXiv 2609.26550 Tablo 1 | T3 | 16 Kasım'da doğrulandı (sunum) |
| Güven eşiği 0.9 olan bir JEV→GPT-6 kademeli yapısı (cascade), maliyetin 41.4%'i ile +0.93 puan kazandırıyor | aynı kaynak, Tablo 4 | T3 | 16 Kasım'da doğrulandı |
| LLM hakemleri, JEV'in en emin olduğu hataların 96%'sını tekrarlıyor; kademeli yapının kazançları sınırlı | Rao & Callison-Burch (UPenn), arXiv 2609.29769 | T3 | 16 Kasım'da doğrulandı |
| 5,219 ajan izi (trajectory) üzerinde JEV'in pozitif sınıf F1'i 77.8, en iyi üretken (generative) hakem GLM-5.2'nin ise 74.1; ATBench500 ve MCPHunt'ta JEV önde, R-Judge ve TraceSafe'te GLM önde | arXiv 2609.34862 (özet) | T3 | özet 18 Kasım'da okundu |
| Girdiye gömülmüş sahte bir politika (counterfeit policy) etiketleri yeniden tanımlıyor ve JEV'in saldırı tespiti F1'ini 90.51%'den 7.46%'ya düşürüyor | Datadog Security Labs | T4 (vendor blogu) | 16 Kasım'da doğrulandı |
| Mimari, ağırlıklar ve eğitim detayları yayımlanmamış; açık yeniden üretimler (Kev, Perplexity Decider) bir omurga (backbone) + seçenek başına puanlama başlığı (scoring head) kullanıyor | TypeSafe dokümanları; Hume blogu; HF model kartları | T4 | 16 Kasım'da doğrulandı |

**Önceki materyale düzeltme:** sunumda başta JEV'in "henüz ajanlar üzerinde test edilmediği" söyleniyordu; arXiv 2609.34862 onu ajan izleri üzerinde test etti (18 Kasım'da slayt 9 ve 30'da düzeltildi).

## Elenmesi gereken alternatif yorumlar (daha düşük güven)
| Olasılık | Neden kastedilmiş olabilir | Nasıl anlaşılır |
|---|---|---|
| G-Eval (düşünce zinciri (chain-of-thought) ve form doldurma kullanan LLM-as-judge; Liu et al., EMNLP 2023) | Almanca hızlı söylenen "G-Eval" ("Geh-Eval") kulağa "JEV" gibi gelebilir; "kendi metriklerini kur" konusuyla ilgili klasik bir hakem yöntemi | Sor: "TypeSafe modelini mi, yoksa G-Eval tarzı LLM hakemlerini mi kastettiniz?" |
| JEPA (Joint-Embedding Predictive Architecture, LeCun et al.; örn. I-JEPA, V-JEPA) | literatür ajanının bulduğu diğer tek "JE…" model ailesi; telaffuzu "JEV"/"JEPA models"a yakın | Sor; bu, ajan güvenliğinden uzak olan dünya modeli / öz-denetimli (self-supervised) görme araştırmalarına işaret ederdi, bu yüzden bu bağlamda olası değil |
| Genel "hakem/değerlendirme modelleri" | Danışman "JEV"i hakem modelleri için gevşek bir şekilde kullanmış olabilir | Aynı soru |
| VW'ye ait bir iç ad | Açık kaynaklardan kontrol edilemez | Sor; iç sistemlerde dışarıdan arama yapma |

## JEV teze nasıl girmeli, nasıl girmemeli
- **Yapılmalı:** E2'de (hakemi insan etiketlerine karşı doğrulama) aday hakemlerden biri ve D2'de aday koruyuculardan biri olarak girmeli — ≤ 2 hafta ile sınırlı bir alt soru (RQ1a).
- **Yapılmalı:** ana hakem/koruyucu deneyleri bir açık karar modeli veya açık LLM ile de çalıştırılmalı, çünkü barındırılan (hosted) model sürüm değiştirebilir ve veriler şirketin dışına çıkar (onayla ilgili danışman sorusu).
- **Yapılmamalı:** durum oracle'ı (state oracle, sistem durumuna bakan kontrol) bulunan yerlerde saldırı başarısının son puanlayıcısı olmamalı; doğrulama yapılmadan, çok adımlı akıl yürütme gerektiren durumlarda da ona güvenilmemeli.
- **Yapılmalı:** ona da saldırılmalı — sahte politika sonucu, ölçüm aracının kendisinin de bir saldırı yüzeyi olduğunu gösteriyor ("ölçeni kim ölçer?").

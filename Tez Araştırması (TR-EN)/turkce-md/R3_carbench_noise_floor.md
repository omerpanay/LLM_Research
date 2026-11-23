# Temiz araç içi ajan çalıştırmalarının gürültü tabanı (noise floor) (CAR-bench'in yayımlanmış yörüngeleri)

**Bu nedir.** Araç içi LLM ajanlarının, **ortada hiç saldırı yokken**, bir saldırı kâhininin (attack oracle) saldırı başarısı sanabileceği şeyleri ne sıklıkla yaptığının sıfır maliyetli bir ölçümü. CAR-bench yazarlarının kendi depolarında yayımladığı çok denemeli (multi-trial) yörüngeleri (trajectories) yeniden analiz ediyor.

- Veri: `github.com/CAR-bench/car-bench`, `results/` klasörü, commit `ce6dc9d` (12 Ekim 2026), MIT lisansı. Makale CAR-bench, ACL 2026 (T1). Yörüngelerin kendisi bir GitHub eseri (kaynak olarak T4, ama yazarların kendi çalıştırmaları).
- Betik: `tools/carbench_noise_floor.py` (çalıştırma: `python3 -I tools/carbench_noise_floor.py third_party/car-bench/results results/carbench_noise_floor`).
- Çıktı: `noise_floor.csv` (Wilson 95% güven aralıklarıyla (CI)), `noise_floor.md`, `examples.json` (elle denetim için işaretlenen çalıştırmalar).
- Kaydı yalnızca bir hata/traceback içeren çalıştırmalar (altyapı arızaları) dışarıda bırakılıyor ve `errored` içinde sayılıyor.

## Tanımlar
Doğru cevap (ground truth) = görevin gerektirdiği, durumu değiştiren eylemler (`info.task.actions`, 26 set-API'ye göre filtrelenmiş).

| Sütun | Anlamı |
|---|---|
| pass1 | ödülü (reward) = 1 olan çalıştırmaların payı |
| pass_k | k denemenin hepsinin geçtiği görevlerin payı (CAR-bench'in Pass^k'si) |
| flip | k temiz denemesi birbiriyle uyuşmayan görevlerin payı (bazıları geçiyor, bazıları kalıyor) |
| usca | ≥1 *istenmemiş durum değiştiren eylem (unrequested state-changing action)* içeren çalıştırmaların payı: aracı (tool) ground-truth araçları arasında olmayan bir set-API çağrısı. **Üst sınır (upper bound)**: simüle edilen kullanıcının sohbet ortasında istediği ama görevin ground truth'unda olmayan eylemleri de sayıyor |
| usca_A2 / usca_A3 | aynısı, ama dışa dönük iletişimle (send_email, call_phone_by_number) / sürüşle ilgili ya da dış fonksiyonlarla (navigasyon düzenlemeleri, camlar, sunroof, bagaj, dış ışıklar) sınırlı |
| usca_spont | usca ile aynı, ama yalnızca öncesindeki kullanıcı mesajı o araç ailesinin hiçbir anahtar kelimesini içermeyen çağrılar. Ajanın kendi başına yaptığı eylemlerin **sezgisel tahmini (heuristic estimate)** |
| param_dev | argümanları hiçbir ground-truth çağrısıyla eşleşmeyen bir ground-truth aracına ≥1 çağrı içeren çalıştırmaların payı ("doğru araç, yanlış parametreler"; sonradan düzeltilen ara denemeleri de kapsar) |

A1/A2/A3 kritiklik ayrımı CAR-bench'in değil, bu tezin önerisi.

## Öne çıkan sayılar (temiz çalıştırmalar, öncü (frontier) modeller)
| Bölüm (split) / model | çalıştırma (runs) | flip (görevler) | usca (üst sınır) | usca_spont (tahmin) | usca_A2 |
|---|---|---|---|---|---|
| base_test / Claude Sonnet 4.6 | 149 | 6/49 | 3/149 | 3/149 | 0/149 |
| base_v2 / Claude Opus 4.6 | 150 | 9/50 | 3/150 | 0/150 | 0/150 |
| base_v2 / GPT-5.2 | 148 | 13/48 | 11/148 | 5/148 | 0/148 |
| hallucination_test / Claude Sonnet 4.6 | 150 | 17/50 | 18/150 | 0/150 | 0/150 |
| hallucination_train_v2 / GPT-5.2 | 138 | 11/43 | 29/138 | 5/138 | 0/138 |
| hallucination / xLAM-2-32b (açık) | 486 | 21/97 | 72/486 | 26/486 | 3/486 |

## Tez için anlamı (çıkarım)
1. **Hiç saldırı olmadan da sonuç kararsızlığı büyük.** Öncü modellerde görevlerin 12–34%'ü birebir aynı temiz denemeler arasında sonuç değiştiriyor (flip). "Kullanıcı görevinde başarısız olan" tek bir saldırılı çalıştırma, saldırı için zayıf bir kanıt: saldırı altındaki fayda (utility-under-attack), *aynı görevin* temiz geçme oranıyla, birkaç deneme üzerinden karşılaştırılmalı.
2. **Geniş kâhinlerin gerçek bir yanlış pozitif tabanı var.** "Ajan, değiştirmesi istenmeyen bir şeyi değiştirdi" durumu temiz çalıştırmaların ~20%'sine kadarında (üst sınır) ve sezgisel kendiliğinden (spontaneous) tahmine göre çalıştırmaların kabaca 0–4%'ünde (öncü) ile ~6%'sında (açık modeller) görülüyor. Bu yüzden "istenmemiş herhangi bir A3 eylemi" olarak tanımlanan bir saldırı kâhini, ortada hiç saldırgan yokken bile sıfırdan büyük ASR (saldırı başarı oranı, attack success rate) raporlar.
3. **Dar, hedefe özgü kâhinler temiz.** Hiçbir öncü model çalıştırması, görevin gerektirmediği bir e-posta göndermedi ya da arama yapmadı (~1,300 öncü çalıştırmanın 0'ı). Belirli bir saldırgan hedef durumu olarak tanımlanan saldırı hedeflerinin (örn. saldırgan adresine e-posta, hedef = saldırgan POI'si) temiz tabanı sıfıra yakın, yani büyük bir düzeltme olmadan kullanılabilirler; geniş sapma kâhinleri ise eşleştirilmiş temiz çalıştırmalar gerektirir (tezin *causal ASR*'si).
4. **Simüle edilen kullanıcı bir "saldırı olmayanlar" kaynağı.** Denetlenen `base_81` örneğinde (Claude Sonnet 4.6, deneme 2) simüle edilen kullanıcı, talimatlarında istememesi söylenen bir rota değişikliği istedi; ortaya çıkan eylem ground truth'a göre istenmemiş ama sohbette istenmiş. Simülatör kayması (simulator drift) kaydedilmeli ve saldırı başarısından çıkarılmalı.

## Uyarılar (caveats)
- Anahtar kelime sezgisi her iki yönde de kaba; tezde herhangi bir sayı alıntılanmadan önce işaretlenen çalıştırmalardan rastgele bir örneklemin elle denetlenmesi (planlanan: 30) gerekiyor.
- CAR-bench görevleri saldırı kontrolleri olarak tasarlanmadı; bunlar yalnızca bu ortam ve bu modeller için tabanlar.
- Bazı `_v2` dosyaları her çalıştırmayı iki kez içeriyor (biri hatalı); hatalı kopyalar dışarıda bırakılıyor.

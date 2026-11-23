# AgentLAB görev enjeksiyonu: saldırı başarı oranının (attack success rate, ASR) ne kadarı saldırganın yeniden denemelerinden geliyor?

**Veri.** AgentLAB'in herkese açık reposu (`github.com/TanqiuJiang/AgentLAB`, commit `36f58e6`, 31 May 2026, MIT), uzun ufuklu (long-horizon) görev enjeksiyonu (task injection) saldırısının deneme başına sonuçlarını `Task-Injection/agentdojo/res/long_horizon/` altında sunuyor. Saldırı AgentDojo üzerinde çalışıyor; AgentDojo'nun `security` kontrolü **ortam durumunu** okuyor (bir LLM hakemi değil, bir oracle). `results.jsonl`'nin her satırı, bir user_task × injection_task çifti için bir denemedir (bir enjeksiyon parçacığı (snippet) iterasyonu/varyantı); `security_passed` (saldırgan hedefine ortamda ulaşıldı) ve `utility_passed` alanlarını içerir.

**Betik.** `python3 -I tools/agentlab_ti_attempts.py third_party/AgentLAB/Task-Injection/agentdojo/res/long_horizon results/agentlab_ti_budget` → `ti_attempt_budget.csv`.

Bir çift, saklanan ilk *b* denemesinden herhangi biri başarılı olduysa *b* bütçesi içinde ele geçirilmiş sayılır (denemeler saklandıkları sırayla alınır).

## Sonuç (banking suite'i, 144 çift, repoda saklandığı haliyle)
| Model klasörü | çift başına deneme (medyan / maks) | 1 denemede ASR | 3'te ASR | 5'te ASR | ASR, herhangi bir deneme | AgentLAB makalesindeki değer |
|---|---|---|---|---|---|---|
| gpt-4o | 3 / 10 | 32.6% | 59.0% | 70.1% | **79.9%** | 79.9% (Tablo 2–3, uzun ufuklu) |
| meta-llama_Llama-3.3-70B-Instruct | 1 / 15 | **50.7%** | 75.0% | 81.9% | **86.8%** | 86.8% uzun ufuklu; 50.7% tek atış (Tablo 3) |
| Qwen3-235B-A22B | 1 / 10 | 72.2% | 85.4% | 90.3% | **93.1%** | 93.1% (Tablo 3) |
| gpt-5.1 | 12 / 13 | 0.7% | 6.9% | 9.7% | 22.9% | 21.5% (Tablo 2) |
| gpt-5.1 + repeat_user_prompt | 10 / 12 | 1.4% | 6.2% | 12.5% | **20.8%** | 20.8% (Tablo 4, RP) |
| gpt-5.1 + transformers_pi_detector | 10 / 10 | 0.0% | 0.0% | 0.7% | **2.8%** | 2.8% (Tablo 4, DD) |
| claude-sonnet-4-5 | 12 / 17 | 0.0% | 0.0% | 0.0% | **0.0%** | 0.0% (Tablo 2) |

Kalın yazılmış herhangi-bir-deneme değerleri makalede raporlanan sayılarla birebir eşleşiyor; GPT-5.1'in herhangi-bir-deneme değeri (22.9%) makaledeki 21.5%'e yakın ama onunla aynı değil. gpt-4o'nun `summary_results.txt` dosyası ayrıca 115 başarılı çiftin 111'inin önceki çalıştırmalardan aktarıldığını ("skipped") belirtiyor; yani nihai sayı birkaç çalıştırmayı bir araya topluyor.

## Ne gösteriyor (gözlem ve çıkarım)
- **Gözlem:** yayımlanan uzun ufuklu görev enjeksiyonu ASR'leri **N deneme içinde herhangi bir başarı** oranlarıdır; N çift başına 10–17 denemeye kadar çıkıyor ve sonuçlar çalıştırmalar arasında toplanıyor.
- **Gözlem:** bir denemelik bütçede, bu dosyalarda GPT-4o'nun uzun ufuklu ASR'si 32.6%; bu, makalenin GPT-4o için tek atış temel değerinin (62.5%, Tablo 3) altında. 62.5%'i ancak 3 ile 5 deneme arasında geçiyor.
- **Gözlem:** Llama-3.3-70B için makalenin "tek atış" değeri (50.7%), bu dosyalardaki uzun ufuklu saldırının ilk deneme ASR'sine eşit; bu da (Çıkarım) makalenin tek atış ile uzun ufuklu karşılaştırmasının o model için 1 deneme ile N deneme karşılaştırması olduğunu düşündürüyor.
- **Çıkarım:** "uzun ufuklu saldırılar daha güçlü" etkisinin bir kısmı bir **saldırı bütçesi** etkisi olabilir. Kazancı çok adımlı yapıya bağlamadan önce bütçesi eşitlenmiş bir karşılaştırma (aynı deneme sayısı veya aynı kurban sorgusu sayısı) gerekiyor. Bu, danışmanın "bu gerçekten bir saldırı mı?" sorusunun doğrudan bir örneği ve yazarların kendi dosyalarından ücretsiz olarak ölçülebilir.
- **Oracle'a yönelik bir eleştiri değil:** burada başarı ortam durumundan okunuyor; bu, en güvenilir ölçüm türüdür. Sorun tek bir denemenin nasıl değerlendirildiği değil, denemelerin nasıl toplandığı.

## Uyarılar
- Saklanan sıranın kronolojik olduğu varsayılıyor (parçacık `iter_i_vj`). Önceki çalıştırmalardan aktarılan çiftlerin geçmişi kırpılmış olabilir; bu nedenle eğri, yalnızca daha önceki denemeler eksikse erken bütçe ASR'si için bir alt sınırdır. Yazarlarla teyit et.
- `gpt-4o-backip`, `gpt-4o-backup-0120` klasörleri ve suite adlı klasörler (`banking`, `slack`, `travel`, `workspace`) modeli belirtilmemiş başka çalıştırmalar/yedeklerdir; CSV'de listeleniyorlar ama yorumlanmıyorlar.
- Tek atış temel değerleri bu dosyalardan değil, makaleden (Tablo 3) alınmıştır.

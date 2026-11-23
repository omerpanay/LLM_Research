# 05 · Teknik yapılabilirlik

Burada yazılanların hepsi, *tahmin* olarak işaretlenmedikçe, 18 Kas 2026'da bu ortamda kontrol edildi. Kod düzeyindeki ayrıntılı notlar: `lit/codebase_audit.md`.

## 1. Üzerine inşa edilecek kod tabanları
| Kod tabanı | Lisans | Tezdeki rolü | Burada doğrulanan | Genişletme noktaları |
|---|---|---|---|---|
| AgentDojo (`ethz-spylab/agentdojo`) | MIT | **Entegrasyon merkezi**: suite formatı, durum oracle'ları (state oracles), yerleşik saldırılar/savunmalar | Bir venv içine kuruldu; `check_suites -s banking --no-check-injectable` 16 kullanıcı + 9 enjeksiyon görevi için **hiç LLM olmadan** geçiyor (enjekte edilebilirlik kontrolü bu kurulumda başarısız oluyor; araştırılacak) | `default_suites/v1/<suite>/{task_suite,user_tasks,injection_tasks}.py`, `data/suites/<suite>/{environment,injection_vectors}.yaml`; `BaseInjectionTask.security()` (`base_tasks.py` st. 97–125) |
| CAR-bench (`CAR-bench/car-bench`) | MIT | Araç içi alanın kaynağı (araçlar, JSONL verisi, görevler, politikalar) ve yayımlanmış gidişatlar (trajectories) | Klonlandı; gidişatlar ücretsiz olarak yeniden analiz edildi (`results/carbench_noise_floor/`) | `car_bench/envs/base.py` (adım döngüsü, durum hash'leri), `envs/car_voice_assistant/tools/*/set_apis`, `mock_data/data_manager.py`, `policy_evaluator.py` |
| AgentLAB (`TanqiuJiang/AgentLAB`) | MIT | Saldırı aileleri ve planlayıcı/saldırgan/hakem promptları; saklanan görev enjeksiyonu sonuçları | Klonlandı; saklanan sonuçlar yeniden analiz edildi (`results/agentlab_ti_budget/`); başarı kriterleri denetlendi | Repo kökünde aile çalıştırıcıları; `Task-Injection/agentdojo/src/agentdojo/attacks/long_horizon_attack.py`; `prompts/*.md` |
| CaMeL (`google-research/camel-prompt-injection`) | Apache-2.0 | Sistem düzeyinde savunma temel çizgisi (baseline); kendi kapımız için politika motoru | Klonlandı; politika dosyaları okundu | `src/camel/pipeline_elements/security_policies/<suite>.py` (suite başına 100–270 satır), `capabilities/`, `interpreter/` |
| carlab_mini (bu repo) | — | Ölçüm hattının (pipeline) ücretsiz prototipi | 14 test geçiyor; tüm matris CPU'da < 1 dk'da çalışıyor | `code/carlab_mini/` |

**Önerilen mimari.** CarDojo = CAR-bench verisi üzerinde ≈20–25 CAR-bench aracını yeniden uygulayan bir AgentDojo suite'i, artı üç ekleme: ortamda sürüş bağlamı + konuşmacı rolü, her durum değişikliğinden sonra anlık görüntü (snapshot) kaydı ve hedefe özgü enjeksiyon görevleri. Bu, hiç yapıştırma kodu (glue code) yazmadan AgentDojo savunmalarını, CaMeL politikalarını ve AgentLAB'in uzun ufuklu (long-horizon) görev enjeksiyonunu kullanmayı sağlar. Boyut referansı: AgentDojo banking ≈ 1,200 satır (araçlar 178, kullanıcı görevleri 571, enjeksiyon görevleri 418); CaMeL politika seti 100–270 satır. *Tahmin:* CarDojo v0 için 3–5 hafta, CaMeL politikaları için 1 hafta.

## 2. Ne nerede çalışır
| Bileşen | Burada ücretsiz (CPU, 4 çekirdek, 15 GB, GPU yok) | VW kaynakları gerekir |
|---|---|---|
| carlab_mini, metrikler, geçerlilik filtresi, istatistik | evet | — |
| Referans doğru (ground-truth) hatlı AgentDojo / CarDojo (LLM yok) | evet | — |
| Saklanan AgentLAB / CAR-bench sonuçlarının yeniden analizi | evet | — |
| Kurban ajan = açık model (ör. Qwen3-30B-A3B, Llama-3.1-8B, Qwen3-32B) | hayır (CPU'da çok yavaş) | vLLM'li GPU. *Tahmin:* bf16'da 8B'lik bir model KV önbelleğine ek olarak ~16 GB VRAM ister; 30B sınıfı modeller bf16'da ~60+ GB veya nicemlenmiş (quantised) halde ~20 GB ister |
| AgentLAB saldırganı (README'ye göre Qwen3-14B abliterated) | hayır | GPU (*tahmin* ~30 GB bf16) + politika onayı |
| Kurban = API modeli (GPT/Claude/Gemini) | hayır (ücretli) | API bütçesi + veri aktarımı onayı |
| LLM hakem / LLM kullanıcı simülatörü | hayır (ücretli veya GPU) | yukarıdaki gibi |

## 3. Maliyet modeli (hiç para harcanmadı)
Ölçülmüş girdiler (CAR-bench'in yayımlanmış loglarından, `info.total_agent_cost` ve `info.user_cost`, temiz bölümler (episodes), yazarların çalıştırma zamanındaki fiyatlar):

| CAR-bench loglarındaki ajan modeli | Temiz bölüm başına ortalama ajan maliyeti | Medyan prompt token sayısı (son çağrı) | Bölüm başına medyan LLM gecikmesi |
|---|---|---|---|
| Claude Sonnet 4.6 | $0.087–0.118 | ≈14.5k | ≈18 s |
| Claude Opus 4.6 (thinking, medium) | $0.138–0.171 | ≈14.4k | ≈17–25 s |
| GPT-5.2 (thinking, medium) | $0.048–0.067 | ≈9.3k | ≈22–29 s |
| Kullanıcı simülatörü olarak Gemini 2.5 Flash | ≈$0.0007–0.0014 | — | — |
| Açık modeller (Qwen3-32B, gpt-oss-120b, xLAM-2-32b) | $0 kaydedildi (kendi sunucumuzda) | 8–14k | 6–340 s (donanıma bağlı) |

Formül (*tahmin*): $C = N_{ep} \cdot (c_{agent}\, m + c_{user} + c_{att} + c_{judge})$; burada $m$ saldırılı çalıştırmalar için bölüm uzunluğu çarpanı (çok turlu saldırılar; 1.5–3× *varsayalım*), $c_{att}$ bölüm başına saldırgan LLM ve $c_{judge}$ hakemdir.

E3 için çözümlü örnek (*tahmin*, 1. hafta ölçümüyle değiştirilecek): 6,480 saldırılı + 6,480 temiz bölüm. Üçte biri temiz bölüm başına $0.05–0.17 maliyetli bir API modelinde çalışırsa ve saldırılı bölümler 2× maliyetliyse → API ajan maliyeti ≈ 2,160 × $0.05–0.17 + 2,160 × 2 × $0.05–0.17 ≈ **$320–1,100**; açık modeldeki üçte ikilik kısım yalnızca GPU zamanına mal olur. Açık modellerdeki hakemler/saldırganlar GPU zamanı ekler; API'lerde ise yine benzer bir miktar eklerler. **Senin açık onayın ve ölçülmüş bölüm başı maliyet olmadan hiçbir ücretli çağrı yapılmayacak.**

En ucuz inandırıcı yapılandırma: tek bir VW GPU'sunda açık model kurban + açık saldırgan + durum oracle'ları (nihai puanlama için LLM hakem gerekmez); 300 çiftlik dış kontrol için yalnızca bir API modeli.

## 4. Mühendislik riskleri
| Risk | Kanıt | Önlem |
|---|---|---|
| AgentDojo enjekte edilebilirlik kontrolü yeni bir venv'de başarısız oluyor | burada gözlemlendi | CarDojo'dan önce araştır (muhtemelen veri yolu/canary işleme); referans doğru kontrollerini engellemiyor |
| AgentLAB çalıştırıcıları conda ortamları, vLLM, planlayıcı/hakem için GPT-5.1 istiyor | README | önce yalnızca görev enjeksiyonu yolunu (AgentDojo tabanlı) kullan; mümkün olan yerde GPT-5.1 hakemini durum oracle'larıyla değiştir |
| CAR-bench her çalıştırmada bir LLM kullanıcı simülatörü istiyor | kod + loglar | saldırı aileleri için senaryolu (scripted) kullanıcı turları; LLM kullanıcı yalnızca dış geçerlilik için |
| Burada Python 3.13, repolar ise 3.10–3.11'i hedefliyor | README'ler | VW'de 3.11 ortamını sabitle |
| Model kayması (API sürümleri) | genel | model ID'lerini ve tarihlerini sabitle; yeniden üretilebilir çapa olarak bir açık modeli tut |

# B · VehicleWorld mü, CAR-bench mi, başka bir şey mi? Simülasyon ortamı seçimi

Tarih: 24 Kasım 2026. Hazırlayan: araştırma alt-ajanı (Claude). Kapsam: yalnızca simülasyon, gerçek araç/CAN yok, ücretli API yok.

**Kaynak seviyeleri (tier):** T1 = hakemli üst düzey venue · T2 = workshop / standart / ikincil hakemli iz · T3 = preprint (arXiv) · T4 = blog / GitHub / HF kartı.
**Kural:** Kaynağın söylediği şeyle benim çıkarımımı ayırıyorum. Benim yorumum olan her şey **"Çıkarım:"** ile başlıyor. "Kendi ölçümüm" = bu oturumda kodu indirip çalıştırarak gördüğüm şey (scratchpad'te, repo dosyalarına dokunmadan).

---

## 0. Kısa cevap (TL;DR)

- **VehicleWorld gerçek ve hakemli:** *Findings of ACL: EMNLP 2025*, s. 403–442, DOI 10.18653/v1/2025.findings-emnlp.23 (ACL Anthology bib kaydı). Fudan / OpenMOSS. 30 cihaz modülü, 250 API, 680 özellik (property), 1.291 görev.
- **Ama VehicleWorld bir *güvenlik* ortamı değil, bir *yetenek* ortamı:** Saldırgan yok. Sürüş bağlamı (hız, park/sürüş) yok. Politika ya da onay mantığı yok. Üçüncü taraf metin kanalı neredeyse yok: POI, takvim, e-posta, web yok. Tek gerçekçi kanal SMS içeriği, bir de medya başlık/açıklamaları. Bellek de yok (bellek sadece türev çalışma VehicleMemBench'te var).
- **Kodda iki ciddi pratik sorun var (kendi ölçümüm):**
  - (1) Modelin ürettiği Python kodu host üzerinde **tam yetkiyle** `exec` ediliyor. Sandbox kontrolü fiilen çalışmıyor. Saldırı deneyinde bu bir güvenlik açığı.
  - (2) GitHub reposunda **LICENSE dosyası yok**. Dataset ise HF'de Apache-2.0.
  - Repo Eylül 2025'ten beri dokunulmamış: toplam 4 commit.
- **Öneri (Çıkarım):** VehicleWorld'ü *tek başına* almak tezi kurtarmıyor. Saldırı katmanını yine biz yazmak zorundayız ve VehicleWorld'de saldırı kanalları CAR-bench'ten daha zayıf. En mantıklısı **hibrit**:
  - Ana ortam yine AgentDojo formatında "CarDojo" olsun.
  - Üçüncü taraf veri kanalları (POI, takvim, kişi, e-posta, şarj) CAR-bench'ten gelsin.
  - Araç kontrol cihazlarının durum modeli (kapı, cam, sunroof, ışıklar, koltuk, klima, global ses/sıcaklık) VehicleWorld'den uyarlansın.
  - VehicleWorld'ün "değişmemesi gereken özellikler" metriği (F1-negative) yan-etki / collateral damage ölçüsü olarak alınsın.
  - Dış geçerlilik kontrolü üç ortamda: CAR-bench'in kendisi, VehicleWorld'ün kendi FC harness'i (SMS enjeksiyonu + eklenmiş sürüş bağlamı ile), bellek zehirlemesi için de opsiyonel olarak VehicleMemBench.
  - Bu sayede hocanın "kendi ortamınızı uydurmayın" kaygısı da karşılanıyor: ortam iki hakemli benchmark'tan türetilmiş oluyor.
  - Ek efor CarDojo planına göre yaklaşık **+1 hafta**. Detay §6'da.

---

## 1. VehicleWorld: kimlik kartı (birincil kaynaklar)

| Alan | Değer | Kaynak (konum) | Tier |
|---|---|---|---|
| Başlık | *VehicleWorld: A Highly Integrated Multi-Device Environment for Intelligent Vehicle Interaction* | arXiv 2509.06736v1, s.1 | T3 (arXiv sürümü) |
| Yazarlar | Jie Yang*, Jiajun Chen*, Zhangyue Yin*, Shuo Chen, Yuxin Wang, Yiran Guo, Yuan Li, Yining Zheng†, Xuanjing Huang, Xipeng Qiu† (Fudan Univ., School of CS & AI) | arXiv PDF s.1; ACL Anthology bib | — |
| arXiv | 2509.06736v1 [cs.AI], 8 Eylül 2025. PDF 40 sayfa, appendix dahil | arXiv PDF başlığı; `pdfinfo` | T3 |
| **Hakemli yayın** | *Findings of the Association for Computational Linguistics: EMNLP 2025*, Suzhou, Kasım 2025, **pp. 403–442**, DOI `10.18653/v1/2025.findings-emnlp.23`, ISBN 979-8-89176-335-7 | aclanthology.org/2025.findings-emnlp.23.bib (bu oturumda indirildi) | **T1** (not aşağıda) |
| Ek doğrulama | Semantic Scholar: venue "EMNLP", DBLP anahtarı `conf/emnlp/YangCYCWGLZHQ25`, citationCount 3 | api.semanticscholar.org (bu oturumda) | T4 (metadata) |
| ACL sürümü ile arXiv sürümü farkı | İkisi de 40 sayfa. Ana sayılar (30/250/680, 302 init senaryosu, 1291 görev, 51.1→61.5) her iki metinde aynı | Kendi karşılaştırmam: `vw_acl.txt` ile `vw_raw.txt` grep | — |
| Kod | https://github.com/OpenMOSS/VehicleWorld. HEAD `6536be9` (16 Eylül 2025). **Toplam 4 commit, hepsi 9–16 Eylül 2025** | `git log` (tam geçmiş çekildi) | T4 |
| Kod lisansı | **Repoda LICENSE dosyası yok.** README'de lisans bölümü yok | Kendi gözlemim: `ls -a`, README | T4 |
| Veri | HF `fnlp/VehicleWorld` adresi şimdi `OpenMOSS-Team/VehicleWorld`'e yönleniyor. **license: apache-2.0**, 1 split, **1.291 örnek**, ~156 MB CSV. Oluşturma 15 Eylül 2025, son değişiklik 20 Mart 2026 | HF API (bu oturumda) | T4 |
| Makalede veri lisansı | "The dataset will be released under the Apache License 2.0" | Appendix C | T1 |
| Bakım | GitHub'da 2 issue var, ikisi de kapalı: #1 "Release VehicleWorld dataset on Hugging Face" (kapanış 16 Eyl 2025) ve #2 task_construct.py eksikliği (kapanış 12 Eyl 2025) | GitHub issues sayfası (WebFetch özeti, ikincil) | T4 |
| Aynı ekibin devam çalışması | **VehicleArena** (arXiv 2609.35916v2, 4 Eki 2026, OpenMOSS). SUMO + 3D şehir + kabin modülleri + LLM yolcu + LLM Judge | arXiv PDF s.1, §3 | T3 |
| Başka ekibin türevi | **VehicleMemBench** (arXiv 2603.23840v1, 25 Mar 2026, USTC + iFLYTEK): "simulation environment based on VehicleWorld", 23 modül, 111 tool, bellek API'si | arXiv PDF §2.2 | T3 |

**Venue notu:** EMNLP Findings, EMNLP'nin hakem sürecinden geçiyor ama ana konferans (main) değil. Tez metninde "peer-reviewed, Findings of EMNLP 2025" diye yazmak doğru olur. CAR-bench'le kıyaslarken dürüst ifade şu: CAR-bench **ACL 2026 Long (main)**, VehicleWorld **EMNLP 2025 Findings**. Yani CAR-bench bir tık daha güçlü bir yayın kanalında.

---
## 2. VehicleWorld'ün içinde ne var? (makaleden, kesin sayılar)

Bu bölümdeki her sayı makaleden alındı (Findings EMNLP 2025, **T1**). Konumlar arXiv v1 metnine göre.

### 2.1 Ortam

| Ne | Değer | Konum |
|---|---|---|
| Cihaz / modül | **30 cihaz**, 4 alan: Multimedia, Touch Control, Car Control, Lighting | Abstract; §3.1; Fig. 2 |
| API | **250 API metodu** ("30 device classes encompassing 250 API methods and 680 attributes") | §3.1 |
| Özellik (attribute/property) | **680** | Abstract; §3.1 |
| Keşif araçları | `search_module` ve `search_api` (AppWorld'den esinlenme) | §3.1 |
| Global durum | `Environment` singleton sınıfı: ses kanalı, volume, dil, sıcaklık, birim sistemi. "the audio channel … can only be utilized by a single device at any given time" | §3.2; App. E.3 |
| Başlangıç durumları | Her cihazda `init()` metotları. Bunların kombinasyonundan **302 init senaryosu** | §3.3 |
| Durum gösterimi | JSON. Her alanda `value`, `description` ve `type` var. Örnek: Navigation `{is_active, destination, midway}`, Door `{is_locked, status}` | §3.3; Table 1; Limitations ("augment each attribute with a value, type, and description field") |
| API'lerin kaynağı | "designed and implemented by domain experts based on real-world user experiences in intelligent cockpit environments … derived from realistic production environments". Sınıf kodları Claude-3.7-Sonnet ile üretilip insan tarafından gözden geçirilmiş | Ethics Statement; App. F Listing 3 |
| Örnek modül API listesi | Conversation modülünde **15 fonksiyon**: telefon araması, SMS gönderme/görüntüleme, kişi silme, eller-serbest vb. | App. G, Table 8 |

### 2.2 Görevler (benchmark)

| Ne | Değer | Konum |
|---|---|---|
| Görev sayısı | **1.291 görev**, 4 split (Multimedia, Touch Control, Car Control, Light) | §5.2. HF kartında da 1.291 |
| Üretim | Claude 3.7 Sonnet XML-tag formatında senaryo üretiyor (`<inits>`, `<query>`, `<api_call>`). Senaryo çalıştırılıyor, sonra uzman insan kontrol ediyor. Elemeden geçemeyen senaryo atılıyor | §5.1; Fig. 3; App. F Listing 4 |
| Tür dağılımı (Table 2) | S-S / S-M / M-S / M-M (ilk harf tek/çok tur, ikinci harf tek/çok niyet). Multimedia 59/96/251/53 · Touch Control 34/93/107/15 · Car Control 135/178/205/173 · Light 79/75/159/161 | Table 2 |
| **Tutarsızlık** | Table 2'deki hücrelerin toplamı **1.873**. Metindeki görev sayısı ise **1.291**. Makale Table 2'yi "distribution of user intents" diye anlatıyor; muhtemelen sayılan birim görev değil. Tezde atıf yaparken **1.291 görev** kullanın ve bu farkı not edin | Kendi toplamam |
| Görev başına (Table 3) | Ortalama cihaz sayısı 2.02–2.11. Ortalama farklı API 2.84–3.54. Ortalama API çağrısı 3.07–3.86. En karmaşık görev: 5 cihaz, 13 API çağrısı | Table 3; §5.2 |
| Ham senaryo dosyası (kendi ölçümüm) | Repodaki `database/querys/scenarios` dosyasında **1.331** `<scenario>` ve **2.946** `<query>` var. Tur dağılımı: 1 tur 578, 2 tur 174, 3 tur 299, 4 tur 279, 5 tur 1. Bu dosya filtre öncesi ham dosya; HF'deki 1.291 ile farkı muhtemelen eleme | Kendi sayımım (`python3 -I`) |
| Çok tur | Var, ama **kullanıcı turları önceden yazılmış (scripted)**. LLM kullanıcı simülatörü yok. Ajan her sorguya sırayla cevap veriyor | §5.3; App. A.4; `fc_evaluation.py` `process_task` |
| Bellek / oturumlar arası kalıcılık | **Yok.** Her görev yeni bir `VehicleWorld()` ile başlıyor | `fc_evaluation.py` |
| Sürüş bağlamı (hız, park/sürüş) | **Yok.** Makalede hiç geçmiyor. Kodda `Environment` sadece şunları tutuyor: volume, sound_channel, unit_system, timestamp, **speaker** (varsayılan "driver's seat"), temperature, language (varsayılan "Chinese"), time_display_format | Kendi gözlemim: `module/environment.py` satır 11–20 |

### 2.3 Başarı nasıl ölçülüyor?

- **Durum tabanlı oracle (state diff). LLM judge yok, trajectory eşleştirme de yok.** Her kullanıcı turunun sonunda altın durum dizisinden (gold `worlds[idx]` → `worlds[idx+1]`) "değişmesi gereken" ve "değişmemesi gereken" özellik kümeleri çıkarılıyor. Sonra modelin ürettiği durum farkıyla karşılaştırılıyor (§5.3; App. B; `eval_utils.calculate_turn_result`).
- Üç metrik var (App. B):
  - **F1-positive:** değişmesi gerekeni değiştirdi mi?
  - **F1-negative:** değişmemesi gerekeni korudu mu?
  - **Accuracy:** değişen değerler doğru mu? Belirsiz sayısal isteklerde ("sesi biraz aç") sadece yön kontrol ediliyor: artış / azalış / sabit.
- Görev skoru = turların ortalaması (§5.3).
- **Ara durum kaydı:** Her *kullanıcı turu* sonrası durum snapshot'ı var. Her *API çağrısı* sonrası yok (`fc_evaluation.py`). Görev oluştururken her `<api_call>` bloğundan sonra `worlds.json`'a snapshot yazılıyor (`task_construct.py`).
- Durum tabanlı ile kural tabanlı değerlendirmenin karşılaştırması:
  - Kural tabanlı = API adı, parametre ve çağrı sayısı tam eşleşmesi.
  - 200 FC çıktısı uzmanlarca etiketlendi. Durum tabanlı değerlendirmenin uzman etiketine göre hata oranı her model boyutunda daha düşük çıktı (Fig. 8; App. A.3).
- Tek örneklem: "results remained highly stable across multiple runs … we therefore adopted single-sample evaluation" (App. A.1). **Çıkarım:** Pass^k / tekrar varyansı raporlanmıyor. Tezde bunu kendimiz eklememiz gerekir.

### 2.4 Ajan paradigmaları ve sonuçlar

- **FC (Function Call):** Ajan ```` ```python ```` bloğu içinde API çağrısı yazıyor (`vw.door.carcontrol_carDoor_lock_switch(...)`). Bu kod çalıştırılıyor.
- **SFC (State-based FC):** Ajan durum JSON'unu görüyor ve doğrudan **durum atama kodu** yazıyor (`radio["is_playing"]=true`). SFC iki aşamalı: önce tüm cihazların tam JSON durumu verilip ilgili cihazlar seçtiriliyor, sonra yalnız seçilen cihazların durumu verilip hedef durum tahmin ettiriliyor (§4.2).
- **FC+SFC:** SFC ile cihaz seçiliyor, FC ile çağrı yapılıyor (§6.3; Fig. 10).
- **Önemli:** Native tool-calling (OpenAI `tools=` JSON şeması) değil, **code-as-action** (`agent_client.py`, `fc_evaluation.py`).
- Prompt stratejileri: ReAct, ReAct+Reflection (+3 yansıtma turu), örneksiz ReAct (§6.1; App. A.2).
- Modeller (Table 7): GPT-4o, Claude-3.7-Sonnet, DeepSeek-v3-250324, Llama-3.1-8B, Qwen2.5-7B/14B/32B/72B, Qwen3-4B/8B/32B.

**Table 4: ReAct, Accuracy, "Overall" sütunu (T1):**

| Model | FC | SFC |
|---|---|---|
| Claude-3.7-Sonnet | 62.9 | **73.4** |
| GPT-4o | **70.2** | 70.9 |
| DeepSeek-v3-250324 | 70.0 | 71.9 |
| Qwen2.5-72B | 58.8 | 64.8 |
| Qwen2.5-32B | 46.8 | 57.5 |
| Qwen2.5-14B | 38.0 | 57.3 |
| Qwen2.5-7B | 33.0 | 49.0 |
| Llama-3.1-8B | 28.7 | 46.8 |
| **Ortalama** | **51.1** | **61.5** |

- Metin de aynısını söylüyor: "average accuracy increasing from 51.1% (FC) to 61.5% (SFC)"; FC'de en iyi GPT-4o (70.2), SFC'de Claude-3.7-Sonnet (73.4) (§6.2).
- Reflection ile (Table 5) FC tarafında GPT-4o 71.8, DeepSeek-v3 72.7, ortalama 53.1.
- Karmaşıklık: Prompta 2, 4 ya da 6 ilgisiz cihaz durumu eklenince bütün Qwen2.5 modellerinde performans düşüyor; 7B en hızlı düşen model (Fig. 5).
- Reasoning: SFC'de "all models experience performance degradation when reasoning is introduced" (§6.3; Fig. 9).
- Qwen3 serisinde FC doğruluğu SFC'yi geçebiliyor (Fig. 10; §6.3).

### 2.5 Hesaplama ihtiyacı

- Açık modeller "vLLM … on 8 interconnected NVIDIA A100 GPUs" ile koşturulmuş. Qwen2.5 için YaRN ile 128k bağlam, Qwen3'te thinking kapalı, sıcaklık 0.7 (App. A.1).
- Bütün çağrılar OpenAI SDK arayüzünden yapılıyor. Herhangi bir OpenAI-uyumlu uç nokta (vLLM, Ollama vb.) ile çalışır (README; `agent_client.py`).
- **Kendi ölçümüm:** Varsayılan dünyanın tam durum JSON'u (`vw.to_dict()`, 31 üst anahtar) **≈99.4 bin karakter**. Kabaca ~25k token mertebesinde (**Çıkarım**, tokenizer'a göre değişir).
  - **Çıkarım:** SFC modunda bu kadar uzun bağlam küçük yerel modellerde sorun çıkarır.
  - FC modunda durum prompta konmadığı için daha hafif.
  - Ortamın kendisi saf Python; CPU'da milisaniyeler içinde çalışıyor. Yük tamamen LLM'de.

---

## 3. Kod denetimi: kendi gözlemlerim (repo HEAD `6536be9`, 16 Eyl 2025; T4 seviyesinde kanıt)

Repo `scratchpad/vw_src`'ye klonlandı. Çalıştırma scratchpad'teki ayrı bir venv içinde, `python -I` ile yapıldı. Kurulan tek paket `RestrictedPython==8.0`. LLM çağrısı yapılmadı.

1. **API sayısı:** Modül dosyalarında aktif `@api(...)` dekoratörü **248** tane. Ayrıca 4 tane yorum satırına alınmış var, hepsi `navigation.py` içinde (`navigation_get_duration`, `navigation_get_distance`, `navigation_route_query`, `navigation_trafficStatus_query`). Çalışma zamanında kayıtlı API sayısı 248, API'li modül sayısı 30 (`utils.apis`). **Çıkarım:** Makaledeki 250 rakamı muhtemelen 248 + `search_module`/`search_api`. En büyük modüller: seat 40 API, music 19, navigation 20 (aktif), airConditioner 22, video 22.
2. **Özellik sayısı:** Benim kaba sayacımla (yaprak `{"value","type"}` düğümleri) varsayılan dünyada **451** yaprak çıktı; makale 680 diyor. Sayım yöntemleri farklı: listeler ve iç sınıflar init'e göre değişiyor. **680'i makaleden alıntılayın, benim sayımı kullanmayın.**
3. **Navigasyon bir taslak (stub):** `navigation_route_plan(address)` adresi sadece string olarak kaydediyor. Mesafe/süre hesaplayan satırlar yorum satırında (`navigation.py` ~585–590). POI veritabanı, harita, rota alternatifi, şarj istasyonu yok.
4. **Üçüncü taraf metin taşıyan alanlar (enjeksiyon için aday):**
   - `conversation.messages[].content`: SMS içeriği. `conversation_message_view` ile ajana dönüyor. Kendi testimde dönüş `{'contact': 'Default Contact', 'content': 'Default content', ...}` şeklindeydi.
   - Kişi adları, arama kayıtları.
   - `video` başlık/açıklamaları (ör. "Highway Safety Tutorial" / "Learn about best practices for highway driving and safety tips", `video.py` l.108–109). Müzik ve radyo meta verisi.
   - Navigasyon `destination`/`midway` string'leri.
   - Takvim, e-posta, web, POI/yorum, hava durumu, şarj **yok**.
   - Ham senaryolarda SMS okuyan (`message_view`) senaryo sadece **11**, SMS gönderen 41, rota planlayan ya da hedef değiştiren 29, kapı API'si kullanan 165, cam API'si kullanan 226 (kendi sayımım).
5. **Politika / onay / güvenlik kuralı yok:** `confirm`, `safety`, `not allowed` aramalarında sadece parametre doğrulamaları çıktı (ör. "value and degree parameters cannot be used simultaneously"). "Sürüşte kapı açılmaz" türünde bir kural yok. Ham senaryolarda bile "I'm driving through a national park… open all windows" gibi istekler doğrudan uygulanıyor (`scenarios` dosyasının 2. senaryosu).
6. **Konuşmacı (speaker) var ama yetki semantiği yok:** `Environment.speaker` (varsayılan "driver's seat") sadece klima/kapı gibi API'lerde konum parametresi verilmezse **varsayılan konumu** belirliyor (`airconditioner.py` l.567–572, `door.py` l.324). Sürücü/yolcu yetki ayrımı yok.
7. **⚠️ Kod çalıştırma sandbox'ı fiilen yok:**
   - `utils.execute()` önce `compile_restricted_exec(modified_code)` çağırıyor. Ama sonra derlenmiş kısıtlı bytecode'u değil, **orijinal kodu** normal `exec(modified_code, global_vars, local_vars)` ile çalıştırıyor.
   - `if safe_code:` kontrolü de bir namedtuple'ın doğruluk değerine bakıyor. Bu yüzden kontrol pratikte hep geçiyor (Çıkarım, kod okumasından).
   - **Kendi testim:** `import os; print(os.getcwd())` başarıyla çalıştı ve `/tmp` döndürdü.
   - **Sonuç (Çıkarım):** Prompt injection ile ajan host'ta keyfi Python çalıştırabilir.
     - Bu, tezin dışında kalan, "araç dışı" bir saldırı yüzeyi. Ayrıca deney altyapımız için de risk.
     - VehicleWorld kullanılırsa çalıştırma ya izole bir konteynerde yapılmalı ya da code-as-action yerine native tool-calling dispatch'e çevrilmeli.
     - Ayrıca SFC modunda ajan API doğrulamasını tamamen atlayıp doğrudan özellik atayabiliyor (tasarım gereği).
8. **Global durum thread-local sınıf değişkenlerinde tutuluyor:** `Environment` sınıfında `_thread_local` var. **Çıkarım:** AgentDojo ortamı `task_environment.model_copy(deep=True)` ile kopyalıyor (`agentdojo/task_suite/task_suite.py` l.374). Bu kopyalama, sınıf düzeyindeki global durumu (volume, ses kanalı, speaker, sıcaklık) yakalamaz. AgentDojo'ya port ederken bu global durumu instance alanlarına taşımak gerekir.
9. **Görev oluşturma kodu da senaryo metnini Python olarak çalıştırıyor:** `task_construct.py` her senaryodan bir `execute.py` üretip subprocess'te koşturuyor. HF'deki CSV'de `execute.py` diye bir sütun var. **Çıkarım:** Veriyi yeniden üretirken de aynı izolasyon gerekiyor.
10. **Bağımlılıklar çok hafif:** `transformers==4.56.0`, `openai==1.102.0`, `RestrictedPython==8.0` (`requirements.txt`). Python 3.10+ (README). Modüller sadece stdlib'e dayanıyor. `from vehicleworld import VehicleWorld` venv içinde sorunsuz çalıştı.

---

## 4. Tez açısından "saldırılabilirlik"

Tezin saldırı aileleri `03_thesis_design.md` §5'te tanımlı. Her biri için VehicleWorld'ün ne verdiğine bakıyorum. Tablodaki hücrelerin hepsi **Çıkarım** (§2–3'teki kaynak ve kod gözlemlerine dayanıyor).

| Saldırı ailesi / ihtiyaç | VehicleWorld'de hazır mı? | Ne eklemek gerekir | Zorluk |
|---|---|---|---|
| **Dolaylı prompt injection (üçüncü taraf veri)** | Kısmen. SMS içeriği, medya meta verisi ve kişi adları serbest metin. Ama gerçekçi otomotiv kanalları (POI yorumu, takvim daveti, e-posta, şarj istasyonu açıklaması) **yok** | Yeni init'ler (`Conversation.init_attack1()` vb.) ya da worlds JSON'u üzerinden payload yerleştirme. POI/takvim için yeni modül yazmak, yani zaten CAR-bench'te olanı yeniden yapmak | SMS: kolay. POI/takvim: orta (sıfırdan) |
| ↳ SFC modunda özel durum | SFC'de **tüm cihazların tam durumu** prompta konuyor (§4.2). Kullanıcı mesaj okumak istemese bile her durum alanı bir enjeksiyon kanalına dönüşüyor | — | **Çıkarım:** Gerçekçi değil, çok geniş bir yüzey. Raporlanırsa ayrı bir koşul olarak raporlanmalı |
| **Çok turlu yolcu saldırısı (tool chaining, intent hijacking)** | Kullanıcı turları önceden yazılmış. Saldırgan turları kolayca listeye eklenebilir. LLM kullanıcı simülatörü yok, ama bu bizim için avantaj (ucuz ve deterministik) | Uyarlamalı saldırgan için AgentLAB tarzı planner döngüsünü harness'e bağlamak. Speaker'a yetki semantiği eklemek | Orta |
| **Bellek zehirleme (oturumlar arası)** | **Yok** | VehicleMemBench (türev çalışma) bellek API'si ve 5 bellek sistemi sunuyor (Mem0, MemOS, LightMem, Memobase, Supermemory; README). Ama onda **Conversation (SMS) modülü yok** (`environment/module/` listesi) | Orta–yüksek |
| **Geçici (transient) güvensiz durum, TUA metriği** | Snapshot'lar sadece tur sonunda alınıyor. Hız/sürüş bağlamı yok, o yüzden "cam ≥50% iken hız ≥50 km/h" gibi invariant'lar tanımlanamıyor | (a) `Environment`'a `vehicle_speed` ve `driving_state` eklemek. (b) `@api` wrapper'ına her çağrıdan sonra `to_dict()` snapshot'ı eklemek. Tüm API'ler tek bir dekoratörden geçtiği için bu kolay | Kolay–orta |
| **Hedefe özel güvenlik oracle'ı** | Durum zaten tam serileştirilebiliyor (`to_dict`/`from_dict`). Ama injection task / security predicate kavramı yok | "Saldırganın numarasına SMS gitti mi", "kapı kilidi açıldı mı", "hedef saldırganın adresi mi" gibi predicate'ler. Kısa fonksiyonlar | Kolay |
| **Yan etki (collateral) ölçümü** | **Var ve iyi:** F1-negative, "değişmemesi gereken özellik korundu mu?" | Doğrudan alınabilir | — |
| **AgentDojo formatına sarma** | Hayır. Code-as-action ve global singleton durum var | Her API için `Annotated[..., Depends("vehicle")]` imzalı wrapper. Pydantic env. Global durumu instance'a taşımak. `@api` kaydı imza ve docstring'i zaten topluyor (`utils.api`), bu da otomatik wrapper üretimini kolaylaştırır | Orta (alt küme için 1–2 hafta) |
| **AgentLAB saldırıları** | AgentLAB'ın task-injection yolu AgentDojo üzerine kurulu (`lit/codebase_audit.md` §1). Yani önce AgentDojo portu gerekiyor | Port bitince bedava gelir | Port'a bağlı |
| **CaMeL politikaları** | CaMeL AgentDojo suite'i bekliyor (`codebase_audit.md` §4) | Port bitince ~150–300 satır politika (audit'teki tahmin) | Port'a bağlı |
| **Açık modelle yerel çalışma** | Evet. OpenAI-uyumlu uç nokta yeterli. Makale Qwen2.5-7B…72B, Qwen3-4B/8B/32B ve Llama-3.1-8B ile koşmuş (Table 7) | — | Kolay |
| **Ara durum logları** | Tur sonu durumları ve mesaj geçmişi `outputs/`'a yazılıyor (`fc_evaluation.py` `task_result["messages"]`). Çağrı düzeyinde snapshot yok | Wrapper ile eklenir | Kolay |

**Çıkarım (özet):** VehicleWorld'ün tez için gerçek katkısı **araç kontrol tarafının zenginliği** (kapı, cam, sunroof, koltuk, ışıklar, klima; 248 API) ve **cihazlar arası bağlılık** (tek ses kanalı, global volume/sıcaklık). Bunlar "fiziksel etki" taşıyan saldırı hedefleri için iyi. Saldırganın *girdiği* kanallar ise (POI, takvim, e-posta, şarj) CAR-bench'te çok daha zengin. Tezin ana sorusu da uzun ufuklu **dolaylı** saldırılar olduğu için saldırı yüzeyi açısından CAR-bench daha önemli.

---

## 5. Yan yana karşılaştırma

**Kaynak notları (her sütunun nereden geldiği):**
- **VehicleWorld:** §1–3 (makale T1 + kod T4).
- **CAR-bench:** `lit/automotive.md` V-01 (PRIMARY-READ: arXiv 2601.22027, ACL 2026 Long, Table 3/4) ve `lit/codebase_audit.md` §2. Tool ve klasör adları `third_party/car-bench` @ `ce6dc9d` üzerinden bu oturumda kontrol edildi.
- **AgentDojo:** arXiv 2406.13352v3 (NeurIPS 2024 D&B; bu oturumda grep ile kontrol edildi). Not: Makale §3'te "74 tools", bir başka yerde "70 tools, 97 realistic user tasks and 27 injection targets" diyor.
- **VehicleMemBench:** arXiv 2603.23840v1 (T3) + repo.
- **Automotive-ENV:** arXiv 2509.21143v3 (T3). arXiv yorumunda "Accepted at NeurIPS 2026" yazıyor; bildiri kitabında doğrulamadım.
- **VehicleArena:** arXiv 2609.35916v2 (T3).
- **Intent-to-Action:** arXiv 2609.19630 (T3), `automotive.md` V-02.

### 5.1 Tablo 1: künye ve ortam özellikleri

| Kriter | **VehicleWorld** | **CAR-bench** | **AgentDojo** | **VehicleMemBench** | **Automotive-ENV** | **VehicleArena** | Intent-to-Action (V-02) |
|---|---|---|---|---|---|---|---|
| Hakemli mi? | ✅ EMNLP 2025 **Findings** (T1) | ✅ **ACL 2026 Long** (T1) | ✅ NeurIPS 2024 D&B (T1) | ❌ preprint (T3) | arXiv yorumuna göre NeurIPS 2026 (T3; doğrulanmadı) | ❌ preprint (T3) | ❌ preprint (T3) |
| Alan | Kokpit cihaz kontrolü | Kokpit asistanı: navigasyon, POI, şarj, takvim, kişi, e-posta, telefon, araç fonksiyonları | Genel: workspace, slack, travel, banking | Kokpit + çok kullanıcılı uzun süreli bellek | Android Automotive GUI | 3D şehir sürüşü (SUMO) + kabin | Tek turlu sesli komut yetkilendirme |
| Tool / API sayısı | **248–250** API, 30 cihaz | **58** tool (27 set, 29 get, 2 no-op) | 74 (ya da 70) tool, 4 suite | **111** tool, 23 modül | GUI eylemleri (ADB) | Sürüş + kabin tool'ları (sayı okunmadı) | Tool şeması (çalıştırılabilir ortam yok) |
| Görev sayısı | 1.291 | 240 (makale) / 254 (repo README tablosu) | 97 user task, 629 security case | 500 sorgu, 50 senaryo | 420 | 112 değerlendirme + 100 train/dev | 202 senaryo |
| Gerçekçilik | Uzman tasarımı API'ler. Navigasyon taslak. Çin pazarı varsayılanları (dil "Chinese", Shanghai/Nanjing) | 48 gerçek Avrupa şehri, 130K POI (adları LLM üretimi), 1.7M rota, 100 takvim, 100 kişi | Sentetik ofis ortamı | VehicleWorld tabanlı + persona geçmişleri | Gerçek AAOS emülatörü | Fiziksel trafik simülasyonu | Sentetik |
| Durum oracle'ı | ✅ durum farkı (F1± ve Acc) | ✅ durum tabanlı ödül + policy değerlendirici (19 politika: 12 kodla, 7 LLM-judge ile) | ✅ `utility`/`security` predicate'leri | ✅ Exact State Match + alan/değer F1 | ✅ ADB validator'ları | Kısmen: LLM Judge + fizik metrikleri | Karar sınıfı eşleşmesi |
| Ara durum kontrolü | Tur sonu snapshot | ✅ her adımda durum hash'i | ❌ sadece pre/post | Final durum | Final durum + iz | Zaman çizelgesi boyunca Judge | — |
| Çok tur | ✅ önceden yazılmış (≤5 tur) | ✅ LLM kullanıcı ile | ❌ tek kullanıcı promptu | Tek sorgu + uzun geçmiş | Tek görev | ✅ LLM yolcu ajanı | ❌ tek tur |
| Kullanıcı simülatörü | ❌ | ✅ LLM (yayınlanan koşularda Gemini 2.5 Flash) | ❌ | ❌ | ❌ | ✅ Personal Agent | ❌ |
| Bellek | ❌ | Tercih aracı (`get_user_preferences`) var | ❌ | ✅ bellek API'si + 5 bellek sistemi | ❌ | Todo panosu | ❌ |
| Sürüş bağlamı (hız, park) | ❌ | ❌ (bu oturumda grep ile kontrol ettim: context'te speed yok) | ❌ | ❌ (okumadım) | ✅ hız, kemer, yakıt vb. sinyaller (§3) | ✅ gerçek hız, şerit | ✅ statik alanlar |
| Politika / onay | ❌ | ✅ | Suite'e bağlı | ❌ (okumadım) | Güvenlik validator'ları | Kural motoru | ✅ 7 karar sınıfı |

### 5.2 Tablo 2: saldırı, lisans ve uyarlama

| Kriter | **VehicleWorld** | **CAR-bench** | **AgentDojo** | **VehicleMemBench** | **Automotive-ENV** | **VehicleArena** | Intent-to-Action (V-02) |
|---|---|---|---|---|---|---|---|
| Saldırgan / enjeksiyon desteği | ❌ | ❌ | ✅ (injection_vectors, saldırılar, savunmalar) | ❌ | ❌ | ❌ | ❌ |
| Doğal enjeksiyon yüzeyi | SMS, medya meta verisi, kişi adı | **POI adı/açıklaması, takvim konu/konum, kişi alanları, e-posta, rota** | Her suite'te var | Konuşma geçmişi (bellek) | Ekran metni | Yolcu, ortam olayları | Yok |
| Lisans | Kod: **LICENSE yok**. Veri: Apache-2.0 (HF) | MIT (kod + HF veri) | MIT | README'de Apache-2.0 yazıyor, LICENSE dosyası yok | Okumadım | Okumadım | Veri yayınlanmadı |
| Bakım | 4 commit, Eyl 2025'ten beri sessiz | HEAD 12 Eki 2026, aktif + IJCAI yarışma reposu | Aktif | 6 commit (Mart 2026) | v3 Eki 2026 | v2 Eki 2026 | — |
| Tezimize uyarlama eforu (Çıkarım) | Orta–yüksek: saldırı katmanı, sürüş bağlamı, sandbox, tool-calling; AgentDojo portu ayrıca | Orta: saldırı katmanı + LLM kullanıcı maliyeti; AgentDojo portu (CarDojo) 3–5 hafta | Düşük (hazır), ama otomotiv değil | Orta | **Yüksek** (emülatör, multimodal, GUI) | **Yüksek** (SUMO + 3D, LLM judge) | Ortam değil; sadece senaryo/metrik ilhamı |
| Açık model desteği | ✅ OpenAI-uyumlu, Qwen/Llama denenmiş | ✅ (Qwen3-32B, gpt-oss-120b, xLAM-2-32b koşuları var) | ✅ (local LLM desteği var) | ✅ OpenAI-uyumlu `LLM_API_BASE` | VLM gerekir | Qwen3-VL-8B/32B denenmiş | Llama 3.2 3B / 3.1 8B denenmiş |

**Çıkarım: tablolardan çıkan net tablo.**
- **Hiçbir otomotiv ortamında saldırgan yok.** Hangisini seçersek seçelim saldırı katmanını biz yazacağız. Bu, CarDojo planının temel varsayımıyla aynı.
- Saldırgan girdisi açısından en zengin ortam **CAR-bench**.
- Fiziksel aktüatör çeşitliliği ve cihaz bağımlılığı açısından en zengin ortam **VehicleWorld**.
- Gerçek sürüş bağlamı isteyen bir deney için VehicleArena ya da Automotive-ENV var. İkisi de ağır ve tezin bütçesine/zamanına uymaz.
- **VehicleMemBench**, VehicleWorld ailesinin bellek zehirleme için hazır tek kapısı.


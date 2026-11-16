# Kaynak Denetimi ve Güncelleme (16 Kasım 2026)

Bu dosya üç soruya cevap veriyor: önceki raporlarda hangi kaynak ne kadar okunmuştu, bugün hangilerini tam metinden okudum, ve okuyunca raporda ne değişti. Sunum rehberi bu bulgulara göre güncellendi; burada gerekçeleri ve ayrıntıları bulursun.

## Kısa sonuç

1. **Kaynaklar neden açılamamıştı.** Site kapalı değildi. Çalışma ortamının ağ kuralı `arxiv.org`, `typesafe.ai`, `en.wikipedia.org`, `huggingface.co` gibi adresleri engelliyordu. İzin listesi düzeltilince hepsi açıldı.
2. **Bugün ne okundu.** 22 makalenin tam PDF'i, TypeSafe'in lansman yazısı (gizli SSS cevaplarıyla), doküman sitesinin tamamı, 4 blog yazısı, Wikipedia maddesi, iki açık model kartı ve JEV'in mimarisini 10.000 API çağrısıyla çözen bağımsız bir inceleme.
3. **En önemli kazanç: mimari.** Önceki rapor "iç mimari yayımlanmadı" deyip bırakıyordu. Bu hâlâ doğru, ama artık üç katmanlı kanıtla anlatabilirsin: şirketin kendi cümleleri, davranış deneyleri, ve aynı tarifi açık kodla yeniden üreten modeller.
4. **Düzeltilen yanlışlar: 4 tane.** Detektör sayısının anlamı, AgentLAB'in "0 tur" sayısının yorumu, cascade'in "en fazla 2,7 puan" kazancı ve CAR-bench lisans riski. Ayrıntı aşağıda.
5. **Doğrulanan sayılar.** Rehberdeki diğer bütün sayılar tam metinde bulundu ve doğru çıktı. "(C)" ile işaretli, ikincil rapordan alınmış beş savunma sayısının hepsi artık birincil kaynaktan doğrulandı.

## 1. Önceki durum: hangi kaynak ne kadar okunmuştu

Önceki raporların kendi beyanlarından derledim.

| Belge | Tam okunan | Yarım okunan | Yalnızca özet | Yalnızca arama özeti | Açılamayan |
| --- | --- | --- | --- | --- | --- |
| JEV raporu | Üretici dokümanları, Datadog, LangChain, Braintrust, VentureBeat, DataCamp, Wikipedia | 4 akademik makale: "ana metnin ilk yarısı, ekler yok" | Deußer vd. (dizin sayfası) | Kev model kartı ve kaynak turu | TypeSafe lansman yazısı, sınırlar (model jaggedness) sayfası, "this-that-model" makalesi |
| Literatür taraması | Yok | 4 makale: "son bölümler ve ekler yok" (AgentLAB, Attacker Moves Second, AgentDojo, AgentHarm) | 9 makale | 15 makale | Yok |
| Sunum rehberi | "Bu dosya için makaleleri yeniden açmadım" | | | | 5 savunma sayısı ikincil rapordan, "(C)" işaretli |

Yani sunumun dayandığı ~45 kaynaktan yalnızca birkaç web sayfası baştan sona okunmuştu; hiçbir akademik makalenin eki görülmemişti; mimari için birincil kaynak hiç açılmamıştı.

## 2. Bugün okunanlar

**Okuma derinliğini dürüstçe ayırıyorum.** "Tam metin" şu demek: PDF'in tamamı indirildi, metne çevrildi, rapordaki her sayı tam metinde arandı ve geçtiği pasaj okundu. "Baştan sona" şu demek: belgeyi satır satır okudum.

| Kaynak | Ne kadar | Önceki durum |
| --- | --- | --- |
| TypeSafe lansman yazısı, SSS cevapları dahil | Baştan sona | Açılamamıştı |
| TypeSafe dokümanları: Model jaggedness, Models, Changelog, AI primer, System One, Confidence, Primitives, Guardrails | Baştan sona (ilk dördü), ilgili bölümler (diğerleri) | Jaggedness açılamamıştı |
| TypeSafe blog: Jev 1.14, Don't Call It a Decision Model, The Bitterest Lesson, Lies Damned Lies and Benchmarks | Baştan sona | Raporda hiç yoktu |
| Jev's Architecture Unmasked (Archer Hume, 17 Eylül 2026) | Baştan sona (yöntem ekinin sonu hariç) | Raporda hiç yoktu |
| Kev model kartları (2 adet) ve kaynak turu; Perplexity Decider v1.1 model kartı | Mimari bölümleri baştan sona | Arama özeti |
| Wikipedia: Jev (AI model) | Baştan sona (kaynak metni) | Okunmuştu |
| JEV-as-a-Judge, CMU, arXiv 2609.26550 **v6**, 53 sayfa | Bölüm 8'den sonuca kadar ve Ek A baştan sona; diğer ekler tam metin | İlk yarı |
| Deußer vd., arXiv 2609.37647 v2, 25 sayfa | Tam metin | Yalnızca dizin sayfası |
| Rao ve Callison-Burch (UPenn) 2609.29769, 83 sayfa; DecisionRobust 2610.19118; Jev in the Wild 2609.30216 | Tam metin | İlk yarı |
| AgentLAB 2602.16901; CAR-bench 2601.22027 | Tam metin; ayrıca iki deponun README ve LICENSE dosyaları | Yarım; CAR-bench "yeniden açılmadı" |
| "(C)" işaretli beş makale: 2610.03448, 2611.04673, 2608.02657, 2611.07483, 2609.19630 | Özet baştan sona, sayılar tam metinde | İkincil rapordan |
| ASB yeniden analizi 2510.05244; A Coin Flip for Safety 2603.06594; Policy Invariance 2605.06161; Know Thy Judge 2503.04474; Attacker Moves Second 2510.09023; CaMeL 2503.18813 | Tam metin | Özet ya da yarım |
| AgentPoison 2407.12784; FuncPoison 2509.24408; CHAI 2510.00181; Nassi vd. 2508.12175 | Tam metin | Arama özeti |
| Datadog: sahte politika saldırısı | İlgili bölümler | Okunmuştu |

**Hâlâ okunmayanlar.** Bunlar sunumda sayı olarak geçmiyor, ama literatür taraması PDF'inde adları var: Meta SecAlign, WASP, Shadow Memory, AutoDojo, Hofer vd., AgentDojo ve AgentHarm'ın ekleri, ASB'nin özgün makalesi, ve arama özetinden alınan 14 makale (Greshake, InjecAgent, MINJA, MCPTox, Prompt Infection, Crescendo, STAC, Spotlighting, MELON, Task Shield, LlamaFirewall, Progent, Design Patterns, Adaptive Attacks). VentureBeat bugün "çok fazla istek" hatası verdi. "this-that-model makalesi"nin ne olduğunu bulamadım; önceki raporda başlık ya da bağlantı yok.

## 3. Düzeltilen dört yanlış

### 3.1 Detektör: "%1 yanlış alarmda yalnızca %2 yakalıyor" cümlesinin anlamı

**Rehberde yazan.** "En iyi enjeksiyon detektörünün yakalama oranı %2; detektör 100 saldırıdan 2'sini yakalıyor."

**Makalenin söylediği** (Passing the Test You Trained On, arXiv 2610.03448). BIPIA benchmark'ında en iyi olan detektör (PIGuard), BIPIA'daki saldırıların %95,1'ini yakalıyor; aynı detektör AgentDojo'nun tool çıktılarında %2,1'ini yakalıyor (ikisi de %1 yanlış alarmda). Başka bir detektör (Prismor) AgentDojo'da %72,2 yakalıyor, τ-bench'te %15,2.

**Arkasındaki fikir.** Detektörler kötü değil; **eğitildikleri metin biçimine benzeyen girdilerde çalışıyorlar**. PIGuard tam BIPIA girdileriyle eğitilmiş; ajanın gördüğü serileştirilmiş tool çıktısı (kayıt, liste, onay mesajı) başka bir biçim. Makale iki benchmark arasındaki sıralama uyumunu Kendall τ = 0,01 buluyor, yani bir benchmark'taki sıralama diğerini hiç öngörmüyor. İkinci bulgu: temiz tool çıktılarındaki yanlış alarm oranı detektöre göre %0 ile %90'ın üstü arasında değişiyor.

**Sunumda doğru cümle.** "Bir detektörün benchmark skoru, ajanın içinde nasıl davranacağını söylemiyor: BIPIA birincisi AgentDojo'da %2 yakalıyor." Tez için anlamı aynı yöne ama daha güçlü: detektörü kendi araç ortamının tool çıktılarında ölçmek zorundasın.

### 3.2 AgentLAB: "0 turda %0, beş turda %80" sayısının yorumu

**Rehberde yazan.** "Tek mesajla başaramayan saldırı, beş tur verilince beş denemenin dördünde başarıyor."

**Makalenin söylediği.** Sayılar doğru: GPT-4o'da task injection ASR'si tur bütçesi 0 iken %0, 5 iken yaklaşık %80. Ama "tek mesajlık saldırı başaramıyor" yorumu yanlış. Aynı makalenin Tablo 3'ü, klasik tek mesajlık enjeksiyonun ("important message" saldırısı) aynı GPT-4o'da **%62,5** başardığını, uzun ufuklu saldırının bunu **%79,9**'a çıkardığını gösteriyor.

**Arkasındaki fikir.** "0 tur" AgentLAB'in kendi saldırı yönteminin tur bütçesi; hiç tur verilmezse saldırı içeriği hiç yerleştirilemiyor, o yüzden %0. Bu, tek mesajlık bir saldırıyla aynı şey değil. Doğru karşılaştırma %62,5'e karşı %79,9: uzun ufuk, zaten yüksek olan bir başarıyı 17 puan daha artırıyor.

**Sunumda doğru cümle.** "GPT-4o'da tek mesajlık enjeksiyon %62,5 başarıyor; aynı hedefi turlara yayan saldırı %79,9. Tur bütçesi arttıkça başarı tekdüze artıyor." Mentor "0'dan 80'e" sayısını sorgularsa hazırlıklı ol.

**Ek doğrulanmış ayrıntılar.** Claude-4.5 task injection'da iki saldırıda da %0. Genel ASR: Qwen-3 %81,5; GPT-4o %78,1; GPT-5.1 %69,9; Gemini-3 %53,7; Claude-4.5 %28,9. Tool chaining her modelde %73 ile %96 arasında; yani en zor savunulan aile o. Planner GPT-5.1 (sıcaklık 0,5), hakem GPT-5.1 (sıcaklık 0), saldırgan Qwen3-14b-abliterated. Makalede hakemin insan etiketleriyle doğrulandığına dair bir bölüm yok. ICML 2026 kabulü doğrulandı (PMLR cilt 306). Depo MIT lisanslı.

### 3.3 Cascade: "en fazla 2,7 puan kazanç" sayısı

**Rehberde yazan.** "En fazla 2,7 puan: cascade'in doğruluğa kattığı en büyük kazanç."

**Makalenin güncel sürümünün (v6, 29 Ekim) söylediği.** Bu sayı v6'da cascade kazancı olarak geçmiyor; 2,7, başka bir tabloda JEV ile GPT-6 arasındaki bir farkın değeri. Dondurulmuş cascade'in gerçek sayıları şöyle:

| Veri | Cascade ile GPT-6 farkı | GPT-6 ücretine oranı | Ne kadarını GPT-6'ya gönderdi |
| --- | --- | --- | --- |
| Tüm 1.610 çift | +0,93 puan (aralık 0,24 ile 1,66) | %41,4 | %31,5 |
| RewardBench kısmı (1.340) | +1,27 puan | %26,7 | %25 |
| JudgeBench kısmı (270) | −0,74 puan | %66,8 | %65 |
| Yeni iki iş yükünde canlı test (570) | Tam eşit (0 puan) | %75,5 | %68 ve %89 |

**Arkasındaki fikir.** Cascade'in kazandırdığı para, ilk basamağın ne kadar iyi olduğuna bağlı. JEV'in zaten iyi olduğu işte (RewardBench) vakaların dörtte üçü JEV'de kalıyor ve ücret dörtte bire iniyor. JEV'in zayıf olduğu işte (JudgeBench, matematik, kod) vakaların çoğu pahalı hakeme gidiyor ve tasarruf dörtte bire düşüyor. Makalenin cümlesi: "Ucuz hakemin her yerde haklı olması gerekmez; nerede haklı olmadığını bilmesi gerekir."

**Tez için anlamı.** Senin kararın ("bu çok turlu iz bir saldırı mı?") türetme isteyen sınıfa yakın. Yani JudgeBench satırını bekle: doğruluk korunur ama tasarruf %60 değil, %25 ile %35 arası olur. Pilotta bunu ölçmek bir bulgu.

**Makalenin eşik tarifi (yeni).** Kararı iki sunum sırasının ortalamasından al. Eşiği kendi iş yükünden yaklaşık 100 etiketli örnekle seç. Nokta tahminine değil, doğruluk kaybının alt güven sınırına bak: nokta kuralı denemelerin %40 ile %50'sinde iki puandan fazla kaybettiriyor, alt sınır kuralı bunu yaklaşık %5'e indiriyor. Her iş yükü için ayrı eşik seç.

### 3.4 CAR-bench lisansı

**Rehberde yazan.** "Makale CAR-bench'in kendi lisansını belirtmiyor"; riskler tablosunda "lisans şirket kullanımına uymuyor" B planı.

**Depoda yazan.** `LICENSE` dosyası MIT. Yayın yeri de doğrulandı: ACL 2026 uzun bildiri (ACL Anthology 2026.acl-long.1886). Ayrıca IJCAI-ECAI 2026'da bir "CAR-bench Challenge" yarışması var; depo bu yarışmanın başlangıç kitini içeriyor.

**Tez için anlamı.** Lisans riski büyük ölçüde kalktı (şirket içi açık kaynak onayı yine gerekir). Yarışmanın varlığı, CAR-bench'in topluluğun kullandığı canlı bir ortam olduğunu gösteriyor; sunumda bir artı olarak söyle.

## 4. Doğrulanan sayılar

Hepsi tam metinde bulundu ve rehberdeki değerle aynı.

| Sayı | Kaynak | Not |
| --- | --- | --- |
| ASR %93,06'dan %9,03'e; fayda %90,28'den %82,64'e | AuthorityFlow, 2611.04673 | Makalenin adı "Right Tool, Wrong Parameters". Saldırı türü parametre zehirleme: ajan doğru tool'u çağırıyor, ama alıcı gibi bir argüman değiştirilmiş. Ölçüm yazarların kendi benchmark'ı FactAuthBench'te |
| ASR %34,6'dan %0'a | Gizli durum prob'ları, 2608.02657 | Model Qwen3.5-27B, AgentDojo'nun zor ayarları. Prob'lar görülmemiş saldırılarda AUROC 0,90 üstü |
| %8,3'ten %75,0'e | Signed but Not Safe, 2611.07483 | Model GPT-5.6-luna. Aynı deney Qwen3-8B'de %14,6'dan %37,5'e, gpt-oss-20b'de %11,1'den %63,9'a |
| 161 durumun 2 ila 3'ü | From Intent to Action, 2609.19630 | 202 senaryo, 7 karar sınıfı. Uyum %40,1 (Llama 3.2 3B) ile %89,1 (Gemini 3.1 Pro) arası |
| Yaklaşık %74'ten %9'a | ASB yeniden analizi, 2510.05244 | Tablo 5: %73,58'den %9,25'e, GPT-4o, savunmasız |
| 12 savunma, çoğunda %90 üstü | The Attacker Moves Second, 2510.09023 | |
| %77'ye karşı %84 | CaMeL, 2503.18813 | |
| Üslup değişikliği kaçırma oranını 0,24 artırıyor | Know Thy Judge, 2503.04474 | ICLR 2025 atölye bildirisi |
| Kararların %9,1'ine kadarı değişiyor | Policy Invariance, 2605.06161 | Judge Card önerisi bu makalede |
| LLM hakemler yazı turaya yakın | A Coin Flip for Safety, 2603.06594 | 6.442 insan doğrulamalı örnek |
| Ortalama %80 üstü, zehir oranı %0,1 altı | AgentPoison, 2407.12784 | Fayda kaybı %1 altı. Test edilen üç ajandan biri RAG tabanlı otonom sürüş ajanı |
| %86 üstü | FuncPoison, 2509.24408 | AgentDriver ve AgentThink sistemleri |
| %81,8 | CHAI, 2510.00181 | DriveLM |
| %73 | Nassi vd., 2508.12175 | Risk sınıflandırması. Yöntem TARA; otomotiv siber güvenlik standardı ISO/SAE 21434'ten uyarlanmış |
| RewardBench 92,5 / 94,3; HaluEval 87,3 / 89,9; JudgeBench 78,6 / 93,1 | CMU, v6 | JudgeBench farkı tabloda −14,6 (yuvarlama); "yaklaşık 14,5" demek doğru |
| 0,044 dolar ve 12,18 dolar; 0,15 saniye | CMU, v6 | |
| AUROC 0,745 ve 0,498 | CMU, v6 | |
| %96 | UPenn, 2609.29769 | 252 emin hatanın 242'si |
| 37 veri setinin 27'si; mikro-F1 0,50'den 0,75'e; ALFWorld %35 ve %54,5 | Deußer vd., v2 | 346.009 istek, toplam maliyet 10 doların altında |
| F1 %90,51'den %7,46'ya | Datadog | Recall %82,90'dan %3,88'e; yakalanan saldırı 3.849'dan 180'e |
| 58 tool, 19 politika (12 kod, 7 LLM), 240 görev, 31 durum değişkeni | CAR-bench | 100 Base, 90 Hallucination, 50 Disambiguation |

**Bu doğrulamadan çıkan iki yeni koz.**

- **Kod, LLM denetçiyi yeniyor.** Signed but Not Safe aynı izlerde iki denetçiyi karşılaştırıyor: deterministik kod doğrulayıcı ihlallerin %78,7'sini yakalıyor ve %7 yanlış alarm veriyor; LLM denetçi %59,0 yakalıyor ve %50 yanlış alarm veriyor. "Başarıyı önce kodla ölçelim" önerinin doğrudan dayanağı.
- **Araç için yazılmış cümle.** From Intent to Action'ın sonucu: "Yapılandırılmış LLM kararları tek başına güvenlik mekanizması olarak yetersizdir; herhangi bir araç fonksiyonu çağrılmadan önce tool izinlerini ve araç durumu kısıtlarını doğrulayan bağımsız bir uygulama katmanı gerekir."

## 5. Yeni bulgular: JEV mimarisi

Önceki rapor "iç mimari yayımlanmadı" diyordu. Bu doğru; ama artık elinde üç ayrı kanıt katmanı var ve üçü aynı resmi çiziyor.

### Katman 1: Şirketin kendi cümleleri (birincil kaynak, bugün okundu)

| Konu | Şirketin yazdığı | Kaynak |
| --- | --- | --- |
| Üç yenilik | "A new model architecture, parallel sampler for maximum efficiency, and training method we call Reinforcement Learning for Calibrated Decisions (RLCD)" | Lansman yazısı |
| Paralel çıktı | "Jev outputs all probabilities in parallel instead of autoregressively generating by token" | Lansman yazısı |
| Durumu bir kez okur | "Jev ingests the state once and evaluates every question against it in parallel" | Models sayfası |
| Sorular bağımsız | "Every question in a request sees the same state, is evaluated independently" | Primitives sayfası |
| Küçük bir LLM mi? | "Jev is neither small nor an LLM" | Lansman SSS |
| RLCD nedir | Ön-eğitimli dil modellerini uyarlamanın üçüncü yolu: RLHF sohbet için, RLVR doğrulanabilir işler için, RLCD kalibre kararlar için | AI primer |
| Eğitim verisi | "We make all the data ourselves." Müşteri verisiyle eğitilmiyor; ince ayar ya da LoRA yok; aynı ağırlıklar her hesaba hizmet ediyor | Lansman SSS, Models |
| Sınırlar | İstek başına 64k token, soru başına 32k; başlıkla 262k'ya çıkıyor ama "daha yavaş ve daha az doğru" | Models |
| Seçenek sayısı | Choice en fazla 255 seçenek | Lansman yazısı |
| Açık benchmark | "We deliberately chose not to publish performance against public benchmarks" | Lansman SSS |

**Buradan çıkan en önemli ipucu.** AI primer RLCD'yi "post-training" (eğitim sonrası uyarlama) yöntemi olarak, ön-eğitimli dil modellerinden çıkan bir dal olarak çiziyor. Yani JEV sıfırdan kurulmuş egzotik bir ağ değil; büyük bir dil modeli gövdesinden başlıyor. "LLM değil" cümlesi çıktı biçimini anlatıyor (metin üretmiyor), gövdeyi değil.

### Katman 2: Davranış deneyleri (Jev's Architecture Unmasked, Archer Hume)

Yazar JEV 1.13'e yaklaşık 10.000 API çağrısı atıp gecikme, token sayımı ve cevap değişimlerinden mimariyi çıkarmaya çalışıyor. Bağımsız bir blog yazısı; hakem değerlendirmesinden geçmedi. Yazar neyin ölçüm, neyin çıkarım olduğunu ayırıyor.

| Deney | Gözlem | Çıkarım |
| --- | --- | --- |
| Gizli kod testi | Gizli bir kodu kardeş soruya koyunca JEV onu göremiyor (olasılık 0,00); aynı kodu state'e koyunca görüyor (0,90 ile 0,92) | Sorular birbirini göremiyor, hepsi state'i görüyor |
| Gecikme | Yaklaşık 100 soruya kadar süre neredeyse değişmiyor; 1.500 soru birkaç yüz milisaniyede dönüyor; süre yalnızca girdi uzunluğuyla artıyor | State bir kez hesaplanıyor, sorular toplu işleniyor |
| Seçenek sayısı | 200 seçenekli soru, 2 seçenekli soru kadar hızlı | Cevap üretilmiyor, okunuyor |
| Sınır hesabı | 23k token'lık state ile 5.000 soru istek sınırına sığıyor | State tek kopya; 2¹⁶ token'lık tek paket, her dal 2¹⁵ |
| İlgisiz seçenek ekleme | Beşinci, ilgisiz bir seçenek eklenince mevcut iki seçenek arasındaki oran değişiyor (10 blokta 10'unda) | Seçenekler ayrı ayrı puanlanmıyor; liste birlikte okunuyor |
| Seçenek sırası | Seçenekleri ters çevirmek olasılığı 0,84 ile 0,89'dan 0,93 ile 0,96'ya oynatıyor | Sıra etkisi var; 0,9 eşiğinde karar değişebilir |
| Sahte seçenek | Metne gömülen sahte seçenek gerçek seçeneklerin yerini alamıyor | Seçenek sınırları metinle taklit edilemeyen özel işaretlerle belirleniyor |
| Tokenizer | 192 açık tokenizer'ın hiçbiriyle eşleşmiyor; en yakını Qwen (415 testin 348'i) | Hangi gövde olduğu bilinmiyor |
| Kalibrasyon | 1.200 MMLU sorusunda beklenen kalibrasyon hatası 0,031 | Olasılıklar toplamda makul; ama modüler üs almada %35 güvenle %56 doğru |

**Yazarın vardığı resim.** Nedensel (causal) bir transformer gövdesi; state bir kez işlenir ve ara sonuçları saklanır; her soru kendi dalında state'e bakar ama diğer soruları görmez; her dalın sonunda metin üretmek yerine seçeneklerin olasılığı doğrudan okunur. Gövdenin seyrek (mixture-of-experts) olduğu tahmini, yazarın da en az emin olduğu kısım.

### Katman 3: Aynı tarifi açık kodla yeniden üretenler

| Model | Tarif | Önemli ayrıntı |
| --- | --- | --- |
| Kev (Jared Palmer), 0,5B'den 27B'ye | Dondurulmuş Qwen gövdesi, rank-16 LoRA adaptörü ve küçük bir "pointer" başlığı. Eğitilen parametre gövdenin %1,9'u | Model kartı Hume'un çıkardığı mimariyi yeniden ürettiğini söylüyor; "JEV değildir" diye de yazıyor |
| Perplexity Decider v1.1 27B | Qwen3.8-27B gövdesi ince ayarlı, dil modeli çıkış katmanı yerine [255 × 5120] boyutunda ayrı bir karar başlığı, kalibrasyon sıcaklığı | Nedensel maskeyi kaldırınca skor arttı. Apache-2.0 |
| reflex | Hiç eğitilmemiş Qwen3.8-27B; etiket olasılıkları doğrudan okunuyor | Tarifin "sıfır" hali |

**CMU makalesinin Ek A'sı** (önceki oturumda görülmemişti) 22 açık modeli JEV ile aynı 5.172 kararda sınıyor:

| Model | Havuz doğruluğu | JudgeBench | Hata AUROC | Gecikme |
| --- | --- | --- | --- | --- |
| Perplexity Decider v1.1 27B | 89,0 | 82,6 | 0,841 | 84 ms |
| Eikos-27B | 89,0 | 78,6 | 0,843 | 61 ms |
| **JEV 1.13 (API)** | **88,3** | **78,6** | **0,822** | 152 ms |
| Kev 27B | 86,5 | 76,3 | 0,816 | 77 ms |
| reflex (eğitimsiz Qwen3.8-27B) | 83,5 | 69,7 | 0,729 | 245 ms |

Makalenin cümleleri: altı açık model JEV'in doğruluğuyla örnekleme hatası içinde; hiçbiri anlamlı biçimde daha iyi değil; beşi JudgeBench'te JEV'in üstünde; "karar ayarı, taban modelden daha önemli" (eğitimsiz 83,5; eğitimli 85,2 ile 89,0); cascade'in bileşenleri "artık JEV'e özgü değil". Gecikmeler tek bir H100 GPU'da yerel ölçüm.

### Mekanizma neden çalışıyor: dört fikir

Mentor "peki nasıl bu kadar hızlı?" diye sorarsa cevap bu dört fikirde.

1. **Okumak paralel, yazmak sıralı.** Bir dil modeli girdiyi okurken (prefill) bütün token'lar zaten bilinir; bir katman hepsini birlikte işler. Yazarken ise her token bir öncekinin seçilmesini bekler. 100 kelimelik cevap 100 ardışık geçiş demek. JEV okumadan sonra duruyor; yazma döngüsü yok. Hızın ve fiyatın asıl kaynağı bu.
2. **State bir kez okunur.** Model, işlediği token'ların ara sonuçlarını saklar (KV cache). 50 soru sorarsan 50'si de aynı saklanmış state'e bakar; state 50 kez yeniden okunmaz. Onuncu soruyu eklemek yalnızca o sorunun token'ları kadar iş çıkarır.
3. **Sorular birbirini göremez.** Dikkat maskesi her soruya "state'i ve kendi dalını gör, diğer soruları görme" der. Bu yüzden bir sorunun cevabı diğerini etkileyemez ve soru eklemek eski cevapları değiştirmez. Bedeli: bir soru diğerinin cevabına muhtaçsa iki ayrı istek gerekir.
4. **Cevap üretilmez, okunur.** Dalın sonundaki iç temsil küçük bir fonksiyona verilir; her seçenek için bir skor çıkar; softmax bu skorları toplamı 1 olan olasılıklara çevirir. Kev'de bu, karar token'ının temsili ile her seçeneğin son token'ının temsili arasındaki iç çarpım. Çıktı her zaman geçerli bir seçenek olduğu için "tip hatası" imkânsız; şirketin "halüsinasyon yapamaz" iddiası bu anlamda doğru, ama yanlış seçeneği seçebilir.

**Eğitim neden "kalibre" ediyor.** Modeli gözlenen sonuca göre log-kayıp ya da Brier kaybıyla cezalandırırsan, kaybı en aza indiren şey gerçek olasılığı söylemektir (bunlara "proper scoring rule" denir). RLCD'nin hangi kaybı kullandığı yayımlanmadı; Wikipedia'daki "Brier skoru içerebilir" cümlesi tahmin. Kev düz çapraz entropi, sıra terimi ve seçenek sırası tutarlılığı için bir KL terimi kullanıyor.

**Tahtaya çizebileceğin şema.** Solda uzun bir yeşil şerit (state, bir kez okunur). Sağında alt alta üç kısa şerit (üç soru; her biri state'e ok çıkarır, birbirine çıkarmaz). Her kısa şeridin ucunda küçük bir kutu (okuma başlığı) ve yanında olasılık çubuğu. Altına tek cümle: "Okuma var, yazma yok."

**Sunumda dürüst cümle.** "Şirket mimariyi yayımlamadı. Ama kendi cümleleri, bağımsız bir API incelemesi ve aynı tarifle JEV'in doğruluğuna ulaşan açık modeller aynı resmi gösteriyor: ön-eğitimli bir dil modeli gövdesi, state'in bir kez okunması, birbirinden yalıtılmış soru dalları ve metin üretimi yerine doğrudan olasılık okuması. Gövdenin hangi model olduğu ve boyutu bilinmiyor."

## 6. Yeni bulgular: sürüm, ad ve üreticinin kendi sınır listesi

**Sürüm değişti.** JEV 1.14 14 Ekim 2026'da çıktı: çok dilli destek iyileşti, görüntü girdisi ve Box (sınırlayıcı kutu) soru tipi geldi, başlıkla 262k token bağlam açıldı. Okuduğun makalelerin hepsi 1.13'ü sınadı. Sunumda "sayılar 1.13 için" de.

**Ad değişti.** TypeSafe 3 Kasım'da "Don't Call It a Decision Model" yazısını yayımladı: "Jev makes judgments, code makes decisions" (JEV yargı verir, kararı kod verir). Şirket "decision model" yerine "System One model" adında ısrar ediyor. Senin için iki sonucu var. Birincisi, sunumda "karar modeli" derken bunun toplulukta tutan ad olduğunu, üreticinin "System One model" dediğini söyle. İkincisi, yazının fikri senin önerinle aynı: tek büyük soru sorma, kararı küçük yargılara böl, mantığı kodda tut. Dört basamaklı ölçüm düzenin bunun uygulaması.

**Üreticinin kendi sınır listesi (Model jaggedness sayfası).** Önceki rapor bunu VentureBeat alıntısından aktarıyordu; şimdi birincil kaynaktan dokuz madde:

| # | Sınır | Üreticinin önerisi | Tezindeki karşılığı |
| --- | --- | --- | --- |
| 1 | Harfi harfine okuma | Koşulu tam yaz | Soruları pilotta sına |
| 2 | Matematik ve sayma | Hesabı kodda yap | Tur sayısı, tutar gibi şeyleri kod saysın |
| 3 | Tarih ve saat karşılaştırma | Parçaları çıkar, kodda karşılaştır | Takvim senaryolarında dikkat |
| 4 | Dolaylılık, çok adımlı akıl yürütme | Adımları azalt | "Bütün iz saldırı mı?" sorusu tam bu sınıf |
| 5 | İlgisiz ayrıntıyla dolu büyük state | Önce filtrele | Uzun izin tamamını verme; ilgili turları seç |
| 6 | Düşmanca içerik | Kriterleri açık yaz, sına | Aşağıya bak |
| 7 | Çelişen talimat ve kriter | Hizala | |
| 8 | Seçenek sırası | Sırayı değiştir, tutarlılığa bak | İki sırayla sor, ortalamasını al |
| 9 | Metin üretimi | Üretici model kullan | |

**6. madde tezin için en önemlisi.** Üreticinin kendi cümlesi: "State is data, and Jev does not treat it as hostile by default. Content written to adversarially steer the model, whether that is an injected instruction, a deliberately misleading framing, or text that argues for its own classification, can move the answer." Yani JEV'in saldırıyla yönlendirilebildiğini artık yalnızca Datadog değil, üretici de yazıyor. "JEV'i saldırı hedefi olarak da test edeceğiz" önerinin en güçlü dayanağı bu.

**5. ve 8. maddeler ölçüm tasarımını değiştiriyor.** Uzun ufuklu bir iz doğası gereği uzun ve ilgisiz ayrıntıyla dolu; üretici bunun doğruluğu düşürdüğünü ("context rot") kendisi söylüyor. Pilotta izin tamamını vermek ile yalnızca ilgili turları vermek arasındaki farkı ölç.

## 7. Öneride ne değişti

| Konu | Önceki öneri | Güncel öneri | Neden |
| --- | --- | --- | --- |
| Hangi model | TypeSafe API'si ya da açık benzeri; mentora sor | Birincil seçenek açık ağırlıklı model, kendi donanımında; JEV API'si karşılaştırma için | Altı açık model JEV ile aynı doğrulukta; veri şirket dışına çıkmıyor; sürüm sabit kalıyor (JEV 1.13'ten 1.14'e bir ayda geçti) |
| Cascade beklentisi | "%41 maliyet" | Kolay kararda yaklaşık %27, zor kararda %67 ile %75 | v6'nın benchmark ayrımı ve canlı testi |
| Eşik | "Kendi verinde seç" | İki sıranın ortalaması, yaklaşık 100 etiket, alt güven sınırı kuralı, iş yükü başına ayrı eşik | CMU v6 tarifi |
| CAR-bench lisansı | Risk | MIT; yalnızca şirket içi onay | Depodaki LICENSE |
| Detektör argümanı | "Detektör %2 yakalıyor" | "Detektör skoru benchmark'tan benchmark'a taşınmıyor" | 2610.03448'in asıl bulgusu |
| Özgünlük iddiası | "Bulabildiğim kadarıyla kimse test etmedi" | Aynı, ama artık kaynaklı: CMU'nun Sınırlar bölümü "ajan içinde kullanım test edilmedi" diyor | CMU v6, Limitations |

## 8. Kaynaklar (bugün açılanlar)

**TypeSafe, birincil.** [Lansman yazısı](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [Jev 1.14](https://typesafe.ai/blog/jev-1-14), [Don't Call It a Decision Model](https://typesafe.ai/blog/dont-call-it-a-decision-model), [The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson), [Lies, Damned Lies, and Benchmarks](https://typesafe.ai/blog/antibenchmaxxing), [Model jaggedness](https://docs.typesafe.ai/model-jaggedness), [Models](https://docs.typesafe.ai/models), [Changelog](https://docs.typesafe.ai/changelog), [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [Confidence](https://docs.typesafe.ai/confidence), [Primitives](https://docs.typesafe.ai/primitives)

**Mimari, bağımsız.** [Jev's Architecture Unmasked](https://archerhume.com/posts/jevs-architecture-unmasked), [Kev model kartı](https://huggingface.co/Terom/kev-0.5b), [Kev kaynak turu](https://pyshine.com/Kev-Trainable-Decision-Models-On-Qwen-Source-Tour/), [Perplexity Decider v1.1](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b), [Wikipedia](https://en.wikipedia.org/wiki/Jev_(AI_model))

**JEV makaleleri.** [JEV-as-a-Judge v6](https://arxiv.org/abs/2609.26550), [Deußer vd.](https://arxiv.org/abs/2609.37647), [Rao ve Callison-Burch](https://arxiv.org/abs/2609.29769), [DecisionRobust](https://arxiv.org/html/2610.19118), [Jev in the Wild](https://arxiv.org/pdf/2609.30216), [Datadog](https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/)

**Benchmark'lar.** [AgentLAB](https://arxiv.org/abs/2602.16901) ([ICML 2026](https://icml.cc/virtual/2026/poster/65640), [kod](https://github.com/TanqiuJiang/AgentLAB)), [CAR-bench](https://arxiv.org/abs/2601.22027) ([ACL 2026](https://aclanthology.org/2026.acl-long.1886/), [kod](https://github.com/CAR-bench/car-bench-ijcai))

**Saldırı, savunma, hakem.** [Passing the Test You Trained On](https://arxiv.org/abs/2610.03448), [AuthorityFlow](https://arxiv.org/abs/2611.04673), [Gizli durum prob'ları](https://arxiv.org/abs/2608.02657), [Signed but Not Safe](https://arxiv.org/abs/2611.07483), [From Intent to Action](https://arxiv.org/abs/2609.19630), [ASB yeniden analizi](https://arxiv.org/abs/2510.05244), [The Attacker Moves Second](https://arxiv.org/abs/2510.09023), [CaMeL](https://arxiv.org/abs/2503.18813), [A Coin Flip for Safety](https://arxiv.org/abs/2603.06594), [Know Thy Judge](https://arxiv.org/abs/2503.04474), [Policy Invariance](https://arxiv.org/abs/2605.06161), [AgentPoison](https://arxiv.org/abs/2407.12784), [FuncPoison](https://arxiv.org/abs/2509.24408), [CHAI](https://arxiv.org/abs/2510.00181), [Nassi vd.](https://arxiv.org/abs/2508.12175)

**Bu denetimin sınırı.** Uzun makalelerde (CaMeL 125 sayfa, UPenn 83 sayfa) her sayfayı satır satır okumadım; tam metni çıkardım, rapordaki her sayıyı aradım ve geçtiği pasajı okudum. Hume'un yazısı bağımsız bir blog; hakem değerlendirmesinden geçmedi ve tek bir hesapla, tek bir günde yapılmış deneylere dayanıyor. Açık modellerin JEV ile aynı mimariyi kullandığı kanıtlanmış değil; aynı arayüzü ve benzer doğruluğu ürettikleri kanıtlanmış.

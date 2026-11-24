# Sunum Soru-Cevap Hazırlığı: "Agent Security and JEV"

Ömer, bu dosya bugünkü sunum için. Mantığı şu: her slaytta hocanın ya da ekipten birinin sorabileceği soruları önceden düşündüm, cevapları da senin ağzından, konuşur gibi yazdım. Sayıların hepsini makalelerin tam metninde tek tek aradım; hangisi doğru, hangisi biraz abartılı, hangisi yanlış, yanına yazdım.

**Nasıl okunur?**
- "Kaynak der ki" = makalenin kendisinde yazan şey.
- "**Çıkarım:**" = benim (ya da senin) yorumun; makalede birebir yazmıyor.
- Tier (seviye) `docs/research/sources.csv`'deki sınıflandırma: **T1** = ana konferans/dergi, hakemli; **T2** = hakemli atölye (workshop) ya da daha küçük hakemli mecra; **T3** = sadece arXiv ön baskı, hakemsiz; **T4** = blog, şirket sayfası.
- ✅ doğrulandı · ⚠️ doğru ama dikkat / biraz abartılı · ❌ yanlış · ❓ doğrulayamadım.

<!-- BOLUM_1_2_BURAYA -->

---

## 3. Slayt slayt sorular ve cevaplar

### Slayt 1 · Cover: "Agent Security and JEV"

**Bu slayt ne diyor:** Literatürü taradın (saldırı, değerlendirici, savunma) ve JEV adlı modelin tezde hakem olarak işe yarayıp yaramayacağına baktın. Altı bölüm var.

**Sayılar:** Yok.

**Olası sorular:**
- **"Bu sunumun amacı ne, bir sonuç mu sunuyorsun yoksa literatür mü?"** → "Bu bir literatür taraması ve tez önerisi. Henüz kendi deneyimi koşmadım; sunduğum sayılar makalelerden. Sonda bu literatürden çıkan boşluğu ve planımı gösteriyorum."
- **"Neden JEV'e bu kadar yer ayırdın?"** → "Hocamız 'JEV modellerini araştır' dedi. Ayrıca tezde her saldırı denemesine bir hakem karar vermek zorunda; LLM hakem pahalı ve yavaş. JEV çok ucuz bir alternatif, ama kandırılabilir mi diye de bakmak gerekiyor. O yüzden hem hakem hem hedef olarak inceledim."
- **"Attack → Evaluate → Defense yapısı nerede?"** → "Bölümler tam o sırada: önce saldırılar, sonra değerlendiriciler, sonra savunmalar, sonra JEV ve tez."

**Zor soru:** "Bu konuda zaten çok survey var, senin katkın ne?" → "Katkım üç şey: araç içi asistan için uzun ufuklu saldırıları ölçen bir test kurmak; 'bu gerçekten saldırı mı?' diye beş kontrolden geçen bir ASR tanımlamak; ve hakemi (LLM ya da JEV) insan etiketine karşı kontrol etmek. Literatürde bu üçünü araçta birlikte yapan bir çalışma bulamadım."

---

### Slayt 2 · Problem: "All the papers I read point to one main problem."

**Bu slayt ne diyor:** Ajan, kullanıcının talimatını ve okuduğu veriyi aynı metin gibi okuyor; ikisini ayıramıyor. Chatbot kandırılınca kötü cevap verir, ajan kandırılınca kötü bir iş yapar (mail atar, rota değiştirir, konum paylaşır).

**Sayılar:** Yok.

**Olası sorular:**
- **"Buna literatürde ne deniyor?"** → "Indirect prompt injection (dolaylı istem enjeksiyonu). 'Dolaylı' çünkü emri kullanıcı değil, ajanın okuduğu veri (e-posta, web sayfası, yorum) taşıyor. Kökü Greshake ve arkadaşlarının 2023 çalışması; AgentDojo ve InjecAgent bunu ajanlar için ölçen ilk büyük benchmark'lar."
- **"Bu neden çözülemiyor? Modele 'veriye uyma' denemez mi?"** → "Deneniyor; prompt'a uyarı koymak, modeli eğitmek gibi. Ama hepsi olasılıksal: model hâlâ aynı metin akışını okuyor. Savunma bölümünde göstereceğim, saldırgan savunmayı bilince bunların çoğu %90'ın üstünde kırılıyor."
- **"Araçta zarar neden daha büyük?"** → "Çünkü ajanın elindeki tool'lar fiziksel ya da kişisel: navigasyon, kapı, cam, telefon, mesaj, konum. E-posta ajanında zarar veri sızıntısı; araçta bir eylem olabilir."
- **"Chatbot'la ajan arasındaki fark tam olarak ne?"** → "Ajan tool çağırıyor ve birden çok adımda çalışıyor. Yani çıktısı sadece metin değil, sistemde kalıcı bir değişiklik."

**Zor soru:** "Bu sorun gerçek bir araçta görüldü mü, yoksa sadece laboratuvarda mı?" → "Araç içi LLM asistanına yapılmış, yayımlanmış uzun ufuklu bir saldırı bulamadım; tezin boşluğu da bu. Sürüş ajanlarına (AgentPoison, FuncPoison, CHAI) ve sesli asistanlara fiziksel kanallardan saldırılar var, ama bunlar simülasyon ya da açık döngü veri setleri. Gerçek araçta görüldü diyemem."

---

### Slayt 3 · Channels: "Where can the attack come in?"

**Bu slayt ne diyor:** Sorun hep aynı, sadece saldırının giriş yolu değişiyor: kullanıcının kendi isteği, ajanın okuduğu metin, bağlı bir uygulamanın açıklaması, hafıza.

**Sayılar ve kaynakları:**

| Slayttaki sayı | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| GPT-4o %48,4 → %72,7 | AgentHarm, arXiv 2410.09024, §4 | ICLR 2025 · T1 | ⚠️ Sayı doğru, ama bu bir **harm score** (rubrikle puanlanan ortalama zarar skoru), "zararlı görevlerin %48,4'ünü yaptı" değil. Makale aynı cümlede reddetme oranının %48,9'dan %13,6'ya düştüğünü yazıyor. |
| AgentDojo: tek gizli metin GPT-4o'da %47,7 | AgentDojo, arXiv 2406.13352, Şekil 8 / Ek Tablo 3 (47,69 ± 3,90) | NeurIPS 2024 D&B · T1 | ✅ Ama dikkat: aynı makalenin Tablo 5'inde (savunma tablosu) savunmasız GPT-4o için **%57,69** yazıyor. İki farklı koşu; hangi tabloyu kullandığını bil. |
| MCPTox: 1.348 test, o1-mini %72,8, reddetme <%3 | MCPTox, arXiv 2508.14925, özet | AAAI 2026 · T1 | ✅ 45 gerçek MCP sunucusu, 353 tool. "Under 3%" en çok reddeden model (Claude-3.7-Sonnet) için; diğerleri daha da az. |
| AgentPoison: >%80 başarı, hafızanın <%0,1'i | AgentPoison, arXiv 2407.12784, özet | NeurIPS 2024 · T1 | ⚠️ Özette "ortalama ≥%80" yazıyor, ama bu **geri getirme (retrieval) başarısı**. Uçtan uca saldırı başarısı daha düşük. Ayrıntı Slayt 7'de. |

**Olası sorular:**
- **"48,4 ne demek, GPT-4o zararlı görevlerin yarısını mı yaptı?"** → "Tam olarak değil. AgentHarm her görevi bir rubrikle puanlıyor; 48,4 ortalama zarar skoru. Yani görevlerin bir kısmını tam, bir kısmını kısmen yapmış. Önemli olan karşılaştırma: basit bir jailbreak şablonu skoru 72,7'ye çıkarıyor, reddetmeyi %48,9'dan %13,6'ya düşürüyor."
- **"MCP nedir?"** → "Model Context Protocol: dış uygulamaların kendi tool'larını ajana tanıttığı standart. Saldırı tool'un açıklamasına yazılıyor; ajan tool'u hiç çalıştırmasa bile açıklamayı okuyor, yani emir doğrudan bağlama giriyor. MCPTox bunu 45 gerçek sunucuda test etti."
- **"Araçta MCP var mı?"** → "**Çıkarım:** Bugün hangi üreticinin MCP kullandığını bilmiyorum. Ama 'araca bağlanan üçüncü taraf uygulama' kanalı genel; MCP sadece bunun en iyi belgelenmiş örneği."
- **"Hafıza saldırısı neden ayrı bir kanal?"** → "Çünkü zaman farkı var: zehirli kayıt bugün yazılıp günler sonra başka bir yolculukta tetiklenebilir. Tek oturumu kontrol eden bir filtre bunu görmez."
- **"AgentDojo'daki %47,7 ile AgentLAB'deki %62,5 aynı saldırı değil mi?"** → "Evet, ikisi de AgentDojo'nun 'important message' saldırısı ve GPT-4o. Fark ortamdan ve koşudan geliyor; AgentLAB kendi görev seçimiyle ölçüyor. Bu yüzden farklı makalelerin sayılarını doğrudan karşılaştırmamak lazım."

**Zor soru:** "Bu dört kanaldan hangisi araçta en gerçekçi?" → "**Çıkarım:** Bence ajanın okuduğu metin: POI yorumları, gelen mesajlar, takvim davetleri. Saldırgan bunlara araca hiç dokunmadan ulaşabiliyor. Bunu ölçülmüş bir sonuç olarak değil, tehdit modelimdeki önceliğim olarak söylüyorum."

---

### Slayt 4 · Many: "The problem is bigger when the attack is split over many messages."

**Bu slayt ne diyor:** Uzun ufuklu (long-horizon) saldırının tanımı: saldırı birçok mesaja bölünüyor, her mesaj tek başına temiz görünüyor, bu yüzden mesaj mesaj kontrol eden filtre kaçırıyor.

**Sayılar:** Yok (resimdeki dört mesaj örnek).

**Olası sorular:**
- **"Long-horizon ile multi-turn aynı şey mi?"** → "Yakın ama aynı değil. Multi-turn jailbreak (örneğin Crescendo) genelde zararlı bir metin çıkarmayı hedefliyor. Long-horizon ajan saldırısında amaç bir eylem: adımlar tool çağrılarına ve hafızaya yayılıyor. AgentLAB bu ayrımı yapıyor."
- **"Bu resimdeki örnek bir makaleden mi?"** → "Hayır, kavramı anlatmak için kendi örneğim. Mantık AgentLAB'in tool chaining tanımından: zararlı hedef, tek başına masum görünen adımlara bölünüyor."
- **"Neden filtre kaçırıyor?"** → "Çünkü filtre her mesaja ayrı bakıyor ve her mesaj gerçekten masum. Zarar ancak bütün sıra birlikte görülünce ortaya çıkıyor. Slayt 21'de AgentLAB'in Llama Guard sonucu bunu sayıyla gösteriyor."

**Zor soru:** "O zaman bütün konuşmayı bir hakeme versek çözülür mü?" → "Kısmen. Bütün izi okuyan bir hakem bağlamı görür, ama iki sorun var: uzun iz doğruluğu düşürüyor (JEV'in kendi üreticisi de 'ilgisiz ayrıntıyla dolu büyük state'te zayıfım' diyor) ve hakem de aynı metni okuduğu için kandırılabilir. Bu yüzden ben önce kodla kontrol, sonra hakem öneriyorum."

---

### Slayt 5 · Families: "The most useful benchmark I found for this is AgentLAB (ICML 2026)."

**Bu slayt ne diyor:** AgentLAB uzun saldırıları beş gruba ayırıyor. İlk ikisinde saldırgan kullanıcı (intent hijacking, tool chaining), son üçünde saldırı ajanın okuduğu veriden geliyor (task injection, objective drifting, memory poisoning).

**Sayılar ve kaynakları:**

| Slayttaki bilgi | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| Beş saldırı türü ve tanımları | AgentLAB, arXiv 2602.16901, Tablo 1 ve §4 | ICML 2026 (PMLR 306) · T1 | ✅ Tablo 1 tanımları: intent hijacking "Deceive agent into executing malicious task", tool chaining "Chain benign tool calls to achieve malicious task", task injection "Inject malicious task alongside benign task", objective drifting "Shift agent's objective", memory poisoning "Persist malicious task in agent's memory". Makale iki tehdit modeli tanımlıyor: kullanıcı saldırgan / ortam saldırgan. |

**Olası sorular:**
- **"Hoca AgentLAB'in önemli olduğunu söylemişti; sen neden önemli buluyorsun?"** → "Üç sebep: uzun ufuklu ajan saldırılarını sistematik ölçen ilk büyük benchmark; ICML 2026'da yayımlandı, yani hakemli; ve kodu MIT lisanslı açık. Tezde saldırı tarafını doğrudan buradan alabilirim."
- **"Kullanıcı saldırgansa bu güvenlik mi, kötüye kullanım mı?"** → "İyi soru. Araçta 'kullanıcı' sürücü olmayabilir: yolcu da sesle komut verebilir. Yani yolcunun sürücü adına yapamayacağı bir şeyi adım adım yaptırması gerçek bir tehdit. Ama 'sürücünün kendi aracına yaptırdığı şey' çoğu zaman saldırı değildir; bunu beş kontrol sorusunun birincisiyle eliyorum."
- **"Tool chaining örneği verir misin?"** → "Takvimi oku, ev adresini bul, onu hedef yap, varış saatini bir yabancıya gönder. Her adım tek başına normal bir asistan işi; birlikte bir takip saldırısı. (Bu benim araç örneğim, makaleden değil.)"
- **"Memory poisoning araçta neye karşılık geliyor?"** → "Sürücü profili ve kayıtlı tercihler. Sahte bir tercih ('her zaman şu adrese de konum paylaş' gibi) bir oturumda kaydedilip sonraki oturumda kullanılıyor."

**Zor soru:** "AgentLAB'in saldırıları gerçekçi mi, yoksa test kurulumundan mı başarılı?" → "Bunu kendim kontrol ettim. AgentLAB'in açık deposundaki task injection sonuçlarına baktım: yayımlanan %79,9 (GPT-4o), her saldırı çifti için 10'a kadar denemenin herhangi birinde başarı demek. Tek denemede bu dosyalarda %32,6 çıkıyor. Yani sayının bir kısmı 'saldırgan çok deneme hakkı aldı' etkisi. Bu hakemli bir sonuç değil, benim depo analizim (`results/agentlab_ti_budget/README.md`); yazarlarla teyit etmem gerekiyor."

---

### Slayt 6 · Attack-text: "What does a real attack look like?"

**Bu slayt ne diyor:** Solda AgentDojo'nun temel saldırı metni kelimesi kelimesine; sağda saldırıların nasıl güçlendirildiği (gradyan/GCG, pekiştirmeli öğrenme, arama, insan) ve "saldırgan savunmayı biliyorsa saldırıyı ona göre kurar" fikri.

**Sayılar ve kaynakları:**

| Slayttaki bilgi | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| `<INFORMATION> This is an important message from me, {user}...` | AgentDojo, arXiv 2406.13352, Ek (Şekil "baseline important message attacker") | NeurIPS 2024 D&B · T1 | ✅ Metin birebir aynı. |
| Dört güçlendirme yöntemi; "500'den fazla kişi çevrimiçi yarışmada" | The Attacker Moves Second, arXiv 2510.09023, §3 ("online red-teaming competition with over 500 participants") | ⚠️ Venue aşağıda | ✅ Sayı doğru. |
| "From 'The Attacker Moves Second' (2025)" | aynı | **Venue düzeltmesi gerekli** | ⚠️ Aşağıdaki nota bak. |

**Venue notu (önemli, kendiliğinden söyle):** The Attacker Moves Second, **ICLR 2026'da reddedildi** (OpenReview: `ICLR.cc/2026/Conference/Rejected_Submission`; `docs/research/00_INDEX.md`). Senin brifinginde bu yüzden "T3, hakemli değil" deniyordu. **Ama** bugün (24 Kasım 2026) usenix.org'daki sayfayı açtım: makale **USENIX Security 2026'da kabul edilmiş** ("Cycle 1 Accepted Papers" altında, sayfa: `usenix.org/conference/usenixsecurity26/presentation/nasr`; aynı bilgi `docs/research/lit/defenses.md` D-44'te de var). Yani repo içinde iki çelişen kayıt var (`sources.csv` A-38 "ICLR 2026 rejected, T3" ve D-44 "USENIX Security 2026, T1"). Güvenli cümle:
> "The Attacker Moves Second ilk olarak ICLR 2026'da reddedildi; daha sonra USENIX Security 2026'ya kabul edildi. Kaynakçamda şu an sadece arXiv numarasıyla duruyor; son versiyonda USENIX künyesiyle düzelteceğim."

Hocana "reddedildi, o yüzden hakemli değil" demek artık eksik olur; "reddedildi ama sonra başka bir hakemli mecrada kabul edildi" demek doğru. Yine de kabul edilen sürümün arXiv sürümüyle aynı sayıları içerdiğini kontrol etmedim (USENIX PDF'ini açmadım).

**Olası sorular:**
- **"Bu metinde hiç zararlı kelime yok, neden işe yarıyor?"** → "Çünkü kibar ve kullanıcıdan geliyormuş gibi yazılmış. Ajan bunu bir veri parçası değil, kullanıcının ek talimatı sanıyor. İçerik filtresi de yakalamıyor çünkü 'zararlı' bir şey yok; zarar {goal} kısmında, o da 'şu adrese e-posta at' gibi normal bir iş olabilir."
- **"Adaptif saldırı ne demek?"** → "Saldırgan savunmayı biliyor ve saldırıyı ona göre optimize ediyor. Sabit bir saldırı listesiyle ölçülen bir savunma o listeyi ezberlemiş olabilir; gerçek saldırgan ikinci hamleyi yapar, adı da oradan geliyor."
- **"GCG nedir?"** → "Greedy Coordinate Gradient: modelin iç gradyanlarını kullanarak saldırı metnine eklenecek en etkili token'ları arayan yöntem. Sadece ağırlıklarına erişebildiğin açık modellerde çalışır."
- **"İnsanlar mı daha iyi, algoritma mı?"** → "Makalenin kendi cümlesi: arama saldırısı %69 başarılı olurken insan kırmızı takımı topluca %100 başarılı oldu (Lesson #3). Yani insanlar hâlâ en güçlü saldırgan."

**Zor soru:** "Tezde adaptif saldırı yapacak mısın? Bu çok pahalı değil mi?" → "Tam AMS ölçeğinde değil. Planım AgentLAB'in kendi saldırgan döngüsünü (planlayıcı + saldırgan + hakem, turlara göre uyarlanıyor) kullanmak; bu zaten bir tür adaptif saldırı. Savunmayı bilen ayrı bir saldırgan versiyonunu bütçeye göre sınırlı bir alt kümede denemeyi düşünüyorum. Kesin bütçeyi pilotta göreceğim."

---

### Slayt 7 · Results: "Two results are important."

**Bu slayt ne diyor:** Birincisi, adımlara yayılan saldırılar daha iyi çalışıyor (GPT-4o'da %62,5 → %79,9). İkincisi, tool chaining en zor durdurulan tür (her modelde %73–96). Bir de araca yakın örnek: AgentPoison.

**Sayılar ve kaynakları:**

| Slayttaki sayı | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| %62,5 (tek mesaj) → %79,9 (çok adım), GPT-4o | AgentLAB, arXiv 2602.16901, **Tablo 3** | ICML 2026 · T1 | ✅ Ama bu karşılaştırma **task injection** türü için; tek mesajlık saldırı AgentDojo'nun "important message" saldırısı. Diğer modeller: Qwen-3 81,9→93,1; Llama-3 50,7→86,8; GPT-5.1 2,08→21,5; Gemini-3 41,0→43,1; Claude-4.5 0→0. |
| Tool chaining %73–96, her modelde | AgentLAB, **Tablo 2** | ICML 2026 · T1 | ✅ En düşük Claude-4.5 %73,3, en yüksek Qwen-3 %96,3. |
| "AgentPoison controlled a driving agent more than 80% of the time while changing less than 0.1% of its memory" | AgentPoison, arXiv 2407.12784 | NeurIPS 2024 · T1 | ❌ **Düzeltilmeli.** Aşağıya bak. |

**AgentPoison düzeltmesi (hoca bunu merak etmişti, kendiliğinden söyle):**
- Makalenin özeti "ortalama ≥%80 saldırı başarısı, <%0,1 zehir oranı" diyor. Ama makale üç ayrı başarı ölçüyor: **ASR-r** (zehirli kayıt geri getirildi mi), **ASR-a** (ajan hedef eylemi üretti mi), **ASR-t** (eylem ortamda hedef etkiyi yarattı mı, uçtan uca).
- Tablo 1, Agent-Driver (sürüş ajanı), ChatGPT + contrastive retriever satırı: **ASR-r 80,0, ASR-a 68,5, ASR-t 56,8**, ACC (normal görev başarısı) 90,4. Yani slayttaki "80" geri getirme başarısı; sürüş ajanını gerçekten hedef eyleme götürme oranı bu ayarda **%56,8**.
- Dört ayarın hepsinde Agent-Driver için ASR-t yaklaşık %54,7–59,6 (`docs/research/lit/attacks.md` A-15, Tablo 1'den).
- Makalenin girişindeki ortalama (üç ajan, tüm ayarlar): "**%82 retrieval başarısı ve %63 uçtan uca saldırı başarısı**, <%1 normal performans kaybı, <%0,1 zehir oranı".
- Bir şey daha: Agent-Driver nuScenes verisi üzerinde **açık döngü** (open-loop) çalışıyor; hedef eylem "SUDDEN STOP" (ani fren). Gerçek ya da kapalı döngü bir sürüş simülasyonu değil.
- **Doğru cümle:** "AgentPoison, sürüş ajanının hafızasının binde birinden azını zehirleyerek zehirli kaydı yaklaşık %80 oranında geri getirtti; uçtan uca, yani ajanın gerçekten ani fren kararı vermesi bu ayarda %57 civarında. Makalenin üç ajan üzerinden ortalaması %82 geri getirme, %63 uçtan uca."

**Olası sorular:**
- **"%62,5 ne demek, 100 denemenin 62'si mi?"** → "Evet, 100 saldırı denemesinden yaklaşık 62'sinde saldırganın hedefi gerçekleşti. AgentDojo ortamında bu ortamın durumuna bakan kodla ölçülüyor."
- **"Claude neden %0?"** → "AgentLAB'in Tablo 3'ünde Claude-4.5 hem tek mesajlık hem uzun saldırıda task injection'da %0. Ama genel ASR'si %28,9, tool chaining'de %73,3. Yani 'Claude güvenli' değil; sadece bu türe dayanıklı."
- **"Tool chaining neden bu kadar zor?"** → "Çünkü her adım gerçekten zararsız bir tool çağrısı. Bir filtre adımı tek başına kontrol ederse yasaklayacak bir şey bulamaz. Zarar sadece sıranın bütününde."
- **"AgentPoison'daki %80 gerçekten 'sürüş ajanını kontrol etti' mi?"** → (yukarıdaki düzeltme) "Hayır, o sayı geri getirme başarısı. Slaytta biraz fazla güçlü yazdım; uçtan uca sayı %57 civarı."
- **"AgentPoison'da tetikleyici ne?"** → "Kullanıcı sorgusuna eklenen optimize edilmiş birkaç token'lık bir tetikleyici; Agent-Driver için 6 token. Yani saldırının çalışması için tetikleyicinin sorguda olması gerekiyor. **Çıkarım:** araçta bunun nasıl gerçekleşeceği ayrı bir soru."

**Zor soru:** "62,5'ten 79,9'a artış gerçekten 'uzun ufuk' yüzünden mi, yoksa saldırgana daha çok deneme hakkı verildiği için mi?" → "Bu tam 'bu gerçekten saldırı mı' sorusu ve haklı bir soru. AgentLAB'in açık deposundaki dosyalara baktım (`results/agentlab_ti_budget/README.md`): GPT-4o'da uzun saldırı ilk denemede %32,6, 3 denemede %59,0, 5 denemede %70,1, herhangi bir denemede %79,9. Yani 62,5'i ancak 3–5 deneme arasında geçiyor. Llama'da makalenin 'tek mesaj' değeri (%50,7) uzun saldırının ilk deneme değeriyle birebir aynı. **Çıkarım:** artışın bir kısmı deneme bütçesi etkisi olabilir; adil karşılaştırma için deneme sayısını eşitlemek lazım. Bunu yazarlarla teyit etmedim; tezde bütçe eşitlenmiş karşılaştırma yapacağım."

---

### Slayt 8 · Real-attack: "We should not trust attack success numbers too quickly."

**Bu slayt ne diyor:** "ASR %74" gibi bir sayı iki şeye bağlı: testin nasıl kurulduğuna ve başarıya kimin karar verdiğine. En iyi örnek ASB: saldırganın tool'ları ajanın listesine zorla ekleniyordu; ajan kendi tool'unu seçince başarı %73,58'den %9,25'e düştü.

**Sayılar ve kaynakları:**

| Slayttaki sayı | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| %73,58 → %9,25 (GPT-4o) | Bhagwatkar vd., "Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?", arXiv 2510.05244, **Tablo 5** ("ASB (ASR ↓) with/without forced attack-tool injection": 73,58 ± 2,70 → 9,25 ± 0,25) | NeurIPS 2025 Lock-LLM Workshop (poster) · **T2** | ✅ Küçük tutarsızlık: makalenin metni aynı yerde "ASR drops sharply from 70% to 9.25%, an almost 8× reduction" diyor; tablo 73,58. Tabloyu kullan. |
| "Agent Security Bench (ASB)" | ASB, arXiv 2410.02644 | Slayt kaynakçasında "ICLR 2025" | ❓ ASB'nin venue'sunu repo'daki `sources.csv`'de bulamadım; ICLR 2025 olarak biliniyor ama ben bu oturumda doğrulamadım. |

**Olası sorular:**
- **"ASB'de tam olarak ne yanlıştı?"** → "ASB her alt görevde saldırganın tool'unu, ajan seçmese bile, ajanın tool listesine zorla ekliyordu ve ajan bu tool'lardan birini çağırınca saldırı başarılı sayılıyordu. Yani test, saldırganın gerçekte yapamayacağı bir şeyi saldırgana veriyordu: ajanın kontrol akışına müdahale. Gerçek saldırgan sadece ajanın okuduğu veriyi değiştirebilir."
- **"Bu ekip başka ne buldu?"** → "AgentDojo'da da düzeltmeler yaptılar: bazı fayda fonksiyonları çok katıydı (örneğin 'kullanıcının gelen kutusunda tam bir mesaj fazla olmalı'), ajan doğru işi yapsa bile fazladan bir mesaj atınca başarısız sayılıyordu. Düzeltince tool_knowledge saldırısı altında GPT-4o'nun faydası 60,87'den 72,19'a çıktı (aynı Tablo 5)."
- **"Bu bir workshop makalesi, güvenilir mi?"** → "Hakemli bir NeurIPS atölyesi (T2), ana konferans değil. Ama iddiası kontrol edilebilir: ASB'nin kodunda zorla ekleme var mı yok mu, bakılabilir. Ben bunu tezde ana iddia olarak değil, 'test kurulumu sonucu şişirebilir' örneği olarak kullanıyorum."
- **"Senin testinde bunu nasıl önleyeceksin?"** → "Beş kontrol sorusunun beşincisi tam bu: 'Gerçek bir saldırgan ajana bu yoldan ulaşabilir mi?' Saldırıyı sadece ajanın normalde okuduğu yerlere (POI yorumu, mesaj, takvim) koyacağım; tool listesine ya da sistem prompt'una dokunmayacağım."

**Zor soru:** "O zaman diğer benchmark'lardaki sayılar da şişkin olabilir mi, AgentLAB dahil?" → "Olabilir, o yüzden 'Checked ASR' öneriyorum. AgentLAB için kendi kontrolüm şu: task injection kısmı AgentDojo'nun durum kontrolüyle ölçülüyor, bu iyi; ama sayı 10'a kadar denemenin herhangi birinde başarı. Diğer dört tür GPT-5.1 hakemiyle ölçülüyor ve o hakem insan etiketiyle kontrol edilmemiş. Ayrıca AgentDojo'nun saklı temiz koşularını saldırı kontrollerine karşı tekrar oynattım: 17.547 çiftte sadece 13'ünde (%0,074) saldırı yokken saldırı kontrolü doğru çıktı, hepsi aynı bankacılık görevinde (`results/agentdojo_clean_oracle_floor/README.md`). Yani AgentDojo'nun kod kontrolü büyük ölçüde temiz."

---

### Slayt 9 · Ev-types: "Who decides that an attack worked?"

**Bu slayt ne diyor:** Saldırının başarılı olduğuna karar veren değerlendirici beş türlü: kod (durum kontrolü), kurallar + küçük LLM soruları, LLM hakem, karar modeli (JEV), insan.

**Sayılar ve kaynakları:**

| Slayttaki bilgi | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| Kod: AgentDojo, InjecAgent | AgentDojo 2406.13352 (state check); InjecAgent 2403.02691 | T1, T1 | ✅ InjecAgent'ta saldırı başarısı = ajanın saldırganın tool'unu çağırması, tool cevapları **simüle** (önceden yazılmış). |
| Kurallar + küçük LLM: AgentHarm | AgentHarm 2410.09024: "human-written rubrics requiring LLM judges only for narrow well-specified subtasks" | ICLR 2025 · T1 | ✅ |
| LLM hakem: AgentLAB | AgentLAB 2602.16901: hakem GPT-5.1, sıcaklık 0 | T1 | ✅ (task injection kısmı hariç; o AgentDojo'nun kod kontrolüyle ölçülüyor. Bkz. Slayt 10.) |
| Karar modeli: JEV; "one study on 5,219 agent traces" | Wang & Gao, "JEV as a Judge for Agent Trace Security", arXiv 2609.34862 | T3 (arXiv) | ✅ 4 benchmark koleksiyonu (R-Judge, ATBench500, TraceSafe alt kümesi, MCPHunt), toplam 5.219 iz. |
| İnsan: referans | – | – | Kavramsal. |

**Olası sorular:**
- **"Kod hakemi neyi göremez?"** → "İz bırakmayan hedefleri. Örneğin 'ajan sürücüyü ikna etmeye çalıştı mı' ya da 'ajan özel bilgiyi cevabında söyledi mi' gibi şeyler sistem durumunda görünmeyebilir. Kod sadece 'e-posta gerçekten gitti mi, rota değişti mi' gibi kalıcı şeyleri kontrol eder."
- **"Karar modeli ile LLM hakem arasındaki fark ne?"** → "LLM hakem bir açıklama yazıp sonunda karar veriyor. Karar modeli hiç metin yazmıyor; durumu bir kez okuyup her seçenek için bir olasılık veriyor. Bu yüzden çok daha ucuz ve hızlı, ama düşünme gerektiren işte daha zayıf."
- **"5.219 izli çalışmada JEV nasıl çıktı?"** → "Dört benchmark ortalamasında JEV'in F1'i 77,8, en iyi LLM hakem GLM-5.2'nin 74,1. Ama ayrıntı önemli: JEV'in precision'ı 77,1, recall'ı 79,2; GLM-5.2'nin precision'ı 91,9, recall'ı 64,1. Doğrulukta (accuracy) GLM daha yüksek: 86,5'e karşı 82,8. Yani JEV daha çok saldırı yakalıyor ama daha çok yanlış alarm veriyor; GLM daha temkinli. Hangisi daha iyi, kullanım amacına bağlı."
- **"İnsan etiketi neden 'referans'?"** → "Çünkü diğer hakemlerin doğruluğunu ölçecek başka bir şey yok. Ama insan da hata yapar, iki kişinin uyuşmasına (inter-annotator agreement) bakmak gerekiyor."

**Zor soru:** "JEV 5.219 izde LLM'leri geçtiyse neden 'kandırılabilir' diyorsun?" → "İki farklı şey. O çalışma normal izlerde doğruluğu ölçtü. Kandırılma ayrı bir test: Datadog, girdiye sahte bir politika metni koyunca JEV'in saldırı yakalama oranının %82,90'dan %3,88'e düştüğünü gösterdi. Ayrıca o çalışma arXiv ön baskısı (T3) ve yazarlar etiketleri revize etmiş; sonuçları 'umut verici bir işaret' olarak söylüyorum, kanıt olarak değil."

---

### Slayt 10 · Ev-bench: "How the main benchmarks decide"

**Bu slayt ne diyor:** Ana benchmark'lar başarıya nasıl karar veriyor: eskiler (InjecAgent, AgentDojo) kodla, AgentHarm kurallarla, AgentLAB LLM hakemle, CAR-bench ikisinin karışımıyla. AgentDojo LLM hakemden kaçınıyor çünkü hakemi de kandırabilecek bir saldırı ölçümü bozar.

**Sayılar ve kaynakları:**

| Slayttaki sayı | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| InjecAgent: 1.054 test | arXiv 2403.02691 ("17 × 62 = 1054": 17 kullanıcı tool'u × 62 saldırgan tool'u) | Findings of ACL 2024 · T1 | ✅ |
| AgentDojo: 97 görev, 629 güvenlik testi | arXiv 2406.13352 | NeurIPS 2024 D&B · T1 | ✅ (70 tool, 27 enjeksiyon hedefi de var.) |
| AgentHarm: 110 zararlı görev (440 varyantlarla) | arXiv 2410.09024 ("110 unique and 330 augmented") | ICLR 2025 · T1 | ✅ 11 zarar kategorisi. |
| AgentLAB: 644 test, LLM hakem (GPT-5.1) | arXiv 2602.16901 | ICML 2026 · T1 | ✅ 28 ortam. ⚠️ Task injection kısmı AgentDojo üzerinde koşuyor ve orada başarı AgentDojo'nun durum kontrolüyle okunuyor (`results/agentlab_ti_budget/README.md`). Yani "AgentLAB = LLM hakem" çoğunlukla doğru, tamamen değil. |
| CAR-bench: 240 görev, 19 kural; 12 kod, 7 LLM hakem | arXiv 2601.22027, Tablo (100 Base, 90 Hallucination, 50 Disambiguation; "19 total → 12 checked code-based, 7 with LLM-as-a-Judge") | ACL 2026 · T1 | ✅ |
| AgentDojo'nun gerekçesi | AgentDojo §3: "if such an attack were particularly successful, there is a chance that it would also hijack the evaluation model" | T1 | ✅ Birebir alıntı bu. |

**Olası sorular:**
- **"Neden yeni benchmark'lar LLM hakeme geçti?"** → "Çünkü uzun ve açık uçlu hedefleri kodla yazmak zor. 'Ajan kullanıcıyı adım adım ikna etti mi' gibi bir şeyi bir durum kontrolüyle ifade edemezsin. LLM hakem her hedefe uyuyor, ama bedeli güvenilirlik."
- **"CAR-bench'te hangi 7 kural LLM'e bırakılmış?"** → "Tam listesini ezbere bilmiyorum; makalenin politika tablosuna bakıp söyleyebilirim. Genel mantık: durumdan okunabilen kurallar (örneğin bir ayarın değeri) kodla, konuşmanın içeriğine bağlı kurallar (örneğin 'kullanıcıya onay sordu mu') LLM'le kontrol ediliyor."
- **"InjecAgent'ın tool cevapları gerçek mi?"** → "Hayır, simüle; önceden yazılmış cevaplar. Bu yüzden ucuz ve tekrarlanabilir, ama ajan gerçek bir ortamda çalışmıyor."
- **"AgentDojo'nun argümanı senin tezin için neden önemli?"** → "Çünkü benim saldırılarım tam olarak ajanın okuduğu metne talimat koymak. Hakem de o metni okursa, aynı talimat hakemi etkileyebilir. AgentLAB'in GPT-5.1 hakemi bu riske açık ve makale bunu ölçmüyor."

**Zor soru:** "AgentLAB'in hakemi saldırı döngüsünün içinde de kullanılıyor mu?" → "Evet. Makalenin ekinde GPT-5.1 hem planlayıcı (sıcaklık 0,5) hem iç hakem (sıcaklık 0) olarak geçiyor; saldırgan iç hakemin geri bildirimine göre metni düzeltiyor. **Çıkarım:** saldırı aynı hakemi geçmek için optimize ediliyorsa, ölçüm hakeme fazla bağımlı olabilir. Bunu ayrı, bağımsız bir hakemle (ya da kodla) tekrar ölçmek tezin bir parçası olabilir."

---

### Slayt 11 · Judge: "The second problem is the judge."

**Bu slayt ne diyor:** Çoğu test saldırının başarılı olup olmadığına bir LLM'le karar veriyor ve bu hakem yanılabilir. AgentLAB'in hakemi GPT-5.1 ve insan etiketine karşı kontrol edilmemiş. Bu yüzden insan etiketli veri eklemeyi düşünüyorsun.

**Sayılar ve kaynakları:**

| Slayttaki bilgi | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| AgentLAB hakemi GPT-5.1, insanla kontrol edilmemiş | AgentLAB 2602.16901 | T1 | ✅ Tam metinde hakemin insan etiketiyle doğrulandığı bir bölüm yok (metinde "human annotation/agreement" araması boş; `Kaynak Denetimi` §3.2 aynı sonuç). |
| (Konuşmacı notu) "A Coin Flip for Safety: 6.642 insan etiketi, LLM hakemler neredeyse tahmin kadar kötü" | Schwinn vd., arXiv 2603.06594 | ICML 2026 · T1 | ✅ ⚠️ Makalenin kendisinde iki sayı geçiyor: özette ve veri bölümünde **6642**, girişte **6,442**. 6.642 de. Ayrıca bu makale **jailbreak çıktılarının zararlı olup olmadığını** değerlendiren hakemlere bakıyor (ajan izi değil); "dağılım değişince (farklı saldırı, farklı model) performans rastgeleye yaklaşıyor" diyor. |

**Olası sorular (hoca burada "insan etiketlemesi çok zaman alır" diyecek, hazırlıklı ol):**
- **"İnsan etiketleme çok uzun sürer, bunu nasıl yapacaksın?"** → "Haklısınız, her şeyi etiketlemeyi düşünmüyorum. Üç şey öneriyorum: (1) Başarıyı önce kodla ölçmek; araç ortamında 'rota değişti mi, mesaj gitti mi' gibi hedefler durumdan okunabiliyor ve insan gerektirmiyor. (2) Hakemi sadece kodun karar veremediği küçük bir alt kümede kullanmak. (3) İnsan etiketini sadece hakemi kalibre etmek için küçük bir örneklemde kullanmak; CMU'nun JEV çalışması eşik seçmek için yaklaşık 100 etiketli örnek öneriyor. Yani yüzlerce değil, iş yükü başına 100 civarı."
- **"100 etiket yeter mi?"** → "Hakemi baştan doğrulamak için değil, eşik seçmek için yeterli; bu CMU makalesinin önerisi (arXiv 2609.26550; T3). Hakemin hata oranını güvenle söylemek için daha fazlası gerekebilir. **Çıkarım:** önce 100 ile başlayıp güven aralığına bakarım."
- **"VehicleWorld'e baktın mı?" (hoca önermişti)** → "Baktım. VehicleWorld (Fudan Üniversitesi, Findings of EMNLP 2025, arXiv 2509.06736) bir sanal araç kokpiti ortamı: 30 modül, 250 API, 680 özellik, 1.291 görev. Önemli yanı: başarıyı **durum geçişlerine bakarak** ölçüyor, yani her API çağrısından sonra ortamın durumu kaydediliyor ve hedef durumla karşılaştırılıyor. Bu, insan etiketine olan ihtiyacı azaltır; kod hakemi için ideal. Eksik yanı: güvenlik ya da saldırı yok, tamamen görev başarısı ölçüyor. **Çıkarım:** CAR-bench'e alternatif ya da tamamlayıcı bir araç ortamı olabilir; özellikle durum tabanlı kontrol için. Lisansını henüz kontrol edemedim (kod GitHub'da OpenMOSS/VehicleWorld)."
- **"LLM hakem neden yanılsın, GPT-5.1 çok güçlü bir model?"** → "Güçlü ama iki risk var: hakem de aynı enjekte metni okuyor, yani kandırılabilir (AgentDojo'nun argümanı); ve dağılım değişince hakemlerin performansı düşüyor (Coin Flip). Bunu ölçmeden 'GPT-5.1 doğru söylüyor' diyemem."

**Zor soru:** "AgentLAB'in hakemi yanlışsa, AgentLAB'in bütün sonuçları mı yanlış?" → "Hayır, öyle demiyorum. Sadece ne kadar doğru olduğunu bilmiyoruz. Task injection kısmı zaten kodla ölçülüyor ve benim depo analizimde yayımlanan sayılar dosyalarla birebir tuttu (GPT-4o %79,9). Diğer türler için hakemin hata payını ölçmek tezin işi."

---

### Slayt 12 · Ev-tested: "Can we check the judges themselves?"

**Bu slayt ne diyor:** Evet: hakeme insanların cevabını bildiği konuşmaları verip ne kadar uyuştuğuna bakılıyor. R-Judge'da en iyi hakem GPT-4o 74,45; AgentAuditor hakeme etiketli örnek hafızası verince skor 96,3'e kadar çıkıyor. Uzun araç saldırılarında bunu yapan kimseyi bulamadın.

**Sayılar ve kaynakları:**

| Slayttaki sayı | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| R-Judge: 569 konuşma; GPT-4o 74,45 | Yuan vd., R-Judge, arXiv 2401.10019 | Findings of EMNLP 2024 · T1 (slaytta "2024") | ✅ 74,45 = **F1** (güvenlik yargısı). 27 senaryo, 10 risk tipi. Not: makalenin özetinde 74,42, girişte ve tabloda 74,45 yazıyor. |
| "Most other models did about as well as guessing" | R-Judge: "no other models significantly exceed the random" | T1 | ✅ Rastgele F1 = 51,32. |
| AgentAuditor: 96,3'e kadar | Luo vd., AgentAuditor, arXiv 2506.00641, Tablo 1 | NeurIPS 2025 · T1 | ⚠️ 96,31 F1 R-Judge'da, ama **GPT-4o değil, Gemini-2.0-Flash-thinking** + AgentAuditor ile. Aynı tabloda GPT-4o: 74,55 → **90,56**. Slayt "the judge ... scored up to 96.3" diyor; "aynı hakem 74'ten 96'ya çıktı" gibi anlaşılabilir. Doğrusu: "en iyi taban modelle 96,3'e kadar; GPT-4o'yla 90,6." |
| "About as good as a human expert" | AgentAuditor: doğruluğu tek bir insan etiketleyicinin ortalamasıyla karşılaştırıyor | T1 | ✅ (Makale "human-level" diyor; doğruluk 96,10, tek insan etiketleyici R-Judge'da %95,7.) |

**Precision / recall ayrıntısı (sorulursa):**
- R-Judge, GPT-4o, **kasıtlı saldırılar** alt kümesi: F1 72,19, **recall 91,50**, **specificity 42,06**. Yani riskli durumların çoğunu yakalıyor ama güvenli durumların yarısından fazlasına da "riskli" diyor (çok yanlış alarm). İstenmeyen riskler alt kümesinde F1 80,90, recall 72,00, specificity 89,09.
- F1 nedir: precision (alarm verdiğinde ne kadar haklı) ile recall (gerçek riskin ne kadarını yakaladı) dengesini tek sayıda veren 0–100 puan.

**Olası sorular:**
- **"74,45 'out of 100' ne demek, %74 doğru mu?"** → "Hayır, F1 skoru. Doğruluk değil; hem kaçırılan riskleri hem yanlış alarmları cezalandıran bir ortalama. Rastgele tahmin bu testte 51 civarı F1 alıyor."
- **"AgentAuditor ne yapıyor?"** → "Hakeme geçmiş etiketli örneklerden bir hafıza veriyor; yeni bir izi değerlendirirken benzer örnekleri getirip onlara bakarak akıl yürütüyor. Yani bir tür örnekle öğrenme (retrieval + reasoning)."
- **"O zaman AgentAuditor'ı kullanıp insan etiketinden kurtulamaz mıyız?"** → "Kısmen. Ama AgentAuditor'ın hafızası da etiketli örneklerden oluşuyor; yani insan etiketi yine lazım, sadece daha az. Ayrıca kısa izlerde ölçüldü; uzun ufuklu araç saldırılarında ne yapacağını bilmiyoruz."
- **"Neden uzun saldırılarda kimse yapmamış?"** → "Bulabildiğim kadarıyla uzun ufuklu saldırı benchmark'ları (AgentLAB) çok yeni ve hakemi doğrulamadan yayımlanmış. Hakem doğrulama çalışmaları ise kısa izlerde. Arada bir boşluk var."

**Zor soru:** "R-Judge 2024'ten ve GPT-4o ile; bugünkü modellerde hakem sorunu hâlâ var mı?" → "Daha yeni kanıt da var: A Coin Flip for Safety (ICML 2026) 6.642 insan doğrulamalı örnekte hakemlerin dağılım değişince rastgeleye yaklaştığını gösteriyor. 5.219 izli JEV çalışmasında da en iyi LLM hakem GLM-5.2'nin recall'ı 64,1; yani saldırıların üçte birini kaçırıyor. Sorun güncel."

---

### Slayt 13 · Metrics: "Which numbers should we report?"

**Bu slayt ne diyor:** Tek bir ASR sayısı yanıltabilir. Raporlanması gerekenler: saldırısız fayda (benign utility), saldırı altında fayda (utility under attack), hedefli ASR, kısmi/tam başarı, tur sayısına göre ASR ve senin önerin "Checked ASR". WASP örneği: saldırılar %86'ya kadar kısmen başarılı ama tam başarı %0–17.

**Sayılar ve kaynakları:**

| Slayttaki sayı | Kaynak | Venue / Tier | Durum |
|---|---|---|---|
| Benign utility, utility under attack, targeted ASR | AgentDojo 2406.13352 | T1 | ✅ AgentDojo'nun tanımları. |
| Kısmi ve tam başarı; "up to 86%", "0–17%", "security by incompetence" | WASP, Evtimov vd., arXiv 2504.18575, özet ve §1 | NeurIPS 2025 D&B · T1 | ✅ "attacks partially succeed in up to 86% of cases ... attacker task completion rates ranging from 0 to 17%". ⚠️ Dikkat: **kısmi başarı (ASR-intermediate) GPT-4o tabanlı bir LLM hakemle** ölçülüyor; uçtan uca başarı kurallarla. |
| ASR by number of turns | AgentLAB, Şekil 7 (izin verilen tur sayısına göre ASR) | T1 | ✅ |
| Checked ASR | Senin önerin | – | Kendi katkın. |

**Olası sorular:**
- **"Benign utility neden güvenlik raporunda?"** → "Çünkü savunmanın bedelini gösteriyor. Hiçbir şey yapmayan bir ajan %0 ASR alır; ama işe yaramaz. MELON tablosunda LLM detektörünün saldırı altında görevlerin %0'ını bitirdiğini göstereceğim."
- **"Security by incompetence ne demek?"** → "Ajan saldırıya uymaya başlıyor ama beceriksiz olduğu için saldırganın işini bitiremiyor. Yani güvenli değil, sadece yetersiz. Model daha yetenekli olunca bu 'güvenlik' kaybolur."
- **"Araçta kısmi başarı zararlı mı?"** → "**Çıkarım:** Olabilir. Web'de yarım kalan bir saldırı zararsız olabilir; araçta 'navigasyonu değiştirmeye başladı ama bitiremedi' bile sürücünün dikkatini dağıtabilir. Bu yüzden zarar ölçeğini fiziksel eylemlere göre ayrı düşünmek istiyorum (Slayt 30, boşluk 6)."
- **"Neden ASR'yi tur sayısına göre veriyorsun?"** → "Çünkü uzun saldırının gücü tur sayısıyla artıyor. Tek bir sayı 'kaç tur izin verildi' sorusunu gizliyor. Ayrıca deneme sayısıyla tur sayısını ayırmak lazım (Slayt 7'deki zor soru)."

**Zor soru:** "Checked ASR'nin bir formülü var mı, yoksa sadece fikir mi?" → "Şu an bir tanım ve bir prototip var. Tanım: hakemin 'başarılı' dediği vakalardan beş kontrolü geçenlerin oranı. Prototipte (sentetik, gerçek LLM yok; `results/prototype/README.md`) bunu 'ham ASR', 'saldırısız aynı görevdeki oran', ikisinin farkı (causal) ve 'doğrulanmış' sütunlarıyla hesaplıyorum. Bu prototip sadece ölçüm hattını test ediyor, LLM'ler hakkında bir kanıt değil. Gerçek sayıyı ilk pilotta göreceğim."

---

### Slayt 14 · Questions: "So before I count something as an attack, I ask five questions"

**Bu slayt ne diyor:** Bir şeyi saldırı saymadan önce beş soru: (1) talimat yetkili birinden mi geldi, (2) saldırı olmadan da aynı şey olur muydu, (3) gerçekten bir zarar var mı, (4) sistemde gerçekten oldu mu (sadece cevapta değil), (5) gerçek bir saldırgan bu yoldan ulaşabilir mi. Çıktı: ham ASR ve Checked ASR.

**Sayılar:** Yok. Dayanaklar: Soru 2 → CAR-bench'in saldırısız hata oranı ve senin `carbench_noise_floor` analizin; Soru 4 → AgentDojo'nun durum kontrolü; Soru 5 → ASB örneği (Slayt 8).

**Bu slayt hocanın "Bu gerçekten saldırı mı?" yönergesinin doğrudan cevabı. Vurgula.**

**Olası sorular:**
- **"Bu beş soruyu nereden aldın?"** → "Kendi önerim. Her soru literatürde gördüğüm bir yanlış pozitif türünü eliyor: 1 meşru talimat (sürücünün kendi isteği), 2 ajanın kendi hatası, 3 zararsız sapma, 4 sahte başarı (ajan 'yaptım' diyor ama sistemde olmamış), 5 gerçekçi olmayan test kurulumu (ASB)."
- **"Soru 2'yi nasıl ölçeceksin?"** → "Her görevi bir de saldırısız koşturarak. CAR-bench yazarlarının yayımladığı saldırısız koşulara baktım: aynı görev, aynı model, üç denemede farklı sonuç veriyor; öncü modellerde görevlerin %12–34'ü denemeler arasında değişiyor. Yani saldırılı bir koşuda görevin başarısız olması tek başına saldırının kanıtı değil (`results/carbench_noise_floor/README.md`, kendi analizim)."
- **"Soru 3, zarar, nasıl tanımlanacak? Bu öznel değil mi?"** → "Öznel olmaması için kategoriler kullanacağım: gizlilik (konum, kişi bilgisi dışarı çıktı mı), para, fiziksel güvenlik (sürüşü etkileyen bir eylem). 'Beyond Attack-Success Rate' (arXiv 2607.07474) tool çağrıları için L0–L6 bir ölçek öneriyor; ben bunu araçtaki fiziksel eylemlere uyarlamayı düşünüyorum."
- **"Soru 4 her zaman kontrol edilebilir mi?"** → "Durumu olan hedeflerde evet: mesaj gitti mi, rota değişti mi, cam açıldı mı. Sadece konuşmada kalan hedeflerde (örneğin bilgi sızdırma sesli cevapla) kod yetmez; orada hakem gerekiyor."
- **"Checked ASR hep ham ASR'den düşük mü çıkar?"** → "Tanım gereği eşit ya da düşük, çünkü sadece eleme yapıyor. Aradaki fark, hakemin ya da testin ne kadar şişirdiğini gösteriyor; bu farkın kendisi bir bulgu."

**Zor soru:** "Bu kontrolleri kim uygulayacak? Yine bir insan ya da LLM mi karar verecek?" → "Mümkün olduğunca kod. Soru 1, 4 ve 5 kodla ya da test tasarımıyla çözülüyor (talimatın kaynağı izleniyor, sistem durumu okunuyor, saldırı sadece gerçekçi kanallara konuyor). Soru 2 eşleştirilmiş saldırısız koşuyla. Soru 3 bir zarar listesiyle; belirsiz kalan az sayıda vakayı insan ya da hakem etiketler. Hangi kontrolün ne kadar insan gerektirdiğini pilotta sayacağım."

---

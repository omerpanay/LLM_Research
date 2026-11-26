# Tez Kararları ve Öneriler (26 Kasım 2026)

Kaynaklar: Tam Rehber Bölüm A (senin kararların), senin düzelttiğin D (Tab 1), F'de slayt 16 ve 19, G.2 ve yeni okunan 10 makale. "Çıkarım:" = benim yorumum, kaynağın söylediği değil.

---

## 1. Alınan kararlar

| Alan | Karar |
|---|---|
| **Ortam** | Şimdilik **VehicleWorld** temel alınıyor. Kalanlar: araç cihazları VehicleWorld'den; ortama sürüş bağlamı (park/sürüş, hız) ve konuşan rolü (sürücü/yolcu) eklenecek; her durum değişikliğinden sonra anlık görüntü alınacak; kod izole konteynerde çalışacak ve lisans yazarlara sorulacak; saldırgan bilgileri (numara, IBAN, POI, adres) hiçbir kullanıcı görevinde geçmeyecek ve her sürümden önce temiz koşu tekrarı yapılacak. |
| **Saldırılar** | AgentLAB'in 5 ailesi, başarı metinden değil ortam durumundan ölçülerek. Talimatsız POI/şarj çarpıtma. Eşit bütçeyle karşılaştırma ve ASR(b) eğrisi. |
| **Değerlendirme** | **4 soruluk filtre** (Q5 yok). **Placebo yok.** **İnsan etiketlemesi şimdilik yok.** Metrikler: Checked ASR, nedensel ASR, bütçe eğrisi, TUA, DIC, yan etki. Ara adım ile uçtan uca sonuç ayrı raporlanacak. Her sonuçta n, deneme sayısı ve güven aralığı verilecek. |
| **Savunma** | D4 (araç durumuna duyarlı karar kökeni kapısı). Onay bütçesi (DIC ile ölçülecek). Savunmalar uyum sağlayan saldırganla test edilecek; ASR her zaman görev başarısıyla birlikte raporlanacak. |
| **JEV** | Ön eleme ve basamaklı kullanımın ilk adımı; son hakem değil. |
| **Araçlar** | Langfuse kullanılacak. İş VW'nin onayladığı araçlarla ve iç GitLab'da sürecek. |
| **Yayın** | Şimdilik yok. |

---

## 2. Kararların sonuçları: dikkat edilecek 5 nokta

1. **VehicleWorld'de de saldırısız hata var.** CAR-bench'i "saldırı olmadan da görev tamamlanamıyor" diye bıraktık. Ama VehicleWorld'de de ReAct ortalaması %51,1 (kod yazarak çağırma) ve %61,5 (durum yazarak); en iyi model GPT-4o %70,2 (VehicleWorld Tablo 4). Yani sorunu ortam seçimi çözmüyor. Çözen şey **eşleşmiş temiz koşu (Q2)** ve **dar, hedefe özel kontrol**. Örneğin "saldırganın numarası arandı mı?" diye bakmak, "ajan istenmeyen bir şey yaptı mı?" diye bakmaktan çok daha temiz. CAR-bench'te dar kontroller saldırısız koşularda neredeyse hiç tetiklenmedi (güçlü modellerin yaklaşık 1.300 koşusunda istenmemiş e-posta veya arama yok, D 7.3).
2. **VehicleWorld'de saldırı kanalı yok denecek kadar az.** Sadece SMS, kişi adı ve medya açıklaması var; POI, şarj, takvim ve e-posta yok. Talimatsız POI saldırısı (Ş) için **küçük bir POI/şarj arama aracını kendimiz eklemeliyiz.** Bunun için CAR-bench'in POI formatını ve verisini (MIT) kullanabiliriz; CAR-bench'in değerlendirmesini kullanmak zorunda değiliz.
3. **Placebo yoksa nedensel ASR temiz koşuyla hesaplanır:** Δ = ortalama(Y − Y⁰). Burada Y⁰ artık aynı görevin **saldırısız koşusu**. D 8.5'teki M2 tanımı ve 4.3'teki "placebo kolunun hazırlanması" satırı buna göre düzeltilmeli. Ayrıca 4.3'te başlık "Dört soru" ama metin hâlâ "beş sorunun hepsine" diyor.
4. **Q5 yoksa gerçekçilik tasarımla sağlanmalı.** ASB tipi hatayı (saldırganın aracını zorla listeye eklemek) artık filtre yakalamayacak. Bunu önlemek için her saldırı için bir **tehdit modeli kartı** yazalım: saldırgan neye dokunabilir, neye dokunamaz. Bu kart koşudan önce bir kez yazılır, ek maliyeti yok.
5. **İnsan etiketi yoksa hakem düzeltmesi de yok.** O zaman **her saldırı hedefi kodla kontrol edilebilir olmalı.** Hedefi sadece metinle ölçülebilen vakalar (ör. AgentLAB'in araçsız niyet kaçırması) ya tezden çıkar ya da "doğrulanmamış hakem ASR'si" diye ayrı raporlanır. JEV'in "insan için ön etiketleme" rolü de bu yüzden şimdilik boşta kalıyor. JEV için iki rol kalıyor: LLM hakemine giden **basamaklı kullanımın ilk adımı** ve **koruma katmanlarından biri**.

---

## 3. Yeni kaynaklar: ne buldum, ne öneriyorum

Hepsinin tam metnini okudum. Yayın yerleri PDF'lerden kontrol edildi. Son yüklediğin 7 PDF için 3b'ye bak.

| Kaynak | Yayın | Bizim için ne var? | Öneri |
|---|---|---|---|
| **AgentSentry** | NDSS 2027 (PDF'te NDSS başlığı ve DOI var), T1. Kod: github.com/CyberGuardianAI/AgentSentry | Araç dönüşlerinde karşı-olgusal yeniden çalıştırma (counterfactual replay) yapıyor: araçtan gelen içerik değiştirilince önerilen eylem aynı kalıyor mu? Değişiyorsa içeriği temizleyip devam ediyor. AgentDojo'da ASR %0, UA %76,1. **Uzun soluklu testte** (96 akış, L = 3–24 tur) ASR %11,5 ve ufuk uzadıkça kötüleşiyor. **Adaptif testte atlatan 2 vakanın ikisi de "talimatsız, makul görünen alıcı bilgisi."** Gecikme yaklaşık 2 kat (saldırılı koşuda 26 → 50 s). | **Kanıt olarak al.** Bu, A.2'deki talimatsız POI saldırımızın en güçlü yeni savunmalardan bile kaçtığını gösteriyor. Baseline olarak çok yavaş; zaman kalırsa (Ö). |
| **AgentSpec** | ICSE 2026, T1. Repoda lisans dosyası yok | Kural = tetikleyici + koşul + yaptırım (durdur / kullanıcıya sor / LLM öz-denetim). Apollo sürüş yazılımında da denenmiş. Yazarların kendi kabul ettiği sınır: tek adımlık kontrol, gidişata bakmıyor, saldırgan testi yok. | **D4 kurallarının yazım biçimi olarak al** (koşullara araç durumu eklenir). Kodunu kopyalama, küçük bir ayrıştırıcıyı (parser) kendin yaz. "LLM öz-denetim" yaptırımını kullanma; kandırılabilir. |
| **FIDES** | NeurIPS 2026, T1. Kod MIT | Her değere iki etiket: güvenilir mi (T/U) ve kim okuyabilir. P-T kuralı: önemli eylem sadece güvenilir bağlamdan tetiklenebilir. P-F kuralı: veri sadece okuma izni olan alıcıya gidebilir. Güvenilmeyen veriyi gizli değişkende tutup tipli soru soruyor (ör. evet/hayır). | **D4'ün hakemli dayanağı olarak al.** P-T tek başına "en yakın şarj istasyonu" görevini de engeller (prototipte fayda 0,95 → 0,00); bizim katkımız araç durumu ve karar kökeni. |
| **PRUDENTIA** | ICLR 2026, T1 | İki metrik tanımlıyor. **HITL load:** başarılı görevlerdeki toplam onay sayısı. **TCR@k:** en fazla k onayla bitirilen görevlerin oranı. Ölçüm **saldırısız** koşularda ve "insan her onayı doğru verir" varsayımıyla yapılıyor. Bir de **"veriyi onaylatma" (endorsement)** fikri var: her araç çağrısı yerine bir veriyi bir kez onaylatmak. | **DIC'yi bunun üstüne kur.** k = sürüş başına onay bütçesi, ölçüm saldırı altında, onay isabeti ve sürüş durumu eklenir (yenilik bizde). Arabada endorsement şuna benzer: "Bu istasyon bilgisine güveneyim mi?" sorusu her işlem için değil, bir kez sorulur. |
| **ShadowMem** | ACM CCS 2026, T1. Lisans yok | Uzun soluklu ve adaptif saldırıyla test edilmiş tek hakemli gidişat savunması (G.2 §1c). Saldırgan, şüpheli işaretleri önceden "açıklayan" cümlelerle %25'e kadar atlatabiliyor. | D5 için Ö (seçmedin). Seçersen tek kural: **defterdeki kritik bilgiler (alıcı rehberde mi, hız ne) LLM özetinden değil, araç API'sinden gelsin.** |
| **SecOPD** | EMNLP 2026, T1. Model: HF'de pybbb/Qwen3.6-27B-SecOPD | Model düzeyinde savunma: adaptif saldırıda ASR %9,0 (Meta-SecAlign %94,0); AgentDojo'da %4,7. Kendi sınırları: sadece dolaylı injection; **kullanıcı/yolcu saldırgansa işe yaramıyor**; güvenilir ve güvenilmeyen girdinin ayrı verilmesi şart; adaptif test ajanda değil, SEP'te yapılmış. | **Çekirdeğe alma.** VW'de GPU olursa ajanın modeli olarak ek bir deney kolu olabilir (ücretsiz, yerel). Yolcu kaynaklı zincirleme saldırıları zaten kapsamıyor. |
| **Adaptive Adversaries** | NeurIPS 2026 E&D, T1. Kod MIT | İlk turda ASR %0–1, 15 turda %7,9–16,8. 3 farklı saldırgan LLM birlikte, en iyi tek saldırgana göre 1,7–2,2 kat daha çok farklı başarılı saldırı buluyor (3 kat bütçeyle). Araç yok. | **Değerlendirme protokolü olarak al:** oturum türü (taze / kalıcı) sabitlensin; ASR(1) ve ASR(15) birlikte raporlansın. Bütçe yeterse saldırgan olarak en az 2 farklı model kullanılsın. |
| **The Attacker Moves Second** (yüklediğin) | USENIX Security 2026, T1 | Arama tabanlı saldırgan: öner → puanla → seç → güncelle döngüsü. Savunmaya özel değil ve ucuz. Önemli tavsiye: "Bütçe kısıtlıysa büyük test setinde zayıf saldırı yerine **küçük test setinde güçlü saldırı**." Başarılı örnek tetikleyicilerden biri sahte bir politika metni ("ACCESS_POLICY_ENFORCED … prerequisite workflow"). | **Uyum sağlayan saldırganımız bu döngü olsun.** Az görevde, güçlü saldırıyla; ASR'yi sorgu sayısına göre eğri olarak raporla. Sahte politika/yetki metnini ayrı bir saldırı varyantı yap (JEV'e karşı Datadog'un bulduğu şeyle aynı desen). |
| **AuthorityFlow** (yüklediğin) | arXiv, ICLR 2027'ye gönderilmiş, T3. Kod yok | Parametre zehirleme: doğru araç, yanlış parametre (alıcı, hesap). Görev başına "hangi bilgi alanı hangi parametreyi belirleyebilir" diye bir yetki tablosunu **bir LLM kuruyor**. 144 eşli vaka. Adaptif test yok. | **Fikri al, LLM kısmını alma.** Arabada alan dar olduğu için bu tabloyu **sabit kodla** yazabiliriz: `navigate.hedef` ← sürücünün sesi, kayıtlı adresler, OEM POI veritabanı; yorum metni asla. Bu D4'ün çekirdeği. 144 eşli vaka düzeni talimatsız POI vakalarımız için şablon. |
| **Agent-Driver** (yüklediğin) | COLM 2024, hakemli | AgentPoison'un saldırdığı sürüş ajanı: araç kütüphanesi + hafıza (kurallar ve geçmiş senaryolar) + akıl yürütme + öz-düzeltme. Öz-düzeltme deterministik bir `collision_check` ile yapılıyor: LLM'in rotası kodla kontrol edilip düzeltiliyor. | Kokpit asistanı değil, hareket planlayıcı; doğrudan kullanmayalım. Ama **D'deki "başka mimari" notuna cevap:** dördüncü mimari olarak **"hafızalı ajan + deterministik son kontrol"** eklenebilir. Hafıza zehirleme ailesini zaten test ediyoruz. |

### 3b. Son yüklenen PDF'ler

AgentSentry ve ShadowMem dosyaları daha önce okuduklarımla aynı; yeni bir şey yok.

| Kaynak | Yayın | Bizim için ne var? | Öneri |
|---|---|---|---|
| **CaMeL** (IEEE sürümü) | IEEE SaTML 2026, s. 587; DOI PDF'te var. **Yayın yeri artık birincil kaynaktan doğrulandı** | 77% vs 84% aynı (o3 modeli). | Künye kesinleşti. |
| **AgentDyn** | arXiv, T3. ROPE ve AutoDojo ile aynı grup (Vorobeychik, Xiao). Kod: github.com/leolee99/AgentDyn | 60 açık uçlu görev, 560 saldırı vakası. **CaMeL her modelde fayda 0, ASR 0** (Tablo 3). Planlamaya dayalı savunmalar (Tool Filter, CaMeL, DRIFT) dinamik görevde çöküyor. PIGuard ve ProtectAI, dış veride **yardımcı talimat** varken faydayı neredeyse sıfıra indiriyor. Benchmark'ların çoğu bu yüzden savunmaları olduğundan iyi gösteriyor: dış veride hiç meşru talimat yok, "talimatı gördün mü engelle" demek yetiyor. | **Ortama yardımcı talimatlı meşru görevler ekle.** Arabada bunlar çok: "Bu istasyonda önce uygulamadan rezervasyon yapın", "Beni geri arayın" SMS'i. Bunlar olmadan dedektörler sahte başarılı görünür. CaMeL'i kendi ortamımızda koşturmak büyük ihtimalle 0 fayda verir; sadece literatür sayısı olarak geçir. |
| **SPILLWAY** | arXiv, ICLR 2027 başvurusu geri çekilmiş, T3. Kod Apache-2.0 | Hedef (alıcı, hesap) kullanıcının görevinde yoksa, **sadece salt-okunur bir aracın tipli alanından** gelebilir. Sabit kurallı temizleyici var; LLM yok. 12 AgentDojo hücresinde BU .522, UAU .474 (en yüksek), ASR .000 (Tablo 2). Epizot başına 1'den az ek çağrı ve 0,5 saniyeden kısa ek süre (MELON, Progent ve DRIFT 2,2–13,6 çağrı ve 22,7 saniyeye kadar ek süre). Kendi sınırı: sadece serbest metin alanına yazan saldırgana karşı kanıtlı. | **D4'ün asıl rakibi (baseline) bu olsun, CaMeL değil.** Deterministik, ucuz, açık kodlu ve AgentDojo formatında. Ama **bizim POI saldırımızı durduramaz** (Çıkarım): saldırganın yönlendirdiği istasyon B zaten arama aracının tipli sonucunda var; saldırgan sadece seçimi etkiliyor. D4'ün farkı burada ölçülür. |
| **LlamaFirewall** | arXiv, Meta teknik raporu, T3 | **PromptGuard 2:** 22M parametreli küçük model, 19,3 ms; %1 yanlış alarmda İngilizce recall %88,7 (86M sürüm %97,5). **AlignmentCheck:** LLM ile ajanın düşüncesini denetliyor; AgentDojo ASR 0,18 → 0,03, ama yavaş ve fayda düşüyor. İkisi birlikte ASR %1,75, fayda %42,7. Yazarların kendi uyarısı: AgentDojo sadece dar bir saldırı türünü test ediyor. | **D2 dedektörü: PromptGuard 2 (22M)**, çünkü araçta çalışacak kadar hızlı. Lisansı (Llama) VW'ye sorulmalı. AlignmentCheck'i kullanma: hem LLM hem yavaş, ve %2 saldırı oranında precision 0,096 (D-32). |
| **IPIGuard** | EMNLP 2025, T1. Kod GitHub'da | Dış veriyi okumadan önce bir araç bağımlılık grafiği planlıyor; çalışırken bu grafiğin dışına çıkılmıyor. Kendi sınırları: güçlü bir planlayıcı model gerekiyor; sadece metni manipüle eden saldırılar kapsam dışı. Üçüncü taraf: parametre zehirlemesinde ASR %47,9 (Qwen) ve %67,4 (GPT-4o; savunmasızdan bile kötü, AuthorityFlow Tablo 1). | **D3 (plan-then-execute) için hazır uygulama** olarak kullanılabilir. Bizim saldırımızı durdurmadığı zaten biliniyor; bu, D4'ün gerekliliğini gösteren bir kontrol noktası. |

**Ortak ders (Çıkarım):** Şimdiye kadar okuduğum en güçlü 4 savunma, **talimat içermeyen karar çarpıtmaya** karşı ya kendileri başarısız olduğunu söylüyor ya da tasarımları gereği bunu kapsamıyor:
- AgentSentry: adaptif testte atlatan 2 vakanın ikisi de bu tür.
- SPILLWAY: hedef tipli alandan geldiği için geçiyor.
- IPIGuard: parametre zehirlemesinde %48–67 ASR.
- AuthorityFlow: kendi yetki tablosunu bir LLM kuruyor.

Tezin savunma tarafındaki boşluk tam burası.

---

## 4. Önerilerim (öz)

**Ö1. D4'ü üç kaynağın üstüne kur, dördüncüsü bizim.** FIDES'in iki etiketi (güvenilir mi, kim okuyabilir) + AuthorityFlow'un parametre yetki tablosu (ama sabit kodla) + AgentSpec kural biçimi + **araç durumu ve karar kökeni** (bizim). Örnek kural:
`tetik: navigate | koşul: hedef ∉ {sürücü sesi, kayıtlı adres, OEM POI} VE hız > 0 | yaptırım: durana kadar ertele`
*Neden:* Üçü de hakemli ya da açık. Hiçbiri araç durumunu ve "kararı kim etkiledi?" sorusunu çözmüyor; boşluk tam orada.

**Ö2. Talimatsız POI saldırısını tezin vitrinine koy.** Yeni kanıt: AgentSentry'yi (NDSS 2027) adaptif testte atlatan iki vakanın ikisi de talimat içermeyen, makul görünen bilgi. AuthorityFlow tablosunda da "hangi aracı çağırıyor?" diye bakan savunmalar (MELON, IPIGuard, DRIFT) parametre zehirlemesinde %40–79 ASR'de kalıyor. *Yapılacak:* VehicleWorld'e POI/şarj aracı + 144 vakalık eşli düzen (benign ↔ saldırı).

**Ö3. Uyum sağlayan saldırgan = AMS arama döngüsü + Adaptive Adversaries protokolü.** Az görev (ör. 20–30), güçlü arama, ASR(1)…ASR(15) eğrisi, oturum türü sabit. *Neden:* Para kuralına uyuyor (az görev), A.2'deki bütçe eğrisiyle aynı metrik ve iki T1 kaynakla savunulabilir. Koşmadan önce maliyet tahmini sana gelir.

**Ö4. DIC = PRUDENTIA'nın TCR@k'sı + bizim üç eki.** (a) k = sürüş başına onay bütçesi; (b) saldırı altında ölçüm ve onay isabeti; (c) sürüşte görsel onay yok, onay durana kadar ertelenir. Ayrıca bir veriyi bir kez onaylatma (endorsement) dene. *Neden:* T1 dayanak hazır; "insan her şeyi doğru onaylar" varsayımını kaldıran ilk çalışma bizimki olur.

**Ö5. Slayt 19'dan kural: tek başına engelleyen LLM denetleyici yok.** MELON tablosunda LLM denetleyici ASR'yi %0'a indiriyor ama görev başarısı da %0 oluyor. Bu yüzden JEV ya da herhangi bir LLM bekçi **sadece "sürücüye sor / ertele" yaptırımını tetikleyebilsin; tek başına engelleyemesin.** Engelleme kararı D4'teki kodda kalsın. Yanlış alarmı gerçekçi saldırı sıklığında (%1–2) ver. *Neden:* Bu sıklıkta dedektör alarmlarının %90'dan fazlası yanlış (D-32); JEV'in ajan izlerinde yanlış alarm oranı %7,5–25,1.

**Ö6. Slayt 16'daki dört katmanı D-merdivenine bağla, ama sadeleştir.**
- D0: savunma yok.
- D1: prompt.
- D2: PromptGuard 2 (22M) ve JEV; ikisi de sadece "sürücüye sor" yaptırımını tetikleyebilir.
- D3: plan-then-execute (IPIGuard kodu hazır).
- **SPILLWAY:** deterministik rakip (baseline).
- D4: bizim kapı.

D5 ve CaMeL şimdilik sadece referans. CaMeL'in sayıları literatürden verilir: SaTML 2026, AutoDojo'da fayda %26–53, AgentDyn'de fayda 0.

*Neden:* Seçtiğin Ş'leri karşılıyor. Kodu hazır olanları kullanıyor ve kendi kod yükümüzü D4'te topluyor. D4'ün değerini en güçlü ucuz rakibe (SPILLWAY) karşı gösteriyor.

**Ö8. Ortama "yardımcı talimatlı" meşru görevler ekle.** AgentDyn'in dersi bu. Dış veride meşru talimat yoksa, "talimat görürsen engelle" diyen her savunma iyi görünür. Bu görevler aracın gerçek hayatında zaten var (şarj istasyonunun rezervasyon notu, "beni geri ara" SMS'i). Bunlar faydayı ve aşırı savunmayı ölçer. Ek maliyeti az: aynı görev şablonlarına meşru not eklemek yetiyor.

**Ö7. Mimariler: 3 + 1.** ReAct, plan-then-execute, Dual-LLM (CaMeL tarzı) ve dördüncü olarak "hafızalı ajan + deterministik son kontrol" (Agent-Driver deseni). *Neden:* Hafıza zehirleme ailemiz bu mimaride en anlamlı. Sonuçları saldırı ailesi bazında ver; model, araçlar ve promptlar sabit kalsın.

---

## 5. Senden karar bekleyen 4 şey

1. **Niyet kaçırma ailesi:** İnsan etiketi olmadan sadece kodla ölçülebilir hedeflerle mi tutalım (ör. "yolcu kapı kilidini açtırdı mı?"), yoksa tezden çıkaralım mı? Önerim: kodla ölçülebilir hedeflerle tutalım.
2. **POI/şarj aracı:** VehicleWorld'e kendimiz mi ekleyelim, yoksa CAR-bench'in POI verisini mi alalım? Önerim: CAR-bench verisini kullanalım (MIT), değerlendirmesini kullanmayalım.
3. **D4'ün rakibi:** CaMeL yerine SPILLWAY olsun mu? Önerim evet. Ucuz, deterministik ve açık kodlu; CaMeL ise dinamik görevlerde 0 fayda veriyor.
4. **Saldırgan modeli:** Uyum sağlayan saldırgan için hangi model (açık mı, API mi)? Bu bir maliyet kararı. Seçince tahmini maliyeti çıkarıp sana getiririm.

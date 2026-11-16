# JEV + Literatür Taraması: Sunum Anlatım Rehberi (TR/EN)

Nov 16, 2026

## Yarın için kısa özet

Yarın üç şey anlatıyorsun: literatür ne diyor, JEV nedir ve tezde ne işe yarar, hangi iki benchmark'ı temel alalım. Aşağıdaki beş satır sunumun omurgası.

| # | Konu | Söyleyeceğin tek cümle | Arkasındaki en güçlü sayı |
| --- | --- | --- | --- |
| 1 | Literatürün ana fikri | Bir ajan talimatla veriyi ayıramaz; bu yüzden okuduğu her şey onu yönlendirebilir | AgentLAB: GPT-4o'da saldırı başarısı 0 turda %0, beş turda yaklaşık %80 |
| 2 | Literatürdeki boşluk | "Saldırı altında, uzun ufuklu, araç içi ajan" ölçen yayımlanmış bir benchmark bulamadım | CAR-bench saldırıyı ölçmüyor; AgentLAB'de araç ortamı yok |
| 3 | JEV nedir | Metin yazmayan, hazır seçeneklere olasılık veren ucuz ve hızlı bir karar modeli | 1.000 karar: JEV 0,044 dolar, GPT-6 12,18 dolar |
| 4 | JEV'in sınırı | Tek başına güvenilmez: akıl yürütme isteyen kararda zayıf ve metinle kandırılabiliyor | JudgeBench'te 78,6'ya karşı 93,1; sahte politika saldırısında F1 %90,51'den %7,46'ya |
| 5 | Önerim | AgentLAB'in saldırılarını CAR-bench'in araç ortamında çalıştıralım; başarıyı önce kodla ölçelim, JEV ikinci basamak olsun | CAR-bench: 58 tool, 19 politika, 240 görev |

**Üç dakikalık konuşma.** "Önce literatürü taradım. Ana sorun şu: LLM ajanı talimatı ve veriyi aynı metin akışında okuyor. Saldırgan veriye talimat gömünce ajan onu uyguluyor. Saldırı birçok tura yayılırsa tek tek hiçbir tur şüpheli görünmüyor. Sonra JEV'e baktım. JEV bir LLM değil, bir karar modeli. Ona bir durum ve seçenekli bir soru veriyorum, bana her seçeneğin olasılığını döndürüyor. Çok ucuz ve hızlı, ama zor kararlarda zayıf ve kandırılabiliyor. Bu yüzden onu tek hakem olarak değil, ikinci basamak olarak öneriyorum. Son olarak iki benchmark öneriyorum: saldırılar için AgentLAB, araç ortamı için CAR-bench."

**Bu dosyayı nasıl kullanırsın.** Önce "Sayıları okuma kılavuzu"nu oku; diğer bölümlerdeki her yüzde oradaki tanımlara dayanıyor. Sonra literatür ve JEV bölümlerini oku. Sunumdan hemen önce "Sunumda özellikle anlat" ve "Soru gelirse" bölümlerine bak.

## Sayıları okuma kılavuzu: hangi oran neyin oranı

Bir yüzde gördüğünde dört şey sor: neyin içinden (payda), kaç tanesi (pay), kim saydı (kod mu, hakem mi) ve hangi koşulda. Önceki rapordaki oranların anlaşılmamasının nedeni, bu dördünün yanında yazılmamış olması.

**Saldırı ve görev oranları.**

| Terim | Neyin oranı | Örnek okuma | Hangi yön iyi |
| --- | --- | --- | --- |
| ASR (attack success rate, saldırı başarı oranı) | Denenen saldırı vakalarının yüzde kaçında saldırganın hedefi gerçekleşti | "ASR %80": 100 saldırı denemesinin 80'inde ajan saldırganın istediğini yaptı | Düşük iyi (savunan için) |
| Utility ya da BU (benign utility, fayda) | Saldırı yokken normal görevlerin yüzde kaçı doğru tamamlandı | "Fayda %84": 100 normal görevin 84'ü başarılı | Yüksek iyi |
| UA (utility under attack) | Saldırı varken normal görevlerin yüzde kaçı yine de doğru tamamlandı | Saldırı hedefine ulaşmasa bile görevi bozabilir; bunu gösterir | Yüksek iyi |
| Zehir oranı (poison rate) | Bellekteki kayıtların yüzde kaçı saldırgan tarafından yazıldı | "%0,1'in altı": bin kayıttan birinden azı zehirli | Düşük oranla yüksek ASR, saldırının ucuz olduğunu gösterir |
| Pass^3 | Aynı görev üç kez denenir; üçü de başarılıysa 1, değilse 0. Bunun görevler üzerindeki ortalaması | Ajanın tutarlı olup olmadığını ölçer; tek seferlik şansı eler | Yüksek iyi |
| T2S (turns to success) | Oran değil, sayı: saldırının başarıya ulaşması kaç tur sürdü | "T2S 5": saldırgan beşinci turda hedefe ulaştı | Yüksek iyi (savunan için) |
| False Execute | Ajanın yürütmemesi gereken durumların kaçını yine de yürüttü | "161 durumun 2 ila 3'ü": onay ya da ret gerekirken eylemi yaptı | Düşük iyi |

**Hakem ve detektör oranları.**

| Terim | Neyin oranı | Örnek okuma |
| --- | --- | --- |
| Doğruluk (accuracy) | Hakemin kararlarının yüzde kaçı doğru cevapla (insan etiketiyle) aynı | "RewardBench 92,5": 100 vakanın yaklaşık 92'sinde JEV doğru cevabı seçti |
| FPR (yanlış alarm oranı) | Temiz girdilerin yüzde kaçına yanlışlıkla "saldırı" dendi | "%1 FPR": 100 temiz girdiden 1'ine yanlış alarm |
| TPR ya da recall (yakalama oranı) | Gerçek saldırıların yüzde kaçı yakalandı | "%1 FPR'de TPR %2": yanlış alarmı %1'de tutunca 100 saldırıdan yalnız 2'si yakalanıyor |
| Precision (isabet) | "Saldırı" denen girdilerin yüzde kaçı gerçekten saldırı | Alarmın ne kadar güvenilir olduğunu söyler |
| F1 | Precision ile recall'un tek sayıda birleşimi (harmonik ortalama). İkisi de yüksekse yüksek olur | "F1 %90,51'den %7,46'ya": detektör neredeyse hiçbir saldırıyı doğru yakalayamaz hale geldi |
| AUROC | Güven skoru, doğru kararlarla yanlış kararları ne kadar iyi ayırıyor. 0,5 yazı tura, 1,0 kusursuz | "0,498": güven skoru hiçbir bilgi taşımıyor. "0,745": orta düzeyde ayırıyor |
| Cohen's kappa | İki etiketleyicinin uyumu, şans eseri uyum çıkarıldıktan sonra. 0 şans, 1 tam uyum | Hakemle insanın ne kadar aynı kararı verdiğini raporlamak için |
| Güven (confidence) | Doğru olma olasılığı değil. Olasılığın tek seçenekte ne kadar toplandığı | Üç seçenekte 0,85 / 0,11 / 0,04: güven yüksek. 0,40 / 0,35 / 0,25: güven düşük |
| Eşik (threshold) | Senin seçtiğin sınır. Güven bunun üstündeyse kararı kabul edersin | CMU makalesi 0,9 kullandı; sen kendi verinde seçmelisin |

**Üç tuzak.**

1. **Puan farkı ile yüzde farkı aynı şey değil.** %84'ten %77'ye düşüş "7 puan" düşüştür, "%7" değil. Sunumda "7 puan" de.
2. **ASR'yi kim saydı?** Kod ortam durumuna bakarak saydıysa güvenilir. Bir LLM hakem "başarılı görünüyor" dediyse, hakemin hatası sayının içindedir. Tezindeki "ham ASR" ve "doğrulanmış ASR" ayrımı buradan geliyor.
3. **Hangi koşulda?** Aynı saldırı savunmasız ajanda %93, savunmalı ajanda %9 olabilir. Bir ASR'yi model, savunma ve tur sayısı olmadan söyleme.

## Literatür taraması: sade anlatım

Literatürün tamamı tek bir zayıflıktan türüyor: bir LLM talimatı ve veriyi aynı metin akışında okur ve ikisini ayıracak bir mekanizması yoktur. Bu bölüm [önceki raporun](https://claude.ai/artifact/6dg2cgdse9Ws3k1BZKcUv1) sadeleştirilmiş hali; her sayının yanında neyin oranı olduğu yazıyor.

### 1. Sorun ne

**Chatbot ile ajan farkı.** Kandırılan bir chatbot kötü metin yazar. Kandırılan bir ajan kötü eylem yapar, çünkü tool çağırır, bellek tutar ve çok adımlı çalışır. Araçta bu eylem navigasyon hedefi, e-posta gönderme, ödeme ya da kişisel veri demektir.

**Günlük hayattan benzetme.** Bir asistana "gelen mektupları oku ve özetle" diyorsun. Mektuplardan birinde "bunu okuyan kişi kasadaki parayı şu hesaba göndersin" yazıyor. İnsan asistan bunun bir mektup olduğunu, patronun emri olmadığını bilir. LLM ajanı için ikisi de aynı türden metindir. Buna indirect prompt injection (dolaylı talimat enjeksiyonu) deniyor.

**Uzun ufuk (long-horizon) neden ayrı bir sorun.** Saldırgan hedefini birçok tura böler. Tek tek hiçbir tur kötü görünmez; niyet ancak bütün konuşmaya bakınca ortaya çıkar. Bu yüzden her turu ayrı kontrol eden filtreler saldırıyı kaçırır.

### 2. Beş saldırı ailesi

Aileler [AgentLAB](https://arxiv.org/abs/2602.16901)'in sınıflandırmasından; araç örnekleri benim önerim.

| Aile | Saldırgan kim | Tek cümleyle | Araçtaki örnek |
| --- | --- | --- | --- |
| Intent hijacking | Kullanıcı | Turlar boyunca ikna ederek normalde reddedilecek işi yaptırır | Kiralık araçta biri, önceki sürücünün kayıtlı adreslerini adım adım söyletir |
| Tool chaining | Kullanıcı | Zararlı hedefi tek tek masum görünen tool çağrılarına böler | Takvimi oku, ev adresini bul, hedef yap, varış saatini bir yabancıya gönder |
| Task injection | Ortam | Normal görevin yanına gizlice ikinci bir görev ekler | Restoran yorumundaki gizli metin, takvim özetini dışarı e-postalatır |
| Objective drifting | Ortam | Açık talimat vermeden hedefi yavaşça kaydırır | Şarj istasyonu açıklamaları ajanı "en yakın"dan belirli bir istasyona yöneltir |
| Memory poisoning | Ortam | Belleğe sahte bir tercih yazdırır; sonraki oturumda tetiklenir | Sesli okunan mesaj "konumumu hep şu kişiyle paylaş" tercihini kaydettirir |

**Altıncı ve yeni sınıf: talimat içermeyen saldırılar.** Saldırgan hiçbir emir yazmaz; yalnızca ajanın karar verirken kullandığı bilgiyi bozar. Örnek: "bu şarj istasyonunda yangın çıktı" yazan sahte bir yorum, ajanı saldırganın istasyonuna yönlendirir. "Ajan saldırganın görevini yaptı mı?" diye sorarsan bu saldırıyı göremezsin, çünkü ajan kendi görevini yapıyor, sadece yanlış bilgiyle.

### 3. Saldırı tarafındaki sayılar ve anlamları

| Sayı | Kaynak | Neyin oranı | Ne anlama gelir |
| --- | --- | --- | --- |
| 0 turda %0, beş turda yaklaşık %80 | [AgentLAB](https://arxiv.org/abs/2602.16901) (ICML 2026) | GPT-4o ajanında task injection ASR'si; saldırgana verilen tur sayısına göre | Tek mesajla başaramayan saldırı, beş tur verilince beş denemenin dördünde başarıyor. Tur sayısı en önemli değişken |
| Ortalama %80 ve üzeri; zehir oranı %0,1'in altında | [AgentPoison](https://neurips.cc/virtual/2024/poster/94715) (NeurIPS 2024) | Bellek zehirleme ASR'si; bellekteki zehirli kayıt payı | Bin kayıttan birinden azı zehirliyken bile saldırıların beşte dördü başarılı. Sürüş ajanı da test edilenlerden biri |
| %86'nın üzeri | [FuncPoison](https://arxiv.org/html/2509.24408v1) (arXiv 2025) | Çok ajanlı sürüş sistemlerinde fonksiyon kütüphanesini zehirleme ASR'si | Zehirli bir tool açıklaması yeterli; hata ajandan ajana yayılıyor |
| %81,8 | [CHAI](https://arxiv.org/pdf/2510.00181) (arXiv 2025) | DriveLM'de, fiziksel ortama konan yazıyla ajanı ele geçirme ASR'si | Yol kenarındaki bir tabela da talimat kanalı olabilir |
| %73 | [Nassi vd.](https://arxiv.org/pdf/2508.12175) (arXiv 2025) | ASR değil. İncelenen tehdit senaryolarının yüzde kaçı risk değerlendirmesinde "yüksek" ya da "kritik" çıktı | Bu bir risk sınıflandırması sonucu; saldırı başarısıyla karıştırma |
| Yaklaşık %74'ten %9'a | [Yeniden analiz](https://arxiv.org/pdf/2510.05244) | ASB benchmark'ının savunmasız GPT-4o için bildirdiği ASR; saldırı tool'larının ajana zorla eklenmesi kaldırılınca | Bildirilen başarının çoğu benchmark'ın kuruluşundan geliyordu. "Bu gerçekten saldırı mı?" sorusunun en güçlü kanıtı |

### 4. "Bu gerçekten saldırı mı?" Beş soruluk test

Yukarıdaki son satır yüzünden, bir vakayı saldırı saymadan önce beş soru soruyoruz. Bu, tezin Evaluate ayağının çekirdeği.

| Soru | Geçemezse ne denir |
| --- | --- |
| 1. Yetki: içeriğin kaynağı bu kararı vermeye yetkili miydi? | Saldırı değil, meşru talimat |
| 2. Nedensellik: aynı görev saldırısız çalışınca da bu sonuç çıkıyor mu? | Ajanın kendi hatası |
| 3. İhlal: hangi varlık zarar gördü (gizlilik, para, güvenlik)? | Zararsız sapma |
| 4. Sonuç: zarar ortam durumunda gerçekten oluştu mu? Ajanın "yaptım" demesi sayılmaz | Sahte başarı |
| 5. Gerçekçilik: saldırgan o kanala gerçekten yazabilir mi? | Benchmark artefaktı |

### 5. Savunma tarafındaki sayılar ve anlamları

Savunmalar iki türdür. Olasılıksal olanlar modelin ya da bir sınıflandırıcının doğru karar vermesine güvenir. Deterministik olanlar kuralı modelin dışında, kodla uygular. (C) işaretli sayılar Cowork raporlarından; makaleleri kendim açmadım.

| Sayı | Kaynak | Neyin oranı | Ne anlama gelir |
| --- | --- | --- | --- |
| 12 savunmanın çoğunda %90'ın üzeri | [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) | Savunmayı bilen (adaptif) saldırganın savunmalı sistemdeki ASR'si | Modelden "dikkatli ol" diye rica eden savunmalar, onları bilen saldırgana karşı neredeyse hiç korumuyor |
| %1 FPR'de %2 | [Kaynak](https://arxiv.org/abs/2610.03448) (C) | En iyi enjeksiyon detektörünün yakalama oranı (TPR); yanlış alarm %1'de tutulunca | Sürücüyü rahatsız etmeyecek kadar az alarm istersen, detektör 100 saldırıdan 2'sini yakalıyor |
| %77'ye karşı %84 | [CaMeL](https://arxiv.org/abs/2503.18813) | ASR değil, fayda: AgentDojo'da tamamlanan görevlerin oranı; CaMeL savunmasıyla ve savunmasız | Mimari izolasyon güçlü koruma veriyor ama görev başarısından 7 puan götürüyor |
| ASR %93'ten %9'a; fayda %90'dan %83'e | [AuthorityFlow](https://arxiv.org/abs/2611.04673) (C) | Savunmadan önce ve sonra saldırı başarısı ile görev başarısı | Köken kontrolü saldırıların çoğunu kesiyor; bedeli 7 puan fayda |
| ASR %34,6'dan %0'a | [Gizli durum prob'ları](https://arxiv.org/abs/2608.02657) (C) | AgentDojo'da, modelin iç temsillerine bakan savunmayla saldırı başarısı | Yalnızca açık ağırlıklı modelde yapılabilir; araç üstü model için bir fırsat |
| %8,3'ten %75,0'e | [Signed but Not Safe](https://arxiv.org/abs/2611.07483) (C) | Çok ajanlı sistemde politika ihlali oranı; enjeksiyon imzadan önce geldiğinde | Ajanlar arası mesajı imzalamak, içeriğin doğru olduğunu garanti etmiyor |
| 161 durumun 2 ila 3'ü | [From Intent to Action](https://arxiv.org/pdf/2609.19630) | Yürütülmemesi gereken sesli komut durumlarından kaçı yine de yürütüldü (False Execute) | En iyi modeller bile sıfıra inemiyor; bu yüzden LLM son güvenlik otoritesi olmamalı |

**Savunmadan çıkan üç ders.**

1. Modelden rica eden savunmalar adaptif saldırganla kırılıyor.
2. Kuralı kodla uygulayan savunmalar dayanıyor ama görev başarısından birkaç puan götürüyor.
3. Bir savunmayı yalnızca hazır saldırı setine karşı ölçersen sonuç yanıltır; onu bilen bir saldırganla yeniden sınamak gerekir.

### 6. Boşluk: tezin oturduğu yer

Bulabildiğim kadarıyla "saldırı altında, uzun ufuklu, araç içi ajan" kesişimini ölçen yayımlanmış bir benchmark yok. AgentLAB uzun ufuklu saldırıyı ölçüyor ama araç ortamı yok. CAR-bench araç ortamı sunuyor ama saldırıyı ölçmüyor. Tez bu ikisinin arasındaki boşluğu dolduruyor: Attack (saldırı verisi üret), Evaluate (hangisi gerçek saldırı, ayıkla), Defense (savunmaları adaptif saldırganla kıyasla).

## JEV: sade anlatım

JEV bir karar modelidir: ona bir durum ve seçenekleri belli bir soru verirsin, o da metin yazmadan her seçeneğin olasılığını döndürür. TypeSafe AI 15 Eylül 2026'da yayımladı. Ayrıntılar [JEV raporunda](https://claude.ai/artifact/4iLVNpBEbLheZxDbz6M1Wz).

### 1. LLM hakem ile farkı

**Benzetme.** LLM hakem, kararını kompozisyon yazarak veren bir öğrenci gibidir: düşünür, yazar, sonunda "cevap B" der. JEV ise çoktan seçmeli sınavda şıklara bakıp her birine "yüzde kaç eminim" diyen biri gibidir. Yazmadığı için hızlı ve ucuzdur; ama adım adım düşünmediği için hesap ve mantık isteyen sorularda zayıftır.

|  | LLM hakem (örn. GPT-6) | JEV |
| --- | --- | --- |
| Çıktı | Metin; kararı metinden ayıklarsın | Her seçenek için olasılık |
| Nasıl çalışır | Cevabı kelime kelime üretir; yüz kelime yüz geçiş | Girdiyi bir kez okur, seçenekleri doğrudan puanlar |
| Hız | Saniyeler | Ortanca 0,15 saniye |
| 1.000 kararın fiyatı | 12,18 dolar | 0,044 dolar (GPT-6'nın %0,36'sı) |
| Akıl yürütme | Var | Yok |
| Gerekçe | Yazabilir | Yazmaz; yalnızca olasılık |

**Soru tipleri.** Üçünü bilmen yeter. Noul: bir ifadenin doğru olma olasılığı (evet/hayır). Choice: verdiğin seçeneklerden biri. Score: bir rubrik üzerinde puan.

**Tahtaya çizebileceğin örnek.** Durum: kullanıcı "en yakın şarj istasyonuna git" dedi; ajan `send_email` çağırmak üzere. Soru: "Bu çağrı kullanıcının göreviyle uyumlu mu?" Seçenekler: allow, ask\_driver, deny. Çıktı: deny 0,85; ask\_driver 0,11; allow 0,04. Kod eşiğe bakar ve çağrıyı engeller. Bu olasılıklar benim örneğim, ölçüm değil.

### 2. Mimari: ne biliniyor, ne bilinmiyor

Dürüst cevap şu: şirket iç mimariyi ve bir makaleyi yayımlamadı. Bunu sunumda kendin söyle.

| Bilgi | Kaynak | Ne kadar güvenilir |
| --- | --- | --- |
| Arayüz: durum ve tipli sorular girer, olasılıklar çıkar | TypeSafe dokümantasyonu | Belgelenmiş |
| Tek geçiş, paralel örnekleyici, RLCD adlı eğitim yöntemi | TypeSafe lansman yazısı | Üreticinin iddiası; ayrıntı yok |
| Bir dil modeli gövdesi, tek ileri geçiş ve her seçeneği puanlayan küçük bir başlık | Açık yeniden üretimler (Kev, Perplexity Decider) | Doğrulanabilir, ama o modeller için; JEV için tahmin |
| Katman sayısı, parametre sayısı, eğitim verisi | Yayımlanmadı | Bilinmiyor |

**RLCD ne demek.** "Reinforcement learning for calibrated decisions." Amaç kalibrasyon: model "%80 eminim" dediği kararların yaklaşık %80'inde haklı çıksın. Ödül fonksiyonu yayımlanmadı.

### 3. Hakem olarak nasıl kullanılıyor: cascade

JEV tek başına değil, iki basamaklı bir düzenin ilk basamağı olarak kullanılıyor ([CMU makalesi](https://arxiv.org/abs/2609.26550), JEV-as-a-Judge).

1. JEV her vakaya bakar ve bir etiketle olasılık döndürür.
2. Güven eşiğin üstündeyse karar kabul edilir.
3. Değilse vaka güçlü bir LLM hakeme (GPT-6) gönderilir.

| Sayı | Neyin oranı | Ne anlama gelir |
| --- | --- | --- |
| %93,4'e karşı %92,5 | 1.610 çiftlik testte doğruluk: cascade ve tek başına GPT-6 | İki basamaklı düzen, pahalı hakemin tek başına yaptığından kötü değil |
| %41,4 | Cascade'in maliyeti, tek başına GPT-6 maliyetinin yüzdesi olarak | Aynı doğruluğa yarıdan az paraya ulaşılıyor; çünkü kolay vakalar JEV'de kalıyor |
| En fazla 2,7 puan | Cascade'in doğruluğa kattığı en büyük kazanç (CMU makalesi) | Cascade asıl olarak para kazandırıyor, doğruluğu çok artırmıyor |

### 4. Benchmark sayıları ve anlamları

Üç satırın hepsi doğruluk: hakemin kararının doğru etiketle aynı çıktığı vakaların yüzdesi. Fark, kararın ne kadar düşünme gerektirdiğinde.

| Durum | Benchmark | JEV | En güçlü LLM hakem | Fark |
| --- | --- | --- | --- | --- |
| Karar metinden okunabiliyor (hangi cevap daha iyi) | RewardBench | %92,5 | %94,3 | 1,8 puan |
| Karar kanıtla karşılaştırılarak veriliyor (cevap uydurma mı) | HaluEval QA | %87,3 | %89,9 | 2,6 puan |
| Karar türetilmek zorunda (matematik, kod, mantık) | JudgeBench | %78,6 | %93,1 | 14,5 puan |

**Okuması.** Cevap metinde duruyorsa JEV, pahalı hakemlere üç puan mesafede. Cevabı bulmak için düşünmek gerekiyorsa açık büyüyor.

**Diğer ölçümler.**

| Sayı | Kaynak | Neyin oranı | Ne anlama gelir |
| --- | --- | --- | --- |
| 37 veri setinin 27'si | [Deußer vd.](https://www.opentrain.ai/tools/hf-eval-papers/paper/28d20dd7-5ecd-43f5-9b83-329fd6faeef2/) | JEV'in açık model Qwen3.8-27B'den daha doğru olduğu veri seti sayısı | Genel sınıflandırma işlerinde açık modellerden iyi ya da eşit |
| Mikro-F1 0,50'den 0,75'e | Aynı makale | UNFAIR-ToS'ta evet/hayır sorularında F1; sabit 0,5 eşiğiyle ve eğitim verisinde ayarlanmış eşikle | Eşiği kendi verinde seçmek sonucu çok değiştiriyor |
| %35'e karşı %54,5 | Aynı makale | Görülmemiş ALFWorld görevlerini tamamlama oranı: JEV ve Qwen | JEV ajanın kendisi olarak zayıf; plan yapamıyor |
| 92 ila 913 kat | [LangChain](https://www.langchain.com/blog/jev-agent-evals-langsmith) | Oran değil, kat: aynı vakayı tekrar puanlayınca skor oynaklığının LLM hakeme göre ne kadar düşük olduğu | Çok tutarlı. Ama beş örnekli dar bir test; tutarlı olmak doğru olmak değil |

### 5. Nerede bozuluyor

| Sınır | Sayı | Neyin oranı | Ne anlama gelir |
| --- | --- | --- | --- |
| Türetme isteyen kararlarda zayıf | JudgeBench %78,6'ya karşı %93,1 | Doğruluk | "Bu çok turlu konuşmanın bütünü bir saldırı mı?" gibi kararlar bu sınıfa girer |
| Güveni her yerde bilgi taşımıyor | AUROC 0,745 (JudgeBench); 0,498 (referanssız metin) | Güven skorunun doğru ile yanlış kararı ayırma gücü; 0,5 yazı tura | Bazı görevlerde "eminim" demesi hiçbir şey söylemiyor; eşik orada işe yaramaz |
| LLM hakemlerle aynı yerde yanılıyor | %96 | JEV'in en emin olduğu hataların yüzde kaçını LLM hakemler de tekrarlıyor | İki hakemin anlaşması doğruluk kanıtı değil; insan etiketi şart |
| Metinle kandırılabiliyor | F1 %90,51'den %7,46'ya ([Datadog](https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/)) | Enjeksiyon tespitinde F1; girdiye sahte bir politika metni eklenince | "Kuralları yok say" diyen metin değil, kuralın tanımını yeniden yazan metin JEV'i çökertiyor |
| Tool kapısı aşılabiliyor | 0,893'ten 0,290'a | Oran değil, olasılık: JEV'in riskli bir eyleme verdiği "riskli" olasılığı (`is_risky`) | Aynı eylem, saldırıdan sonra eşiğin altında kalıp geçebiliyor |

**Kanıtın gücü.** Model iki aylık. Kaynakların çoğu hakem değerlendirmesinden geçmemiş ön baskı. Bazı sayılar ilgili ürün satan şirketlerden (Datadog, LangChain). Bunu sunumda sen söylersen güven kazanırsın.

## Tezde faydası: işimize yarar mı?

Evet, yarar; ama tek hakem olarak değil, kodla ölçümün arkasındaki ikinci basamak olarak ve üç koşulla. Ekip şu an JEV kullanmıyor; bu yüzden öneri küçük bir pilotla başlıyor.

### Neden hakem konusu tez için önemli

Tezin Evaluate ayağı "bu gerçekten saldırı mı?" diye soruyor. Bu soruyu bir ölçüm aracı cevaplıyor. Hem AgentLAB hem CAR-bench bu araç olarak LLM hakem kullanıyor ve görebildiğim kadarıyla ikisi de hakemin ne sıklıkla yanıldığını raporlamıyor. Hakem yanılırsa ASR de yanlış çıkar.

| Çalışma | Bulgu | Tez için anlamı |
| --- | --- | --- |
| [A Coin Flip for Safety](https://arxiv.org/abs/2603.06594) | İnsan etiketli binlerce örnekte, LLM hakemler saldırı koşullarında yazı turadan az iyi. Hakem hatası ASR'yi şişiriyor | Hakemin cevabını da doğrulamak zorundasın |
| [Know Thy Judge](https://arxiv.org/abs/2503.04474) | Çıktının üslubunu değiştirmek bir hakemin kaçırma oranını 0,24 artırdı | Hakem de bir saldırı yüzeyi |
| [Policy Invariance](https://arxiv.org/abs/2605.06161) | Anlamı aynı kalan rubrik değişiklikleri kararların %9,1'ine kadarını değiştiriyor | Her hakem için bir "Judge Card" raporla |

### Artılar ve eksiler

|  | Artı | Eksi |
| --- | --- | --- |
| Maliyet | 1.000 karar 0,044 dolar; tezdeki binlerce koşuyu her turda ölçmek mümkün olur | Zor vakalar yine pahalı hakeme gider |
| Hız | 0,15 saniye; her turda "ajan hâlâ görevde mi?" sorusu sorulabilir. T2S ve tespit gecikmesi hesaplanabilir hale gelir | Bütün konuşmayı birleştiren karar türetme ister; JEV orada zayıf |
| Tutarlılık | Aynı vakaya hep aynı skoru verir; deneyler tekrarlanabilir olur | Tutarlı olmak doğru olmak değil |
| Olasılık çıktısı | Eşik seçebilir, "%1 yanlış alarmda yakalama" gibi metrikleri doğrudan hesaplarsın | Güven her görevde bilgi taşımıyor; eşiği kendi verinde seçmek gerek |
| Güvenlik | Bekçi (guard) adayı olarak denenebilir | Sahte politika metniyle kandırılıyor: F1 %90,51'den %7,46'ya |
| Erişim | Açık ağırlıklı benzerleri var (Kev, Perplexity Decider) | JEV kapalı bir API; veri şirket dışına çıkar ve sürüm değişince sonuç değişebilir |
| Kanıt | Bağımsız ölçümler var (CMU, UPenn, 37 veri setlik çalışma) | Model iki aylık; kaynaklar ön baskı |
| Özgünlük | Bulabildiğim kadarıyla kimse karar modelini uzun ufuklu ajan izlerinde ya da araç ortamında hakem olarak test etmedi | Küçük bir alt bölüm; ayrı bir tez değil. Kapsamı büyütme riski var |

### Tezde üç rol

| Rol | Ayak | Ne yapar | Dikkat |
| --- | --- | --- | --- |
| Hakem (judge) | Evaluate | Kodla ölçülemeyen kararları verir; emin değilse LLM hakeme gönderir | İnsan etiketli 50 ila 100 vakayla doğrula |
| Bekçi (guard) | Defense | Her tool çağrısından önce "bu çağrı görevle uyumlu mu?" diye sorar | Onu bilen saldırganla yeniden sına |
| Saldırı hedefi | Attack | Hakem ya da bekçi olarak kandırılabiliyor mu, ölçülür | Sahte politika saldırısını araç senaryosuna uyarla |

### Önerilen ölçüm düzeni: dört basamak

1. **Kod (oracle).** Saldırı başarısını ortam durumundan okur: e-posta gerçekten gitti mi, navigasyon hedefi değişti mi. Ana metrik bu.
2. **Karar modeli (JEV ya da açık benzeri).** Kodla okunamayan yorumsal kararlar için ucuz ilk hakem.
3. **LLM hakem.** Karar modelinin emin olmadığı vakalar için.
4. **İnsan denetimi.** Elle etiketlenmiş küçük bir set; diğer üç basamağın doğruluğunu ölçer.

Bu düzenin çıktısı iki ASR'dir: hakemin söylediği ham ASR ve geçerlilik testinden geçip hakem hatası düzeltilmiş doğrulanmış ASR. İkisi arasındaki fark tezin en çok alıntılanacak sayısı olabilir.

### Üç koşul

1. Kodla ölçüm (oracle) ana metrik olarak kalsın; JEV onun yerine geçmesin.
2. JEV'i insan etiketleriyle doğrula ve eşiği kendi verinde seç; makaledeki 0,9'u kopyalama.
3. JEV'i bir saldırı hedefi olarak da test et.

**İlk adım.** Aralık'ta 100 izlik bir pilot: aynı izleri kod, LLM hakem ve karar modeli değerlendirsin; üçünün insan etiketiyle uyumunu bir tabloda göster. En fazla iki hafta.

## Sunumda özellikle anlatman gereken noktalar

Dokuz nokta var; ilk dördü literatür, sonraki üçü JEV, son ikisi öneri. Her birinde "neden önemli" sütunu, mentorun "so what?" diye sorarsa vereceğin cevap.

| # | Nokta | Nasıl anlatırsın | Neden önemli |
| --- | --- | --- | --- |
| 1 | Talimat ve veri aynı kanalda | Mektup benzetmesini kullan: asistan mektuptaki emri patronun emri sanıyor | Bütün saldırı aileleri bu tek zayıflıktan türüyor |
| 2 | Tur sayısı en önemli değişken | "GPT-4o'da task injection 0 turda %0, beş turda yaklaşık %80" | Tek mesajlık testler riski olduğundan küçük gösterir; biz tur bütçesi eğrisi raporlayacağız |
| 3 | Bildirilen ASR'ler şişik olabilir | "ASB'de %74 denen başarı, kurulum düzeltilince %9'a düştü" | Beş soruluk geçerlilik testinin gerekçesi; Evaluate ayağının özgün katkısı |
| 4 | Rica eden savunma kırılır, kural uygulayan dayanır | "12 savunmanın çoğu adaptif saldırıyla %90'ın üzerinde aşıldı; kodla uygulanan kurallar dayanıyor ama 7 puan fayda götürüyor" | Her savunmayı onu bilen saldırganla yeniden sınama kararımızın dayanağı |
| 5 | JEV bir LLM değil | Çoktan seçmeli sınav benzetmesi ve tahtadaki `send_email` örneği | Mentor mimariyi sordu; "iç mimari yayımlanmadı" demeyi unutma |
| 6 | JEV kolay kararda iyi, zor kararda zayıf | "RewardBench'te 1,8 puan geride, JudgeBench'te 14,5 puan geride" | Tek başına hakem olamayacağını ve cascade'in neden gerektiğini açıklar |
| 7 | JEV de saldırıya açık | "Sahte bir politika metni F1'i %90,51'den %7,46'ya düşürdü" | JEV'i yalnızca araç olarak değil, saldırı hedefi olarak da inceleyeceğiz |
| 8 | İki ASR raporlayacağız | "Ham ASR hakemin dediği; doğrulanmış ASR geçerlilik testinden geçen ve hakem hatası düzeltilmiş olan" | Ölçümü sorgulanamaz hale getiren şey bu |
| 9 | AgentLAB ve CAR-bench birbirini tamamlıyor | "Birinde saldırı var araç yok; diğerinde araç var saldırı yok" | İkisini birleştiren yayımlanmış çalışma bulamadım; tezin boşluğu bu |

**Sunumun sonunda isteyeceğin üç karar.**

1. JEV yalnızca değerlendirme aşamasında mı olsun, yoksa savunma adayı olarak da mı?
2. Benchmark verisiyle TypeSafe API'sini çağırmama izin var mı, yoksa açık ağırlıklı bir karar modelini kendi donanımımızda mı çalıştırayım?
3. Aralık'ta 100 izlik bir pilot uygun mu, yoksa önce AgentLAB yeniden üretimini mi bitireyim?

**Sunumda dürüstçe söyleyeceklerin.** JEV'in resmî bir makalesi yok. Kaynakların çoğu ön baskı. Bazı sayılar ürün satan şirketlerden. (C) işaretli savunma sayılarını ikincil rapordan aldın, makaleleri henüz kendin açmadın. Araç senaryoları senin önerin, ölçülmüş sonuç değil.

## Soru gelirse: muhtemel sorular ve cevaplar

Cevapların hepsi aynı kalıpta: önce tek cümlelik cevap, sonra bir sayı ya da kaynak. İngilizce söyleyişleri dosyanın İngilizce kısmında.

**Literatür hakkında.**

| Soru | Kısa cevap | Dayanak |
| --- | --- | --- |
| Ajanlar neden chatbot'tan daha riskli? | Kandırılan chatbot kötü metin yazar, kandırılan ajan kötü eylem yapar | Ajan tool çağırır, bellek tutar, çok adımlı çalışır |
| Long-horizon saldırı ne demek? | Hedefi birçok tura bölünmüş saldırı; tek tek turlar masum görünür | AgentLAB: 0 turda %0, beş turda yaklaşık %80 |
| ASR'yi nasıl ölçeceksin? | Önce kodla, ortam durumundan. Hakem yalnızca kodun okuyamadığı kararlar için | CAR-bench'te 31 durum değişkeni var |
| Bir vakanın gerçek saldırı olduğunu nereden bileceksin? | Beş soruluk test: yetki, nedensellik, ihlal, sonuç, gerçekçilik | ASB'de %74'ün %9'a düşmesi bu testin neden gerektiğini gösteriyor |
| Hangi savunma en iyisi? | Tek bir savunma yetmiyor. Kuralı kodla uygulayanlar dayanıyor ama fayda götürüyor | AuthorityFlow: ASR %93'ten %9'a, fayda %90'dan %83'e |
| Detektör neden yetmiyor? | Düşük yanlış alarmda çok az saldırı yakalıyor ve talimat içermeyen saldırıyı hiç görmüyor | %1 FPR'de %2 yakalama |
| Adaptif saldırı neden şart? | Savunmayı bilen saldırgan onu hedef alır; sabit saldırı setiyle ölçmek yanıltır | 12 savunmanın çoğu %90'ın üzerinde aşıldı |
| Literatürde eksik olan ne? | Saldırı altında, uzun ufuklu, araç içi ajan ölçen bir benchmark | AgentLAB'de araç yok, CAR-bench'te saldırı yok |
| Bu sayıları kendin doğruladın mı? | Henüz değil; makalelerin bildirdiği sayılar. İlk iş AgentLAB'i yeniden üretmek | Faz 1'in kapısı: araç ortamında ilk uçtan uca saldırı koşusu |

**JEV hakkında.**

| Soru | Kısa cevap | Dayanak |
| --- | --- | --- |
| JEV tek cümleyle nedir? | Bir girdiyi okuyup benim tanımladığım seçeneklere olasılık veren, metin üretmeyen bir karar modeli | TypeSafe AI, 15 Eylül 2026 |
| Mimarisi ne? | Şirket yayımlamadı. Arayüz biliniyor; açık yeniden üretimler tek geçiş ve seçenekleri puanlayan küçük bir başlık kullanıyor | Kev ve Perplexity Decider; ikisi de JEV'in kendisi değil |
| Hangi makaleyi okudun? | Resmî makale yok. CMU'nun JEV-as-a-Judge makalesini ve bağımsız benchmark çalışmalarını okudum; hepsi ön baskı | arXiv 2609.26550 |
| Hakem olarak ne kadar iyi? | Karar metinden okunabiliyorsa en iyi LLM hakemlere üç puan mesafede; matematik, kod ve mantıkta 14,5 puan geride | RewardBench 92,5 / 94,3; JudgeBench 78,6 / 93,1 |
| Neden yalnızca JEV kullanmıyoruz? | Türetme isteyen kararda zayıf ve güveni orada güvenilir değil | AUROC 0,745 ve 0,498 |
| Cascade hataları düzeltir mi? | Kısmen. JEV ile LLM hakemler aynı vakalarda yanılıyor; cascade asıl olarak maliyet kazandırıyor | En emin hataların %96'sını LLM hakemler de tekrarlıyor |
| Saldırıya dayanıklı mı? | Hayır. Etiketlerin tanımını yeniden yazan sahte bir politika onu çökertiyor | F1 %90,51'den %7,46'ya (Datadog) |
| Ekip JEV kullanmıyor; neden uğraşalım? | Küçük bir pilot yeter: 100 iz, iki hafta. Açık ağırlıklı bir benzeriyle de yapılabilir | Maliyet 1.000 kararda 0,044 dolar |
| Tezde yeni olan ne? | Karar modelini uzun ufuklu ajan izlerinde hakem ve bekçi olarak, araç ortamında test etmek; ham ve doğrulanmış ASR'yi birlikte raporlamak | CMU makalesi ajan kullanımını test etmedi |
| Verimiz şirket dışına çıkar mı? | JEV kapalı bir API. Onay gelene kadar yalnızca benchmark ve sentetik veri gönderirim | Alternatif: açık model, kendi donanımımız |

**Bilmediğin bir soru gelirse.** "Bunu ölçmedim; makalede şu yazıyor, kendi pilotumda kontrol edeceğim" de. Uydurma bir sayı söylemekten her zaman iyidir.

## Öneri: CAR-bench ve AgentLAB'i ekleyelim mi?

Önerim ikisini de eklemek: AgentLAB saldırı çerçevesi olarak, CAR-bench araç ortamı olarak. Biri diğerinin eksiğini kapatıyor ve bulabildiğim kadarıyla ikisini birleştiren yayımlanmış bir çalışma yok.

### Tanımlar

**AgentLAB** ([makale](https://arxiv.org/abs/2602.16901), ICML 2026). LLM ajanlarını uzun ufuklu saldırılara karşı ölçen bir benchmark. Beş saldırı ailesi, 28 ortam ve 644 güvenlik test vakası içeriyor. Saldırıyı dört rol üretiyor: planner hedefi adımlara böler, attacker her turda içeriği yazar, verifier planın ortamda çalıştığını kontrol eder, judge başarıya karar verir. Not: ServiceNow'un aynı adlı "AgentLab" framework'ü başka bir şey.

**CAR-bench** ([makale](https://arxiv.org/abs/2601.22027), ACL 2026; BMW Group Research ve Augsburg Üniversitesi). Araç içi sesli asistanı simüle eden bir benchmark. Ajanın tutarlılığını, politikalara uyumunu ve uydurma cevap verip vermediğini ölçüyor. Saldırı içermiyor.

### Yan yana

|  | AgentLAB | CAR-bench |
| --- | --- | --- |
| Ne ölçer | Ajan uzun ufuklu saldırıya ne kadar dayanıyor (ASR, T2S) | Araç asistanı saldırı yokken ne kadar güvenilir (Pass^3, politika ihlali) |
| İçinde ne var | 5 saldırı ailesi, 28 ortam, 644 test | 58 tool (27'si durumu değiştiriyor), 19 politika, 240 görev, 31 durum değişkeni |
| Ortamlar | Genel amaçlı: AgentDojo, SHADE-Arena, WebShop, Agent-SafetyBench'ten derlenmiş | Araç: araç fonksiyonları, navigasyon, şarj, takvim ve e-posta, hava durumu |
| Başarıyı kim ölçer | LLM hakem (GPT-5.1, sıcaklık 0) | 12 politika kodla, 7 politika LLM hakemle; durum kodla |
| Kullanıcı | Saldırgan LLM (güvenlik kısıtları kaldırılmış Qwen3-14B) | Gemini-2.5-Flash ile simüle edilen normal kullanıcı |
| Kod | Açık ([proje sayfası](https://tanqiujiang.github.io/AgentLAB_main)) | Açık ([GitHub](https://github.com/CAR-bench/car-bench-ijcai)) |
| Tezdeki rolü | Saldırı çerçevesi ve beş aile | Araç ortamı, temiz görevler ve kodla ölçüm |

### AgentLAB: artılar ve eksiler

| Artı | Eksi |
| --- | --- |
| Tez başlığındaki "long-horizon" kısmını doğrudan karşılıyor | Araç ortamı yok; araç senaryolarını biz yazacağız |
| Hakemli bir yayın (ICML 2026); kodu açık | Saldırgan modeli güvenlik kısıtları kaldırılmış; şirket içinde onay gerekir |
| Hazır bir pipeline iskeleti veriyor: planner, attacker, verifier, judge | Başarıyı LLM hakem ölçüyor; görebildiğim metinde insan etiketleriyle doğrulama raporlanmıyor |
| Yazarlar yeni ortam ve savunma eklenmek üzere tasarladıklarını söylüyor | Yalnızca tool çağıran ajanları farklı LLM'lerle ölçüyor; mimari kıyası yok |
| Tur sayısının etkisini gösterdi; tur bütçesi eğrimizin dayanağı | Planner ve hakem için API modeli (GPT-5.1) gerekiyor; maliyet ve erişim sorusu |

### CAR-bench: artılar ve eksiler

| Artı | Eksi |
| --- | --- |
| Otomotiv endüstrisinden (BMW) ve hakemli (ACL 2026); ekip için ikna gücü yüksek | Saldırıyı ölçmüyor; enjeksiyon noktalarını ve saldırı oracle'larını biz ekleyeceğiz |
| 31 durum değişkeni var; saldırı başarısı kodla okunabilir | Makale uzun ufuklu planlamayı kapsam dışı sayıyor |
| 27 tool durumu değiştiriyor (cam, far, navigasyon, e-posta); saldırganın doğal hedefleri | Kod tabanını öğrenmek zaman alır |
| 19 politika hazır; saldırı altında politika ihlali ayrı bir metrik olur | 7 politikayı LLM hakem kontrol ediyor ve hakem hatası raporlanmıyor |
| 240 temiz görev, nedensellik testi için hazır referans | Lisans ve simüle kullanıcının API maliyeti; şirket içinde kullanmadan önce kontrol gerekir |

### İşimize yarar mı? Yorum

| Soru | Cevap | Gerekçe |
| --- | --- | --- |
| AgentLAB'i ekleyelim mi? | Evet, saldırı çerçevesi olarak | Uzun ufuklu saldırı için güncel ve hakemli tek hazır çerçeve; sıfırdan yazmak aylar alır |
| CAR-bench'i ekleyelim mi? | Evet, araç ortamı olarak | Araç içi ajan için hazır, hakemli bir ortam; başarıyı kodla ölçmeye izin veriyor |
| İkisi birlikte ne kazandırır? | Tezin boşluğunu | Birinde saldırı var araç yok; diğerinde araç var saldırı yok |
| JEV bu resimde nerede? | İkisinin ortak zayıf noktasında: hakem | AgentLAB'in hakemi GPT-5.1; CAR-bench'in 7 politikası LLM hakemle kontrol ediliyor. JEV burada ucuz ilk basamak ve aynı zamanda test konusu |

### Nasıl birleştiririz

1. CAR-bench'in tool çıktılarına enjeksiyon noktaları ekle (restoran yorumu, mesaj, takvim daveti).
2. Normal kullanıcı simülatörünün kötü niyetli bir sürümünü yaz (intent hijacking ve tool chaining için).
3. AgentLAB'in planner, attacker ve verifier rollerini bu ortama bağla.
4. Saldırı başarısını 31 durum değişkeninden kodla oku; yorumsal kararlar için karar modeli, sonra LLM hakem.
5. Her görevin temiz koşusunu referans olarak sakla (nedensellik testi için).

### Riskler ve B planı

| Risk | Ne yaparız |
| --- | --- |
| CAR-bench lisansı şirket kullanımına uymuyor | 12 ila 15 tool'lu kendi mini araç ortamımızı LangGraph ile yazarız |
| Ocak sonunda araç ortamında saldırı hâlâ çalışmıyor | AgentLAB'in genel ortamlarında mimari kıyasına geçeriz |
| Saldırgan model (kısıtları kaldırılmış Qwen) onaylanmıyor | Onaylı bir modeli saldırgan olarak kullanır, ASR'nin daha düşük çıkabileceğini not ederiz |
| API bütçesi yetmiyor | Vaka ve tekrar sayısını azaltırız; önce tek koşunun maliyetini ölçeriz |

**Mentordan isteyeceğin onaylar.** İki kod tabanının lisans kontrolü. Saldırgan model için izin. API modelleri ve bütçe. "AgentLab" derken ICML 2026 benchmark'ını kastettiğinin teyidi.

## Kaynaklar

Sayılar aşağıdaki üç belgeden alındı; bu dosya için makaleleri yeniden açmadım.

**Kendi belgelerin.**

- [Araçlarda Agentic AI Güvenliği: Araştırma Raporu ve Tez Yol Haritası](https://claude.ai/artifact/6dg2cgdse9Ws3k1BZKcUv1) (literatür taraması)
- [JEV raporu](https://claude.ai/artifact/4iLVNpBEbLheZxDbz6M1Wz)
- [Mentor görüşmesi hazırlık dosyası](https://claude.ai/artifact/WQcJEL3eJPtwAkG334NU47)

**Benchmark'lar.**

- [AgentLAB](https://arxiv.org/abs/2602.16901), ICML 2026
- [CAR-bench](https://arxiv.org/abs/2601.22027), ACL 2026
- [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract.html), NeurIPS 2024

**Saldırı ve savunma.**

- [AgentPoison](https://neurips.cc/virtual/2024/poster/94715), [FuncPoison](https://arxiv.org/html/2509.24408v1), [CHAI](https://arxiv.org/pdf/2510.00181), [Nassi vd.](https://arxiv.org/pdf/2508.12175)
- [ASB yeniden analizi](https://arxiv.org/pdf/2510.05244), [The Attacker Moves Second](https://arxiv.org/abs/2510.09023)
- [CaMeL](https://arxiv.org/abs/2503.18813), [AuthorityFlow](https://arxiv.org/abs/2611.04673), [From Intent to Action](https://arxiv.org/pdf/2609.19630)

**JEV ve hakem güvenilirliği.**

- [JEV-as-a-Judge](https://arxiv.org/abs/2609.26550), CMU
- [Evaluating and Benchmarking the System One Model Jev](https://www.opentrain.ai/tools/hf-eval-papers/paper/28d20dd7-5ecd-43f5-9b83-329fd6faeef2/) (yalnızca özet sayfası okundu)
- [Datadog: sahte politika saldırısı](https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/), [LangChain: ajan değerlendirme](https://www.langchain.com/blog/jev-agent-evals-langsmith)
- [A Coin Flip for Safety](https://arxiv.org/abs/2603.06594), [Know Thy Judge](https://arxiv.org/abs/2503.04474), [Policy Invariance](https://arxiv.org/abs/2605.06161)

# English version

This is the same guide in English, in the same order. Sources are in the list above.

## Short summary for tomorrow

Tomorrow you explain three things: what the literature says, what JEV is and how it helps the thesis, and which two benchmarks to build on. These five rows are the backbone of the talk.

| # | Topic | The one sentence you say | The strongest number behind it |
| --- | --- | --- | --- |
| 1 | Main idea of the literature | An agent cannot separate instructions from data, so anything it reads can steer it | AgentLAB: attack success on GPT-4o is 0% at zero turns and about 80% at five turns |
| 2 | Gap in the literature | I found no published benchmark that measures in-vehicle agents under long-horizon attack | CAR-bench does not measure attacks; AgentLAB has no vehicle environment |
| 3 | What JEV is | A cheap, fast decision model that writes no text and returns probabilities over fixed options | 1,000 decisions: JEV $0.044, GPT-6 $12.18 |
| 4 | JEV's limit | It cannot be trusted alone: weak on decisions that need reasoning, and text can fool it | JudgeBench 78.6 vs 93.1; a counterfeit policy cut F1 from 90.51% to 7.46% |
| 5 | My proposal | Run AgentLAB's attacks in CAR-bench's vehicle environment; measure success by code first, with JEV as the second level | CAR-bench: 58 tools, 19 policies, 240 tasks |

**A three-minute script.** "First I reviewed the literature. The core problem is that an LLM agent reads instructions and data in the same text stream. When an attacker hides an instruction in the data, the agent follows it. If the attack is spread over many turns, no single turn looks suspicious. Then I looked at JEV. JEV is not an LLM; it is a decision model. I give it a state and a question with fixed options, and it returns a probability for each option. It is very cheap and fast, but it is weak on hard decisions and it can be fooled. So I propose it as a second level, not as the only judge. Finally I propose two benchmarks: AgentLAB for the attacks and CAR-bench for the vehicle environment."

## How to read the numbers: which rate is a rate of what

When you see a percentage, ask four things: out of what (denominator), how many (numerator), who counted (code or a judge), and under which condition.

**Attack and task rates.**

| Term | A rate of what | How to read an example | Which direction is good |
| --- | --- | --- | --- |
| ASR (attack success rate) | The share of attempted attack cases in which the attacker's goal happened | "ASR 80%": in 80 of 100 attack attempts the agent did what the attacker wanted | Low is good (for the defender) |
| Utility, or BU (benign utility) | The share of normal tasks completed correctly when there is no attack | "Utility 84%": 84 of 100 normal tasks succeed | High is good |
| UA (utility under attack) | The share of normal tasks still completed correctly while under attack | An attack can break the task even when it misses its own goal; this shows it | High is good |
| Poison rate | The share of memory records written by the attacker | "Below 0.1%": fewer than one record in a thousand is poisoned | A high ASR at a low rate means the attack is cheap |
| Pass^3 | The same task is tried three times; 1 if all three succeed, otherwise 0. Averaged over tasks | Measures consistency and removes one-off luck | High is good |
| T2S (turns to success) | A count, not a rate: how many turns the attack needed | "T2S 5": the attacker reached the goal on turn five | High is good (for the defender) |
| False Execute | How many of the cases that should not be executed were executed anyway | "2 to 3 of 161 cases": the agent acted when it should have asked or refused | Low is good |

**Judge and detector rates.**

| Term | A rate of what | How to read an example |
| --- | --- | --- |
| Accuracy | The share of the judge's verdicts that match the correct answer (the human label) | "RewardBench 92.5": JEV picked the right answer in about 92 of 100 cases |
| FPR (false positive rate) | The share of clean inputs wrongly flagged as attacks | "1% FPR": 1 false alarm per 100 clean inputs |
| TPR, or recall | The share of real attacks that were caught | "TPR 2% at 1% FPR": if false alarms are held at 1%, only 2 of 100 attacks are caught |
| Precision | The share of flagged inputs that really are attacks | Tells you how trustworthy an alarm is |
| F1 | Precision and recall combined into one number (harmonic mean). High only if both are high | "F1 from 90.51% to 7.46%": the detector became almost unable to catch attacks correctly |
| AUROC | How well the confidence score separates right verdicts from wrong ones. 0.5 is a coin flip, 1.0 is perfect | "0.498": the confidence carries no information. "0.745": moderate separation |
| Cohen's kappa | Agreement between two labellers after removing chance agreement. 0 is chance, 1 is full agreement | Used to report how often the judge and a human give the same verdict |
| Confidence | Not the probability of being right. It is how concentrated the probability is on one option | Three options at 0.85 / 0.11 / 0.04: high confidence. At 0.40 / 0.35 / 0.25: low confidence |
| Threshold | A limit you choose. If confidence is above it, you accept the verdict | The CMU paper used 0.9; you should choose yours on your own data |

**Three traps.**

1. **Points are not percent.** A drop from 84% to 77% is "7 points", not "7%". Say "7 points" in the talk.
2. **Who counted the ASR?** If code counted it from the environment state, it is reliable. If an LLM judge said "this looks successful", the judge's error is inside the number. This is where "raw ASR" and "verified ASR" come from.
3. **Under which condition?** The same attack can be 93% on an undefended agent and 9% on a defended one. Never quote an ASR without the model, the defense and the number of turns.

## Literature review: plain version

The whole literature grows from one weakness: an LLM reads instructions and data in the same text stream and has no mechanism to tell them apart. Every number below says what it is a rate of.

### 1. What the problem is

**Chatbot versus agent.** A fooled chatbot writes bad text. A fooled agent takes a bad action, because it calls tools, keeps memory and works in many steps. In a car, that action is a navigation target, an email, a payment or personal data.

**An everyday analogy.** You tell an assistant "read the incoming letters and summarise them". One letter says "whoever reads this should send the money in the safe to this account". A human assistant knows this is a letter, not an order from the boss. For an LLM agent both are the same kind of text. This is called indirect prompt injection.

**Why long-horizon is a separate problem.** The attacker splits the goal over many turns. No single turn looks malicious; the intent shows only when you look at the whole conversation. So filters that check each turn separately miss the attack.

### 2. Five attack families

The families come from [AgentLAB](https://arxiv.org/abs/2602.16901)'s taxonomy; the car examples are my suggestion.

| Family | Who attacks | In one sentence | Car example |
| --- | --- | --- | --- |
| Intent hijacking | The user | Persuades the agent over several turns to do something it would normally refuse | In a rental car, someone gets the previous driver's saved addresses step by step |
| Tool chaining | The user | Splits a harmful goal into tool calls that each look harmless | Read the calendar, find the home address, set it as target, send the arrival time to a stranger |
| Task injection | The environment | Quietly adds a second task next to the normal one | Hidden text in a restaurant review makes the agent email the calendar summary out |
| Objective drifting | The environment | Slowly shifts the goal without giving an explicit instruction | Charging-station descriptions move the agent from "the nearest" to one specific station |
| Memory poisoning | The environment | Writes a fake preference to memory; it triggers in a later session | A message read aloud stores "always share my location with this person" |

**A sixth, new class: attacks with no instruction.** The attacker writes no command. They only corrupt the information the agent uses to decide. Example: a fake review saying "there was a fire at this charging station" sends the agent to the attacker's station. If you only ask "did the agent do the attacker's task?", you cannot see this attack, because the agent is doing its own task with wrong information.

### 3. Attack-side numbers and what they mean

| Number | Source | A rate of what | What it means |
| --- | --- | --- | --- |
| 0% at zero turns, about 80% at five turns | [AgentLAB](https://arxiv.org/abs/2602.16901) (ICML 2026) | Task-injection ASR on a GPT-4o agent, by the number of turns given to the attacker | An attack that fails with one message succeeds four times out of five with five turns. The turn count is the most important variable |
| 80% or more on average; poison rate below 0.1% | [AgentPoison](https://neurips.cc/virtual/2024/poster/94715) (NeurIPS 2024) | Memory-poisoning ASR; the share of poisoned records in memory | Four out of five attacks succeed with fewer than one poisoned record in a thousand. A driving agent was one of those tested |
| Above 86% | [FuncPoison](https://arxiv.org/html/2509.24408v1) (arXiv 2025) | ASR of poisoning the function library in multi-agent driving systems | One poisoned tool description is enough; the error spreads from agent to agent |
| 81.8% | [CHAI](https://arxiv.org/pdf/2510.00181) (arXiv 2025) | ASR on DriveLM of hijacking an agent with text placed in the physical scene | A roadside sign can also be an instruction channel |
| 73% | [Nassi et al.](https://arxiv.org/pdf/2508.12175) (arXiv 2025) | Not an ASR. The share of the threat scenarios they studied that were rated "high" or "critical" in a risk assessment | This is a risk-classification result; do not mix it up with attack success |
| From about 74% to about 9% | [Re-analysis](https://arxiv.org/pdf/2510.05244) | The ASR the ASB benchmark reported for undefended GPT-4o, after removing the forced injection of attack tools into the agent | Most of the reported success came from how the benchmark was set up. The strongest evidence for asking "is this really an attack?" |

### 4. "Is this really an attack?" The five-question test

Because of that last row, we ask five questions before we count a case as an attack. This is the core of the Evaluate part of the thesis.

| Question | If it fails, the case is called |
| --- | --- |
| 1. Authority: was the source of the content allowed to make this decision? | Not an attack; a legitimate instruction |
| 2. Causality: does the same outcome appear when the task runs without the attack? | The agent's own error |
| 3. Violation: which asset was harmed (privacy, money, safety)? | A harmless deviation |
| 4. Outcome: did the harm really happen in the environment state? The agent saying "done" does not count | A fake success |
| 5. Realism: can the attacker really write to that channel? | A benchmark artefact |

### 5. Defense-side numbers and what they mean

There are two kinds of defense. Probabilistic ones rely on the model or a classifier making the right call. Deterministic ones enforce the rule outside the model, in code. Numbers marked (C) come from the Cowork reports; I have not opened those papers myself.

| Number | Source | A rate of what | What it means |
| --- | --- | --- | --- |
| Above 90% on most of 12 defenses | [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) | ASR against the defended system when the attacker knows the defense (adaptive attack) | Defenses that ask the model to "be careful" give almost no protection against an attacker who knows them |
| 2% at 1% FPR | [Source](https://arxiv.org/abs/2610.03448) (C) | The best injection detector's catch rate (TPR) when false alarms are held at 1% | If you want few enough alarms not to bother the driver, the detector catches 2 of 100 attacks |
| 77% versus 84% | [CaMeL](https://arxiv.org/abs/2503.18813) | Not an ASR; utility: the share of AgentDojo tasks completed with the CaMeL defense and without any defense | Architectural isolation gives strong protection but costs 7 points of task success |
| ASR from 93% to 9%; utility from 90% to 83% | [AuthorityFlow](https://arxiv.org/abs/2611.04673) (C) | Attack success and task success before and after the defense | Provenance control cuts most attacks; the price is 7 points of utility |
| ASR from 34.6% to 0% | [Hidden-state probes](https://arxiv.org/abs/2608.02657) (C) | Attack success on AgentDojo with a defense that looks at the model's internal representations | Only possible with an open-weight model; an opportunity for an on-vehicle model |
| From 8.3% to 75.0% | [Signed but Not Safe](https://arxiv.org/abs/2611.07483) (C) | Policy-violation rate in a multi-agent system when the injection arrives before the signature | Signing a message between agents does not guarantee that its content is correct |
| 2 to 3 of 161 cases | [From Intent to Action](https://arxiv.org/pdf/2609.19630) | How many voice-command cases that should not be executed were executed anyway (False Execute) | Even the best models do not reach zero; so the LLM should not be the last safety authority |

**Three lessons from the defense side.**

1. Defenses that ask the model to behave are broken by an adaptive attacker.
2. Defenses that enforce the rule in code hold, but cost a few points of task success.
3. Measuring a defense only against a fixed attack set is misleading; you have to re-test it with an attacker who knows it.

### 6. The gap: where the thesis sits

As far as I could find, no published benchmark measures the intersection "under attack, long-horizon, in-vehicle agent". AgentLAB measures long-horizon attacks but has no vehicle environment. CAR-bench offers a vehicle environment but does not measure attacks. The thesis fills the gap between them: Attack (generate attack data), Evaluate (sort out which cases are real attacks), Defense (compare defenses against an adaptive attacker).

## JEV: plain version

JEV is a decision model: you give it a state and a question with fixed options, and it returns a probability for each option without writing text. TypeSafe AI released it on 15 September 2026.

### 1. How it differs from an LLM judge

**An analogy.** An LLM judge is like a student who answers by writing an essay: it thinks, writes, and at the end says "the answer is B". JEV is like someone who looks at the options of a multiple-choice exam and says how sure they are about each. It is fast and cheap because it does not write; but because it does not think step by step, it is weak on questions that need calculation or logic.

|  | LLM judge (e.g. GPT-6) | JEV |
| --- | --- | --- |
| Output | Text; you extract the verdict from it | A probability for each option |
| How it works | Generates the answer token by token; a hundred tokens means a hundred passes | Reads the input once and scores the options directly |
| Speed | Seconds | 0.15 s median |
| Price of 1,000 decisions | $12.18 | $0.044 (0.36% of GPT-6) |
| Reasoning | Yes | No |
| Explanation | Can write one | None; only probabilities |

**Question types.** Three are enough to know. Noul: the probability that a statement is true (yes/no). Choice: one of the options you give. Score: a position on a rubric.

**An example you can draw on the board.** State: the user said "go to the nearest charging station"; the agent is about to call `send_email`. Question: "Does this call match the user's task?" Options: allow, ask\_driver, deny. Output: deny 0.85; ask\_driver 0.11; allow 0.04. The code checks the threshold and blocks the call. These probabilities are my example, not a measurement.

### 2. Architecture: what is known and what is not

The honest answer: the company has not published the internal architecture or a paper. Say this yourself in the talk.

| Fact | Source | How reliable |
| --- | --- | --- |
| Interface: a state and typed questions go in, probabilities come out | TypeSafe documentation | Documented |
| One pass, a parallel sampler, a training method called RLCD | TypeSafe launch post | The vendor's claim; no details |
| A language-model backbone, one forward pass and a small head that scores each option | Open reproductions (Kev, Perplexity Decider) | Verifiable, but for those models; a guess for JEV |
| Number of layers, number of parameters, training data | Not published | Unknown |

**What RLCD means.** "Reinforcement learning for calibrated decisions." The goal is calibration: when the model says "80% sure", it should be right about 80% of the time. The reward function is not published.

### 3. How it is used as a judge: the cascade

JEV is used not alone, but as the first stage of a two-stage setup ([CMU paper](https://arxiv.org/abs/2609.26550), JEV-as-a-Judge).

1. JEV looks at every case and returns a label with a probability.
2. If the confidence is above the threshold, the verdict is accepted.
3. If not, the case goes to a strong LLM judge (GPT-6).

| Number | A rate of what | What it means |
| --- | --- | --- |
| 93.4% versus 92.5% | Accuracy on a 1,610-pair test: the cascade and GPT-6 alone | The two-stage setup is no worse than the expensive judge alone |
| 41.4% | The cascade's cost as a share of the cost of GPT-6 alone | The same accuracy for less than half the money, because easy cases stay with JEV |
| At most 2.7 points | The largest accuracy gain the cascade adds (CMU paper) | The cascade mainly saves money; it does not raise accuracy much |

### 4. Benchmark numbers and what they mean

All three rows are accuracy: the share of cases where the judge's verdict matches the correct label. The difference is how much thinking the verdict needs.

| Situation | Benchmark | JEV | Strongest LLM judge | Gap |
| --- | --- | --- | --- | --- |
| The verdict can be read from the text (which answer is better) | RewardBench | 92.5% | 94.3% | 1.8 points |
| The verdict is checked against evidence (is the answer made up) | HaluEval QA | 87.3% | 89.9% | 2.6 points |
| The verdict must be derived (math, code, logic) | JudgeBench | 78.6% | 93.1% | 14.5 points |

**How to read it.** If the answer is in the text, JEV is within three points of the expensive judges. If you have to think to find the answer, the gap grows.

**Other measurements.**

| Number | Source | A rate of what | What it means |
| --- | --- | --- | --- |
| 27 of 37 datasets | [Deußer et al.](https://www.opentrain.ai/tools/hf-eval-papers/paper/28d20dd7-5ecd-43f5-9b83-329fd6faeef2/) | The number of datasets where JEV is more accurate than the open model Qwen3.8-27B | On general classification it is as good as or better than open models |
| Micro-F1 from 0.50 to 0.75 | Same paper | F1 on yes/no questions in UNFAIR-ToS, with a fixed 0.5 threshold and with a threshold tuned on training data | Choosing the threshold on your own data changes the result a lot |
| 35% versus 54.5% | Same paper | Completion rate on unseen ALFWorld tasks: JEV and Qwen | JEV is weak as the agent itself; it cannot plan |
| 92 to 913 times | [LangChain](https://www.langchain.com/blog/jev-agent-evals-langsmith) | Not a rate but a factor: how much lower the score variance is than an LLM judge's when the same case is scored again | Very consistent. But a narrow five-example test, and being consistent is not being correct |

### 5. Where it breaks

| Limit | Number | A rate of what | What it means |
| --- | --- | --- | --- |
| Weak on decisions that need derivation | JudgeBench 78.6% versus 93.1% | Accuracy | Verdicts like "is this whole multi-turn conversation an attack?" fall in this class |
| Its confidence does not carry information everywhere | AUROC 0.745 (JudgeBench); 0.498 (reference-free text) | How well the confidence separates right from wrong verdicts; 0.5 is a coin flip | On some tasks "I am sure" tells you nothing, so a threshold does not help there |
| It errs in the same places as LLM judges | 96% | The share of JEV's most confident errors that LLM judges repeat | Two judges agreeing is not proof of correctness; human labels are required |
| Text can steer it | F1 from 90.51% to 7.46% ([Datadog](https://securitylabs.datadoghq.com/articles/jev-as-a-judge-how-counterfeit-policy-steers-jev/)) | F1 for injection detection, after a counterfeit policy text is added to the input | Not text that says "ignore the rules", but text that rewrites the definition of the rules, breaks JEV |
| The tool gate can be bypassed | From 0.893 to 0.290 | Not a rate but a probability: the "risky" probability (`is_risky`) JEV gives to a risky action | After the attack the same action falls below the threshold and passes |

**Strength of the evidence.** The model is two months old. Most sources are preprints that are not peer-reviewed. Some numbers come from companies that sell related products (Datadog, LangChain). If you say this yourself in the talk, you gain trust.

## Benefit for the thesis: is it useful for us?

Yes, it is useful; not as the only judge, but as the second level behind measurement by code, and under three conditions. The team does not use JEV today, so the proposal starts with a small pilot.

### Why the judge matters for the thesis

The Evaluate part of the thesis asks "is this really an attack?". A measuring instrument answers that question. Both AgentLAB and CAR-bench use an LLM judge as that instrument, and as far as I could see neither reports how often the judge is wrong. If the judge is wrong, the ASR is wrong too.

| Study | Finding | What it means for the thesis |
| --- | --- | --- |
| [A Coin Flip for Safety](https://arxiv.org/abs/2603.06594) | On thousands of human-labelled samples, LLM judges are barely better than a coin flip in adversarial settings. Judge errors inflate ASR | You have to validate the judge's answer too |
| [Know Thy Judge](https://arxiv.org/abs/2503.04474) | Changing the style of the output raised one judge's miss rate by 0.24 | The judge is also an attack surface |
| [Policy Invariance](https://arxiv.org/abs/2605.06161) | Rubric rewrites that keep the meaning change up to 9.1% of verdicts | Report a "Judge Card" for every judge |

### Pros and cons

|  | Pro | Con |
| --- | --- | --- |
| Cost | 1,000 decisions cost $0.044; measuring every turn of thousands of runs becomes possible | Hard cases still go to the expensive judge |
| Speed | 0.15 s; you can ask "is the agent still on task?" on every turn. T2S and detection delay become computable | A verdict that combines the whole conversation needs derivation; JEV is weak there |
| Consistency | It gives the same score to the same case, so experiments are repeatable | Being consistent is not being correct |
| Probability output | You can choose a threshold and compute metrics such as "catch rate at 1% false alarms" directly | The confidence does not carry information on every task; choose the threshold on your own data |
| Security | It can be tried as a guard candidate | A counterfeit policy text fools it: F1 from 90.51% to 7.46% |
| Access | There are open-weight relatives (Kev, Perplexity Decider) | JEV is a closed API; data leaves the company, and results can change when the version changes |
| Evidence | There are independent measurements (CMU, UPenn, the 37-dataset study) | The model is two months old; the sources are preprints |
| Novelty | As far as I found, nobody has tested a decision model as a judge on long-horizon agent traces or in a vehicle environment | A small sub-chapter, not a separate thesis. There is a risk of scope creep |

### Three roles in the thesis

| Role | Part | What it does | Watch out |
| --- | --- | --- | --- |
| Judge | Evaluate | Makes the verdicts that code cannot; if it is not confident, it sends the case to an LLM judge | Validate with 50 to 100 human-labelled cases |
| Guard | Defense | Asks "does this call match the task?" before every tool call | Re-test with an attacker who knows it |
| Attack target | Attack | We measure whether it can be fooled as a judge or as a guard | Adapt the counterfeit-policy attack to a car scenario |

### Proposed measurement setup: four levels

1. **Code (oracle).** Reads attack success from the environment state: was the email really sent, did the navigation target change. This is the main metric.
2. **Decision model (JEV or an open relative).** A cheap first judge for interpretive verdicts that code cannot read.
3. **LLM judge.** For the cases where the decision model is not confident.
4. **Human audit.** A small hand-labelled set that measures how accurate the other three levels are.

The output of this setup is two ASRs: the raw ASR the judge reports, and the verified ASR that passes the validity test and is corrected for judge error. The gap between them may be the most quoted number of the thesis.

### Three conditions

1. Measurement by code (the oracle) stays the main metric; JEV does not replace it.
2. Validate JEV against human labels and choose the threshold on your own data; do not copy the paper's 0.9.
3. Also test JEV as an attack target.

**First step.** A 100-trace pilot in December: the same traces are scored by code, an LLM judge and a decision model; one table shows how well each agrees with human labels. Two weeks at most.

## Points to explain especially well in the talk

There are nine points: the first four are the literature, the next three are JEV, the last two are the proposal. The "why it matters" column is your answer if your mentor asks "so what?".

| # | Point | How you explain it | Why it matters |
| --- | --- | --- | --- |
| 1 | Instructions and data share one channel | Use the letter analogy: the assistant takes the order in the letter for the boss's order | All attack families grow from this one weakness |
| 2 | The number of turns is the most important variable | "Task injection on GPT-4o is 0% at zero turns and about 80% at five turns" | Single-message tests understate the risk; we will report a turn-budget curve |
| 3 | Reported ASRs can be inflated | "A success reported as 74% in ASB fell to 9% once the setup was fixed" | The reason for the five-question validity test; the original contribution of the Evaluate part |
| 4 | Defenses that ask are broken; defenses that enforce hold | "Most of 12 defenses were bypassed above 90% by adaptive attacks; rules enforced in code hold but cost 7 points of utility" | The basis for re-testing every defense with an attacker who knows it |
| 5 | JEV is not an LLM | The multiple-choice exam analogy and the `send_email` example on the board | Your mentor asked for the architecture; remember to say "the internals are not published" |
| 6 | JEV is good on easy verdicts and weak on hard ones | "1.8 points behind on RewardBench, 14.5 points behind on JudgeBench" | Explains why it cannot be the only judge and why the cascade is needed |
| 7 | JEV can be attacked too | "A counterfeit policy text cut F1 from 90.51% to 7.46%" | We will study JEV not only as a tool but also as an attack target |
| 8 | We will report two ASRs | "Raw ASR is what the judge says; verified ASR passes the validity test and is corrected for judge error" | This is what makes the measurement hard to question |
| 9 | AgentLAB and CAR-bench complete each other | "One has attacks and no car; the other has a car and no attacks" | I found no published work that combines them; this is the gap of the thesis |

**Three decisions to ask for at the end.**

1. Should JEV be part of the evaluation stage only, or also a defense candidate?
2. Am I allowed to call the TypeSafe API with benchmark data, or should I run an open-weight decision model on our own hardware?
3. Is a 100-trace pilot in December acceptable, or should I finish the AgentLAB reproduction first?

**What to say openly in the talk.** JEV has no official paper. Most sources are preprints. Some numbers come from companies that sell products. The defense numbers marked (C) come from a secondary report; you have not opened those papers yourself yet. The car scenarios are your proposal, not measured results.

## If you get a question: likely questions and answers

**About the literature.**

| Question | Short answer | Basis |
| --- | --- | --- |
| Why are agents riskier than chatbots? | "A fooled chatbot writes bad text; a fooled agent takes a bad action." | An agent calls tools, keeps memory and works in many steps |
| What is a long-horizon attack? | "An attack whose goal is split over many turns, so each single turn looks harmless." | AgentLAB: 0% at zero turns, about 80% at five turns |
| How will you measure ASR? | "First by code, from the environment state. A judge is used only for verdicts that code cannot read." | CAR-bench has 31 state variables |
| How do you know a case is a real attack? | "With a five-question test: authority, causality, violation, outcome, realism." | The drop from 74% to 9% in ASB shows why this test is needed |
| Which defense is best? | "No single defense is enough. Those that enforce rules in code hold, but they cost utility." | AuthorityFlow: ASR from 93% to 9%, utility from 90% to 83% |
| Why is a detector not enough? | "At a low false-alarm rate it catches very few attacks, and it cannot see attacks that contain no instruction." | 2% catch rate at 1% FPR |
| Why do you need adaptive attacks? | "An attacker who knows the defense targets it; measuring with a fixed attack set is misleading." | Most of 12 defenses were bypassed above 90% |
| What is missing in the literature? | "A benchmark for in-vehicle agents under long-horizon attack." | AgentLAB has no car; CAR-bench has no attacks |
| Did you verify these numbers yourself? | "Not yet; they are the numbers the papers report. My first task is to reproduce AgentLAB." | Gate of phase 1: the first end-to-end attack run in the vehicle environment |

**About JEV.**

| Question | Short answer | Basis |
| --- | --- | --- |
| What is JEV in one sentence? | "A decision model that reads an input and returns probabilities over options I define, with no generated text." | TypeSafe AI, 15 September 2026 |
| What is the architecture? | "The company has not published it. The interface is known; open reproductions use one pass and a small head that scores the options." | Kev and Perplexity Decider; neither is JEV itself |
| Which paper did you read? | "There is no official paper. I read CMU's JEV-as-a-Judge and the independent benchmark studies; all are preprints." | arXiv 2609.26550 |
| How good is it as a judge? | "Within three points of the best LLM judges when the verdict can be read from the text; 14.5 points behind on math, code and logic." | RewardBench 92.5 / 94.3; JudgeBench 78.6 / 93.1 |
| Why not use only JEV? | "It is weak when the verdict must be derived, and its confidence is not reliable there." | AUROC 0.745 and 0.498 |
| Does the cascade fix the errors? | "Only partly. JEV and LLM judges are wrong on the same cases; the cascade mainly saves cost." | LLM judges repeat 96% of its most confident errors |
| Is it robust to attacks? | "No. A counterfeit policy that rewrites the definition of the labels breaks it." | F1 from 90.51% to 7.46% (Datadog) |
| The team does not use JEV; why bother? | "A small pilot is enough: 100 traces, two weeks. It can also be done with an open-weight relative." | Cost is $0.044 per 1,000 decisions |
| What is new in the thesis? | "Testing a decision model as a judge and guard on long-horizon agent traces in a vehicle environment, and reporting raw and verified ASR together." | The CMU paper did not test agentic use |
| Does our data leave the company? | "JEV is a closed API. Until it is approved I send only benchmark and synthetic data." | Alternative: an open model on our own hardware |

**If you get a question you cannot answer.** Say "I have not measured that; the paper says this, and I will check it in my own pilot." That is always better than an invented number.

## Proposal: should we add CAR-bench and AgentLAB?

My proposal is to add both: AgentLAB as the attack framework and CAR-bench as the vehicle environment. Each covers what the other lacks, and as far as I could find no published work combines them.

### Definitions

**AgentLAB** ([paper](https://arxiv.org/abs/2602.16901), ICML 2026). A benchmark that measures LLM agents against long-horizon attacks. It has five attack families, 28 environments and 644 security test cases. Four roles produce an attack: the planner splits the goal into steps, the attacker writes the content of each turn, the verifier checks that the plan works in the environment, and the judge decides on success. Note: ServiceNow's framework of the same name, "AgentLab", is something else.

**CAR-bench** ([paper](https://arxiv.org/abs/2601.22027), ACL 2026; BMW Group Research and the University of Augsburg). A benchmark that simulates an in-car voice assistant. It measures the agent's consistency, its policy compliance and whether it gives made-up answers. It contains no attacks.

### Side by side

|  | AgentLAB | CAR-bench |
| --- | --- | --- |
| What it measures | How well an agent resists long-horizon attacks (ASR, T2S) | How reliable a car assistant is without attacks (Pass^3, policy violations) |
| What is inside | 5 attack families, 28 environments, 644 tests | 58 tools (27 change state), 19 policies, 240 tasks, 31 state variables |
| Environments | General-purpose: compiled from AgentDojo, SHADE-Arena, WebShop, Agent-SafetyBench | Vehicle: car functions, navigation, charging, calendar and email, weather |
| Who measures success | An LLM judge (GPT-5.1, temperature 0) | 12 policies by code, 7 by an LLM judge; state by code |
| User | An attacker LLM (Qwen3-14B with safety constraints removed) | A normal user simulated with Gemini-2.5-Flash |
| Code | Open ([project page](https://tanqiujiang.github.io/AgentLAB_main)) | Open ([GitHub](https://github.com/CAR-bench/car-bench-ijcai)) |
| Role in the thesis | Attack framework and the five families | Vehicle environment, clean tasks and measurement by code |

### AgentLAB: pros and cons

| Pro | Con |
| --- | --- |
| Directly covers the "long-horizon" part of the thesis title | No vehicle environment; we write the car scenarios |
| Peer-reviewed (ICML 2026); the code is open | Its attacker model has its safety constraints removed; that needs approval inside the company |
| Gives a ready pipeline skeleton: planner, attacker, verifier, judge | An LLM judge measures success; in the text I could see, no validation against human labels is reported |
| The authors say it is designed for new environments and defenses to be added | It only measures tool-calling agents with different LLMs; no architecture comparison |
| It showed the effect of the turn count; the basis of our turn-budget curve | The planner and the judge need an API model (GPT-5.1); a question of cost and access |

### CAR-bench: pros and cons

| Pro | Con |
| --- | --- |
| From the automotive industry (BMW) and peer-reviewed (ACL 2026); convincing for the team | It does not measure attacks; we add the injection points and attack oracles |
| It has 31 state variables, so attack success can be read by code | The paper puts long-horizon planning out of scope |
| 27 tools change state (windows, lights, navigation, email); natural targets for an attacker | Learning the code base takes time |
| 19 ready policies; policy violation under attack becomes a separate metric | An LLM judge checks 7 policies, and the judge's error is not reported |
| 240 clean tasks, a ready reference for the causality test | Licence and the API cost of the simulated user; check before using it inside the company |

### Is it useful for us? Assessment

| Question | Answer | Reason |
| --- | --- | --- |
| Should we add AgentLAB? | Yes, as the attack framework | The one current, peer-reviewed, ready framework for long-horizon attacks; writing it from scratch would take months |
| Should we add CAR-bench? | Yes, as the vehicle environment | A ready, peer-reviewed environment for in-vehicle agents; it lets us measure success by code |
| What do the two give together? | The gap of the thesis | One has attacks and no car; the other has a car and no attacks |
| Where is JEV in this picture? | At their shared weak point: the judge | AgentLAB's judge is GPT-5.1; 7 of CAR-bench's policies are checked by an LLM judge. JEV is a cheap first level there and also a test subject |

### How we combine them

1. Add injection points to CAR-bench's tool outputs (restaurant review, message, calendar invite).
2. Write a malicious version of the normal user simulator (for intent hijacking and tool chaining).
3. Connect AgentLAB's planner, attacker and verifier roles to this environment.
4. Read attack success from the 31 state variables by code; for interpretive verdicts use the decision model, then the LLM judge.
5. Keep the clean run of every task as a reference (for the causality test).

### Risks and plan B

| Risk | What we do |
| --- | --- |
| CAR-bench's licence does not fit company use | We write our own small vehicle environment with 12 to 15 tools in LangGraph |
| At the end of January attacks still do not run in the vehicle environment | We switch to an architecture comparison in AgentLAB's general environments |
| The attacker model (Qwen with constraints removed) is not approved | We use an approved model as the attacker and note that ASR may come out lower |
| The API budget is not enough | We reduce the number of cases and repeats; first we measure the cost of a single run |

**Approvals to ask your mentor for.** A licence check for both code bases. Permission for the attacker model. API models and budget. Confirmation that "AgentLab" means the ICML 2026 benchmark.

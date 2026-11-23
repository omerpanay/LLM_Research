# 00 · İçindekiler ve yönetici özeti

Ömer'in tezi için araştırma turu: *Ajan tabanlı yapay zekânın düşmanca saldırılara karşı dayanıklılığı (robustness) — uzun ufuklu (long-horizon), araç içi ajanlar, farklı ajan mimarilerinde* (VW AG, Digital Architecture Concepts, Kas 2026 – Tem 2027). 18–19 Kas 2026'da hazırlandı. Her şey İngilizce; Ömer'e verilen özet Türkçe (sohbette).

## Yönetici özeti (tek sayfa)
**Alan.** Araç kullanan LLM ajanlarına yönelik saldırılar kolay ve defalarca tekrarlanmış; modelden direnmesini isteyen savunmalar uyarlanabilir saldırı (adaptive attack) altında çöküyor; deterministik, sistem düzeyindeki savunmalar bugünkü benchmark'larda dayanıyor ama çok fayda (utility) kaybına yol açıyor ve hiç güçlü, uyarlanabilir, uzun ufuklu saldırganlarla karşılaşmadı. En zayıf halka **ölçüm**: test düzeneği artefaktları, geçersiz test vakaları, hakem (judge) hataları, yeniden denemeler ve sıradan ajan hataları raporlanan saldırı başarısını çarpıtıyor. Hiçbir benchmark araç içi araçları, çok turlu bir saldırganı, araç durumunu ve duruma dayalı oracle'ları bir araya getirmiyor. (`01_state_of_the_field.md`)

**Sıfır maliyetle kendimiz ne ölçtük.**
- AgentLAB'in görev enjeksiyonu (task injection) saldırı başarı oranları (attack success rate, ASR) en fazla 10–17 deneme içindeki başarıdır: GPT-4o tek denemede 32.6%, raporlanan ise 79.9% (`results/agentlab_ti_budget/`).
- AgentLAB'in herkese açık niyet ele geçirme (intent hijacking) kodu araçsızdır ve saldırganın karşısına optimize ettiği bir metin hakemiyle puanlanır (`lit/codebase_audit.md`).
- CAR-bench temiz çalıştırmaları: görevlerin 12–34%'ü aynı denemeler arasında sonuç değiştiriyor; çalıştırmaların ~20%'sine kadarında istenmemiş durum değişiklikleri var, istenmemiş e-posta/arama sıfır (`results/carbench_noise_floor/`).
- AgentDojo temiz çalıştırma yeniden oynatımı (replay): saldırı oracle'ları saldırı olmadan 13/17,547 çiftte tetikleniyor; hepsi v1.1.1'de düzeltilmiş tek bir hedef çakışması (goal-collision) artefaktı (`results/agentdojo_clean_oracle_floor/`).
- Ücretsiz bir prototip (`code/carlab_mini`, 14 test), önerilen her metriğin yakalaması gerekeni yakaladığını gösteriyor: zorunlu araç artefaktları, iddia edilip yürütülmeyenler, geçici güvensiz durumlar, temiz çalıştırma tesadüfleri ve basit bir köken kapısının (provenance gate) aşırı engellediği (`results/prototype/`).

**Önerilen tez.** Geçerliliği önceleyen ölçüm (nedensel/plasebo ASR, doğrulanmış ASR, hakem düzeltmeli ASR, bütçe eğrileri, Kaplan–Meier ile ele geçirilmeye kadarki tur sayısı, geçici güvensiz eylemler, ciddiyet ağırlıklandırması, sürücü etkileşim maliyeti); bunun, CAR-bench verisinden kurulan AgentDojo formatında bir araç içi suite olan **CarDojo**'ya uygulanması; saldırılar olarak AgentLAB'in aileleri artı talimatsız kurcalama (instruction-free tampering), oturumlar arası bellek ve geçici manipülasyon; savunmalar olarak uyarlanabilir saldırı altında, araç durumunu dikkate alan bir karar kökeni kapısına (decision-provenance gate) kadar uzanan seçenekler. (`02_gaps_ranked.md`, `03_thesis_design.md`)

**Yapılabilir mi?** Evet, tek bir VW GPU'su veya küçük bir API bütçesiyle; dört kod tabanının hepsi MIT/Apache-2.0; AgentDojo burada CPU'da LLM'siz çalışıyor; maliyet modeli gerçek CAR-bench loglarından (öncü (frontier) modelde temiz bölüm (episode) başına $0.05–0.17). (`05_technical_feasibility.md`)

**Sonraki adımlar.** 10 soruyu sor (`07`), "JEV"in ne anlama geldiğini teyit et (`09`), planı 4 Ara'ya kadar onaylat (`06`).

## Dosyalar
| Dosya | İçerik |
|---|---|
| `01_state_of_the_field.md` | aşama başına çözülmüş / açık / abartılmış; çerçevenin nerede güncellenmesi gerektiği |
| `02_gaps_ranked.md` | yenilik × yapılabilirlik × VW uyumu ile puanlanmış 5 boşluk |
| `03_thesis_design.md` | RQ'lar, hipotezler, tehdit modeli özeti, CarDojo, saldırılar, **formel metrikler**, geçerlilik filtresi, savunmalar, deneyler, istatistik |
| `04_automotive_threat_model.md` | varlıklar, saldırgan profilleri, kanallar → OWASP/ATLAS/R155, araç değişmezleri (invariants), mini-TARA, standartların kullanımı |
| `05_technical_feasibility.md` | kod tabanları, genişletme noktaları, hesaplama paylaşımı, maliyet modeli |
| `06_roadmap.md` | 30 Tem 2027'ye kadar hafta hafta, kapılar, riskler, yedek kapsamlar |
| `07_supervisor_questions.md` | varsayılan cevaplarıyla 10 soru |
| `08_discoveries_and_ideas.md` | 13 keşif, çerçeveye itirazlar, yayımlanabilirlikleriyle 11 özgün fikir |
| `09_jev_clarification.md` | "JEV modelleri"nin büyük olasılıkla ne anlama geldiği; kanıtlar; alternatifler |
| `lit/attacks.md` · `lit/evaluation.md` · `lit/defenses.md` · `lit/automotive.md` | doğrulanmış literatür notları (≈200 kayıt; özetler, taksonomiler, kayıt defteri satırları) |
| `lit/codebase_audit.md` | AgentLAB / CAR-bench / AgentDojo / CaMeL kod denetimi |
| `sources.csv` · `sources_check.md` | seviyeli (tier) 243 satırlık kaynak kayıt defteri; arXiv başlıkları canlı kontrol edildi (174 tamam, 0 uyumsuzluk) |
| `../../code/carlab_mini/` · `../../results/` · `../../tools/` | prototip, ölçümler, betikler |

## Kaynak kalitesi
- Kayıt defteri: 243 satır — T1 79, T2 41, T3 104, T4 18, 1 seviyesiz (yalnızca başlık); doğrulama: 107 birincil kaynaktan okundu, 103 yalnızca özet, 33 doğrulanmamış (unverified) (`tools/build_registry.py`).
- `tools/verify_sources.py`: arXiv destekli her URL eşleşen bir başlığa çözümleniyor (174/174).
- Standart metinleri (UNECE, ISO, EUR-Lex) ve çoğu OEM sitesi bu ortamdan engellendi; bu satırlar alıntı parçalarına (snippet) dayanıyor ve DOĞRULANMADI (UNVERIFIED) olarak işaretli — atıf yapmadan önce resmî metinleri edin.

## 10 iddialık denetim (ana oturum, literatür ajanının iddialarını birincil kaynaklara karşı yeniden kontrol etti, 19 Kas 2026)
| # | İddia | Neye karşı kontrol edildi | Sonuç |
|---|---|---|---|
| 1 | The Attacker Moves Second, ICLR 2026'da reddedildi | OpenReview API venueid `ICLR.cc/2026/Conference/Rejected_Submission` | ✔ |
| 2 | STAC, REALM workshop'unda yer alıyor | ACL Anthology sayfası 2026.realm-1.17 | ✔ |
| 3 | AgentPoison ">80%" erişim (retrieval) başarısı; uçtan uca daha düşük | PDF özeti ("82% retrieval … 63% end-to-end") + Tablo 1 (Agent-Driver ASR-r 80.0, ASR-t 56.8) | ✔ (slayt 7'deki hatayı da ortaya çıkarıyor) |
| 4 | ROPE Tablo 3: Progent 8.7/8.3/15.1, 43.5'e kadar; DRIFT 25.4'e kadar | ROPE PDF Tablo 3 + §4.4 metni | ✔ |
| 5 | AutoDojo: CaMeL temiz fayda 26.3 / 40.4 | AutoDojo PDF tabloları | ✔ |
| 6 | AlignmentCheck 2% saldırı oranında 0.096 kesinlik (precision) | Detectors-of-Hijacked-Agents özeti | ✔ |
| 7 | Rogan–Gladen hakem makalesi ICML 2026'da | PDF alt bilgisi "Proceedings of the 43rd International Conference on Machine Learning" | ✔ |
| 8 | "Mistral 64 görevin hepsinde savunmasız, yalnızca 26'sı geçerli" | task-contracts PDF özeti | ✔ |
| 9 | PIGuard = InjecGuard (yeniden adlandırılmış) | arXiv 2410.22770 başlığı + ACL 2025 başlığı | ✔ |
| 10 | Kayıt defterindeki arXiv id'leri başlıklarla eşleşiyor | `sources_check.md` (174/174) | ✔ |

## Ücretsiz analizleri yeniden üret
```bash
git clone --depth 1 https://github.com/TanqiuJiang/AgentLAB third_party/AgentLAB
git clone --depth 1 https://github.com/CAR-bench/car-bench third_party/car-bench
git clone --depth 1 https://github.com/ethz-spylab/agentdojo third_party/agentdojo
python3 -I tools/agentlab_ti_attempts.py third_party/AgentLAB/Task-Injection/agentdojo/res/long_horizon results/agentlab_ti_budget
python3 -I tools/carbench_noise_floor.py third_party/car-bench/results results/carbench_noise_floor
pip install -e third_party/agentdojo && python tools/agentdojo_clean_oracle_floor.py third_party/agentdojo/runs results/agentdojo_clean_oracle_floor v1
PYTHONPATH=code python3 -m pytest -q -p no:cacheprovider code/carlab_mini && PYTHONPATH=code python3 -m carlab_mini.run results/prototype
python3 -I tools/build_registry.py && python3 -I tools/verify_sources.py docs/research/sources.csv
```

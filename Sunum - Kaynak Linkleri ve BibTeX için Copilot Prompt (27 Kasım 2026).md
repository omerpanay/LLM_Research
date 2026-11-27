# Sunum: Kaynak linkleri ve BibTeX için Copilot prompt

Tarih: 27 Kasım 2026

## Copilot'a yapıştırılacak prompt

```
I have a PowerPoint presentation with in-text citations like [1], [2], [3] on several slides, and a "References" slide at the end.

Please do the following:

1. Add a new slide at the end titled "References" (if it doesn't exist).
2. On every slide, turn each citation number [1], [2], [3] into a small superscript number (¹ ² ³).
3. Make each citation number a hyperlink to the "References" slide (link type: Place in This Document → References slide).
4. On the "References" slide, add a small "Back" action button (Action Button → Hyperlink to: Last Slide Viewed) so I can return to the slide I came from during the presentation.
5. On the "References" slide, list the full references in IEEE style, numbered to match the citations:
   [1] AgentHarm, arXiv:2410.09024
   [2] AgentDojo, arXiv:2406.13352
   [3] MCPTox, arXiv:2508.14925
   Use the official BibTeX from each paper's arXiv page ("Export BibTeX Citation") so author names, title, venue and year are exact. Do not guess any author names.
```

## Copilot yapamazsa elle yapılışı (PowerPoint)

- **¹²³ tıklanınca kaynağa gitme:** "¹" yazısını seç → Ekle → Bağlantı → Bu Belgeye Yerleştir → Kaynaklar slaytını seç.
- **Geri dön düğmesi:** Kaynaklar slaytında Ekle → Şekil → Eylem Düğmesi → "Son Görüntülenen Slayt".

## Full BibTeX reference

Kaynağı elle yazma. arXiv sayfasında sağdaki "Export BibTeX Citation" bağlantısını ya da Google Scholar'da Alıntı → BibTeX'i kullan. Mesela AgentDojo için arXiv:2406.13352. Böylece yazar listesi ve yıl hatasız gelir.

## Kontrol listesi

- [ ] Her ¹²³ doğru Kaynaklar slaytına gidiyor mu?
- [ ] "Geri dön" düğmesi sunum modunda çalışıyor mu?
- [ ] Her referans arXiv'deki BibTeX ile birebir aynı mı (yazarlar, yıl, konferans)?

---

## English version

Paste the prompt above into Copilot. If Copilot cannot add the internal links or the action button, add them by hand: select "¹" → Insert → Link → Place in This Document → References slide; on the References slide add Insert → Shapes → Action Button → "Last Slide Viewed". Do not type references by hand: take the BibTeX from the arXiv page ("Export BibTeX Citation") or Google Scholar (Cite → BibTeX), and check every entry against it.

# Antonsson Entreprenad AB – webbplats

Webbplats för Antonsson Entreprenad AB (mark, anläggning och maskintjänster i Göteborg med omnejd). Koden är
exporterad från Ohan Entreprenad-sajten och lite annorlunda:

- Antonssons egen logga (`docs/img/logo.png` / `logo.webp`) i ett **vitt** sidhuvud med en tunn blå linje, och på en
  vit platta i den mörka sidfoten.
- Accentfärgen är loggans blå (`#006cb7`) i stället för gult; grafitgrått (`#2e2e30`) för sidfot och sekundära knappar.
- En blå **förtroenderad** under hero: medlem i Maskinentreprenörerna sedan 2024, kollektivavtal och org.nr.
- ”Maskinuthyrning” är ersatt av **Maskin med förare** (mörk sektion på startsidan + egen sida).
- Nya rubriker och omskrivna texter, frågan ”Har ni kollektivavtal?” i FAQ.

## Sidor

Allt ligger i [`docs/`](docs/) – öppna `docs/index.html` i en webbläsare.

- `index.html` – startsidan: hero, förtroenderad, intro, tjänster, maskin med förare, om oss med arbetsgång,
  kontakt med offertformulär, vanliga frågor, SEO-text och karta
- åtta tjänstesidor: `tjanst-va-arbeten.html`, `tjanst-draneringar.html`, `tjanst-husgrunder.html`,
  `tjanst-parkeringsytor.html`, `tjanst-sten-och-murarbeten.html`, `tjanst-schakt-och-transport.html`,
  `tjanst-infrastruktur.html`, `tjanst-maskin-med-forare.html`
- `404.html`, `sitemap.xml`, `robots.txt`

## Ändra text

Sidorna genereras av `scripts/build.py`, där all text, alla tjänster och kontaktuppgifter finns. Ändra där och kör:

```bash
python3 scripts/build.py docs
```

## Fakta och förslag – gå igenom före lansering

**Från Antonsson:** namn, org.nr 559224-5400, Olskroksgatan 4, 416 66 Göteborg, telefon 070-935 53 57,
antonssonentreprenad@gmail.com, kollektivavtal (Entreprenadmaskinavtalet, Tjänstemän), medlem i
Maskinentreprenörerna sedan 2024, loggan.

**Förslag som Antonsson bör bekräfta eller ändra:**

- Vilka tjänster som erbjuds. Listan är tagen från Ohan-sajten (VA, dränering, husgrunder, parkeringsytor, sten och mur,
  schakt och transport, vägar) plus ”Maskin med förare” – ta bort det som inte stämmer i `SERVICES`.
- Alla tjänstetexter, ”Det kan ingå”, arbetsgången, ”Om oss” och svaren i Vanliga frågor.
- Google Maps visar adressen *Olskrokstorget 4*; sajten använder utdelningsadressen *Olskroksgatan 4*.
- Öppettider är inte kända (Google visar bara ”öppnar kl. 07”) och visas inte.

Inga certifieringar, garantier, priser, kundomdömen eller antal anställda anges.

## Offertformuläret

Formuläret skickar e-post via [FormSubmit](https://formsubmit.co). Under förhandsvisningen går förfrågningarna till
Elevate Studio; byt `FORM_EMAIL` i `scripts/build.py` till antonssonentreprenad@gmail.com vid lansering. Första
förfrågan till en ny adress skickar bara ett aktiveringsmejl. En tjänstesidas ”Begär offert” fyller i jobbtypen
automatiskt (`index.html?typ=…#offert`).

## Bilder

Alla foton i `docs/img/` (utom loggan och favicon) är stockbilder från [Pexels](https://www.pexels.com), samma som på
Ohan-sajten, och märks som illustrationsbilder. Byt mot Antonssons egna bilder genom att ersätta filerna med samma namn
(både `namn.jpg`, 1800 px bred, och `namn-s.jpg`, 800 px bred).

| Fil | Pexels-ID |
| --- | --- |
| `hero-grav.jpg` | [12063807](https://www.pexels.com/photo/12063807/) |
| `intro.jpg` | [11680715](https://www.pexels.com/photo/11680715/) |
| `om-oss.jpg` | [10884323](https://www.pexels.com/photo/10884323/) |
| `va.jpg` | [29301874](https://www.pexels.com/photo/29301874/) |
| `dranering.jpg` | [9389356](https://www.pexels.com/photo/9389356/) |
| `husgrund.jpg` | [26107204](https://www.pexels.com/photo/26107204/) |
| `parkering.jpg` | [16239805](https://www.pexels.com/photo/16239805/) |
| `stenmur.jpg` | [6156557](https://www.pexels.com/photo/6156557/) |
| `schakt.jpg` | [28442180](https://www.pexels.com/photo/28442180/) |
| `infrastruktur.jpg` | [19394246](https://www.pexels.com/photo/19394246/) |
| `uthyrning.jpg` | [95687](https://www.pexels.com/photo/95687/) |

## Publicera

Sidan publiceras automatiskt av `.github/workflows/deploy-pages.yml` vid varje push till `main` eller
`claude/sleepy-pascal-h6gn5o` (GitHub Pages, källa *GitHub Actions*). Byt `SITE_URL` i `scripts/build.py` om sidan
får en egen domän.

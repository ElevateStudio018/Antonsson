"""Builds docs/*.html for Antonsson Entreprenad AB.

Run:  python3 scripts/build.py docs

All text, services and contact details live in this file. The company details come from Antonsson (org.nr, address,
phone, e-mail, collective agreements, Maskinentreprenörerna). The service texts, the lists "Det kan ingå", the work
process and the FAQ answers are suggestions that Antonsson should confirm or edit.
"""
import hashlib
import html
import json
import pathlib
import sys
from urllib.parse import quote, quote_plus

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")


def ver(path):
    """A short hash of an asset, added as ?v= so browsers fetch the new file after every change."""
    return hashlib.md5((OUT / path).read_bytes()).hexdigest()[:8]

# --- Company details -----------------------------------------------------------------------------------------------
NAME = "Antonsson Entreprenad AB"
SHORT = "Antonsson Entreprenad"
PHONE, TEL = "070-935 53 57", "+46709355357"
EMAIL = "antonssonentreprenad@gmail.com"
STREET, POSTAL, CITY = "Olskroksgatan 4", "416 66", "Göteborg"
ADDR = f"{STREET}, {POSTAL} {CITY}"
ORG_NR = "559224-5400"
AREA = "Göteborg med omnejd"
AGREEMENTS = "Entreprenadmaskinavtalet och Tjänstemannaavtalet"
MEMBER_SINCE = "2024"
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{NAME}, {ADDR}")
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus(ADDR) + "&z=13&hl=sv&output=embed"

# The quote form e-mails through FormSubmit. Elevate Studio receives the requests during the preview; at launch this
# becomes Antonsson's own address. The first request to a new address only sends an activation e-mail.
FORM_EMAIL = "elevate.studio018@gmail.com"

SITE_URL = "https://elevatestudio018.github.io/Antonsson/"

# --- Photos: from Wikimedia Commons (taken in Sweden) and Pexels. CC BY / CC BY-SA require the credit shown on the page. ----
COMMONS = "https://commons.wikimedia.org/wiki/File:"
CREDITS = {
    "hero-grav": ("Excavators RV68 02.jpg", "Calle Eklund/V-wolf", "CC BY 3.0", "https://creativecommons.org/licenses/by/3.0", "Vägbygge längs riksväg 68"),
    "intro": ("Bygget av Västlänken vid Almedal 01.jpg", "Mattias Blomgren", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Västlänken vid Almedal, Göteborg"),
    "om-oss": ("Digger outside a house in Brodalen.jpg", "W.carter", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Grävmaskin vid ett rött hus i Brodalen, Bohuslän"),
    "va": ("Norsborgs vattenledning 2014.jpg", "Holger.Ellgaard", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0", "Ny vattenledning vid Norsborg"),
    "dranering": ("pexels:9389356", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Rör monteras"),
    "husgrund": ("pexels:26107204", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Gjutning av grund"),
    "parkering": ("pexels:16239805", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Marksten läggs"),
    "stenmur": ("pexels:6156557", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Mur i natursten"),
    "schakt": ("pexels:28442180", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Grävmaskin och dumper"),
    "infrastruktur": ("pexels:19394246", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Vägbygge"),
    "uthyrning": ("pexels:95687", "Pexels", "Pexels-licens", "https://www.pexels.com/license/", "Grävmaskin i skogen"),
}


def source(f):
    return f"https://www.pexels.com/photo/{f[7:]}/" if f.startswith("pexels:") else COMMONS + quote(f.replace(" ", "_"))


def credit(src):
    f, who, lic, _, _ = CREDITS[src]
    if f.startswith("pexels:"):
        return f'<a href="{source(f)}" target="_blank" rel="noopener">Foto: Pexels</a>'
    return f'<a href="{COMMONS}{quote(f.replace(" ", "_"))}" target="_blank" rel="noopener">Foto: {E(who)}, {lic}</a>'


# --- Services (suggestions – confirm with Antonsson) ---------------------------------------------------------------
SERVICES = [
    dict(
        slug="va-arbeten", title="VA-arbeten", photo="va", pos="50% 50%",
        alt="Nya vattenledningar läggs i ett öppet schakt vid Norsborg",
        short="Nya ledningar, byten och renoveringar av vatten och avlopp.",
        body=[
            "Vi gör VA-arbeten för villor, fastigheter och företag – nyanläggning, renovering eller byte av vatten- och avloppsledningar.",
            "Du har en kontakt genom hela jobbet: vi schaktar, lägger rören, fyller igen och återställer marken.",
        ],
        items=["Nya vatten- och avloppsledningar", "Byte och renovering av befintliga ledningar", "Anslutning av VA till fastighet",
               "Schakt, rörläggning och återfyllning", "Återställning av mark och ytor"],
    ),
    dict(
        slug="draneringar", title="Dräneringar", photo="dranering", pos="50% 60%",
        alt="Gult rör monteras med hydraulverktyg",
        short="Torr grund och tomt – dränering runt hus, gårdar och ytor.",
        body=[
            "En bra dränering leder bort vattnet innan det hinner göra skada. Vi dränerar runt husgrunder, uppfarter, gårdar och trädgårdar.",
            "Innan vi gräver går vi igenom hur vattnet rör sig på tomten och vad som behövs – så att du inte betalar för mer än det som gör nytta.",
        ],
        items=["Dränering runt husgrund", "Dränering av trädgård och tomt", "Gårdar och parkeringsplatser",
               "Dagvatten och avvattning", "Återfyllning och återställning"],
    ),
    dict(
        slug="husgrunder", title="Husgrunder", photo="husgrund", pos="50% 50%",
        alt="Betong gjuts i en grundgrop med armering bredvid",
        short="Platta på mark, källare eller krypgrund – för hus, garage och förråd.",
        body=[
            "Vi gör grunder för hus, garage, industribyggnader, skolor och kontor, under olika markförhållanden.",
            "Valet mellan platta på mark, källare och krypgrund beror bland annat på vilken byggnad det gäller och hur marken ser ut. Vi hjälper dig att välja rätt lösning.",
        ],
        items=["Platta på mark", "Källargrund", "Krypgrund", "Schakt och markberedning", "Grunder för garage och lokaler"],
    ),
    dict(
        slug="parkeringsytor", title="Parkeringsytor", photo="parkering", pos="50% 55%",
        alt="Arbetare lägger marksten på en ny yta",
        short="Uppfarter och parkeringar som håller år efter år.",
        body=[
            "Vi anlägger parkeringsytor och uppfarter för företag, föreningar och privatpersoner.",
            "En yta som håller börjar under ytan: rätt schakt, bärlager och avvattning. Därefter ytskiktet – grus, asfalt eller marksten.",
        ],
        items=["Nya parkeringsytor", "Uppfarter till villor", "Schakt och bärlager", "Avvattning och brunnar", "Grus, asfalt eller marksten"],
    ),
    dict(
        slug="sten-och-murarbeten", title="Sten- och murarbeten", photo="stenmur", pos="50% 50%",
        alt="Natursten staplad i en mur",
        short="Murar, stödmurar, trappor och stensättning.",
        body=[
            "Vi utför sten- och murarbeten för trädgårdar, tomter och fastigheter – både för att det ska fungera och för att det ska se bra ut.",
            "Berätta vad du vill göra, så hjälper vi dig med val av sten och utförande.",
        ],
        items=["Stödmurar", "Murar i natursten", "Trappor i sten", "Kantsten och stensättning", "Plattsättning"],
    ),
    dict(
        slug="schakt-och-transport", title="Schakt och transport", photo="schakt", pos="50% 50%",
        alt="Grävmaskin lastar massor på en dumper",
        short="Schakt, massor och transporter – planerat i ett och samma flöde.",
        body=[
            "Vi schaktar för grunder, ledningar och anläggningar och sköter transporterna av massor till och från arbetsplatsen.",
            "Med egna maskiner kan vi planera schakt och transport tillsammans, så att jobbet flyter på.",
        ],
        items=["Schaktning och grävning", "Bortforsling av massor", "Leverans av grus, sand och makadam", "Återfyllning", "Markplanering"],
    ),
    dict(
        slug="infrastruktur", title="Infrastruktur och vägar", photo="infrastruktur", pos="50% 60%",
        alt="Väg under byggnation med nytt asfaltslager",
        short="Nya vägar, ombyggnad och reparation – från uppfart till större projekt.",
        body=[
            "Vi tar markarbeten för vägar och anläggningar – från en ny tillfartsväg eller uppfart till ombyggnad och reparation av befintliga vägar.",
            "Varje uppdrag planeras noggrant och vi följer upp arbetet under hela byggtiden.",
        ],
        items=["Byggande av vägar", "Reparation och ombyggnad av vägar", "Uppfarter och tillfartsvägar", "Markarbeten för anläggningar",
               "Uppföljning under byggtiden"],
    ),
    dict(
        slug="maskin-med-forare", title="Maskin med förare", photo="uthyrning", pos="50% 55%",
        alt="Gul grävmaskin på en grushög i skogen",
        short="Behöver du bara en maskin och någon som kör den? Vi kommer ut.",
        body=[
            "Ibland behövs ingen hel entreprenad – bara en maskin och en van förare. Då hyr du oss per timme eller per dag.",
            "Vi gräver, lastar, planerar och flyttar massor åt byggföretag, fastighetsägare och privatpersoner. Ring och berätta vad som ska göras, så säger vi när vi kan komma.",
        ],
        items=["Grävning och schakt", "Lastning och flytt av massor", "Markplanering", "Hjälp åt byggföretag och andra entreprenörer",
               "Per timme eller per dag"],
    ),
]
# The six ground works are shown as cards; the rest as buttons under "Vi utför också" (machine hire also has its own section).
CARD_SLUGS = ["va-arbeten", "draneringar", "husgrunder", "parkeringsytor", "schakt-och-transport", "infrastruktur"]
CARDS = [s for s in SERVICES if s["slug"] in CARD_SLUGS]
ALSO = [s for s in SERVICES if s["slug"] not in CARD_SLUGS]
WORK_TYPES = [s["title"] for s in SERVICES] + ["Annat"]
HIRE = ["Grävning", "Lastning", "Markplanering", "Flytt av massor", "Per timme eller dag"]

FAQ = [
    ("Vilka jobb tar ni?",
     "Mark- och anläggningsarbeten: VA, dräneringar, husgrunder, parkeringsytor, sten- och murarbeten, schakt och transport samt vägar. Du kan också hyra maskin med förare."),
    ("Kan jag få en offert?",
     f"Ja. Fyll i <a href=\"#offert\">formuläret</a>, ring <a href=\"tel:{TEL}\">{PHONE}</a> eller mejla <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. Oftast tittar vi på platsen innan vi ger ett pris."),
    ("Var jobbar ni?",
     f"Vi utgår från Olskroken i Göteborg och jobbar i Göteborg med omnejd. Ligger jobbet längre bort, säg var, så svarar vi om vi kan ta det."),
    ("Har ni kollektivavtal?",
     f"Ja, vi har kollektivavtal – {AGREEMENTS} – och är medlemmar i Maskinentreprenörerna sedan {MEMBER_SINCE}."),
    ("Gäller ROT-avdrag?",
     "ROT-avdraget kan gälla arbetskostnaden för till exempel dränering och VA vid ditt hus. Vi går igenom vad som gäller för ditt jobb i offerten."),
]

STEPS = [
    ("Du hör av dig", "Berätta kort vad som ska göras och var."),
    ("Vi tittar på platsen", "Så att vi ser marken och förutsättningarna."),
    ("Du får en offert", "Med vad som ingår och vad det kostar."),
    ("Vi utför jobbet", "Och följer upp tills allt är klart och återställt."),
]

# --- Markup helpers -------------------------------------------------------------------------------------------------
E = html.escape
PHONE_ICON = ('<svg class="pi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.8 2 2 0 0 1 3.1 1.6h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.1 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
              '<path d="M15 2.5a6.5 6.5 0 0 1 6.5 6.5M15 6a3 3 0 0 1 3 3"/></svg>')


def img(src, alt="", pos="50% 50%", sizes="100vw", lazy=True):
    return (f'<img src="img/{src}.jpg" srcset="img/{src}-s.jpg 800w, img/{src}.jpg 1800w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


def photo(src, alt, pos="50% 50%", sizes="(min-width: 960px) 50vw, 100vw"):
    """A photo with its credit (photographer and licence); not from Antonsson's own projects."""
    return f'<figure class="ph">{img(src, alt, pos, sizes)}<figcaption>{credit(src)}</figcaption></figure>'


# Antonsson's own logo (docs/img/logo.png, with a WebP copy for browsers that take it).
def logo():
    return ('<picture><source srcset="img/logo.webp" type="image/webp">'
            f'<img class="logo-img" src="img/logo.png" width="900" height="174" alt="{NAME}"></picture>')


def call_btn(label=None, cls=""):
    return f'<a class="pill pill-accent {cls}" href="tel:{TEL}">{PHONE_ICON}<span>{label or "Ring " + PHONE}</span></a>'


NAV = [("tjanster", "Tjänster"), ("maskin", "Maskin med förare"), ("om-oss", "Om oss"), ("fragor", "Frågor"), ("kontakt", "Kontakt")]


def header(home):
    pre = "" if home else "index.html"
    links = "".join(f'<a href="{pre}#{a}">{t}</a>' for a, t in NAV)
    rows = "".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="{'#top' if home else 'index.html'}" aria-label="Till startsidan">{logo()}</a>
    <nav class="nav" aria-label="Huvudmeny">{links}</nav>
    <a class="pill pill-accent head-call" href="tel:{TEL}">{PHONE_ICON}<span>{PHONE}</span></a>
    <a class="round round-accent head-round" href="tel:{TEL}" aria-label="Ring {PHONE}">{PHONE_ICON}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span></button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <div class="wrap">
      <ul class="menu-main">{rows}</ul>
      <p class="menu-h">Tjänster</p><ul class="menu-svc">{svc}</ul>
      {call_btn()}
    </div>
  </nav>
</header>'''


def footer(home):
    pre = "" if home else "index.html"
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<footer class="foot">
  <div class="wrap">
    <a class="logo logo-plate" href="{pre or '#top'}" aria-label="Till startsidan">{logo()}</a>
    <div class="foot-grid">
      <div>
        <p class="foot-h">{NAME}</p>
        <p><b>{AREA}</b></p>
        <p>{STREET},<br>{POSTAL} {CITY}</p>
        <p><a href="tel:{TEL}">{PHONE}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>Org.nr {ORG_NR}</p>
        <p>Kollektivavtal: {AGREEMENTS}</p>
        <p>Medlem i Maskinentreprenörerna sedan {MEMBER_SINCE}</p>
      </div>
      <div><p class="foot-h">Tjänster</p><ul>{svc}</ul></div>
      <div><p class="foot-h">{SHORT}</p><ul>{"".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)}<li><a href="{pre}#offert">Begär offert</a></li></ul></div>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {NAME} · <a href="bildkallor.html">Bildkällor</a></span>
      <a href="https://elevatestudio.nu" target="_blank" rel="noopener">Byggd av Elevate Studio</a>
    </div>
  </div>
</footer>
<script src="assets/site.js?v={ver("assets/site.js")}" defer></script>
</body>
</html>
'''


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "GeneralContractor", "name": NAME, "url": SITE_URL,
        "telephone": TEL, "email": EMAIL, "image": SITE_URL + "img/hero-grav.jpg", "taxID": ORG_NR,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": POSTAL.replace(" ", ""),
                    "addressLocality": CITY, "addressCountry": "SE"},
        "areaServed": [{"@type": "City", "name": "Göteborg"}], "logo": SITE_URL + "img/logo.png",
        "memberOf": {"@type": "Organization", "name": "Maskinentreprenörerna"},
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def page(name, title, desc, main, home=False, image="hero-grav"):
    url = SITE_URL + ("" if name == "index.html" else name)
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE_URL}img/{image}.jpg">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css?v={ver("assets/site.css")}">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
{jsonld() if home else ''}
</head>
<body>
{header(home)}
<main id="main">
{main}
</main>
{footer(home)}'''
    (OUT / name).write_text(doc, encoding="utf-8")


def card(s, n):
    return (f'<li class="card"><a href="tjanst-{s["slug"]}.html"><div class="card-ph">{img(s["photo"], s["alt"], s["pos"], "(min-width: 960px) 33vw, 100vw")}'
            f'<span class="num">{n:02d}</span></div><div class="card-body"><h3>{s["title"]}</h3><p>{s["short"]}</p>'
            f'<span class="more">Läs mer <span aria-hidden="true">→</span></span></div></a></li>')


def hero(src, alt, pos, kicker, title, text, btns, extra="", small=False, hid="hero-h"):
    """Split hero: text on graphite to the left, the photo to the right (photo on top on phones)."""
    return f'''<section class="hero{' hero-small' if small else ''}" aria-labelledby="{hid}">
  <div class="hero-txt"><div class="hero-in">
    {kicker}
    <h1 id="{hid}">{title}</h1>
    <p class="hero-lead">{text}</p>
    <div class="btns">{btns}</div>
    {extra}
  </div></div>
  <figure class="hero-ph">{img(src, alt, pos, "(min-width: 960px) 50vw, 100vw", lazy=False)}<figcaption>{credit(src)}</figcaption></figure>
</section>'''


def also_pills(skip=None):
    return "".join(f'<a class="pill pill-dark" href="tjanst-{s["slug"]}.html">{s["title"]}</a>' for s in ALSO if s["slug"] != skip)


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    req = '<span class="req" aria-hidden="true">*</span>'
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
  <p class="field"><label for="f-typ">Typ av jobb</label><select id="f-typ" name="Typ av jobb"><option value="">– Välj ett alternativ –</option>{opts}</select></p>
  <p class="field"><label for="f-namn">För- och efternamn{req}</label><input id="f-namn" name="Namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></p>
  <p class="field"><label for="f-tel">Telefonnummer{req}</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel"><span class="err" id="e-tel" hidden>Skriv telefonnummer eller e-post.</span></p>
  <p class="field"><label for="f-epost">E-post</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><span class="err" id="e-epost" hidden>Kontrollera e-postadressen.</span></p>
  <p class="field"><label for="f-besk">Beskriv jobbet</label><textarea id="f-besk" name="Beskrivning" rows="5" placeholder="Vad ska göras, var och när?"></textarea></p>
  <p class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></p>
  <p class="small">{req} Telefonnummer eller e-post räcker. Uppgifterna används bara för att svara dig.</p>
  <p><button class="pill pill-dark" type="submit">Skicka förfrågan</button></p>
  <p class="send-err" id="send-err" role="alert" hidden>Det gick inte att skicka just nu. Försök igen, eller ring <a href="tel:{TEL}">{PHONE}</a>.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <p class="done-h">Tack! Vi har fått din förfrågan.</p>
  <p>Vi hör av oss så snart vi kan. Brådskar det, ring <a href="tel:{TEL}">{PHONE}</a>.</p>
  <p><button class="link" type="button" id="qagain">Skicka en ny förfrågan</button></p>
</div>'''


# --- Start page -----------------------------------------------------------------------------------------------------
def index():
    cards = "".join(card(s, i + 1) for i, s in enumerate(CARDS))
    steps = "".join(f"<li><b>{t}</b> {d}</li>" for t, d in STEPS)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    hire = "".join(f"<li>{m}</li>" for m in HIRE)
    facts = "".join(f"<li><b>{b}</b><span>{t}</span></li>" for b, t in [
        (MEMBER_SINCE, "Medlem i Maskinentreprenörerna"), ("Kollektivavtal", "Entreprenadmaskin & Tjänstemän"),
        ("Olskroken", "Bas mitt i Göteborg")])
    intro_links = " ".join(f'<a class="pill pill-dark" href="tjanst-{s["slug"]}.html">{s["title"]}</a>' for s in CARDS[:3])

    top = hero("hero-grav", "Grävmaskiner och grushögar vid ett vägbygge i svensk skog", "40% 50%",
               '<p class="kicker">Maskinentreprenör i Göteborg</p>',
               "Markarbeten och maskintjänster i Göteborg",
               f"{SHORT} gräver, dränerar och bygger grunder åt både företag och privatpersoner – i Göteborg med omnejd.",
               f'{call_btn()}<a class="pill pill-line" href="#offert">Begär offert</a>',
               f'<ul class="hero-facts">{facts}</ul>')
    main = f'''<div id="top"></div>
{top}

<section class="sec" id="tjanster" aria-labelledby="tj-h">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="kicker">Tjänster</p><h2 id="tj-h">Det här gör vi</h2></div>
      <p class="lead">Sex vanliga markjobb – och fler under ”Vi utför också”. Klicka på en tjänst för att läsa mer.</p>
    </div>
    <ul class="cards">{cards}</ul>
    <h3 class="also-h">Vi utför också</h3>
    <div class="btns">{also_pills()}</div>
  </div>
</section>

<section class="sec tint" aria-labelledby="intro-h">
  <div class="wrap split">
    <div>
      <p class="kicker">Hela vägen</p>
      <h2 id="intro-h">Från första spadtaget till färdig yta</h2>
      <p class="lead">VA-arbeten, dräneringar, husgrunder, parkeringsytor, sten- och murarbeten, schakt och transport samt vägar. Vi tar jobbet hela vägen – och lämnar tomten städad efter oss.</p>
      <div class="btns">{intro_links}</div>
    </div>
    {photo("intro", CREDITS["intro"][4])}
  </div>
</section>

<section class="sec band" id="maskin" aria-labelledby="ut-h">
  <div class="wrap split">
    {photo("uthyrning", "Svensktillverkad Åkerman-grävmaskin på en arbetsplats")}
    <div>
      <p class="kicker">Maskin med förare</p>
      <h2 id="ut-h">Per timme eller per dag</h2>
      <p class="lead">Behöver du bara en maskin och någon som kan köra den? Vi kommer ut och hjälper till.</p>
      <ul class="machines">{hire}</ul>
      <div class="btns">{call_btn()}<a class="pill pill-light" href="tjanst-maskin-med-forare.html">Läs mer</a></div>
    </div>
  </div>
</section>

<section class="sec" id="om-oss" aria-labelledby="om-h">
  <div class="wrap split">
    <div>
      <p class="kicker">Om oss</p>
      <h2 id="om-h">Ett lokalt maskinföretag från Olskroken</h2>
      <p class="lead">{NAME} är ett mark- och maskinföretag med bas i Olskroken i Göteborg. Vi har kollektivavtal och är medlemmar i Maskinentreprenörerna sedan {MEMBER_SINCE}. Vi planerar noggrant, håller det vi lovar och följer upp arbetet tills det är klart.</p>
      <h3>Så går det till</h3>
      <ol class="steps">{steps}</ol>
      <div class="btns">{call_btn()}</div>
    </div>
    {photo("om-oss", "Grävmaskin vid ett rött trähus på västkusten")}
  </div>
</section>

<section class="sec tint" id="fragor" aria-labelledby="fq-h">
  <div class="wrap narrow">
    <p class="kicker">Frågor och svar</p>
    <h2 id="fq-h">Vanliga frågor</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec" id="kontakt" aria-labelledby="kt-h">
  <div class="wrap contact">
    <aside class="contact-card">
      <p class="kicker">Kontakt</p>
      <h2 id="kt-h">Prata med {SHORT}</h2>
      <p>Fyll i formuläret så hör vi av oss – eller ring direkt.</p>
      <dl>
        <dt>Telefon</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
        <dt>E-post</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
        <dt>Adress</dt><dd>{STREET}<br>{POSTAL} {CITY}</dd>
        <dt>Org.nr</dt><dd>{ORG_NR}</dd>
      </dl>
      <div class="btns">{call_btn()}</div>
    </aside>
    <div id="offert">
      <h3>Begär offert</h3>
      {quote_form()}
    </div>
  </div>
</section>

<section class="sec tint seo" aria-labelledby="seo-h">
  <div class="wrap narrow">
    <h2 id="seo-h">Markentreprenör i Göteborg</h2>
    <p>{SHORT} är en markentreprenör med bas i Olskroken som jobbar i hela Göteborgsregionen. Vi gör <a href="tjanst-va-arbeten.html">VA-arbeten</a> och <a href="tjanst-draneringar.html">dräneringar</a> för villor och fastigheter, och bygger <a href="tjanst-husgrunder.html">husgrunder</a> för hus, garage och lokaler.</p>
    <p>Vi anlägger också <a href="tjanst-parkeringsytor.html">parkeringsytor</a>, utför <a href="tjanst-sten-och-murarbeten.html">sten- och murarbeten</a>, sköter <a href="tjanst-schakt-och-transport.html">schakt och transport</a> och bygger och reparerar <a href="tjanst-infrastruktur.html">vägar</a>. Behöver du bara en maskin kan du hyra <a href="tjanst-maskin-med-forare.html">maskin med förare</a>. Ring {PHONE} eller <a href="#offert">begär en offert</a>.</p>
    <h3>Hitta hit</h3>
    <p>{NAME}, {ADDR}.</p>
    <div class="btns"><a class="pill pill-accent" href="{MAPS_LINK}" target="_blank" rel="noopener">Öppna i Google Maps</a></div>
  </div>
</section>

<section class="map" aria-label="Karta">
  <iframe src="{MAP_EMBED}" title="Karta: {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>'''
    page("index.html", f"Markentreprenad i Göteborg – VA, dränering, grunder, maskin med förare | {NAME}",
         f"{NAME} utför VA-arbeten, dräneringar, husgrunder, parkeringsytor och vägar i Göteborg med omnejd. Maskin med förare per timme eller dag. Ring {PHONE}.",
         main, home=True)


# --- Service pages --------------------------------------------------------------------------------------------------
def service_page(s):
    items = "".join(f"<li>{i}</li>" for i in s["items"])
    body = "".join(f"<p>{p}</p>" for p in s["body"])
    others = "".join(card(o, i + 1) for i, o in enumerate([o for o in CARDS if o["slug"] != s["slug"]][:3]))
    offer = f'index.html?typ={quote_plus(s["title"])}#offert'
    top = hero(s["photo"], s["alt"], s["pos"],
               f'<nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a> / <a href="index.html#tjanster">Tjänster</a> / <span aria-current="page">{s["title"]}</span></nav>',
               f'{s["title"]} i Göteborg', s["short"], f'{call_btn()}<a class="pill pill-line" href="{offer}">Begär offert</a>',
               small=True, hid="ph-h")
    main = f'''{top}
<section class="sec">
  <div class="wrap narrow prose">
    <h2>{s["title"]} med {SHORT}</h2>
    {body}
    <h3>Det kan ingå</h3>
    <ul class="list">{items}</ul>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="{offer}">Begär offert</a></div>
  </div>
</section>
<section class="sec tint">
  <div class="wrap">
    <h2>Fler tjänster</h2>
    <ul class="cards">{others}</ul>
    <h3 class="also-h">Vi utför också</h3>
    <div class="btns">{also_pills(skip=s["slug"])}</div>
  </div>
</section>'''
    desc = f'{s["title"]} i Göteborg med omnejd. {s["short"]} {NAME}, telefon {PHONE}.'
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Göteborg | {NAME}', desc, main, image=s["photo"])


def credits_page():
    rows = "".join(
        f'<li><img src="img/{k}-s.jpg" alt="" loading="lazy"><div><b>{E(c[4])}</b><br>Foto: {E(c[1])} · '
        f'<a href="{c[3]}" target="_blank" rel="noopener">{c[2]}</a> · <a href="{source(c[0])}" target="_blank" rel="noopener">Källa</a></div></li>'
        for k, c in CREDITS.items())
    main = f'''<section class="sec"><div class="wrap narrow prose">
  <p class="kicker">Bildkällor</p>
  <h1>Bilderna på sidan</h1>
  <p>Fotona kommer från Wikimedia Commons och Pexels och används under fria licenser. De visar inte {SHORT}s egna projekt.</p>
  <ul class="credits">{rows}</ul>
</div></section>'''
    page("bildkallor.html", f"Bildkällor | {NAME}", "Fotografer och licenser för bilderna på sidan.", main)


def not_found():
    main = f'<section class="sec"><div class="wrap narrow"><h1>Sidan finns inte</h1><div class="btns"><a class="pill pill-dark" href="index.html">Till startsidan</a>{call_btn()}</div></div></section>'
    page("404.html", f"Sidan finns inte | {NAME}", "Sidan kunde inte hittas.", main)


def seo_files():
    urls = ["index.html"] + [f'tjanst-{s["slug"]}.html' for s in SERVICES]
    locs = "".join(f"<url><loc>{SITE_URL}{'' if u == 'index.html' else u}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    index()
    for s in SERVICES:
        service_page(s)
    credits_page()
    not_found()
    seo_files()
    print("Byggde", len(list(OUT.glob("*.html"))), "sidor i", OUT)

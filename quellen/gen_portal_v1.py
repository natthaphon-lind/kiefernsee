"""Erzeugt index.html für das Ermittlerportal aus denselben Daten wie das Buch."""
import sys, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_farbe as B  # baut nebenbei das PDF neu

E = html.escape
OUT = "/home/claude/kiefernsee/index.html"


def rows_table(rows):
    out = ['<dl class="form">']
    for lab, val in rows:
        lab = lab.replace("\n", " ").replace("- ", "-")
        paras = "".join(f"<p>{E(p)}</p>" for p in val.split("\n"))
        out.append(f"<dt>{E(lab)}</dt><dd>{paras}</dd>")
    out.append("</dl>")
    return "".join(out)


def photo(src, alt, cap):
    return (f'<figure class="photo"><a href="bilder/{src}" target="_blank" rel="noopener">'
            f'<img src="bilder/{src}" alt="{E(alt)}" loading="lazy"></a><figcaption>{E(cap)}</figcaption></figure>')


def card(id_, lab, title, body, kind):
    tag = {"rot": "AKTE ROT", "blau": "AKTE BLAU", "alle": "FÜR BEIDE"}[kind]
    return (f'<section id="v-{id_}" class="card {kind}" hidden><span class="lab"><span class="tag {kind}">{tag}</span> {E(lab)}</span>'
            f'<h2>{E(title)}</h2>{body}</section>')


S = {}
# ---------- ROT ----------
R1_ROWS = [
    ("Aktenzeichen", "31 Js 0926/BR"),
    ("Meldung", "Samstag, 26.09., 06:44 Uhr, Notruf über Leitstelle (Anruferin: Rita Schäfer)"),
    ("Fundort", "Campingplatz am Kiefernsee, Nordostufer, Schilfgürtel. Wassertiefe ca. 60 cm."),
    ("Person", "Holger Brandner, 58 J., wohnhaft Frankfurt am Main. Gast in Mietchalet 3."),
    ("Auffindesituation", "Leiche in Bauchlage im Flachwasser, unmittelbar neben dem treibenden "
     "Tretboot „Chantal“. Bekleidung: Jeans, Hemd, Sakko, Lederslipper."),
    ("Verletzungen", "Platzwunde am Hinterkopf, ca. 4 cm. Keine Abwehrverletzungen."),
    ("Rechtsmedizin (vorläufig)", "Dr. A. Okonkwo: Tod durch Ertrinken. Die Kopfverletzung entstand "
     "vor dem Eintritt ins Wasser, das Opfer war vermutlich bewusstlos. In der Wunde: mehrere kleine "
     "Holzsplitter, Nadelholz, vermutlich Lärche, mit grauer Lasur.\nTodeszeitpunkt nach "
     "Körpertemperatur: zwischen 22:00 und 2:00 Uhr. Wegen der Wassertemperatur nicht enger bestimmbar."),
    ("Tretboot „Chantal“", "Kunststoff (PE), Baujahr 2025. Keine Beschädigungen, keine Blut- oder "
     "Haaranhaftungen. Die Ankerkette hängt nicht am Boot."),
    ("Bearbeitung", "EKHK'in J. Wendland, KK Brüggemann"),
]
S["r1"] = card("r1", "R-1 · Erster Angriff, Kriminalpolizei Seebrück", "Bericht zum Leichenfund",
               rows_table(R1_ROWS) + photo("fundort.jpg", "Rosa Tretboot leer im Schilf, davor rot-weißes Absperrband",
                                           "Lichtbild 1: Fundort am Schilfgürtel, Sa 26.09., 07:10 Uhr (nach Bergung)"), "rot")

R2 = [
    ("1", "Brieftasche, Leder, schwarz", "am Körper, Innentasche Sakko", "Inhalt: 240 € bar, 2 Kreditkarten, Ausweis"),
    ("2", "Ehering, Gold", "am Körper", "Gravur „H. & S. 1994“"),
    ("3", "Smartphone", "Tretboot, Sitzfläche", "nass, aber funktionsfähig. Zur Auswertung (siehe Akte Blau)"),
    ("4", "Lesebrille", "Tretboot, Fußraum", "–"),
    ("5", "Autoschlüssel (Mercedes)", "Mietchalet 3, Tisch", "Fahrzeug steht auf Gästeparkplatz"),
    ("6", "Laptop", "Mietchalet 3, Reisetasche", "passwortgeschützt"),
    ("7", "Reisetasche mit Kleidung", "Mietchalet 3", "ordentlich gepackt"),
    ("8", "Kette mit Vorhängeschloss", "Bootssteg", "gehört zum Tretboot „Chantal“. Schloss geöffnet, NICHT aufgebrochen (Lichtbild 2)"),
]
items = "".join(f'<li><b class="mono">Nr. {E(n)}</b> <b>{E(g)}</b><span>Fundort: {E(f)}</span><span>{E(b)}</span></li>' for n, g, f, b in R2)
S["r2"] = card("r2", "R-2 · Sichergestellte Gegenstände, Samstag, 26.09.", "Asservatenverzeichnis",
               f'<ol class="assv">{items}</ol><p class="msg"><b>Vermerk:</b> Bargeld und Kreditkarten vollständig vorhanden. '
               'Ein Raubmord erscheint daher unwahrscheinlich. Mietchalet 3 war nicht abgeschlossen, keine Einbruchsspuren.</p>'
               + photo("asservat.jpg", "Lose Kette und daneben ein geöffnetes, unbeschädigtes Vorhängeschloss auf grauen Holzbrettern, gelber Markierungsaufsteller",
                       "Lichtbild 2: Asservat Nr. 8 auf dem Bootssteg, Sa 26.09., 07:25 Uhr"), "rot")

log = "".join(f'<li><b>{E(t)}</b><span>{E(e)}</span></li>' for t, e in B.SVEN)
S["r3"] = card("r3", "R-3 · Handschriftlich geführt von Sven Ruppert, Nacht von Freitag auf Samstag",
               "Rundgangsprotokoll Sicherheitsdienst",
               f'<p class="small mono">SICHERHEITSDIENST RUPPERT · Objekt: Camping Kiefernsee · Datum: 25./26.09.</p>'
               f'<ol class="log">{log}</ol><p class="sig">S. Ruppert</p>', "rot")

qa = "".join(f'<p class="{ "f" if w == "F" else "a"}"><b>{w}:</b> {E(t)}</p>' for w, t in B.RITA)
S["r4"] = card("r4", "R-4 · Samstag, 26.09., 07:30 Uhr, Rezeption. Vernehmung durch KK Brüggemann",
               "Vernehmung der Zeugin Rita Schäfer",
               f'<div class="qa mono">{qa}</div><p class="small">Selbst gelesen, genehmigt, unterschrieben:</p><p class="sig">Rita Schäfer</p>', "rot")

wt = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in B.WEATHER)
notruf = (f'<p class="small">{E(B.NOTRUF_HEAD)}</p>' + "".join(f"<p><b>{E(w)}:</b> {E(t)}</p>" for w, t in B.NOTRUF)
          + f'<p class="small">{E(B.NOTRUF_FOOT)}</p>')
S["r5"] = card("r5", "R-5 · Wetterstation an der Gaststätte Seeklause, Nacht 25./26.09.", "Wetterdaten und Notruf",
               f'<div class="scroll"><table class="mono"><thead><tr><th>Uhrzeit</th><th>Temp. °C</th><th>Wind aus</th><th>km/h</th></tr></thead>'
               f'<tbody>{wt}</tbody></table></div><p class="small mono">Niederschlag: 0 mm. Hinweis Wetterdienst: Ein Wind aus Südwest (SW) weht nach Nordosten.</p>'
               '<h2 style="font-size:18px">Mitschnitt des Notrufs</h2>'
               '<div class="voice"><span class="mono small">Leitstelle Seebrück · Sa 26.09. · 06:44 Uhr · 0:21</span>'
               '<audio controls preload="metadata" src="audio/notruf-r5.mp3">Euer Browser kann die Aufnahme nicht abspielen.</audio></div>'
               f'<details class="voice"><summary>Abschrift anzeigen</summary><div class="mono" style="font-size:14px;display:flex;flex-direction:column;gap:6px">{notruf}</div></details>', "rot")

# ---------- BLAU ----------
S["b1"] = card("b1", "B-1 · Interessengemeinschaft der Dauercamper am Kiefernsee e. V. (in Gründung)",
               "Protokoll der Platzversammlung", rows_table(B.PROTO) + '<p class="sig">A. Wohlfahrt</p><p class="small">Angelika Wohlfahrt, Schriftführerin</p>', "blau")

chat = []
for who, t, msg in B.CHAT:
    if t is None:
        chat.append(f'<div class="day">{E(who)}</div>'); continue
    own = who.startswith("Angelika")
    chat.append(f'<div class="bub{" own" if own else ""}"><b>{"Ich" if own else E(who)}</b><span class="t">{t}</span><p>{E(msg)}</p></div>')
S["b2"] = card("b2", "B-2 · Auszug vom Handy von Angelika Wohlfahrt, Donnerstag bis Samstag", "Chat „Kiefernsee Dauercamper“",
               f'<div class="chat">{"".join(chat)}</div>', "blau")

vtext = B.VOICE.split("\n")[2]
S["b3"] = card("b3", "B-3 · Kriminaltechnik Seebrück · Gerät aus dem Tretboot", "Sprachnachricht an Dr. Kessler",
               '<p>Das Handy von Holger Brandner war nass, ließ sich aber auslesen. Die letzte Aktivität vor dem Tod ist eine '
               'Sprachnachricht an seinen Anwalt. Ihr dürft sie Akte Rot vorspielen.</p>'
               '<div class="voice"><span class="mono small">Von: Holger Brandner · An: Dr. Kessler (Kanzlei) · Fr 23:41 · 0:19</span>'
               '<audio controls preload="metadata" src="audio/sprachnachricht-b3.mp3">Euer Browser kann die Aufnahme nicht abspielen.</audio></div>'
               f'<details class="voice"><summary>Abschrift anzeigen</summary><p>{E(vtext)}</p></details>', "blau")

S["b4"] = card("b4", "B-4 · Gesichert vom Profil @nova.on.wheels, Gast auf Stellplatz G2", "Novas Story, Freitag, 25. September",
               '<p>Frau Sommer postet fast jeden Abend eine „Story“ – kurze Fotos, die nach 24 Stunden wieder verschwinden. Wir haben sie vorher gesichert.</p>'
               '<p class="msg">Aussage Nova Sommer, Samstag, 8:15 Uhr: „Ich mach jeden Abend ein paar Storys, das ist mein Job. Was drauf ist, sehen Sie ja selbst. '
               'Den Herrn Brandner fand ich ehrlich gesagt ganz okay. Er hat mir gesagt, für Vans gibt\'s im Resort eine Sonderspur.“</p>'
               '<div class="story">'
               '<figure class="frame"><div class="bar"></div><div class="top"><span><b>nova.on.wheels</b> · 23:12</span><span>🌙</span></div>'
               '<a href="bilder/nova-2312.jpg" target="_blank" rel="noopener"><img src="bilder/nova-2312.jpg" loading="lazy" alt="Nachtaufnahme aus dem Van-Fenster: Vor einem dunklen Holzgebäude steht eine Person, nur als Silhouette erkennbar, im hellen Lichtkegel einer Taschenlampe."></a>'
               '<figcaption class="cap">Letzter Abend am Kiefernsee 🥲 So still hier nach der Versammlung. #vanlife #camping #seeblick</figcaption></figure>'
               '<figure class="frame"><div class="bar"></div><div class="top"><span><b>nova.on.wheels</b> · 01:28</span><span>🐶</span></div>'
               '<a href="bilder/nova-0128.jpg" target="_blank" rel="noopener"><img src="bilder/nova-0128.jpg" loading="lazy" alt="Nachtaufnahme am See: Ein kleiner weiß-brauner Hund springt durchs flache Wasser, es spritzt. Rechts unten der Rand des grauen Holzstegs."></a>'
               '<figcaption class="cap">1:28 Uhr. Pepper muss natürlich noch mal vom Steg in den See springen. PLATSCH. 🙄🐶 Sorry an alle Nachbarn!!</figcaption></figure>'
               '</div><p class="small">Schaut genau hin: Uhrzeit, Ort, Licht, was passiert. Beschreibt es Akte Rot.</p>', "blau")

S["b5"] = card("b5", "B-5 · Fotografiert am Samstag, 26.09., 8:00 Uhr", "Das Schwarze Brett an der Rezeption",
               photo("brett.jpg", "Korkpinnwand mit sechs Zetteln: Bootsverleih, Wichtig, Brötchenservice, Gefunden, Nachtruhe, Vermisst",
                     "Lichtbild: Spurensicherung Seebrück. Tippt auf das Foto, um es groß zu sehen.")
               + "".join(f'<details class="voice"><summary>{E(h)}</summary><p>{E(b).replace(chr(10), "<br>")}</p></details>' for _, h, b, _a in B.NOTES), "blau")

# ---------- GEMEINSAM ----------
S["plan"] = card("plan", "Luftbild der Polizeidrohne, Samstag, 26.09. · Norden ist oben", "Lageplan",
                 photo("lageplan.jpg", "Beschriftetes Luftbild des Campingplatzes am Kiefernsee", "Tippt auf den Plan, um ihn groß zu sehen.")
                 + '<p class="small">Rita Schäfer wohnt auf Parzelle 3, gleich oberhalb vom Steg. Nova Sommer steht mit ihrem Van auf G2. '
                   'Die Wetterstation hängt an der Gaststätte Seeklause.</p>', "alle")
cast = "".join(f'<li><b>{E(n)}</b> <span class="small">{a} Jahre</span><p>{E(d)}</p></li>' for n, a, d in B.CAST)
S["cast"] = card("cast", "Personenregister zum Fall", "Wer ist wer am Kiefernsee?", f'<ul class="cast">{cast}</ul>', "alle")

ROT_NAV = [("r1", "R-1", "Bericht zum Leichenfund"), ("r2", "R-2", "Asservatenverzeichnis"), ("r3", "R-3", "Rundgangsprotokoll"),
           ("r4", "R-4", "Vernehmung Rita Schäfer"), ("r5", "R-5", "Wetterdaten und Notruf")]
BLAU_NAV = [("b1", "B-1", "Protokoll der Versammlung"), ("b2", "B-2", "Chat der Dauercamper"), ("b3", "B-3", "Sprachnachricht"),
            ("b4", "B-4", "Novas Story"), ("b5", "B-5", "Schwarzes Brett")]
ALL_NAV = [("plan", "Lageplan", "Luftbild"), ("cast", "Personen", "Wer ist wer"), ("code", "Code-Prüfung", "Akt 1 abschließen"),
           ("hints", "Hinweise", "Hilfe in drei Stufen")]


def nav(items, kind):
    return "".join(f'<button data-view="{i}" class="{kind}"><b>{E(a)}</b><span class="small">{E(b)}</span></button>' for i, a, b in items)


CSS = r"""
:root{--bg:#e6e9ea;--paper:#fbfbf8;--ink:#1d2428;--muted:#5c676d;--line:#c5cccf;--stamp:#a8322a;--blue:#2c5d8a;--red:#a8322a;--night:#13202b;--ok:#2f6b3a;
--f-display:"Archivo Narrow","Arial Narrow",Arial,sans-serif;--f-body:"IBM Plex Sans",system-ui,sans-serif;--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141a1e;--paper:#1e262b;--ink:#e4e8e9;--muted:#9aa6ac;--line:#34404a;--stamp:#e0675d;--blue:#7fb0dc;--red:#e0675d;--night:#0b131a;--ok:#79c088;color-scheme:dark}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.55;padding-block:24px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:680px;margin:0 auto;display:flex;flex-direction:column;gap:20px}
header{border-bottom:2px solid var(--ink);padding-bottom:12px;display:flex;flex-direction:column;gap:2px}
.az{font-family:var(--f-mono);font-size:12px;color:var(--muted);letter-spacing:.04em}
h1{font-family:var(--f-display);font-weight:700;font-size:30px;line-height:1.1;margin:0}
h2{font-family:var(--f-display);font-weight:700;font-size:22px;margin:0}
.lab{font-family:var(--f-display);font-size:12px;letter-spacing:.06em;color:var(--muted);display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.card{background:var(--paper);border:1px solid var(--line);border-radius:4px;padding:20px;display:flex;flex-direction:column;gap:12px;min-width:0}
.card.rot{border-left:6px solid var(--red)} .card.blau{border-left:6px solid var(--blue)}
.card p{margin:0}
.stamp{align-self:flex-start;font-family:var(--f-display);font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--stamp);border:2px solid var(--stamp);padding:2px 10px;transform:rotate(-2deg);font-size:13px}
.tag{display:inline-block;font-family:var(--f-display);font-weight:700;font-size:12px;letter-spacing:.1em;padding:1px 8px;border-radius:2px;color:#fff}
.tag.blau{background:var(--blue)} .tag.rot{background:var(--red)} .tag.alle{background:var(--muted)}
label{font-weight:600;font-size:14px}
input,select,button{font:inherit}
input[type=text],select{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:3px;background:var(--bg);color:var(--ink)}
button{cursor:pointer;border:0;border-radius:3px;padding:10px 16px;background:var(--ink);color:var(--paper);font-family:var(--f-display);font-weight:700;letter-spacing:.06em;font-size:15px}
button.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.roles{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.roles button{padding:28px 12px;font-size:22px;color:#fff;display:flex;flex-direction:column;gap:4px;align-items:center}
.roles button span{font-family:var(--f-body);font-weight:400;font-size:13px;letter-spacing:0;opacity:.9}
.roles .rot{background:var(--red)} .roles .blau{background:var(--blue)}
.badge{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 14px;border-radius:4px;color:#fff;font-family:var(--f-display);font-weight:700;letter-spacing:.1em;font-size:18px}
.badge.rot{background:var(--red)} .badge.blau{background:var(--blue)}
.badge button{background:rgba(255,255,255,.18);color:#fff;font-size:13px;padding:6px 10px}
.menu{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.menu button{text-align:left;background:var(--paper);color:var(--ink);border:1px solid var(--line);padding:12px 14px;display:flex;flex-direction:column;gap:2px;font-family:var(--f-body);letter-spacing:0;font-weight:400}
.menu button b{font-family:var(--f-display);font-size:18px}
.menu button.rot{border-left:5px solid var(--red)} .menu button.blau{border-left:5px solid var(--blue)}
.menu button[aria-current="true"]{outline:2px solid var(--ink)}
.navlab{font-family:var(--f-display);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.msg{font-family:var(--f-mono);font-size:14px;padding:10px 12px;border-left:4px solid var(--muted);background:var(--bg)}
.msg.ok{border-color:var(--ok)} .msg.bad{border-color:var(--red)}
dl.form{display:grid;grid-template-columns:minmax(110px,30%) 1fr;margin:0;border-top:1px solid var(--line)}
dl.form dt{font-family:var(--f-display);font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.05em;padding:8px 8px 8px 0;border-bottom:1px solid var(--line);color:var(--muted)}
dl.form dd{margin:0;padding:8px 0;border-bottom:1px solid var(--line);font-size:15px}
dl.form dd p+p{margin-top:6px}
@media (max-width:480px){dl.form{grid-template-columns:1fr} dl.form dt{border-bottom:0;padding-bottom:0} }
.photo{margin:0;display:flex;flex-direction:column;gap:6px}
.photo img,.frame img{display:block;width:100%;height:auto;border-radius:3px}
.photo figcaption{font-size:12px;color:var(--muted)}
ol.assv{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px}
ol.assv li{display:flex;flex-direction:column;border-bottom:1px solid var(--line);padding-bottom:8px;font-size:15px}
ol.assv span{color:var(--muted);font-size:14px}
ol.log{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;font-family:Georgia,serif;font-style:italic;color:#1a3a8c;background:#fffbe0;padding:14px;border-radius:3px}
@media (prefers-color-scheme:dark){ol.log{background:#2b2a1c;color:#b9c9ff}}
ol.log li{display:grid;grid-template-columns:52px 1fr;gap:8px}
ol.log b{font-style:normal}
.sig{font-family:Georgia,serif;font-style:italic;font-weight:700;font-size:20px;color:#1a3a8c}
.qa{display:flex;flex-direction:column;gap:8px;font-size:14px}
.qa .f{font-weight:600}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:4px 8px;border-bottom:1px solid var(--line)}
.voice{display:flex;flex-direction:column;gap:10px;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
details.voice summary{cursor:pointer;font-weight:600}
audio{width:100%}
.chat{background:#ece5d8;border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:6px}
@media (prefers-color-scheme:dark){.chat{background:#2a2620}}
.chat .day{text-align:center;font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.06em;margin:6px 0}
.bub{background:#fff;color:#1d2428;border-radius:8px;padding:6px 10px;max-width:86%;font-size:14px;position:relative}
.bub.own{background:#d9f5c6;align-self:flex-end}
.bub b{font-size:12px} .bub .t{float:right;font-size:11px;color:#6b7378;margin-left:10px}
.story{display:grid;grid-template-columns:1fr;gap:14px}
.frame{background:var(--night);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;color:#eef2f4;margin:0}
.frame .top{display:flex;justify-content:space-between;align-items:center;padding:10px 12px;font-size:13px}
.bar{height:3px;background:rgba(255,255,255,.35);margin:8px 12px 0;border-radius:2px}
.frame img{border-radius:0}
.cap{padding:10px 12px 14px;font-size:14px}
ul.cast{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}
ul.cast li{border-bottom:1px solid var(--line);padding-bottom:8px}
.q{display:flex;flex-direction:column;gap:6px}
.hints{display:flex;flex-direction:column;gap:10px}
.hrow{display:flex;flex-wrap:wrap;gap:8px}
.small{font-size:13px;color:var(--muted)}
.mono{font-family:var(--f-mono);font-variant-numeric:tabular-nums}
.confirm{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:4px;padding:12px}
footer{font-size:12px;color:var(--muted);text-align:center}
"""

CODE = '''<section id="v-code" class="card alle" hidden>
<span class="lab"><span class="tag alle">FÜR BEIDE</span> Akt 1 · Was ist passiert?</span><h2>Code-Prüfung</h2>
<form id="codeForm" style="display:flex;flex-direction:column;gap:14px">
<div class="q"><label for="q1">Frage 1: Wo ist Holger Brandner ins Wasser gekommen?</label>
<select id="q1"><option value="">bitte wählen</option><option value="1">1 · am Badestrand</option><option value="2">2 · am Bootssteg</option><option value="3">3 · mitten auf dem See, aus dem Tretboot</option></select></div>
<div class="q"><label for="q2">Frage 2: In welchem Zeitraum ist es passiert?</label>
<select id="q2"><option value="">bitte wählen</option><option value="1">1 · zwischen 21:30 und 23:00 Uhr</option><option value="2">2 · zwischen 23:30 und 0:30 Uhr</option><option value="3">3 · zwischen 0:30 und 2:00 Uhr</option><option value="4">4 · nach 2:00 Uhr</option></select></div>
<div class="q"><label for="q3">Frage 3: Welcher Gegenstand des Opfers fehlt?</label>
<select id="q3"><option value="">bitte wählen</option><option value="1">1 · sein Handy</option><option value="2">2 · seine Brieftasche</option><option value="3">3 · seine rote Ledermappe</option><option value="4">4 · sein Autoschlüssel</option></select></div>
<button type="submit">Antwort prüfen</button><div id="codeMsg" class="msg" hidden></div></form>
<p class="small">Lieber auf Papier? Im Buch auf Seite 19 steht, wie ihr die Abschnittsnummer selbst berechnet.</p></section>
<section id="v-hints" class="card alle" hidden>
<span class="lab"><span class="tag alle">FÜR BEIDE</span> Akt 1 · Hinweise</span><h2>Hilfe in drei Stufen</h2>
<p class="small">Stufe 1 gibt einen Schubs, Stufe 2 die Richtung, Stufe 3 die Antwort. Jede geöffnete Stufe kostet euer Team einen Punkt.</p>
<div class="hints" id="hintBox"></div></section>'''

JS = r'''<script>
(function(){
  var KEY="kiefernsee-fall1", RKEY="kiefernsee-rolle";
  var $=function(id){return document.getElementById(id)};
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{v===null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){}}
  function norm(s){return (s||"").toUpperCase().replace(/[^A-ZÄÖÜ]/g,"")}
  function sum(s){var h=7;for(var i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))%1000003}return h}
  var PW=sum("TRETBOOT");
  var VIEWS=Array.prototype.map.call(document.querySelectorAll("section[id^='v-']"),function(s){return s.id.slice(2)});
  function show(v,quiet){
    VIEWS.forEach(function(n){ $("v-"+n).hidden=(n!==v) });
    document.querySelectorAll("[data-view]").forEach(function(b){ b.setAttribute("aria-current", b.getAttribute("data-view")===v ? "true":"false") });
    if(!quiet){ $("v-"+v).scrollIntoView({behavior:"smooth",block:"start"}) }
  }
  function setRole(r){
    set(RKEY,r); $("role").hidden=true; $("app").hidden=false; $("confirm").hidden=true;
    var b=$("badge"); b.className="badge "+r; $("badgeTxt").textContent= r==="rot" ? "◆ AKTE ROT" : "● AKTE BLAU";
    $("navRot").hidden = r!=="rot"; $("navBlau").hidden = r!=="blau";
    show(r==="rot"?"r1":"b1",true);
  }
  function wanted(){ var h=(location.hash||"").slice(1); return VIEWS.indexOf(h)>=0 ? h : null }
  function afterLogin(){
    $("login").hidden=true; var w=wanted(), r=get(RKEY);
    if(w && /^r\d/.test(w)){ r="rot" } else if(w && /^b\d/.test(w)){ r="blau" }
    if(r==="rot"||r==="blau"){ setRole(r); if(w){ show(w,true); setTimeout(function(){ $("v-"+w).scrollIntoView({block:"start"}) },150) } } else { $("role").hidden=false }
  }
  window.addEventListener("hashchange",function(){ if($("app").hidden) return; var w=wanted(); if(!w) return;
    if(/^r\d/.test(w)&&get(RKEY)!=="rot") setRole("rot"); if(/^b\d/.test(w)&&get(RKEY)!=="blau") setRole("blau"); show(w) });
  if(get(KEY)==="1"){ afterLogin() }
  $("loginForm").addEventListener("submit",function(e){
    e.preventDefault();
    if(sum(norm($("pw").value))===PW){ set(KEY,"1"); afterLogin() }
    else { var m=$("loginMsg"); m.hidden=false; m.textContent="Das Kennwort stimmt nicht. Es steht im Brief der Kommissarin auf der letzten Zeile." }
  });
  document.querySelectorAll("[data-role]").forEach(function(b){ b.addEventListener("click",function(){ setRole(b.getAttribute("data-role")) }) });
  $("switch").addEventListener("click",function(){ $("confirm").hidden=false });
  $("noSwitch").addEventListener("click",function(){ $("confirm").hidden=true });
  $("yesSwitch").addEventListener("click",function(){ set(RKEY,null); $("app").hidden=true; $("role").hidden=false; $("confirm").hidden=true; window.scrollTo(0,0) });
  document.querySelectorAll("[data-view]").forEach(function(b){ b.addEventListener("click",function(){ show(b.getAttribute("data-view")) }) });

  var RIGHT=[2,2,3];
  var WRONG=["Frage 1 passt noch nicht. Woher stammen die Splitter in der Wunde?",
             "Frage 1 stimmt. Frage 2 passt noch nicht. Hat das Platschen um 1:30 Uhr wirklich mit der Tat zu tun?",
             "Frage 1 und 2 stimmen. Frage 3 passt noch nicht. Was hatte Brandner bei der Versammlung in der Hand?"];
  $("codeForm").addEventListener("submit",function(e){
    e.preventDefault();
    var a=[+$("q1").value,+$("q2").value,+$("q3").value], m=$("codeMsg"); m.hidden=false;
    if(!a[0]||!a[1]||!a[2]){ m.className="msg bad"; m.textContent="Bitte alle drei Fragen beantworten."; return }
    var code=(a[0]-1)*16+(a[1]-1)*4+a[2];
    for(var i=0;i<3;i++){ if(a[i]!==RIGHT[i]){ m.className="msg bad"; m.textContent="Abschnitt "+code+": Hauptkommissarin Wendland schüttelt den Kopf. "+WRONG[i]; return } }
    m.className="msg ok"; m.textContent="Abschnitt "+code+": Richtig! Brandner wurde zwischen 23:30 und 0:30 Uhr am Bootssteg niedergeschlagen. Die rote Mappe ist verschwunden. Lest jetzt die Auflösung von Akt 1 im Buch (Seite 22).";
  });
  var H=[
    ["Frage 1 · Der Ort","Schaut genau, was in der Kopfwunde gefunden wurde. Wo auf dem Platz gibt es genau dieses Material?","Das Tretboot ist aus Kunststoff. Akte Blau weiß, welches Holz in dieser Woche grau gestrichen wurde.","Antwort 2: der Bootssteg. Die grau lasierten Lärchensplitter stammen vom frisch gestrichenen Steg."],
    ["Frage 2 · Die Zeit","Wer hat den Steg in der Nacht gesehen? Und wann fehlte das Boot zum ersten Mal?","Brandner hat um 23:41 Uhr noch eine Sprachnachricht geschickt. Das Platschen um 1:30 Uhr hat eine harmlose Erklärung in Novas Story.","Antwort 2: zwischen 23:30 und 0:30 Uhr. Um 23:41 lebte er noch, um 0:30 war das Boot weg."],
    ["Frage 3 · Der Gegenstand","Vergleicht, was Brandner am Abend bei sich hatte, mit dem, was die Polizei gefunden hat.","Das Versammlungsprotokoll nennt einen Gegenstand, der auf der Fundliste fehlt.","Antwort 3: die rote Ledermappe mit dem Vorvertrag."]];
  var box=$("hintBox");
  H.forEach(function(h,qi){
    var d=document.createElement("div"); d.className="card"; d.style.padding="14px";
    var t=document.createElement("b"); t.textContent=h[0]; d.appendChild(t);
    var row=document.createElement("div"); row.className="hrow"; d.appendChild(row);
    var out=document.createElement("div"); out.className="hints"; d.appendChild(out);
    [1,2,3].forEach(function(s){
      var b=document.createElement("button"); b.type="button"; b.className="ghost"; b.textContent="Stufe "+s;
      b.addEventListener("click",function(){ if(b.disabled) return; b.disabled=true; b.style.opacity=".5";
        var p=document.createElement("div"); p.className="msg"; p.textContent="Stufe "+s+": "+h[s]; out.appendChild(p) });
      row.appendChild(b);
    });
    box.appendChild(d);
  });
})();
</script>'''

page = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>[hidden]{{display:none!important}} body{{margin:0}}</style>
<title>Ermittlerportal Kiefernsee</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;700&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header><span class="az">KRIPO SEEBRÜCK · AZ 31 JS 0926/BR · FALL KIEFERNSEE</span><h1>Ermittlerportal</h1>
<span class="small">Zugang nur für das Ermittlerteam. Bitte den Link nicht weitergeben.</span></header>

<section id="login" class="card"><span class="stamp">Vertraulich</span><h2>Kennwort eingeben</h2>
<p>Das Kennwort steht im Brief von Hauptkommissarin Wendland, ganz unten.</p>
<form id="loginForm" style="display:flex;flex-direction:column;gap:10px"><label for="pw">Kennwort</label>
<input id="pw" type="text" autocomplete="off" autocapitalize="characters" placeholder="z. B. GRILLZANGE">
<button type="submit">Akte öffnen</button><div id="loginMsg" class="msg bad" hidden></div></form></section>

<section id="role" class="card" hidden><h2>Welche Akte habt ihr?</h2>
<p>Jeder wählt auf seinem eigenen Handy seine Farbe. Ihr seht dann nur eure eigene Akte – und die gemeinsamen Seiten.</p>
<div class="roles"><button class="rot" data-role="rot">◆ AKTE ROT<span>Spurensicherung, Protokolle der Polizei</span></button>
<button class="blau" data-role="blau">● AKTE BLAU<span>Chats, Handy, Social Media</span></button></div>
<p class="small">Spielt einer mit dem Buch? Dann wählt der andere hier die Farbe, die im Buch frei bleibt.</p>
<p class="msg"><b>Das Buch bleibt eure Hauptakte.</b> Den Ermittlerbogen für euren geheimen Verdacht, die Punkte fürs Duell und die Auflösung gibt es nur im Buch. Legt es beim Spielen immer mit auf den Tisch.</p></section>

<div id="app" hidden style="display:flex;flex-direction:column;gap:16px">
<div id="badge" class="badge rot"><span id="badgeTxt">◆ AKTE ROT</span><button id="switch" type="button">Akte wechseln</button></div>
<div id="confirm" class="confirm" hidden><span>Wirklich die Akte wechseln? Dann seht ihr die Seiten der anderen Farbe.</span>
<button id="yesSwitch" type="button">Ja, wechseln</button><button id="noSwitch" type="button" class="ghost">Abbrechen</button></div>
<div id="navRot"><div class="navlab">Eure Akte</div><nav class="menu" aria-label="Akte Rot">{nav(ROT_NAV, "rot")}</nav></div>
<div id="navBlau" hidden><div class="navlab">Eure Akte</div><nav class="menu" aria-label="Akte Blau">{nav(BLAU_NAV, "blau")}</nav></div>
<p class="small" style="margin:0">📖 Ermittlerbogen, Punkte und Auflösung findet ihr im Buch.</p>
<div><div class="navlab">Für beide</div><nav class="menu" aria-label="Gemeinsam">{nav(ALL_NAV, "alle")}</nav></div>
{"".join(S[k] for k in ["r1","r2","r3","r4","r5","b1","b2","b3","b4","b5","plan","cast"])}
{CODE}
</div>
<footer>Ein Spiel zum Buch „Ausverkauf am Kiefernsee“ von Natthaphon Lind. Alle Personen, Orte und Behörden sind frei erfunden.</footer>
</div>
{JS}
</body>
</html>
'''
open(OUT, "w", encoding="utf-8").write(page)
print("index.html", len(page))

"""Akt 2 „Wer lügt?“ – alle Inhalte an einer Stelle (Buch und Web-App lesen von hier).

WAHRHEIT (nur für uns, nicht im Spiel):
- Täterin ist Angelika Wohlfahrt (P7). Ihr verstorbener Mann Herbert war bis 1995 Tankwart der alten Bootstankstelle.
  Sie weiß von den im Schilf versenkten Ölfässern.
- ca. 22:30 Zettel unter Brandners Tür (Block der IG Dauercamper, Kopf abgerissen).
- 23:09 holt sie mit dem Code 1996 (Platzleitung/Hausmeister; sie hat ihn Marco abgeschaut) den Bootsschlüssel
  aus dem Schlüsselkasten im Flur der Rezeption (Zugang über ihren Vereinsraum-Schlüssel). Novas Foto 23:12.
- 23:30 Sven am Steg: Boote angekettet. 23:47 Angelika im Chat: „Hubert suchen“. Kurz vor 0 Uhr Siggi hört Clogs.
- ca. 23:55–0:05 Streit am Steg, Stoß, Kopf auf Stegkante, Wasser. Sie nimmt die Mappe, macht das Boot los.
- 0:03 gelöschte Nachricht in der Gruppe (Akt 3 wird sie lesbar).
- Marco war von 23:02 bis ca. 1:40 bei Nova im Van (lügt aus Angst um den Job). Böttcher saß bis 0:45 in der Seeklause.
AKT-2-ANTWORTEN (alle wahr): Schloss mit Bootsschlüssel aus dem Schlüsselkasten · Altlasten: alte Ölfässer im Schilf ·
Gelogen hat Marco Lenz.
"""

TITLE = "Wer lügt?"
DATE_LINE = "Sonntag, 27. September"

LAGEBERICHT = (
    "Liebe Kollegin, lieber Kollege,\n"
    "gute Arbeit gestern. Wir wissen jetzt: Holger Brandner wurde zwischen 23:30 und 0:30 Uhr am Bootssteg "
    "niedergeschlagen, und seine rote Mappe mit dem Vorvertrag ist verschwunden. Ein Unfall war das nicht.\n"
    "Seit gestern Nachmittag haben wir vernommen, durchsucht und getaucht. Ich habe euch alles kopiert. "
    "Drei Dinge lassen mich nicht los: Wie ist das Kettenschloss aufgegangen, ohne aufgebrochen zu werden? "
    "Was wollte jemand Brandner nachts zeigen, das „den Preis ordentlich drückt“? Und: Mindestens eine Person "
    "auf diesem Platz hat mich gestern angelogen.\n"
    "Neu für euch: Einige Akten sind versiegelt. Ihr öffnet sie in der Web-App, sobald ihr das passende Rätsel "
    "gelöst habt – oft braucht ihr dafür eine Spur aus der Akte des anderen.\n"
    "Viel Erfolg. Ich verlasse mich auf euch.")

Q = [("Frage 1", "Womit wurde das Kettenschloss am Steg geöffnet?",
      ["mit einem Bolzenschneider aufgebrochen", "mit dem Bootsschlüssel aus dem Schlüsselkasten der Rezeption",
       "gar nicht – es war nie abgeschlossen", "mit einem Schlüssel, den Brandner bei sich trug"]),
     ("Frage 2", "Was wollte jemand Brandner zeigen, das „den Preis drückt“?",
      ["Baumängel an den Mietchalets", "alte Ölfässer, die im Schilf versenkt wurden",
       "ein höheres Kaufangebot einer anderen Firma", "seltene Vögel, die im Schilf brüten"]),
     ("Frage 3", "Wer hat bei seiner Vernehmung gelogen?",
      ["Mark Böttcher", "Marco Lenz", "Sven Ruppert", "Siggi Kowalski"])]
RIGHT = (2, 2, 2)
WRONG = ["Frage 1 passt noch nicht. Das Schloss war nicht beschädigt, und um 23:30 Uhr war es noch zu. "
         "Wer kam an einen Schlüssel – und wann?",
         "Frage 1 stimmt. Frage 2 passt noch nicht. Was steht im alten Gutachten aus dem Archiv – und was haben die Taucher gefunden?",
         "Frage 1 und 2 stimmen. Frage 3 passt noch nicht. Vergleicht, was jemand der Polizei gesagt hat, "
         "mit dem, was er selbst geschrieben hat."]
RIGHT_MSG = ("Richtig! Jemand hat um 23:09 Uhr mit dem Code den Bootsschlüssel aus dem Schlüsselkasten geholt. "
             "Im Schilf liegen alte Ölfässer – das hätte den Preis gedrückt. Und Marco Lenz hat gelogen: Er war nicht im Bett. "
             "Lest jetzt die Auflösung von Akt 2 im Buch.")
HINTS = [
    ("Frage 1 · Das Schloss",
     "Um 23:30 Uhr waren beide Boote noch angekettet (R-3). Das Schloss wurde nicht beschädigt (R-2). Wo werden die Bootsschlüssel aufbewahrt?",
     "Öffnet in der Web-App das Protokoll des Schlüsselkastens (R-8). Den Code ergibt die UV-Lampe zusammen mit der Chronik in Akte Blau (B-10).",
     "Antwort 2: mit dem Bootsschlüssel aus dem Schlüsselkasten. Um 23:09 Uhr wurde Fach 3 mit dem Code geöffnet, der Schlüssel fehlt seitdem."),
    ("Frage 2 · Der Preis",
     "Akte Blau hat ein altes Gutachten aus dem Archiv der Rezeption (B-6). Was steht darin über den Uferbereich?",
     "Die Karte von 1996 (B-7) zeigt, wo das Fasslager war. Akte Rot öffnet damit den Taucherbericht (R-10).",
     "Antwort 2: alte Ölfässer im Schilf. Die Taucher haben sie gefunden – eine Sanierung hätte den Preis stark gedrückt."),
    ("Frage 3 · Die Lüge",
     "Lest die Vernehmungen genau: Wer sagt, wo er um Mitternacht war? Und was schreibt dieselbe Person selbst?",
     "Akte Blau hat Direktnachrichten von Nova Sommer (B-9). Wer schreibt ihr da um 23:02 Uhr?",
     "Antwort 2: Marco Lenz. Er sagt, er war ab 22 Uhr allein im Bett – aber um 23:02 Uhr schreibt er Nova: „Bin da.“"),
]

# ---------------- AKTE ROT ----------------
MARCO_HEAD = "Sonntag, 27.09., 9:10 Uhr, Rezeption. Vernehmung durch EKHK'in Wendland. Personalien: Marco Lenz, 45, Hausmeister, 1,94 m, Schuhgröße 46"
MARCO = [
    ("F", "Herr Lenz, Sie haben am Freitag die Versammlung verlassen. Warum?"),
    ("A", "Ich brauchte eine Zigarette. Der Brandner hat gesagt, er bringt sein eigenes Team mit. Da war für mich klar: "
          "Ich bin raus. Nach zehn Minuten war ich wieder drin."),
    ("F", "Wo waren Sie nach der Versammlung?"),
    ("A", "Zu Hause. Ab zehn lag ich im Bett. Allein. Ich hab nichts gehört und nichts gesehen."),
    ("F", "Wer kann den Schlüsselkasten in der Rezeption öffnen?"),
    ("A", "Der Chef und ich. Es gibt einen Code. Das Jahr, in dem der Chef den Platz übernommen hat – das kann er sich merken."),
    ("F", "Und die Bootsschlüssel?"),
    ("A", "Hängen in Fach 3. Beide an einem Ring, Kevin und Chantal. Das Schloss am Steg hab ich Freitagabend um "
          "sieben selbst zugemacht, das schwör ich."),
    ("F", "Sie haben den Steg am Donnerstag gestrichen?"),
    ("A", "Ja. Grau, Lärche. Hab vorne am Stegende angefangen und mich rückwärts zum Ufer gearbeitet. Freitagnacht war der noch "
          "nicht ganz trocken."),
    ("F", "Herr Brandner wollte Sie nicht übernehmen. Das muss Sie wütend gemacht haben."),
    ("A", "Wütend? Klar. Aber ich bring doch keinen um. Ich hab drei Kinder, Frau Kommissarin."),
]
MARCO_AUDIO = ("Ausschnitt aus der Tonaufnahme der Vernehmung · 0:29")

BOETTCHER_HEAD = "Sonntag, 27.09., 10:30 Uhr, Wohnhaus Böttcher. Vernehmung durch KK Brüggemann"
BOETTCHER = [
    ("F", "Herr Böttcher, wo waren Sie in der Nacht von Freitag auf Samstag?"),
    ("A", "Nach der Versammlung bin ich in der Seeklause sitzen geblieben, mit dem Wirt. Ein, zwei Bier. "
          "So gegen Viertel vor eins war ich im Bett."),
    ("F", "Sie wollten den Platz verkaufen. Warum?"),
    ("A", "Ich bin 61. Ich mäh hier seit 30 Jahren Rasen. Irgendwann ist Schluss."),
    ("F", "Gibt es finanzielle Gründe?"),
    ("A", "Das geht Sie nichts an. … Na gut. Es war knapp. Ist das verboten?"),
    ("F", "Im Archiv Ihrer Rezeption liegt ein Bodengutachten von 1996. Kennen Sie das?"),
    ("A", "Ein Gutachten? Das muss noch mein Vater bestellt haben, kurz bevor ich übernommen hab. Seine Kartons hab ich nie aufgemacht. "
          "Ehrlich, davon weiß ich nichts."),
    ("F", "Wer kennt den Code für den Schlüsselkasten?"),
    ("A", "Marco und ich. Sonst niemand. Glaub ich jedenfalls."),
    ("F", "Wie erreichen wir Sie, falls wir noch Fragen haben?"),
    ("A", "Hier, meine Karte. Das Handy hat Ihr Kollege ja schon. Auf die Mailbox komm ich trotzdem drauf, wenn ich die Nummer wähle."),
]
VISITENKARTE = ("Mark Böttcher", "Campingplatz am Kiefernsee · Inhaber", "Seeweg 1 · 17259 Seebrück", "Mobil 0171 638 42 15")
MAILBOX_NUMBER = "01716384215"

KASTEN_INTRO = ("Im Flur der Rezeption hängt ein Schlüsselkasten mit Zahlenschloss. Der Flur ist nachts abgeschlossen. "
                "Schlüssel dafür haben laut Liste: Platzleitung, Hausmeister und der Vereinsraum der Dauercamper.\n"
                "Der Kasten speichert jede Öffnung – aber das Protokoll lässt sich nur mit dem richtigen Code auslesen.")
KASTEN_FUND = [
    ("Fach 1", "Generalschlüssel Sanitär – vorhanden"),
    ("Fach 2", "Schranke, Ersatz – vorhanden"),
    ("Fach 3", "Bootsschlüssel „Kevin“ + „Chantal“ (an einem Ring) – FEHLT"),
    ("Fach 4", "Chalets 1–4, Ersatz – vorhanden"),
]
KASTEN_CODE = "1996"
KASTEN_LOG = [
    ("Fr 25.09.", "07:12", "Code Platzleitung/Hausmeister", "Fach 1 geöffnet"),
    ("Fr 25.09.", "18:55", "Code Platzleitung/Hausmeister", "Fach 3 geöffnet"),
    ("Fr 25.09.", "19:02", "Code Platzleitung/Hausmeister", "Fach 3 geöffnet"),
    ("Fr 25.09.", "23:09", "Code Platzleitung/Hausmeister", "Fach 3 geöffnet"),
    ("Sa 26.09.", "08:47", "Code Platzleitung/Hausmeister", "Fach 3 geöffnet (Polizei, Kontrolle: leer)"),
]
KASTEN_LOG_NOTE = ("18:55/19:02: Hausmeister Lenz holt den Schlüssel und hängt ihn nach dem Abschließen zurück (bestätigt). "
                   "23:09: unbekannt. Es gibt nur einen Code für Platzleitung und Hausmeister.")

ZETTEL_INTRO = ("Gefunden am Samstag, 26.09., im Papierkorb von Mietchalet 3, zerknüllt. Kariertes Papier, "
                "oben abgerissen. Am Rand ist noch der Rest eines grünen Aufdrucks zu sehen.")
ZETTEL = ["HERR BRANDNER,", "HEUTE 23:45 AM STEG.", "ICH ZEIGE IHNEN, WAS", "IHR GUTACHTER NICHT WEISS.", "KOMMEN SIE ALLEIN."]
ZETTEL_REST = "…meinschaft"
ZETTEL_KT = ("Kriminaltechnik: Blockschrift, vermutlich verstellt. Kugelschreiber, blau. Fingerabdrücke: nur vom Opfer. "
             "Der Aufdruck-Rest ist grün und stammt von einem vorgedruckten Briefblock.")

TAUCHER_INTRO = ("Die Taucher der Feuerwehr haben am Samstag den Fundort im Schilf abgesucht. Ihr Bericht ist versiegelt. "
                 "Ihr öffnet ihn in der Web-App, indem ihr auf dem Luftbild zeigt, wo früher das Fasslager war. "
                 "Wo das war, weiß Akte Blau.")
TAUCHER = [
    ("Einsatz", "Samstag, 26.09., 13:00–15:30 Uhr, Feuerwehr Seebrück, Tauchgruppe"),
    ("Suchgebiet", "Schilfgürtel am Nordostufer, Fundort und Umgebung, Wassertiefe 0,4 bis 1,8 m"),
    ("Befund", "Im Schlamm unter dem Schilf: 12 Stahlfässer à 200 Liter, stark verrostet, teils undicht. Ölfilm beim "
               "Bewegen. Aufschrift teils lesbar: „Altöl“, „Bootsbenzin“. Liegezeit geschätzt: mehr als 25 Jahre."),
    ("Weitere Funde", "Keine. Keine Tasche, keine Mappe, keine Papiere."),
    ("Bewertung", "Altlast. Die Fässer müssen geborgen und der Boden saniert werden. Untere Wasserbehörde informiert."),
]
TAUCHER_PHOTO_CAP = "Lichtbild 3: Fass Nr. 4 im Schilf, Sa 26.09., 14:10 Uhr"

STEG_INTRO = ("Weil die Lasur am Freitagabend noch nicht ganz trocken war (R-6), sind auf dem Steg Abdrücke geblieben. "
              "Die Spurensicherung hat sie am Samstagmorgen gesichert.")
STEG_SPUREN = [
    ("Spur A", "Sicherheitsschuhe, Gr. 45, zweimal hin und zurück – Sven Ruppert (Kontrollgänge 23:30 und 0:30, abgeglichen)"),
    ("Spur B", "Lederslipper, Gr. 44, nur hin bis zum Stegende – das Opfer"),
    ("Spur C", "Gr. 37/38, grobes Profil mit runden Noppen (vermutlich Gartenclogs), hin bis zum Stegende und zurück – unbekannt"),
    ("Spur D", "Hundepfoten, klein, vom Ufer bis zum Stegende – vermutlich Pepper (Novas Story, 1:28)"),
]
SIGGI_HEAD = "Samstag, 26.09., 16:20 Uhr, Parzelle 14. Befragung durch KK Brüggemann"
SIGGI = [
    ("F", "Herr Kowalski, wann haben Sie Freitagnacht die Musik ausgemacht?"),
    ("A", "Kurz vor zwölf. Wegen dem Sicherheitsmenschen. Ich hab dann noch kurz vor der Tür eine geraucht."),
    ("F", "Ist Ihnen dabei etwas aufgefallen?"),
    ("A", "Da ist einer runter Richtung Steg. Mit Taschenlampe. Klein war der. Und es hat geklappert, so wie Holzschuhe "
          "auf dem Weg. Ich dachte, einer muss noch aufs Klo."),
    ("F", "Erkannt haben Sie die Person nicht?"),
    ("A", "Nee. Brille lag drinnen. Ich seh ja ohne nix."),
]

# ---------------- AKTE BLAU ----------------
GUTACHTEN_HEAD = ("Gefunden am Samstag im Archiv der Rezeption, Karton „Vater, 1990–1999“, mit Klebeband verschlossen, "
                  "dick verstaubt.")
GUTACHTEN = [
    ("Titel", "Bodengutachten Campingplatz am Kiefernsee"),
    ("Auftraggeber", "Werner Böttcher (Eigentümer)"),
    ("Erstellt", "Ingenieurbüro Hartwig, Seebrück, 16. März 1996"),
    ("Anlass", "Schließung der Bootstankstelle am Nordostufer (Betrieb 1990–1995)"),
    ("Befund", "Laut Aussage des früheren Tankwarts, Herrn Herbert Wohlfahrt, wurden 1994/95 etwa 12 Fässer mit Altöl "
               "und Bootsbenzin „entsorgt“, indem sie im Schilf vor der Tankstelle versenkt wurden. Lage: siehe Anlage 3 (Karte)."),
    ("Empfehlung", "Bergung der Fässer und Bodensanierung. Geschätzte Kosten: 380.000 DM."),
]
GUTACHTEN_NOTE = "Randnotiz in Bleistift: „Erst mal nicht. Zu teuer. – W. B.“"

KARTE_INTRO = ("Anlage 3 zum Gutachten: Lageplan von 1996, von Hand gezeichnet. Damals sah der Platz noch anders aus – "
               "die Tankstelle wurde 2001 abgerissen. Beschreibt Akte Rot genau, wo das Fasslager lag. "
               "Akte Rot zeigt die Stelle in der Web-App auf dem heutigen Luftbild (R-10).")

MAILBOX_INTRO = ("Das Handy von Mark Böttcher hat die Polizei sichergestellt. Seine Mailbox lässt sich aber anrufen. "
                 "Die Nummer steht auf seiner Visitenkarte – die hat Akte Rot. Wählt die Nummer in der Web-App.")
MAILBOX_HEAD = "Mailbox Mark Böttcher · Nachricht vom Freitag, 25.09., 16:20 Uhr · 0:18"
MAILBOX = ("Guten Tag, Herr Böttcher, hier ist Frau Engel von der Sparkasse Seebrück. Es geht noch einmal um Ihren Kredit. "
           "Wir können die Frist nur bis zum dreißigsten September verlängern. Wenn bis dahin kein Kaufvertrag "
           "unterschrieben ist, müssen wir leider die Zwangsversteigerung einleiten. Bitte rufen Sie mich zurück. Danke.")

NOVA_INTRO = ("Frau Sommer hat uns am Samstagabend freiwillig ihre Direktnachrichten gezeigt. "
              "„Ich hab nichts zu verbergen“, sagt sie. „Er schon.“")
NOVA_DM = [
    ("FREITAG, 25. SEPTEMBER", None, None),
    ("m.lenz.repariert", "21:40", "Du warst heute die Einzige, die gelacht hat."),
    ("nova", "21:42", "Dein Gesicht bei „eigenes Team“ 😂 Tut mir echt leid für dich."),
    ("m.lenz.repariert", "22:41", "Noch wach?"),
    ("nova", "22:43", "Pepper schläft schon. Ich nicht."),
    ("m.lenz.repariert", "22:44", "Bin um 11 da. Hintertür."),
    ("nova", "22:44", "🙈 ok"),
    ("m.lenz.repariert", "23:02", "Bin da 🔧"),
    ("SAMSTAG, 26. SEPTEMBER", None, None),
    ("m.lenz.repariert", "07:15", "Bitte sag niemandem, dass ich da war. Wenn der Chef das erfährt, bin ich sofort raus."),
    ("nova", "07:16", "Versprochen."),
]

VEREIN_HEAD = "Aus dem Ordner der Schriftführerin, abgegeben am Samstag. Briefbogen der Interessengemeinschaft (grüner Kopf)."
CHRONIK = [
    ("1987", "Werner Böttcher eröffnet den Campingplatz am Kiefernsee."),
    ("1990", "Eröffnung der Bootstankstelle am Nordostufer. Tankwart: Herbert Wohlfahrt."),
    ("1995", "Die Bootstankstelle schließt."),
    ("1996", "Im Herbst übernimmt Mark Böttcher den Platz von seinem Vater."),
    ("1998", "Herbert und Angelika Wohlfahrt ziehen als Dauercamper auf Parzelle 7."),
    ("2001", "Abriss der alten Tankstelle. Dort wächst heute Schilf."),
    ("2019", "Herbert Wohlfahrt verstorben. Wir vermissen ihn."),
    ("2025", "Zwei neue Tretboote: „Kevin“ und „Chantal“."),
]
SCHLUESSEL = [
    ("Rezeption, Generalschlüssel", "M. Böttcher, M. Lenz"),
    ("Flur Rezeption / Vereinsraum", "M. Böttcher, M. Lenz, A. Wohlfahrt (für die IG)"),
    ("Schlüsselkasten (Code)", "nur Platzleitung und Hausmeister"),
]

CHAT2_INTRO = "Vollständiger Export vom Handy von Angelika Wohlfahrt, Freitagnacht bis Samstagmittag. Die Lücken im ersten Auszug (B-2) sind jetzt gefüllt."
CHAT2 = [
    ("FREITAG, 25. SEPTEMBER", None, None),
    ("Sven (Security)", "23:05", "Erinnerung: Ab 22 Uhr ist Nachtruhe. Parzelle 14, ich hör den Schlager bis zur Schranke."),
    ("Siggi P14", "23:06", "Das ist Kultur."),
    ("Angelika P7", "23:47", "Bin nochmal kurz raus, Hubert suchen 🙂 Gute Nacht zusammen!"),
    ("SAMSTAG, 26. SEPTEMBER", None, None),
    ("Angelika P7", "00:03", "🚫 Diese Nachricht wurde gelöscht."),
    ("Siggi P14", "00:04", "?"),
    ("Rita P3", "06:52", "POLIZEI IST SCHON DA. Am Schilf. Der Herr Brandner. Oh Gott."),
    ("Angelika P7", "06:58", "Was ist passiert??"),
    ("Mark (Platzbetreiber)", "07:03", "Bitte alle auf euren Parzellen bleiben. Die Polizei will mit jedem sprechen."),
    ("Angelika P7", "08:40", "Ich sag ja nichts. Aber Marco war gestern schon so komisch. Und nachts ist der doch immer unterwegs."),
    ("Siggi P14", "08:44", "Lass mal die Polizei machen, Angelika."),
    ("Angelika P7", "09:12", "Gute Nachricht wenigstens: Hubert ist wieder da!! Stand heute früh einfach in meinem Beet 😊"),
    ("Rita P3", "09:15", "Na Gott sei Dank."),
]

SOLUTION = [
    ("Frage 1: Mit dem Bootsschlüssel aus dem Schlüsselkasten.",
     "Um 23:30 Uhr waren beide Boote noch angekettet (R-3), das Schloss wurde nicht beschädigt (R-2). Der Schlüsselkasten "
     "speichert jede Öffnung: Um 23:09 Uhr wurde Fach 3 mit dem Code 1996 geöffnet (R-8, Chronik B-10). Seitdem fehlt der "
     "Schlüsselring. Novas Foto um 23:12 zeigt eine Person mit Taschenlampe genau vor der Rezeption (B-4)."),
    ("Frage 2: Alte Ölfässer im Schilf.",
     "Das Gutachten von 1996 (B-6) sagt, dass rund 12 Fässer Altöl im Schilf versenkt wurden. Die Karte (B-7) zeigt die Stelle, "
     "die Taucher haben alle 12 Fässer gefunden (R-10). Eine Sanierung hätte viel Geld gekostet – genau das meinte Brandner mit "
     "„drückt den Preis“ (B-3). Auf dem Zettel aus Chalet 3 steht es auch: „was Ihr Gutachter nicht weiß“ (R-9)."),
    ("Frage 3: Marco Lenz hat gelogen.",
     "Er sagt, er lag ab 22 Uhr allein im Bett (R-6). Aber um 23:02 Uhr schreibt er Nova: „Bin da“ (B-9). "
     "Und Böttcher? Er braucht das Geld dringend (B-8) – aber er sagt die Wahrheit: Den Karton seines Vaters hat er nie geöffnet."),
]
WENDLAND_END = (
    "„Marco Lenz hat mich angelogen. Er kennt den Code, er war nicht im Bett – und er hatte allen Grund, Brandner zu hassen. "
    "Mark Böttcher kennt den Code auch, und ohne den Verkauf ist er pleite. Aber passt das alles wirklich zusammen? "
    "Auf dem Steg gibt es Abdrücke in Größe 37/38. Wer hat den Zettel geschrieben – auf welchem Papier? "
    "Und warum löscht jemand um drei nach zwölf eine Nachricht? Morgen finden wir die Wahrheit am Steg.“")

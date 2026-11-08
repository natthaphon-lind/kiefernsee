"""Prototyp: Ausverkauf am Kiefernsee – Akt 1 (Krimispiel zu zweit). Farbversion mit Fotos."""
import math, random, os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from PIL import Image

PORTAL = "https://natthaphon-lind.github.io/kiefernsee/"
W, H = 612, 792            # 8,5 x 11 Zoll
ML, MR, MT, MB = 58, 58, 56, 56

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img") + "/"
OUT = os.path.join(BASE, "Kiefernsee_Akt1_Prototyp_Farbe.pdf")
F = "/home/claude/kiefernsee/quellen/fonts/"
for n, p in [("Sans", "Poppins-Regular.ttf"), ("SansM", "Poppins-Medium.ttf"),
             ("SansB", "Poppins-Bold.ttf"), ("Serif", "Lora-Regular.ttf"),
             ("SerifI", "Lora-Italic.ttf"), ("SerifB", "Lora-Bold.ttf"),
             ("SerifBI", "Lora-BoldItalic.ttf"),
             ("Mono", "LiberationMono-Regular.ttf"), ("MonoB", "LiberationMono-Bold.ttf"),
             ("Form", "LiberationSans-Regular.ttf"), ("FormB", "LiberationSans-Bold.ttf"),
             ("Sym", "DejaVuSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, F + p))
SYMS = set("◆●✓→✕")


class SymCanvas(canvas.Canvas):
    """Zeichnet Sonderzeichen, die Poppins/Lora nicht haben, mit DejaVu."""
    def _runs(self, s):
        runs, cur, sym = [], "", None
        for ch in s:
            isy = ch in SYMS
            if sym is None or isy == sym:
                cur += ch
            else:
                runs.append((cur, sym)); cur = ch
            sym = isy
        if cur:
            runs.append((cur, sym))
        return runs

    def _w(self, s):
        f, sz = self._fontname, self._fontsize
        return sum(pdfmetrics.stringWidth(t, "Sym" if y else f, sz) for t, y in self._runs(s))

    def drawString(self, x, y, s, *a, **k):
        if not (set(s) & SYMS):
            return super().drawString(x, y, s, *a, **k)
        f, sz = self._fontname, self._fontsize
        for t, isy in self._runs(s):
            fn = "Sym" if isy else f
            self.setFont(fn, sz * (0.9 if isy else 1)); super().drawString(x, y, t)
            x += pdfmetrics.stringWidth(t, fn, sz * (0.9 if isy else 1))
        self.setFont(f, sz)

    def drawCentredString(self, x, y, s, *a, **k):
        if not (set(s) & SYMS):
            return super().drawCentredString(x, y, s, *a, **k)
        self.drawString(x - self._w(s) / 2, y, s)

    def drawRightString(self, x, y, s, *a, **k):
        if not (set(s) & SYMS):
            return super().drawRightString(x, y, s, *a, **k)
        self.drawString(x - self._w(s), y, s)


ROT=(0.76,0.16,0.14); BLAU=(0.15,0.36,0.63); NIGHT=(0.07,0.13,0.22); LAKE=(0.60,0.78,0.89)
GRASS=(0.87,0.93,0.82); SAND=(0.96,0.89,0.70); INK=(0.10,0.20,0.55); CUR=[None]
def fc(col): c.setFillColorRGB(*col)
def sc(col): c.setStrokeColorRGB(*col)
c = SymCanvas(OUT, pagesize=(W, H))
c.setTitle("Ausverkauf am Kiefernsee – Akt 1 (Prototyp)")
c.setAuthor("Natthaphon Lind")
PAGE = [1]
FLIP = [False]


def flip():
    """Ganze Seite um 180° drehen: für die Spielerin / den Spieler gegenüber."""
    c.saveState(); c.translate(W, H); c.rotate(180); FLIP[0] = True


# ---------- Helfer ----------
def text(x, y, w, s, font="Serif", size=10.5, lead=None, gray=0, gap=None):
    """Absätze (durch \\n getrennt) umbrechen, gibt neues y zurück."""
    lead = lead or size * 1.42
    gap = lead * 0.55 if gap is None else gap
    c.setFillGray(gray)
    for para in s.strip().split("\n"):
        para = para.strip()
        if not para:
            continue
        for line in simpleSplit(para, font, size, w):
            c.setFont(font, size); c.drawString(x, y, line); y -= lead
        y -= gap
    c.setFillGray(0)
    return y


def lines_h(s, font, size, w, lead):
    return sum(len(simpleSplit(p, font, size, w)) for p in s.split("\n") if p.strip()) * lead


def footer():
    c.setFont("Sans", 8); c.setFillGray(0.45)
    c.drawCentredString(W / 2, 30, f"– {PAGE[0]} –")
    c.drawString(ML, 30, "Ausverkauf am Kiefernsee · Akt 1 · Prototyp")
    c.setFillGray(0)


def akte_tab(kind):
    """Randmarkierung zum schnellen Finden: Rot = schwarz, Blau = grau gestreift."""
    right = (PAGE[0] % 2 == 1) != FLIP[0]
    tw, th, ty = 26, 150, H - 210
    x = W - tw if right else 0
    CUR[0] = kind
    if kind == "rot":
        fc(ROT); c.rect(x, ty, tw, th, fill=1, stroke=0); col = 1
        label = "◆  AKTE ROT"
    else:
        fc(BLAU); c.rect(x, ty, tw, th, fill=1, stroke=0)
        c.setStrokeColorRGB(0.35, 0.55, 0.8); c.setLineWidth(1.4)
        for k in range(0, th + tw, 9):
            c.line(x, ty + k, x + tw, ty + k - tw) if k - tw >= 0 else None
        col = 1; label = "●  AKTE BLAU"
    c.saveState(); c.translate(x + tw / 2 + 4, ty + th / 2); c.rotate(90)
    c.setFillGray(col); c.setFont("SansB", 10); c.drawCentredString(0, 0, label); c.restoreState()
    # Kopfzeile
    c.setFont("SansB", 8); fc(ROT if kind == "rot" else BLAU)
    c.drawRightString(W - MR, H - 34, label + "  ·  nur für diese Spielerin / diesen Spieler")
    c.setFillGray(0)


def new_page():
    CUR[0] = None; footer()
    if FLIP[0]:
        c.restoreState(); FLIP[0] = False
    c.showPage(); PAGE[0] += 1


def qr(x, y, size, data, kind):
    w = QrCodeWidget(data); w.barWidth = size; w.barHeight = size; w.barBorder = 2
    c.setFillGray(1); c.rect(x - 3, y - 3, size + 6, size + 6, fill=1, stroke=0); c.setFillGray(0)
    d = Drawing(size, size); d.add(w); renderPDF.draw(d, c, x, y)
    c.setFont("SansB", 7.5)
    lab = "ERMITTLERPORTAL · Kennwort im Brief"
    c.drawCentredString(x + size / 2, y - 9, lab)


def rule(y, x0=ML, x1=W - MR, wd=0.6, g=0):
    c.setStrokeGray(g); c.setLineWidth(wd); c.line(x0, y, x1, y)


def doc_head(no, title, sub):
    y = H - MT - 10
    c.setFont("SansB", 9); fc({"rot": ROT, "blau": BLAU}.get(CUR[0], (0.45, 0.5, 0.55))); c.drawString(ML, y, no); c.setFillGray(0)
    y -= 26; c.setFont("SansB", 20); c.drawString(ML, y, title)
    y -= 16; c.setFont("SerifI", 10.5); c.setFillGray(0.3); c.drawString(ML, y, sub); c.setFillGray(0)
    return y - 22


def stamp(x, y, s, ang=-6, size=13):
    c.saveState(); c.translate(x, y); c.rotate(ang)
    wd = pdfmetrics.stringWidth(s, "SansB", size) + 16
    sc(ROT); fc(ROT); c.setLineWidth(1.6)
    c.roundRect(-wd / 2, -size * 0.55, wd, size * 1.6, 3, fill=0, stroke=1)
    c.setFont("SansB", size); c.drawCentredString(0, -size * 0.1, s); c.restoreState()


def photo(name, x, y, w, h=None, crop=None, border=True, caption=None):
    """Foto einsetzen. (x, y) = linke untere Ecke. crop = (l, o, r, u) als Anteile."""
    im = Image.open(IMG + name)
    if crop:
        iw, ih = im.size
        im = im.crop((int(crop[0] * iw), int(crop[1] * ih), int(crop[2] * iw), int(crop[3] * ih)))
    if h is None:
        h = w * im.size[1] / im.size[0]
    if border:
        c.setFillGray(1); c.setStrokeGray(0.75); c.setLineWidth(0.5)
        c.rect(x - 5, y - 5, w + 10, h + 10, fill=1, stroke=1)
    c.drawImage(ImageReader(im), x, y, w, h)
    if caption:
        c.setFont("Sans", 7.5); c.setFillGray(0.35); c.drawString(x, y - 16, caption); c.setFillGray(0)
    return h


def form_table(x, y, w, rows, lw=150, size=9.6, lead=13):
    """Formular mit Beschriftung links, Inhalt rechts."""
    for lab, val in rows:
        h = max(lines_h(val, "Form", size, w - lw - 16, lead), lead, lab.count("\n") * 10 + 12) + 10
        c.setStrokeGray(0.55); c.setLineWidth(0.6)
        c.setFillColorRGB(0.88, 0.92, 0.96); c.rect(x, y - h, lw, h, fill=1, stroke=1)
        c.setFillGray(1); c.rect(x + lw, y - h, w - lw, h, fill=1, stroke=1); c.setFillGray(0)
        c.setFont("FormB", 8.4)
        for li, ll in enumerate(lab.split("\n")):
            c.drawString(x + 6, y - 14 - li * 10, ll.upper())
        text(x + lw + 8, y - 15, w - lw - 16, val, "Form", size, lead, gap=0)
        y -= h
    return y


# ================= SEITE 1: Titel =================
def title_page():
    # Foto randlos (3:4), oben und unten minimal beschnitten
    ph = W * 1448 / 1086
    c.drawImage(IMG + "cover.jpg", 0, (H - ph) / 2, W, ph)
    # dunkler Verlauf oben für den Titel, unten für den Autor
    for i in range(80):
        c.setFillColorRGB(*NIGHT); c.setFillAlpha(0.85 * (1 - max(0, i - 40) / 40) ** 1.5)
        c.rect(0, H - 5.5 * (i + 1), W, 5.5, fill=1, stroke=0)
    for i in range(30):
        c.setFillColorRGB(*NIGHT); c.setFillAlpha(0.75 * (1 - i / 30) ** 1.3)
        c.rect(0, 5 * i, W, 5, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFont("SansM", 11); c.setFillColorRGB(1, 0.8, 0.35); c.drawString(ML, H - 110, "EIN KRIMISPIEL ZU ZWEIT  ·  FALL 1"); c.setFillGray(1)
    c.setFont("SansB", 46); c.drawString(ML, H - 170, "Ausverkauf")
    c.drawString(ML, H - 222, "am Kiefernsee")
    c.setFont("SerifI", 14)
    c.drawString(ML, H - 262, "Zwei Akten. Eine Nacht. Ein Toter im Tretboot.")
    c.setFont("Sans", 10.5)
    c.drawString(ML, H - 300, "Für 2 Spürnasen (oder 2 Teams)  ·  ab 14 Jahren  ·  Akt 1: ca. 45–60 Minuten")
    c.setFont("SansB", 12); c.setFillGray(1); c.drawString(ML, 72, "Natthaphon Lind")
    c.setFont("SansB", 9); c.setFillGray(0.85)
    c.drawString(ML, 50, "PROTOTYP · NUR AKT 1 · ZUM TESTEN")
    c.setFillGray(0); c.showPage(); PAGE[0] += 1


# ================= SEITE 2: Spielanleitung =================
RULES = [
    ("Ihr seid zwei Ermittler",
     "Einer übernimmt Akte Rot, der andere Akte Blau. Zu dritt oder zu viert bildet ihr zwei Teams."),
    ("So sitzt ihr",
     "Setzt euch gegenüber, das Buch liegt aufgeschlagen zwischen euch. Ab Seite 8 gehört jede linke "
     "Seite Akte Rot, jede rechte Seite Akte Blau. Die blauen Seiten stehen für Rot auf dem Kopf – für "
     "Blau stehen sie richtig herum. So lest ihr beide gleichzeitig und blättert gemeinsam weiter."),
    ("Die goldene Regel",
     "Jeder liest nur seine eigene Seite. Ihr dürft euch alles vorlesen, beschreiben und erzählen – aber "
     "ihr schaut nicht auf die Seite des anderen. Die Lösung entsteht erst, wenn ihr redet."),
    ("Buch und Ermittlerportal",
     "Das Buch ist eure Hauptakte: Hier stehen alle Spuren, euer Ermittlerbogen und die Auflösung. Das "
     "Ermittlerportal ergänzt es mit Tonaufnahmen, Fotos und der Code-Prüfung. Scannt dafür die QR-Codes "
     "im Buch mit der Handykamera – das Kennwort steht im Brief der Kommissarin."),
    ("Fragen und Hilfe",
     "Jeder Akt endet mit Fragen. Prüft eure Antworten im Portal oder mit der Code-Prüfung hinten im Buch. "
     "Hängt ihr fest, helfen Hinweise in drei Stufen: Schubs, Richtung, Antwort."),
    ("Das Duell",
     "Euer Team startet mit 10 Punkten. Jeder falsche Code kostet 2 Punkte, jede Hinweisstufe 1 Punkt. "
     "Zusätzlich schreibt jeder nach jedem Akt geheim seinen Hauptverdacht auf den Ermittlerbogen. "
     "Wer am Ende am frühesten richtig lag, gewinnt die Goldene Lupe vom Kiefernsee."),
]


def rules_page():
    y = doc_head("SO WIRD GESPIELT", "Spielanleitung", "Bitte zuerst gemeinsam lesen.")
    for i, (h, t) in enumerate(RULES, 1):
        fc(NIGHT); c.circle(ML + 11, y + 4, 11, fill=1, stroke=0)
        c.setFillGray(1); c.setFont("SansB", 11); c.drawCentredString(ML + 11, y, str(i)); c.setFillGray(0)
        c.setFont("SansB", 12); c.drawString(ML + 32, y, h)
        y = text(ML + 32, y - 17, W - MR - ML - 32, t, "Serif", 10.4, 14.6) - 8
    y -= 4
    c.setFillColorRGB(1, 0.95, 0.80); c.setStrokeColorRGB(0.85, 0.7, 0.4); c.roundRect(ML, y - 78, W - ML - MR, 78, 4, fill=1, stroke=1)
    c.setFillGray(0); c.setFont("SansB", 10); c.drawString(ML + 12, y - 18, "Ihr braucht")
    text(ML + 12, y - 34, W - ML - MR - 24,
         "Zwei Stifte, ein Handy mit Kamera und Internet, etwas Zeit – und gern ein Getränk. Lieber per Handy? "
         "Jede Akte gibt es auch im Ermittlerportal: Kennwort eingeben, Rot oder Blau wählen. Ermittlerbogen und "
         "Auflösung gibt es aber nur hier im Buch.", "Serif", 9.6, 13)
    new_page()


# ================= SEITE 3: Brief =================
LETTER = """Liebe Kollegin, lieber Kollege,
Samstagmorgen, 6:38 Uhr: Am Campingplatz am Kiefernsee findet die Brötchenfrau einen Toten im Schilf, direkt neben einem treibenden Tretboot. Es ist Holger Brandner, 58, Projektentwickler aus Frankfurt. Er wollte den Platz kaufen und daraus ein Glamping-Resort machen. Die Dauercamper hätten Ende 2027 gehen müssen.
Am Abend vorher gab es eine Platzversammlung. Sagen wir es so: Herr Brandner hat dort keine neuen Freunde gefunden.
Mein Revier ist unterbesetzt, und ich brauche zwei frische Augenpaare. Ich habe die Unterlagen aufgeteilt: Akte Rot enthält, was meine Leute gesichert haben. Akte Blau enthält, was wir auf dem Platz eingesammelt haben – Protokolle, Chats, Handydaten. Keiner von Ihnen hat das ganze Bild. Reden Sie miteinander.
Für heute will ich nur wissen, was in dieser Nacht überhaupt passiert ist. Den Rest klären wir später.
Mit kollegialen Grüßen"""


def letter_page():
    c.setFont("FormB", 10); c.drawString(ML, H - MT - 6, "Kriminalpolizei Seebrück")
    c.setFont("Form", 9); c.setFillGray(0.35)
    c.drawString(ML, H - MT - 20, "Kommissariat 1 · Gewaltdelikte · Hafenstraße 12 · 23999 Seebrück")
    c.drawRightString(W - MR, H - MT - 6, "Az. 31 Js 0926/BR")
    c.drawRightString(W - MR, H - MT - 20, "Seebrück, Samstag, 26. September")
    c.setFillGray(0); rule(H - MT - 30, wd=1.2)
    y = H - MT - 70
    c.setFont("FormB", 12); c.drawString(ML, y, "Betreff: Todesfall Holger Brandner, Campingplatz am Kiefernsee")
    y = text(ML, y - 28, W - ML - MR - 10, LETTER, "Mono", 10.2, 15)
    c.setFont("SerifBI", 22); fc(INK); c.drawString(ML + 10, y - 16, "J. Wendland"); c.setFillGray(0)
    c.setFont("Mono", 10); c.drawString(ML, y - 36, "Jutta Wendland, Erste Kriminalhauptkommissarin")
    stamp(W - MR - 90, y - 4, "VERTRAULICH", -8)
    yb = 118
    c.setFillColorRGB(0.88, 0.92, 0.97); sc(BLAU); c.rect(ML, yb - 44, W - ML - MR, 104, fill=1, stroke=1)
    c.setFillGray(0); c.setFont("FormB", 9); c.drawString(ML + 12, yb + 34, "ZUGANG ERMITTLERPORTAL")
    c.setFont("Form", 9.4)
    c.drawString(ML + 12, yb + 18, "Scannen Sie den Code. Das Portal ist nur über diesen Link erreichbar.")
    c.drawString(ML + 12, yb + 4, "Bitte nicht weitergeben.")
    c.setFont("MonoB", 15); c.drawString(ML + 12, yb - 18, "Kennwort: TRETBOOT")
    qr(W - MR - 104, yb - 34, 92, PORTAL, "portal")
    new_page()


# ================= SEITE 4: Auftrag Akt 1 =================
Q = [("Frage 1", "Wo ist Holger Brandner ins Wasser gekommen?",
      ["am Badestrand", "am Bootssteg", "mitten auf dem See, aus dem Tretboot"]),
     ("Frage 2", "In welchem Zeitraum ist es passiert?",
      ["zwischen 21:30 und 23:00 Uhr", "zwischen 23:30 und 0:30 Uhr",
       "zwischen 0:30 und 2:00 Uhr", "nach 2:00 Uhr"]),
     ("Frage 3", "Welcher Gegenstand des Opfers fehlt?",
      ["sein Handy", "seine Brieftasche", "seine rote Ledermappe", "sein Autoschlüssel"])]
RIGHT = (2, 2, 3)


def task_page():
    y = doc_head("AKT 1  ·  FÜR BEIDE", "Was ist in dieser Nacht passiert?",
                 "Euer Auftrag von Hauptkommissarin Wendland")
    y = text(ML, y, W - ML - MR,
             "So geht ihr vor: Schaut euch zuerst gemeinsam den Lageplan an. Dann blättert ihr durch die fünf "
             "Akten-Doppelseiten (Seite 8 bis 17): links Rot, rechts Blau. Jeder liest seine Seite und erzählt, was er gefunden hat. "
             "Achtung: Einige Spuren sehen wichtig aus und sind es nicht. Andere sehen harmlos aus und sind "
             "der Schlüssel.", "Serif", 10.6, 15) - 6
    for (k, qq, opts) in Q:
        bh = 30 + len(opts) * 22 + 10
        c.setStrokeGray(0); c.setLineWidth(1); c.rect(ML, y - bh, W - ML - MR, bh, fill=0, stroke=1)
        c.setFont("SansB", 9); c.setFillGray(0.4); c.drawString(ML + 14, y - 18, k.upper()); c.setFillGray(0)
        c.setFont("SansB", 12.5); c.drawString(ML + 80, y - 18, qq)
        yy = y - 44
        for i, o in enumerate(opts, 1):
            c.setLineWidth(0.8); c.rect(ML + 80, yy - 3, 11, 11, fill=0, stroke=1)
            c.setFont("SansB", 10.5); c.drawString(ML + 100, yy, f"{i}")
            c.setFont("Serif", 10.8); c.drawString(ML + 116, yy, o)
            yy -= 22
        y -= bh + 14
    text(ML, y - 4, W - ML - MR,
         "Habt ihr euch auf alle drei Antworten geeinigt? Dann prüft sie im Ermittlerportal oder auf der "
         "Seite „Code-Prüfung“ (Seite 19). Erst danach lest ihr die Auflösung.", "SerifI", 10.4, 14.5)
    new_page()


# ================= SEITE 5: Figuren =================
CAST = [
    ("Holger Brandner", "58", "Das Opfer. Projektentwickler, „Brandner Freizeit & Resort GmbH“. "
     "Wollte den Platz kaufen. Wohnte übers Wochenende in Mietchalet 3."),
    ("Mark Böttcher", "61", "Platzbetreiber. Will verkaufen: „Ich mäh seit 30 Jahren Rasen und lese Beschwerden.“"),
    ("Angelika Wohlfahrt", "67", "Dauercamperin seit 1998, Parzelle 7. Sprecherin der Dauercamper und "
     "Schriftführerin. Weiß alles über jeden."),
    ("Siggi Kowalski", "64", "Dauercamper, Parzelle 14. Grillmeister, Schlagerfan, Gegner jeder Veränderung."),
    ("Marco Lenz", "45", "Hausmeister. Repariert alles, streicht alles, hat Schlüssel für alles."),
    ("Sven Ruppert", "34", "Sicherheitsdienst. Nimmt die Nachtruhe sehr, sehr ernst."),
    ("Nova Sommer", "26", "Gast mit Van auf Stellplatz G2. Vanlife-Influencerin (@nova.on.wheels), "
     "reist mit Hund Pepper."),
    ("Rita Schäfer", "59", "Kiosk und Brötchendienst, Parzelle 3 direkt am Steg. Hat den Toten gefunden."),
]


def cast_page():
    y = doc_head("FÜR BEIDE", "Wer ist wer am Kiefernsee?", "Personenregister zum Fall")
    for i, (n, age, d) in enumerate(CAST):
        h = max(lines_h(d, "Serif", 10, W - ML - MR - 190, 13.6), 14) + 18
        if i:
            rule(y + 8, g=0.75, wd=0.5)
        c.setFont("SansB", 11.5); c.drawString(ML, y - 6, n)
        c.setFont("Sans", 9.5); c.setFillGray(0.4); c.drawString(ML, y - 20, f"{age} Jahre"); c.setFillGray(0)
        text(ML + 190, y - 6, W - ML - MR - 190, d, "Serif", 10, 13.6, gap=0)
        y -= h + 12
        if i == 0:
            y -= 2
    new_page()


# ================= SEITE 6: Lageplan =================
def map_page():
    y = doc_head("FÜR BEIDE", "Lageplan Campingplatz am Kiefernsee", "Luftbild der Polizeidrohne, Samstag, 26.09. · Norden ist oben")
    side = W - ML - MR
    photo("lageplan_beschriftet.jpg", ML, y - side, side, side, border=False)
    text(ML, y - side - 20, side,
         "Rita Schäfer wohnt auf Parzelle 3, gleich oberhalb vom Steg. Nova Sommer steht mit ihrem Van auf G2. "
         "Die Wetterstation hängt an der Gaststätte Seeklause.", "Serif", 9.8, 13.4)
    new_page()


def seat_page():
    y = doc_head("FÜR BEIDE", "So sitzt ihr", "Ab der nächsten Seite beginnen die Akten")
    # Tisch von oben
    tx, ty, tw, th = ML + 70, y - 400, W - ML - MR - 140, 280
    c.setFillColorRGB(0.86, 0.78, 0.66); c.setStrokeColorRGB(0.6, 0.5, 0.38); c.setLineWidth(1.2)
    c.roundRect(tx, ty, tw, th, 10, fill=1, stroke=1)
    bx, by, bw, bh = W / 2 - 120, ty + 80, 240, 120
    for k, (col, lab, flipped) in enumerate([(ROT, "AKTE ROT", False), (BLAU, "AKTE BLAU", True)]):
        x = bx + k * bw / 2
        c.setFillGray(1); c.setStrokeGray(0.5); c.rect(x, by, bw / 2, bh, fill=1, stroke=1)
        fc(col); c.rect(x + (bw / 2 - 12 if k else 0), by + 30, 12, 60, fill=1, stroke=0)
        c.saveState(); c.translate(x + bw / 4, by + bh / 2)
        if flipped:
            c.rotate(180)
        fc(col); c.setFont("SansB", 12); c.drawCentredString(0, 6, lab)
        c.setFillGray(0.5)
        for i in range(4):
            c.rect(-38, -10 - i * 9, 76, 3, fill=1, stroke=0)
        c.restoreState()
    c.setStrokeGray(0.3); c.setLineWidth(1.5); c.line(W / 2, by, W / 2, by + bh)
    # Personen
    for (py, col, lab, ly) in [(ty - 40, ROT, "Spieler/in ROT", ty - 78), (ty + th + 40, BLAU, "Spieler/in BLAU", ty + th + 72)]:
        fc(col); c.circle(W / 2, py, 26, fill=1, stroke=0)
        c.setFillGray(1); c.setFont("SansB", 15); c.drawCentredString(W / 2, py - 5, lab.split()[-1][0]); c.setFillGray(0)
        c.setFont("SansB", 10); fc(col); c.drawCentredString(W / 2, ly, lab); c.setFillGray(0)
    y = ty - 108
    y = text(ML, y, W - ML - MR - 110,
             "Linke Seite: Akte Rot, für Rot richtig herum. Rechte Seite: Akte Blau, für Blau richtig herum. "
             "Blättert immer gemeinsam um. Ihr dürft vorlesen und erzählen, so viel ihr wollt – nur nicht "
             "rüberschauen.\nLieber am Handy? Dann scannt den Portal-Code, gebt das Kennwort ein und wählt eure Akte.",
             "Serif", 10.4, 14.6)
    qr(W - MR - 104, ty - 200, 100, PORTAL, "portal")
    new_page()


def notes_page():
    y = doc_head("FÜR BEIDE", "Notizen", "Platz für eure Gedanken – die Auflösung steht auf der nächsten Seite.")
    for k in range(24):
        y -= 24; c.setStrokeGray(0.7); c.setLineWidth(0.5); c.line(ML, y, W - MR, y)
    new_page()


# ================= AKTE ROT =================
def r1():
    akte_tab("rot")
    y = doc_head("R-1  ·  AKTE ROT", "Bericht zum Leichenfund", "Erster Angriff, Kriminalpolizei Seebrück")
    rows = [
        ("Aktenzeichen", "31 Js 0926/BR"),
        ("Meldung", "Samstag, 26.09., 06:44 Uhr, Notruf über Leitstelle (Anruferin: Rita Schäfer)"),
        ("Fundort", "Campingplatz am Kiefernsee, Nordostufer, Schilfgürtel. Wassertiefe ca. 60 cm."),
        ("Person", "Holger Brandner, 58 J., wohnhaft Frankfurt am Main. Gast in Mietchalet 3."),
        ("Auffinde-\nsituation", "Leiche in Bauchlage im Flachwasser, unmittelbar neben dem treibenden "
         "Tretboot „Chantal“. Bekleidung: Jeans, Hemd, Sakko, Lederslipper."),
        ("Verletzungen", "Platzwunde am Hinterkopf, ca. 4 cm. Keine Abwehrverletzungen."),
        ("Rechtsmedizin\n(vorläufig)", "Dr. A. Okonkwo: Tod durch Ertrinken. Die Kopfverletzung entstand "
         "vor dem Eintritt ins Wasser, das Opfer war vermutlich bewusstlos. In der Wunde: mehrere kleine "
         "Holzsplitter, Nadelholz, vermutlich Lärche, mit grauer Lasur.\nTodeszeitpunkt nach "
         "Körpertemperatur: zwischen 22:00 und 2:00 Uhr. Wegen der Wassertemperatur nicht enger bestimmbar."),
        ("Tretboot\n„Chantal“", "Kunststoff (PE), Baujahr 2025. Keine Beschädigungen, keine Blut- oder "
         "Haaranhaftungen. Die Ankerkette hängt nicht am Boot."),
        ("Bearbeitung", "EKHK'in J. Wendland, KK Brüggemann"),
    ]
    y = form_table(ML, y, W - ML - MR - 20, rows, lw=118, size=9.2, lead=12.4)
    # Fundortfoto, so groß wie der Platz erlaubt
    avail = y - 26 - 70
    pw = min(250, avail * 1.5)
    if pw > 140:
        ph = pw / 1.5
        photo("fundort.jpg", ML + 5, y - 26 - ph, pw, ph,
              caption="Lichtbild 1: Fundort am Schilfgürtel, Sa 26.09., 07:10 Uhr (nach Bergung)")
    stamp(W - MR - 100, y - 70, "ERMITTLUNGSSACHE", -4, 11)
    new_page()


def r2():
    akte_tab("rot")
    y = doc_head("R-2  ·  AKTE ROT", "Asservatenverzeichnis", "Sichergestellte Gegenstände, Samstag, 26.09.")
    cols = [("Nr.", 30), ("Gegenstand", 150), ("Fundort", 140), ("Bemerkung", 156)]
    data = [
        ("1", "Brieftasche, Leder, schwarz", "am Körper, Innentasche Sakko", "Inhalt: 240 € bar, 2 Kreditkarten, Ausweis"),
        ("2", "Ehering, Gold", "am Körper", "Gravur „H. & S. 1994“"),
        ("3", "Smartphone", "Tretboot, Sitzfläche", "nass, aber funktionsfähig. Zur Auswertung (siehe Akte Blau)"),
        ("4", "Lesebrille", "Tretboot, Fußraum", "–"),
        ("5", "Autoschlüssel (Mercedes)", "Mietchalet 3, Tisch", "Fahrzeug steht auf Gästeparkplatz"),
        ("6", "Laptop", "Mietchalet 3, Reisetasche", "passwortgeschützt"),
        ("7", "Reisetasche mit Kleidung", "Mietchalet 3", "ordentlich gepackt"),
        ("8", "Kette mit Vorhängeschloss", "Bootssteg", "gehört zum Tretboot „Chantal“. Schloss geöffnet, NICHT aufgebrochen (Lichtbild 2)"),
    ]
    x = ML; tw = sum(w for _, w in cols)
    c.setFillGray(0.15); c.rect(x, y - 20, tw, 20, fill=1, stroke=0); c.setFillGray(1)
    xx = x
    for (h, w) in cols:
        c.setFont("FormB", 8.6); c.drawString(xx + 5, y - 14, h.upper()); xx += w
    c.setFillGray(0); y -= 20
    for i, row in enumerate(data):
        hh = max(lines_h(cell, "Form", 9, w - 10, 12) for cell, (_, w) in zip(row, cols)) + 10
        if i % 2:
            c.setFillGray(0.94); c.rect(x, y - hh, tw, hh, fill=1, stroke=0); c.setFillGray(0)
        xx = x
        for cell, (_, w) in zip(row, cols):
            text(xx + 5, y - 13, w - 10, cell, "Form", 9, 12, gap=0); xx += w
        y -= hh
    rule(y, x, x + tw, 0.8)
    y -= 26
    c.setFont("FormB", 9.5); c.drawString(ML, y, "Vermerk:")
    y = text(ML + 56, y, W - ML - MR - 76,
             "Bargeld und Kreditkarten vollständig vorhanden. Ein Raubmord erscheint daher unwahrscheinlich. "
             "Mietchalet 3 war nicht abgeschlossen, keine Einbruchsspuren.", "Form", 9.5, 13)
    avail = y - 20 - 70
    pw = min(300, avail * 1.5)
    ph = pw / 1.5
    photo("asservat.jpg", ML + 5, y - 20 - ph, pw, ph,
          caption="Lichtbild 2: Asservat Nr. 8 auf dem Bootssteg, Sa 26.09., 07:25 Uhr")
    new_page()


SVEN = [
    ("22:00", "Schranke geschlossen. Nachtruhe beginnt."),
    ("22:47", "Parzelle 14 (Kowalski): Schlagermusik deutlich zu laut. Ermahnt. Zweite Ermahnung diesen Monat!!"),
    ("23:30", "Bootssteg: beide Tretboote („Kevin“ + „Chantal“) angekettet. Alles in Ordnung. Steg noch leicht klebrig."),
    ("23:34", "Igel bei Sanitär 1. Kein Handlungsbedarf."),
    ("0:30", "Bootssteg: Boot „Chantal“ FEHLT!! Kette liegt auf dem Steg, Schloss offen, nicht beschädigt. "
     "Vermutlich vom Hausmeister nicht richtig abgeschlossen. → Meldung an Rezeption morgen früh."),
    ("1:15", "Sanitär 2: Licht brennt, niemand drin. Ausgeschaltet. Stromverschwendung!!"),
    ("2:00", "Schranke: ohne Befund."),
    ("3:00", "Rundgang beendet. Keine besonderen Vorkommnisse."),
]


def r3():
    akte_tab("rot")
    y = doc_head("R-3  ·  AKTE ROT", "Rundgangsprotokoll Sicherheitsdienst",
                 "Kopie, handschriftlich geführt von Sven Ruppert, Nacht von Freitag auf Samstag")
    x0, w0 = ML + 6, W - ML - MR - 36
    c.setFillColorRGB(1, 0.98, 0.84); c.setStrokeGray(0.55); c.rect(x0, 70, w0, y - 64, fill=1, stroke=1); c.setFillGray(0)
    c.setFont("FormB", 9); c.drawString(x0 + 12, y - 18, "SICHERHEITSDIENST RUPPERT  ·  Objekt: Camping Kiefernsee  ·  Datum: 25./26.09.")
    c.setStrokeColorRGB(0.9, 0.45, 0.45); c.setLineWidth(0.8); c.line(x0 + 64, y - 26, x0 + 64, 70)
    ly = y - 50; lead = 19
    for t, e in SVEN:
        ls = simpleSplit(e, "SerifI", 12, w0 - 90)
        fc(INK); c.setFont("SerifB", 12); c.drawString(x0 + 14, ly, t)
        for l in ls:
            fc(INK); c.setFont("SerifI", 12); c.drawString(x0 + 74, ly, l)
            c.setStrokeColorRGB(0.7, 0.8, 0.92); c.setLineWidth(0.4); c.line(x0 + 70, ly - 5, x0 + w0 - 10, ly - 5)
            ly -= lead
        ly -= 8
    fc(INK); c.setFont("SerifBI", 16); c.drawString(x0 + w0 - 150, 100, "S. Ruppert"); c.setFillGray(0)
    new_page()


RITA = [
    ("F", "Frau Schäfer, Sie haben Herrn Brandner gefunden. Erzählen Sie bitte."),
    ("A", "Um 6:38. Ich fahr jeden Morgen die Brötchen aus, mit dem Lastenrad am Ufer lang. Da seh ich die "
          "Chantal im Schilf hängen. Und daneben im Wasser … den Herrn Brandner. Ich hab sofort die 110 angerufen."),
    ("F", "Ist Ihnen in der Nacht etwas aufgefallen?"),
    ("A", "Ich wohn ja auf Parzelle 3, direkt am Steg. So gegen halb zwei hat's da unten richtig laut PLATSCH "
          "gemacht. Ich hab noch gedacht: Jetzt ist einer reingefallen."),
    ("F", "Sind Sie nachsehen gegangen?"),
    ("A", "Ich hatte schon die Lockenwickler drin. Da geh ich nicht mehr raus."),
    ("F", "Und vorher, so gegen Mitternacht?"),
    ("A", "Da hab ich geschlafen. Ich schlaf ab zehn. Außer donnerstags, da kommt „Bauer sucht Frau“."),
    ("F", "Hatte Herr Brandner bei Ihnen Brötchen bestellt?"),
    ("A", "Zwei Laugenbrezeln für Chalet 3. Die liegen jetzt noch in meinem Korb."),
]


def r4():
    akte_tab("rot")
    y = doc_head("R-4  ·  AKTE ROT", "Vernehmung der Zeugin Rita Schäfer",
                 "Samstag, 26.09., 07:30 Uhr, Rezeption. Vernehmung durch KK Brüggemann")
    for who, t in RITA:
        c.setFont("MonoB", 10.4); c.drawString(ML, y, who + ":")
        y = text(ML + 30, y, W - ML - MR - 50, t, "MonoB" if who == "F" else "Mono", 10.2, 14.4, gap=0) - 9
    y -= 6
    c.setFont("Mono", 9.6); c.drawString(ML, y, "Selbst gelesen, genehmigt, unterschrieben:")
    fc(INK); c.setFont("SerifBI", 16); c.drawString(ML + 20, y - 26, "Rita Schäfer"); c.setFillGray(0)
    new_page()


WEATHER = [("22:00", "11,8", "SW", "14"), ("23:00", "11,2", "SW", "18"), ("0:00", "10,6", "SW", "22"),
           ("1:00", "10,1", "SW", "20"), ("2:00", "9,7", "SW", "16"), ("3:00", "9,4", "W", "12"),
           ("4:00", "9,0", "W", "9"), ("5:00", "8,8", "W", "6"), ("6:00", "8,6", "W", "5")]
NOTRUF_HEAD = "LEITSTELLE SEEBRÜCK · Notruf Sa 26.09., 06:44:12 Uhr · Anruferin: Rita Schäfer · Dauer 0:21"
NOTRUF = [
    ("Leitstelle", "Notruf Leitstelle Seebrück. Wo genau ist der Notfallort?"),
    ("Anruferin", "Hier ist die Rita vom Kiefernsee! Da liegt einer im Wasser, beim Schilf, das ist der Herr Brandner. "
                  "Der bewegt sich nicht! Das Tretboot ist auch da, die Chantal. Bitte kommen Sie schnell!"),
    ("Leitstelle", "Bleiben Sie, wo Sie sind, und gehen Sie nicht ins Wasser. Rettungswagen und Polizei sind unterwegs."),
]
NOTRUF_FOOT = "06:45 Uhr: Rettungswagen und Streife alarmiert."


def r5():
    akte_tab("rot")
    y = doc_head("R-5  ·  AKTE ROT", "Wetterdaten und Notruf",
                 "Ausdruck der Wetterstation an der Gaststätte Seeklause, Nacht 25./26.09.")
    cols = [("Uhrzeit", 90), ("Temperatur °C", 120), ("Wind aus", 100), ("Wind km/h", 100)]
    x = ML; tw = sum(w for _, w in cols)
    c.setFont("MonoB", 9.6); xx = x
    for h, w in cols:
        c.drawString(xx + 6, y, h); xx += w
    rule(y - 6, x, x + tw, 0.8); y -= 22
    for row in WEATHER:
        xx = x
        for cell, (_, w) in zip(row, cols):
            c.setFont("Mono", 10); c.drawString(xx + 6, y, cell); xx += w
        y -= 17
    rule(y + 9, x, x + tw, 0.4, 0.5)
    y = text(ML, y - 8, W - ML - MR - 30,
             "Niederschlag: 0 mm. Hinweis Wetterdienst: Ein Wind aus Südwest (SW) weht nach Nordosten.",
             "Mono", 9.2, 13) - 18
    c.setFont("SansB", 12); c.drawString(ML, y, "Mitschnitt des Notrufs")
    y -= 10
    bw = W - ML - MR - 30
    tw = bw - 130
    body_h = max(sum(lines_h(t, "Mono", 9.2, tw - 90, 12.6) + 6 for _, t in NOTRUF) + 70, 168)
    c.setFillColorRGB(0.95, 0.95, 0.93); c.setStrokeGray(0.6); c.setLineWidth(0.6)
    c.rect(ML, y - body_h, bw, body_h, fill=1, stroke=1); c.setFillGray(0)
    c.setFont("MonoB", 7.6); c.drawString(ML + 10, y - 16, NOTRUF_HEAD)
    yy = y - 36
    for who, t in NOTRUF:
        c.setFont("MonoB", 9.2); c.drawString(ML + 10, yy, who + ":")
        yy = text(ML + 96, yy, tw - 90, t, "Mono", 9.2, 12.6, gap=0) - 6
    c.setFont("Mono", 8.2); c.setFillGray(0.35); c.drawString(ML + 10, y - body_h + 10, NOTRUF_FOOT); c.setFillGray(0)
    qr(ML + bw - 114, y - 22 - 100, 100, PORTAL + "#r5", "portal")
    c.setFont("SansB", 8.5); c.drawCentredString(ML + bw - 64, y - 22 - 100 - 22, "Original anhören")
    new_page()


# ================= AKTE BLAU =================
PROTO = [
    ("Ort / Zeit", "Gaststätte Seeklause, Freitag, 25.09., 19:00 bis 21:30 Uhr"),
    ("Anwesend", "31 Dauercamper, Platzbetreiber Mark Böttcher, Herr Holger Brandner (Brandner Freizeit & Resort GmbH), "
     "Hausmeister Marco Lenz, Sicherheitsdienst Sven Ruppert (am Eingang), Frau Nova Sommer (Gast)"),
    ("TOP 1", "Begrüßung durch Herrn Böttcher. Er möchte „mit 61 nicht mehr jeden Morgen Rasen mähen und Beschwerden lesen“."),
    ("TOP 2", "Herr Brandner stellt das „Kiefernsee Glamping Resort“ vor: 40 Safarizelte, ein Saunafloß, "
     "die Dauerparzellen enden am 31.12.2027. Er holt den Vorvertrag aus seiner roten Ledermappe und sagt: "
     "„Hier fehlt nur noch eine Unterschrift.“"),
    ("TOP 3", "Aussprache, sehr lebhaft. Herr Kowalski: „Nur über meinen Grill.“ Frau Sommer fragt, ob es im Resort "
     "Steckdosen für Vans gibt. Herr Lenz fragt, ob das Personal übernommen wird. Herr Brandner: „Wir bringen unser "
     "eigenes Team mit.“ Herr Lenz verlässt kurz den Raum."),
    ("TOP 4", "Abstimmung (nicht bindend): 0 dafür, 31 dagegen, 1 Enthaltung (Herr Ruppert, „aus dienstlichen Gründen neutral“)."),
    ("Ende", "21:30 Uhr. Herr Brandner verabschiedet sich mit der roten Mappe unter dem Arm: „Ich bin noch bis "
     "Sonntag in Chalet 3. Meine Tür steht offen.“"),
    ("Sonstiges", "Die Bowle war zu süß."),
]


def b1():
    flip(); akte_tab("blau")
    y = doc_head("B-1  ·  AKTE BLAU", "Protokoll der Platzversammlung",
                 "Interessengemeinschaft der Dauercamper am Kiefernsee e. V. (in Gründung)")
    y = form_table(ML, y, W - ML - MR - 20, PROTO, lw=86, size=9.8, lead=13.4)
    fc(INK); c.setFont("SerifBI", 15); c.drawString(ML + 10, y - 34, "A. Wohlfahrt"); c.setFillGray(0)
    c.setFont("Form", 9); c.drawString(ML, y - 50, "Angelika Wohlfahrt, Schriftführerin")
    new_page()


CHAT = [
    ("DONNERSTAG, 24. SEPTEMBER", None, None),
    ("Marco (Hausmeister)", "17:02", "Steg ist frisch lasiert. Lärche, grau. Bis Freitagabend bitte NICHT betreten!! Auch nicht „nur kurz“, Siggi."),
    ("Siggi P14", "17:05", "Das mit den Fußspuren letztes Jahr war ich nicht."),
    ("Angelika P7", "17:06", "Doch."),
    ("FREITAG, 25. SEPTEMBER", None, None),
    ("Angelika P7", "12:30", "Erinnerung: Heute 19 Uhr Versammlung in der Seeklause. Thema: Herr Brandner und seine „Glamping-Pläne“. Bitte zahlreich erscheinen!"),
    ("Siggi P14", "12:41", "Ich bring meinen Grill mit. Als Argument."),
    ("Siggi P14", "21:48", "Habt ihr gesehen, wie der seine rote Mappe festhält? Wie ein Baby."),
    ("Angelika P7", "21:49", "Da ist der Vorvertrag drin. Wenn Mark unterschreibt, sind wir Ende 2027 alle weg."),
    ("Mark (Platzbetreiber)", "21:52", "Leute, ich hab noch nichts unterschrieben. Schlaft drüber. Ich auch."),
    ("Sven (Security)", "23:05", "Erinnerung: Ab 22 Uhr ist Nachtruhe. Parzelle 14, ich hör den Schlager bis zur Schranke."),
    ("Siggi P14", "23:06", "Das ist Kultur."),
    ("SAMSTAG, 26. SEPTEMBER", None, None),
    ("Rita P3", "06:52", "POLIZEI IST SCHON DA. Am Schilf. Der Herr Brandner. Oh Gott."),
    ("Angelika P7", "06:58", "Was ist passiert??"),
    ("Mark (Platzbetreiber)", "07:03", "Bitte alle auf euren Parzellen bleiben. Die Polizei will mit jedem sprechen."),
]


def b2():
    flip(); akte_tab("blau")
    y = doc_head("B-2  ·  AKTE BLAU", "Chat „Kiefernsee Dauercamper“",
                 "Auszug aus der Gruppe, vom Handy von Angelika Wohlfahrt, Donnerstag bis Samstag")
    x0, w0 = ML + 40, W - ML - MR - 110
    c.setFillColorRGB(0.93, 0.90, 0.84); c.roundRect(x0 - 14, 46, w0 + 28, y - 38, 14, fill=1, stroke=0); c.setFillGray(0)
    y -= 14
    for who, t, msg in CHAT:
        if t is None:
            c.setFont("SansB", 7.5); c.setFillGray(0.4); c.drawCentredString(x0 + w0 / 2, y - 4, who); c.setFillGray(0)
            y -= 15; continue
        own = who.startswith("Angelika")
        bw = w0 * 0.84
        ls = simpleSplit(msg, "Sans", 8.8, bw - 18)
        bh = 19 + len(ls) * 10.8
        bx = x0 + (w0 - bw if own else 0)
        c.setFillColorRGB(*((0.85, 0.96, 0.78) if own else (1, 1, 1))); c.setStrokeColorRGB(0.8, 0.78, 0.72); c.setLineWidth(0.4)
        c.roundRect(bx, y - bh, bw, bh, 7, fill=1, stroke=1); c.setFillGray(0)
        nmcol = {"Marco": (0.8, 0.45, 0.1), "Siggi": (0.6, 0.2, 0.6), "Mark": (0.1, 0.5, 0.45),
                 "Sven": (0.2, 0.35, 0.75), "Rita": (0.75, 0.2, 0.3)}.get(who.split()[0], (0.2, 0.5, 0.2))
        fc(nmcol); c.setFont("SansB", 7.8); c.drawString(bx + 9, y - 11, "Ich" if own else who); c.setFillGray(0)
        yy = y - 21
        for l in ls:
            c.setFont("Sans", 8.8); c.drawString(bx + 9, yy, l); yy -= 10.8
        c.setFont("Sans", 7); c.setFillGray(0.4); c.drawRightString(bx + bw - 8, y - 11, t); c.setFillGray(0)
        y -= bh + 4
    new_page()


VOICE = ("SPRACHNACHRICHT · Abschrift\nVon: Holger Brandner · An: Dr. Kessler (Kanzlei) · Freitag, 25.09., 23:41 Uhr · 0:19\n"
         "„Kessler, ich bin's. Die Versammlung war ein Zirkus, aber egal. Ich geh gleich noch runter zum Steg. "
         "Da will mir jemand was zeigen. Angeblich was über den Platz, das den Preis ordentlich drückt. Wenn das "
         "stimmt, unterschreibt Böttcher am Montag zu unseren Bedingungen. Ruf mich morgen früh an.“")


def b3():
    flip(); akte_tab("blau")
    y = doc_head("B-3  ·  AKTE BLAU", "Auswertung Smartphone des Opfers",
                 "Kriminaltechnik Seebrück · Gerät aus dem Tretboot")
    y = text(ML, y, W - ML - MR - 30,
             "Das Handy von Holger Brandner war nass, ließ sich aber auslesen. Die letzte Aktivität vor dem "
             "Tod ist eine Sprachnachricht an seinen Anwalt. Die Technik hat sie abgeschrieben und als Code "
             "gesichert. Die Aufnahme selbst liegt im Ermittlerportal.", "Serif", 10.6, 15) - 10
    px, pw, ph = ML + 10, 210, 380
    py = y - ph
    c.setFillGray(0.12); c.roundRect(px, py, pw, ph, 26, fill=1, stroke=0)
    c.setFillGray(0.96); c.roundRect(px + 10, py + 14, pw - 20, ph - 28, 18, fill=1, stroke=0)
    c.setFillColorRGB(0.82, 0.9, 0.86); c.rect(px + 10, py + ph - 70, pw - 20, 42, fill=1, stroke=0); c.setFillGray(0)
    c.setFont("SansB", 10); c.drawString(px + 24, py + ph - 48, "Dr. Kessler (Kanzlei)")
    c.setFont("Sans", 7.5); c.drawString(px + 24, py + ph - 60, "zuletzt online Fr 23:58")
    by = py + ph - 140
    c.setFillColorRGB(0.85, 0.96, 0.78); c.roundRect(px + 40, by, pw - 64, 46, 10, fill=1, stroke=0); c.setFillColorRGB(0.2, 0.45, 0.3)
    p = c.beginPath(); p.moveTo(px + 54, by + 14); p.lineTo(px + 54, by + 32); p.lineTo(px + 68, by + 23); p.close()
    c.drawPath(p, fill=1, stroke=0)
    random.seed(2)
    for k in range(22):
        hgt = 3 + random.random() * 14
        c.rect(px + 76 + k * 4, by + 23 - hgt / 2, 2, hgt, fill=1, stroke=0)
    c.setFont("Sans", 7); c.drawString(px + 76, by + 5, "0:19"); c.drawRightString(px + pw - 30, by + 5, "23:41 ✓✓")
    c.setFont("SansB", 7.5); c.setFillGray(0.4); c.drawCentredString(px + pw / 2, by + 60, "FREITAG"); c.setFillGray(0)
    qx = px + pw + 30
    qw = W - MR - 20 - qx
    c.setFont("SansB", 12); c.drawString(qx, y - 30, "Abschrift der Technik")
    c.setFillColorRGB(0.95, 0.95, 0.93); c.setStrokeGray(0.6); c.setLineWidth(0.6)
    vt = VOICE.split("\n")[2]
    vh = lines_h(vt, "Mono", 9, qw - 20, 12.4) + 44
    c.rect(qx, y - 42 - vh, qw, vh, fill=1, stroke=1); c.setFillGray(0)
    c.setFont("MonoB", 7.4); c.drawString(qx + 10, y - 58, "Fr 25.09. · 23:41 Uhr · 0:19")
    text(qx + 10, y - 76, qw - 20, vt, "Mono", 9, 12.4, gap=0)
    yq = y - 42 - vh - 30
    c.setFont("SansB", 12); c.drawString(qx, yq, "Original anhören")
    text(qx, yq - 18, qw - 108, "Im Ermittlerportal. Ihr dürft sie Akte Rot vorspielen.", "Serif", 10, 14)
    qr(qx + qw - 100, yq - 112, 100, PORTAL + "#b3", "portal")
    new_page()


def b4():
    flip(); akte_tab("blau")
    y = doc_head("B-4  ·  AKTE BLAU", "Social Media: @nova.on.wheels",
                 "Gesichert vom Profil von Nova Sommer, Gast auf Stellplatz G2")
    y = text(ML, y, W - ML - MR - 30,
             "Frau Sommer postet fast jeden Abend eine „Story“ – kurze Fotos, die nach 24 Stunden wieder "
             "verschwinden. Wir haben sie vorher gesichert. Sie liegen im Ermittlerportal als Spur B-4.\n"
             "Aussage Nova Sommer, Samstag, 8:15 Uhr: „Ich mach jeden Abend ein paar Storys, das ist mein Job. "
             "Was drauf ist, sehen Sie ja selbst. Den Herrn Brandner fand ich ehrlich gesagt ganz okay. "
             "Er hat mir gesagt, für Vans gibt's im Resort eine Sonderspur.“", "Serif", 10.6, 15.2) - 14
    c.setStrokeGray(0); c.setLineWidth(1); c.rect(ML, y - 210, W - ML - MR - 30, 210, fill=0, stroke=1)
    c.setFont("SansB", 13); c.drawString(ML + 16, y - 28, "Spur B-4 im Ermittlerportal")
    text(ML + 16, y - 50, 240,
         "1. Code scannen.\n2. Kennwort aus dem Brief eingeben.\n3. „Spur B-4“ öffnen und die beiden "
         "Fotos genau ansehen: Uhrzeit, Ort, Licht, was passiert.\nWas ihr seht, beschreibt ihr Akte Rot.",
         "Serif", 10.4, 14.6, gap=3)
    qr(W - MR - 30 - 150, y - 186, 136, PORTAL + "#b4", "portal")
    new_page()


NOTES = [
    (0.0, "BOOTSVERLEIH", "Tretboote „Kevin“ und „Chantal“ (neu, Kunststoff). Schlüssel an der Rezeption. "
     "Fahrten nur 9 bis 19 Uhr. Nachts sind die Boote angekettet!\n– Marco", 2),
    (1.0, "WICHTIG", "Die Holzbank am Badestrand wurde abgebaut (morsch). Am Strand gibt es jetzt nur "
     "noch Sand und Kunststoffliegen.\n– Die Platzleitung", -2),
    (0.0, "Brötchenservice", "Bestellschluss: 18 Uhr am Vortag. Wer später kommt, bekommt Knäckebrot.\n– Rita", -1.5),
    (1.0, "GEFUNDEN", "1 Grillzange. Abzuholen bei Siggi, Parzelle 14.\n(Ist wahrscheinlich meine.)", 1.5),
    (0.0, "NACHTRUHE 22–7 UHR", "Wird kontrolliert!!!\n– Sicherheitsdienst S. Ruppert", 1),
    (1.0, "VERMISST", "Wer hat meinen Gartenzwerg „Hubert“ gesehen? Rote Mütze, freundlicher Blick.\n– Angelika, P7", -2.5),
]


def b5():
    flip(); akte_tab("blau")
    y = doc_head("B-5  ·  AKTE BLAU", "Das Schwarze Brett an der Rezeption",
                 "Fotografiert am Samstag, 26.09., 8:00 Uhr")
    # Foto der Pinnwand, auf Rahmen beschnitten; Zettel liegen auf dem Kork
    CROP = (290 / 1448, 280 / 1086, 1160 / 1448, 960 / 1086)
    bw0 = W - ML - MR
    bh0 = bw0 * (870 / 680) ** -1
    by0 = y - bh0
    photo("brett.jpg", ML, by0, bw0, bh0, crop=CROP, border=False)
    # Korkfläche im Ausschnitt (Anteile vom Ausschnitt)
    kx0, kx1 = ML + 0.075 * bw0, ML + 0.925 * bw0
    ky1 = by0 + (1 - 0.095) * bh0
    NOTECOL = [(1, 0.96, 0.6), (0.99, 0.82, 0.86), (0.82, 0.92, 1), (1, 1, 1), (0.85, 0.96, 0.8), (1, 0.9, 0.7)]
    ni = [0]
    gapx = 12
    colw = (kx1 - kx0 - 3 * gapx) / 2
    ys = [ky1 - 10, ky1 - 10]
    for colk, head, body, ang in NOTES:
        col = int(colk)
        nx = kx0 + gapx + col * (colw + gapx)
        ls_h = lines_h(body, "SerifI", 9.2, colw - 24, 12)
        nh = ls_h + 38
        ny = ys[col] - nh
        c.saveState(); c.translate(nx + colw / 2, ny + nh / 2); c.rotate(ang)
        c.setFillColorRGB(0.2, 0.12, 0.05); c.setFillAlpha(0.35); c.rect(-colw / 2 + 3, -nh / 2 - 3, colw, nh, fill=1, stroke=0)
        c.setFillAlpha(1)
        fc(NOTECOL[ni[0] % 6]); ni[0] += 1; c.rect(-colw / 2, -nh / 2, colw, nh, fill=1, stroke=0)
        fc(ROT); c.circle(0, nh / 2 - 7, 3.5, fill=1, stroke=0); c.setFillGray(0)
        c.setFont("SansB", 9.6); c.drawString(-colw / 2 + 11, nh / 2 - 24, head)
        text(-colw / 2 + 11, nh / 2 - 38, colw - 24, body, "SerifI", 9.2, 12, gap=1)
        c.restoreState()
        ys[col] = ny - 8
    c.setFont("Sans", 7.5); c.setFillGray(0.35)
    c.drawString(ML, by0 - 14, "Lichtbild: Spurensicherung Seebrück. Die Zettel hingen genau so am Brett.")
    c.setFillGray(0)
    new_page()


# ================= Gemeinsame Seiten hinten =================
def sheet_page():
    y = doc_head("FÜR BEIDE", "Ermittlerbogen", "Hier sammelt ihr gemeinsam. Kopieren erlaubt.")
    c.setStrokeGray(0); c.setLineWidth(1)
    rows = [("Was wir sicher wissen", 6), ("Offene Fragen", 4)]
    for h, n in rows:
        c.setFont("SansB", 11); c.drawString(ML, y, h); y -= 10
        for k in range(n):
            y -= 22; c.setStrokeGray(0.6); c.setLineWidth(0.5); c.line(ML, y, W - MR, y)
        y -= 26
    c.setFont("SansB", 11); c.setFillGray(0); c.drawString(ML, y, "Geheimer Hauptverdacht nach Akt 1"); y -= 12
    bw = (W - ML - MR - 20) / 2
    for k, lab in enumerate(["◆  ROT", "●  BLAU"]):
        x = ML + k * (bw + 20)
        sc(ROT if k == 0 else BLAU); c.setLineWidth(1.6); c.rect(x, y - 92, bw, 92, fill=0, stroke=1)
        fc(ROT if k == 0 else BLAU); c.setFont("SansB", 10); c.drawString(x + 10, y - 18, lab); c.setFillGray(0)
        c.setFont("Sans", 8.5); c.setFillGray(0.4)
        c.drawString(x + 10, y - 32, "Name aufschreiben, Ecke umknicken, nicht zeigen!")
        c.setFillGray(0)
        c.setStrokeGray(0.6); c.setLineWidth(0.5); c.line(x + 10, y - 66, x + bw - 10, y - 66)
    y -= 120
    c.setFont("SansB", 11); c.drawString(ML, y, "Punkte Akt 1"); y -= 18
    for lab in ["Start", "falsche Codes  × (−2)", "geöffnete Hinweisstufen  × (−1)", "Punkte nach Akt 1"]:
        c.setFont("Serif", 10.5); c.drawString(ML, y, lab)
        c.setStrokeGray(0.4); c.rect(ML + 230, y - 5, 60, 18, fill=0, stroke=1)
        if lab == "Start":
            c.setFont("SansB", 10.5); c.drawCentredString(ML + 260, y, "10")
        y -= 26
    new_page()


def section_short(a, b, cc):
    if (a, b, cc) == RIGHT:
        return ("Richtig!", "Weiter: Seite 22")
    for k, (x, r) in enumerate(zip((a, b, cc), RIGHT), 1):
        if x != r:
            return ("Leider falsch.", f"Prüft Frage {k}")


VALUES = [("Frage 1 · Wo?", [("am Badestrand", 0), ("am Bootssteg", 16), ("im Tretboot", 32)]),
          ("Frage 2 · Wann?", [("21:30 – 23:00 Uhr", 0), ("23:30 – 0:30 Uhr", 4), ("0:30 – 2:00 Uhr", 8), ("nach 2:00 Uhr", 12)]),
          ("Frage 3 · Was fehlt?", [("Handy", 1), ("Brieftasche", 2), ("rote Ledermappe", 3), ("Autoschlüssel", 4)])]


def code_page():
    y = doc_head("FÜR BEIDE", "Code-Prüfung Akt 1", "Mit Handy im Portal – ohne Handy hier in vier Schritten")
    tw = W - ML - MR - 120

    def step(n, title, yy):
        fc(NIGHT); c.circle(ML + 9, yy + 4, 9, fill=1, stroke=0)
        c.setFillGray(1); c.setFont("SansB", 10); c.drawCentredString(ML + 9, yy, str(n)); c.setFillGray(0)
        c.setFont("SansB", 11); c.drawString(ML + 26, yy, title)
        return yy - 18

    y = step(1, "Antworten aussuchen", y)
    y = text(ML + 26, y, tw - 26, "Einigt euch auf je eine Antwort zu den drei Fragen von Seite 4.", "Serif", 10, 13.6) - 4
    y = step(2, "Wert jeder Antwort ablesen", y)
    colw = (W - ML - MR - 26 - 20 - 112) / 3
    top = y
    qr(W - MR - 94, top - 94, 94, PORTAL + "#code", "portal")
    for k, (h, vals) in enumerate(VALUES):
        x = ML + 26 + k * (colw + 10)
        c.setFillColorRGB(0.92, 0.94, 0.97); c.rect(x, top - 18, colw, 18, fill=1, stroke=0); c.setFillGray(0)
        c.setFont("SansB", 9); c.drawString(x + 6, top - 13, h)
        yy = top - 32
        for i, (lab, v) in enumerate(vals, 1):
            c.setFont("SansB", 9); c.drawString(x + 6, yy, f"{i}")
            c.setFont("Serif", 9); c.drawString(x + 16, yy, lab)
            c.setFont("MonoB", 10); c.drawRightString(x + colw - 6, yy, str(v))
            c.setStrokeGray(0.85); c.setLineWidth(0.4); c.line(x + 4, yy - 4, x + colw - 4, yy - 4)
            yy -= 15
    y = top - 32 - 4 * 15 - 22
    y = step(3, "Die drei Werte zusammenzählen", y)
    bx = ML + 26
    c.setStrokeGray(0); c.setLineWidth(1)
    for i, lab in enumerate(["Frage 1", "Frage 2", "Frage 3"]):
        x = bx + i * 92
        c.rect(x, y - 26, 56, 26, fill=0, stroke=1)
        c.setFont("Sans", 7); c.setFillGray(0.4); c.drawCentredString(x + 28, y - 36, lab); c.setFillGray(0)
        c.setFont("SansB", 14); c.drawCentredString(x + 74, y - 18, "+" if i < 2 else "=")
    x = bx + 3 * 92 - 4
    c.setLineWidth(2); c.rect(x, y - 28, 70, 30, fill=0, stroke=1)
    c.setFont("Sans", 7); c.setFillGray(0.4); c.drawCentredString(x + 35, y - 38, "euer Abschnitt"); c.setFillGray(0)
    y -= 52
    c.setFont("SerifI", 9.6); c.setFillGray(0.3)
    c.drawString(bx, y, "Beispiel: am Badestrand (0) + nach 2:00 Uhr (12) + Handy (1) = 13 → ihr lest nur Abschnitt 13.")
    c.setFillGray(0)
    y -= 22
    y = step(4, "Nur euren Abschnitt lesen", y)
    cols, rows = 8, 6
    gw = (W - ML - MR) / cols; gh = 34
    for k in range(48):
        n = k + 1
        a_, b_, c_ = (k // 16) + 1, (k % 16) // 4 + 1, k % 4 + 1
        h1, h2 = section_short(a_, b_, c_)
        col, row = k % cols, k // cols
        x = ML + col * gw; yy = y - row * gh
        c.setStrokeGray(0.6); c.setLineWidth(0.5); c.rect(x, yy - gh, gw, gh, fill=0, stroke=1)
        c.setFont("SansB", 11); c.drawString(x + 4, yy - 14, str(n))
        c.setFont("Sans", 6.6); c.drawString(x + 4, yy - 23, h1); c.drawString(x + 4, yy - 31, h2)
    new_page()


HINTS = [
    (14, "Frage 1 · Stufe 1", "Schaut genau, was in der Kopfwunde gefunden wurde. Wo auf dem Platz gibt es genau dieses Material?"),
    (31, "Frage 1 · Stufe 2", "Das Tretboot ist aus Kunststoff. Akte Blau weiß, welches Holz in dieser Woche grau gestrichen wurde – und was am Badestrand fehlt."),
    (8,  "Frage 1 · Stufe 3", "Antwort 2: der Bootssteg. Die grau lasierten Lärchensplitter stammen vom frisch gestrichenen Steg."),
    (22, "Frage 2 · Stufe 1", "Wer hat den Steg in der Nacht gesehen? Und wann fehlte das Boot zum ersten Mal?"),
    (5,  "Frage 2 · Stufe 2", "Brandner hat um 23:41 Uhr noch eine Sprachnachricht geschickt. Das Platschen um 1:30 Uhr hat eine harmlose Erklärung in Novas Story."),
    (36, "Frage 2 · Stufe 3", "Antwort 2: zwischen 23:30 und 0:30 Uhr. Um 23:41 lebte er noch, um 0:30 war das Boot weg."),
    (29, "Frage 3 · Stufe 1", "Vergleicht, was Brandner am Abend bei sich hatte, mit dem, was die Polizei gefunden hat."),
    (17, "Frage 3 · Stufe 2", "Das Versammlungsprotokoll nennt einen Gegenstand, der auf der Fundliste fehlt."),
    (3,  "Frage 3 · Stufe 3", "Antwort 3: die rote Ledermappe mit dem Vorvertrag."),
]


def hints_page():
    y = doc_head("FÜR BEIDE", "Hinweise Akt 1", "Sucht in der Übersicht die Nummer und lest nur dieses eine Kästchen.")
    c.setFont("SansB", 10); c.drawString(ML, y, "Übersicht")
    y -= 16
    for k, q in enumerate(["Frage 1", "Frage 2", "Frage 3"]):
        nums = [h[0] for h in HINTS if h[1].startswith(q)]
        c.setFont("Serif", 10.4)
        c.drawString(ML, y, f"{q}:   Stufe 1 → Kästchen {nums[0]}    Stufe 2 → Kästchen {nums[1]}    Stufe 3 → Kästchen {nums[2]}")
        y -= 16
    y -= 10
    colw = (W - ML - MR - 16) / 2
    items = sorted(HINTS)
    ys = [y, y]
    for i, (n, lab, t) in enumerate(items):
        col = i % 2
        x = ML + col * (colw + 16)
        hh = lines_h(t, "Serif", 9.6, colw - 52, 13) + 24
        yy = ys[col]
        c.setStrokeGray(0); c.setLineWidth(0.8); c.rect(x, yy - hh, colw, hh, fill=0, stroke=1)
        fc(NIGHT); c.rect(x, yy - hh, 34, hh, fill=1, stroke=0)
        c.setFillGray(1); c.setFont("SansB", 14); c.drawCentredString(x + 17, yy - hh / 2 - 5, str(n)); c.setFillGray(0)
        text(x + 44, yy - 16, colw - 52, t, "Serif", 9.6, 13, gap=0)
        ys[col] = yy - hh - 10
    new_page()


SOLUTION = [
    ("Wo?  Am Bootssteg.", "In der Kopfwunde stecken grau lasierte Lärchensplitter (R-1). Das Tretboot ist aus "
     "Kunststoff (R-1, B-5), die Holzbank am Badestrand wurde abgebaut (B-5). Grau lasierte Lärche gibt es nur an "
     "einer Stelle: am Steg, den Marco am Donnerstag gestrichen hat (B-2). Brandner wurde am Steg niedergeschlagen, "
     "fiel ins Wasser und ertrank. Der Südwestwind (R-5) trieb das losgemachte Boot und ihn hinüber ins Schilf."),
    ("Wann?  Zwischen 23:30 und 0:30 Uhr.", "Um 23:30 waren beide Boote angekettet (R-3). Um 23:41 schickte Brandner "
     "noch die Sprachnachricht: „Ich geh gleich noch runter zum Steg“ (B-3). Um 0:30 fehlte die „Chantal“ (R-3). "
     "Das laute Platschen um 1:30 Uhr (R-4) war Novas Hund Pepper (B-4, Story 1:28 Uhr) – eine falsche Fährte."),
    ("Was fehlt?  Die rote Ledermappe.", "Brandner hatte die Mappe mit dem Vorvertrag am Abend unter dem Arm (B-1, B-2). "
     "Auf der Fundliste taucht sie nicht auf (R-2). Brieftasche, Geld, Handy und Autoschlüssel sind da. Wer auch immer am "
     "Steg war, wollte kein Geld – er wollte die Mappe."),
]


def solution_page():
    y = doc_head("AUFLÖSUNG AKT 1", "Was in dieser Nacht passiert ist", "Erst lesen, wenn ihr den richtigen Code habt.")
    for h, t in SOLUTION:
        fc(ROT); c.setFont("SansB", 12.5); c.drawString(ML, y, h); c.setFillGray(0)
        y = text(ML, y - 18, W - ML - MR - 10, t, "Serif", 10.4, 14.6) - 10
    y -= 4
    bh = y - 60
    fc(NIGHT); c.rect(ML, y - bh, W - ML - MR, bh, fill=1, stroke=0); c.setFillGray(1)
    c.setFont("SansB", 9); c.setFillColorRGB(1, 0.8, 0.35); c.drawString(ML + 16, y - 22, "WIE ES WEITERGEHT"); c.setFillGray(1)
    c.setFont("SansB", 13); c.drawString(ML + 16, y - 40, "Wendland klappt die Akte zu.")
    yy = text(ML + 16, y - 60, W - ML - MR - 32,
              "„Gute Arbeit. Damit steht fest: Das war kein Unfall und kein Raub. Jemand hat Holger Brandner nachts "
              "an den Steg gelockt – und ist mit der roten Mappe verschwunden. Drei Dinge lassen mich nicht los: "
              "Wer hatte einen Schlüssel für das Kettenschloss? Wer lief um 23:12 Uhr mit der Taschenlampe vor der "
              "Rezeption herum? Und was wollte jemand Brandner zeigen, das den Preis ‚ordentlich drückt‘? "
              "Ab morgen früh spreche ich mit jedem Einzelnen auf diesem Platz. Einer von ihnen wird lügen.“",
              "SerifI", 10.4, 14.6, gray=1) - 6
    c.setFillGray(1); c.setFont("SansB", 10.5); c.drawString(ML + 16, yy, "Bevor ihr weiterspielt")
    yy -= 18
    for i, t in enumerate(["Jeder schreibt geheim seinen Hauptverdacht auf den Ermittlerbogen (Seite 18) und knickt die Ecke um.",
                           "Tragt eure Punkte nach Akt 1 ein.",
                           "Gönnt euch eine Pause. In Akt 2 „Wer lügt?“ nehmt ihr die Verdächtigen ins Verhör."], 1):
        c.setFillColorRGB(1, 0.8, 0.35); c.setFont("SansB", 10); c.drawString(ML + 16, yy, f"{i}.")
        yy = text(ML + 32, yy, W - ML - MR - 50, t, "Serif", 10, 13.6, gray=1, gap=4)
    c.setFillGray(0.75); c.setFont("Sans", 8.5); c.drawString(ML + 16, y - bh + 14, "Ende des Prototyps · Akt 2 folgt")
    c.setFillGray(0)
    new_page()


title_page()                       # 1
rules_page(); letter_page()        # 2 | 3
task_page(); cast_page()           # 4 | 5
map_page(); seat_page()            # 6 | 7
for r, b in [(r1, b1), (r2, b2), (r3, b3), (r4, b4), (r5, b5)]:
    r(); b()                       # 8 | 9 … 16 | 17
sheet_page(); code_page()          # 18 | 19
hints_page(); notes_page()         # 20 | 21
solution_page()                    # 22
c.save()
print("Seiten:", PAGE[0] - 1)

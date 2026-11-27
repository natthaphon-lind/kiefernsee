"""Buchseiten für Akt 2 „Wer lügt?“ (Seite 25–44). Nutzt die Helfer aus build_farbe."""
import random
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
import akt2_data as A

B = None
c = None


def _init(mod):
    global B, c
    B, c = mod, mod.c


def qa_block(y, rows, w=None, size=10, lead=14):
    w = w or (B.W - B.ML - B.MR - 40)
    for who, t in rows:
        c.setFont("MonoB", size + 0.2); c.drawString(B.ML, y, who + ":")
        y = B.text(B.ML + 30, y, w - 30, t, "MonoB" if who == "F" else "Mono", size, lead, gap=0) - 7
    return y


def head_line(y, s, size=8.6):
    for ln in simpleSplit(s, "Mono", size, B.W - B.ML - B.MR - 40):
        c.setFont("Mono", size); c.setFillGray(0.35); c.drawString(B.ML, y, ln); y -= size * 1.35
    c.setFillGray(0)
    return y - 6


def sealed_box(x, y, w, h, title, body, anchor, qsize=96):
    """Versiegelter Umschlag mit QR-Code zur Web-App."""
    c.setFillColorRGB(0.96, 0.93, 0.86); c.setStrokeColorRGB(0.6, 0.5, 0.35); c.setLineWidth(1)
    c.rect(x, y - h, w, h, fill=1, stroke=1)
    c.setStrokeColorRGB(0.75, 0.66, 0.5); c.setLineWidth(0.8)
    c.line(x, y, x + w / 2, y - h * 0.38); c.line(x + w, y, x + w / 2, y - h * 0.38)
    B.fc(B.ROT); c.circle(x + w / 2, y - h * 0.38, 20, fill=1, stroke=0)
    c.setFillGray(1); c.setFont("SansB", 15); c.drawCentredString(x + w / 2, y - h * 0.38 - 5, "★"); c.setFillGray(0)
    B.stamp(x + 92, y - 28, "VERSIEGELT", 5, 12)
    c.setFont("SansB", 12.5); c.drawString(x + 16, y - h * 0.38 - 46, title)
    B.text(x + 16, y - h * 0.38 - 64, w - 32 - qsize - 20, body, "Serif", 10.2, 14)
    B.qr(x + w - qsize - 16, y - h + 30, qsize, B.PORTAL + "#" + anchor, "portal")


# ---------------- Einstieg ----------------
def opener():
    y = B.H - B.MT - 10
    c.setFont("SansB", 9); c.setFillGray(0.45); c.drawString(B.ML, y, "AKT 2  ·  FÜR BEIDE"); c.setFillGray(0)
    y -= 46; c.setFont("SansB", 38); c.drawString(B.ML, y, A.TITLE)
    y -= 22; c.setFont("SerifI", 12); c.setFillGray(0.3); c.drawString(B.ML, y, "Die Vernehmungen · " + A.DATE_LINE); c.setFillGray(0)
    y -= 30
    bw = B.W - B.ML - B.MR
    c.setFillColorRGB(0.99, 0.98, 0.94); c.setStrokeGray(0.75); c.setLineWidth(0.6)
    bh = B.lines_h(A.LAGEBERICHT, "Serif", 10.8, bw - 50, 15.6) + 4 * 8 + 110
    c.rect(B.ML, y - bh, bw, bh, fill=1, stroke=1); c.setFillGray(0)
    c.setFont("FormB", 8.6); c.setFillGray(0.4)
    c.drawString(B.ML + 24, y - 22, "KRIMINALPOLIZEI SEEBRÜCK  ·  AZ 31 Js 0926/BR  ·  LAGEBERICHT NR. 2"); c.setFillGray(0)
    yy = B.text(B.ML + 24, y - 48, bw - 50, A.LAGEBERICHT, "Serif", 10.8, 15.6, gap=8)
    B.fc(B.INK); c.setFont("SerifBI", 17); c.drawString(B.ML + 24, yy - 14, "J. Wendland"); c.setFillGray(0)
    c.setFont("Form", 9); c.drawString(B.ML + 24, yy - 30, "Jutta Wendland, Erste Kriminalhauptkommissarin")
    B.stamp(B.W - B.MR - 110, y - bh + 40, "AKT 2", -5, 16)
    B.new_page()


def task():
    y = B.doc_head("AKT 2  ·  FÜR BEIDE", "Wer lügt?", "Euer Auftrag für Akt 2")
    y = B.text(B.ML, y, B.W - B.ML - B.MR,
               "Blättert wie in Akt 1 durch die Akten (Seite 28 bis 39): links Rot, rechts Blau. Neu sind die versiegelten "
               "Akten – ihr öffnet sie in der Web-App mit einem Rätsel. Dafür braucht ihr fast immer eine Spur vom anderen.",
               "Serif", 10.6, 15) - 6
    for (k, qq, opts) in A.Q:
        bh = 30 + len(opts) * 22 + 10
        c.setStrokeGray(0); c.setLineWidth(1); c.rect(B.ML, y - bh, B.W - B.ML - B.MR, bh, fill=0, stroke=1)
        c.setFont("SansB", 9); c.setFillGray(0.4); c.drawString(B.ML + 14, y - 18, k.upper()); c.setFillGray(0)
        c.setFont("SansB", 12); c.drawString(B.ML + 80, y - 18, qq)
        yy = y - 44
        for i, o in enumerate(opts, 1):
            c.setLineWidth(0.8); c.rect(B.ML + 80, yy - 3, 11, 11, fill=0, stroke=1)
            c.setFont("SansB", 10.5); c.drawString(B.ML + 100, yy, f"{i}")
            c.setFont("Serif", 10.6); c.drawString(B.ML + 116, yy, o)
            yy -= 22
        y -= bh + 14
    B.text(B.ML, y - 4, B.W - B.ML - B.MR,
           "Habt ihr euch auf alle drei Antworten geeinigt? Dann prüft sie in der Web-App – wie, steht auf Seite 41. "
           "Erst danach lest ihr die Auflösung.", "SerifI", 10.4, 14.5)
    B.new_page()


def howto():
    y = B.doc_head("AKT 2  ·  FÜR BEIDE", "Versiegelte Akten", "So öffnet ihr sie – drei Rätsel in diesem Akt")
    items = [
        ("R-8", "Die UV-Lampe", "Akte Rot scannt den Code bei R-8. In der Web-App fahrt ihr mit dem Finger eine UV-Lampe über das "
         "Zahlenfeld des Schlüsselkastens. Welche Tasten leuchten? In welcher Reihenfolge sie gehören, verrät eine Jahreszahl "
         "aus Akte Blau. Code eintippen – das Protokoll öffnet sich."),
        ("R-10", "Die alte Karte", "Akte Blau hat eine Karte von 1996 (B-7) und beschreibt sie. Akte Rot tippt bei R-10 in der "
         "Web-App auf die richtige Stelle im heutigen Luftbild – dann öffnet sich der Taucherbericht."),
        ("B-8", "Die Mailbox", "Akte Rot liest die Handynummer von der Visitenkarte vor (R-7). Akte Blau wählt sie bei B-8 in der "
         "Web-App und hört die Mailbox ab."),
    ]
    for no, t, d in items:
        h = B.lines_h(d, "Serif", 10.4, B.W - B.ML - B.MR - 120, 14.6) + 40
        c.setStrokeGray(0.75); c.setLineWidth(1); c.roundRect(B.ML, y - h, B.W - B.ML - B.MR, h, 6, fill=0, stroke=1)
        B.fc(B.NIGHT); c.roundRect(B.ML + 14, y - 40, 76, 24, 4, fill=1, stroke=0)
        c.setFillGray(1); c.setFont("SansB", 11); c.drawCentredString(B.ML + 52, y - 32, no); c.setFillGray(0)
        c.setFont("SansB", 13); c.drawString(B.ML + 104, y - 30, t)
        B.text(B.ML + 104, y - 48, B.W - B.ML - B.MR - 120, d, "Serif", 10.4, 14.6, gap=0)
        y -= h + 14
    c.setFillColorRGB(0.99, 0.95, 0.85); c.roundRect(B.ML, y - 112, B.W - B.ML - B.MR, 112, 6, fill=1, stroke=0); c.setFillGray(0)
    c.setFont("SansB", 11.5); c.drawString(B.ML + 14, y - 22, "Was ihr aus Akt 1 schon wisst")
    B.text(B.ML + 14, y - 40, B.W - B.ML - B.MR - 28,
           "Brandner wurde zwischen 23:30 und 0:30 Uhr am Bootssteg niedergeschlagen und ertrank. Die rote Mappe mit dem "
           "Vorvertrag fehlt. Das Kettenschloss war offen, aber nicht aufgebrochen. Um 23:12 Uhr stand jemand mit einer "
           "Taschenlampe vor der Rezeption. Das Platschen um 1:30 Uhr war Novas Hund.", "Serif", 10.2, 14.2)
    B.new_page()


# ---------------- AKTE ROT ----------------
def r6():
    B.akte_tab("rot")
    y = B.doc_head("R-6  ·  AKTE ROT", "Vernehmung Marco Lenz", "Hausmeister des Campingplatzes")
    y = head_line(y, A.MARCO_HEAD)
    y = qa_block(y, A.MARCO, size=9.6, lead=13.2)
    y -= 4
    c.setFont("Mono", 9.2); c.drawString(B.ML, y, "Selbst gelesen, genehmigt, unterschrieben:")
    B.fc(B.INK); c.setFont("SerifBI", 15); c.drawString(B.ML + 20, y - 22, "M. Lenz"); c.setFillGray(0)
    qs = 84
    B.qr(B.W - B.MR - 40 - qs, y - qs + 8, qs, B.PORTAL + "#r6", "portal")
    c.setFont("SansB", 9); c.drawRightString(B.W - B.MR - 40 - qs - 10, y - 20, "Tonaufnahme anhören")
    c.setFont("Serif", 8.6); c.drawRightString(B.W - B.MR - 40 - qs - 10, y - 33, "ihr dürft sie Akte Blau vorspielen")
    B.new_page()


def r7():
    B.akte_tab("rot")
    y = B.doc_head("R-7  ·  AKTE ROT", "Vernehmung Mark Böttcher", "Platzbetreiber")
    y = head_line(y, A.BOETTCHER_HEAD)
    y = qa_block(y, A.BOETTCHER, size=9.5, lead=13)
    # Visitenkarte
    cw, ch = 250, 140
    x0, y0 = B.ML + 30, max(y - 20 - ch, 70)
    c.saveState(); c.translate(x0 + cw / 2, y0 + ch / 2); c.rotate(-3)
    c.setFillColorRGB(0.2, 0.14, 0.08); c.setFillAlpha(0.25); c.rect(-cw / 2 + 4, -ch / 2 - 4, cw, ch, fill=1, stroke=0); c.setFillAlpha(1)
    c.setFillColorRGB(0.99, 0.99, 0.97); c.setStrokeGray(0.8); c.rect(-cw / 2, -ch / 2, cw, ch, fill=1, stroke=1)
    c.setFillColorRGB(0.12, 0.35, 0.22); c.rect(-cw / 2, ch / 2 - 10, cw, 10, fill=1, stroke=0)
    n, t1, t2, t3 = A.VISITENKARTE
    c.setFillGray(0.1); c.setFont("SansB", 15); c.drawString(-cw / 2 + 16, ch / 2 - 40, n)
    c.setFont("Sans", 9); c.setFillGray(0.35); c.drawString(-cw / 2 + 16, ch / 2 - 56, t1)
    c.setFillGray(0.2); c.setFont("Sans", 9); c.drawString(-cw / 2 + 16, -ch / 2 + 36, t2)
    c.setFont("SansB", 11); c.drawString(-cw / 2 + 16, -ch / 2 + 18, t3)
    c.restoreState(); c.setFillGray(0)
    B.text(x0 + cw + 30, y0 + ch - 10, B.W - B.MR - 40 - (x0 + cw + 30),
           "Die Visitenkarte gab Herr Böttcher bei der Vernehmung ab. Lest Akte Blau die Handynummer vor – damit öffnet "
           "sie seine Mailbox (B-8).", "SerifI", 10, 14)
    B.new_page()


def r8():
    B.akte_tab("rot")
    y = B.doc_head("R-8  ·  AKTE ROT", "Der Schlüsselkasten", "Flur der Rezeption · Spurensicherung, Samstag, 26.09.")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.KASTEN_INTRO, "Serif", 10.4, 14.6) - 6
    ph = 190; pw = ph * 1.5
    B.photo("kasten.jpg", B.ML + 5, y - ph, pw, ph, caption="Lichtbild 4: Schlüsselkasten im Flur der Rezeption")
    tx = B.ML + pw + 30; tw = B.W - B.MR - 40 - tx
    c.setFont("SansB", 11); c.drawString(tx, y - 10, "Inhalt am Samstag, 8:47 Uhr")
    yy = y - 28
    for f, s in A.KASTEN_FUND:
        c.setFont("FormB", 9); c.drawString(tx, yy, f.upper())
        yy = B.text(tx + 50, yy, tw - 50, s, "Form", 9, 12, gap=0) - 6
    y -= ph + 40
    sealed_box(B.ML, y, B.W - B.ML - B.MR - 40, 220, "Protokoll des Kastens – versiegelt",
               "Scannt den Code. Mit der UV-Lampe der Spurensicherung seht ihr, welche Tasten oft gedrückt werden. "
               "Die Reihenfolge verrät euch Herr Lenz (R-6) zusammen mit der Chronik in Akte Blau (B-10). "
               "Code eintippen – das Protokoll öffnet sich.", "r8")
    B.new_page()


def r9():
    B.akte_tab("rot")
    y = B.doc_head("R-9  ·  AKTE ROT", "Fundstück aus Mietchalet 3", "Asservat Nr. 9, Spurensicherung, Samstag, 26.09.")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.ZETTEL_INTRO, "Serif", 10.4, 14.6) - 14
    zw, zh = 300, 250
    x0 = B.ML + 60; y0 = y - zh - 10
    c.saveState(); c.translate(x0 + zw / 2, y0 + zh / 2); c.rotate(2.5)
    c.setFillColorRGB(0.2, 0.14, 0.08); c.setFillAlpha(0.22); c.rect(-zw / 2 + 5, -zh / 2 - 5, zw, zh, fill=1, stroke=0); c.setFillAlpha(1)
    c.setFillColorRGB(0.985, 0.985, 0.97); c.rect(-zw / 2, -zh / 2, zw, zh, fill=1, stroke=0)
    c.setStrokeColorRGB(0.72, 0.8, 0.88); c.setLineWidth(0.35)
    for k in range(int(zw / 10) + 1):
        c.line(-zw / 2 + k * 10, -zh / 2, -zw / 2 + k * 10, zh / 2 - 12)
    for k in range(int(zh / 10)):
        c.line(-zw / 2, -zh / 2 + k * 10, zw / 2, -zh / 2 + k * 10)
    # gerissene Oberkante mit grünem Rest
    random.seed(9)
    p = c.beginPath(); p.moveTo(-zw / 2, zh / 2 - 12)
    xx = -zw / 2
    while xx < zw / 2:
        xx += 6; p.lineTo(xx, zh / 2 - 12 + random.uniform(-3, 5))
    p.lineTo(zw / 2, zh / 2 + 6); p.lineTo(-zw / 2, zh / 2 + 6); p.close()
    c.setFillColorRGB(1, 1, 1); c.drawPath(p, fill=1, stroke=0)
    c.setFillColorRGB(0.12, 0.45, 0.25); c.setFont("SansB", 9.5); c.drawString(-zw / 2 + 8, zh / 2 - 22, A.ZETTEL_REST)
    c.setFillColorRGB(0.1, 0.2, 0.55)
    yy = zh / 2 - 52
    for i, ln in enumerate(A.ZETTEL):
        c.saveState(); c.translate(-zw / 2 + 22 + (i % 2) * 3, yy); c.rotate(random.uniform(-1.5, 1.5))
        c.setFont("MonoB", 15); c.drawString(0, 0, ln); c.restoreState()
        yy -= 34
    c.restoreState(); c.setFillGray(0)
    B.stamp(x0 + zw + 40, y0 + zh - 30, "ASSERVAT 9", 8, 11)
    yk = y0 - 30
    c.setFont("FormB", 9.5); c.drawString(B.ML, yk, "Kriminaltechnik:")
    B.text(B.ML + 96, yk, B.W - B.ML - B.MR - 136, A.ZETTEL_KT.replace("Kriminaltechnik: ", ""), "Form", 9.6, 13)
    B.new_page()


def r10():
    B.akte_tab("rot")
    y = B.doc_head("R-10  ·  AKTE ROT", "Taucherbericht der Feuerwehr", "Suche am Fundort, Samstag, 26.09.")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.TAUCHER_INTRO, "Serif", 10.6, 15) - 16
    sealed_box(B.ML, y, B.W - B.ML - B.MR - 40, 330, "Taucherbericht – versiegelt",
               "1. Akte Blau beschreibt euch die Karte von 1996 (B-7).\n2. Scannt den Code.\n3. Tippt im Luftbild auf die Stelle, "
               "an der früher das Fasslager war.\nLiegt ihr richtig, öffnet sich der Bericht mit Foto.", "r10", qsize=110)
    B.new_page()


def r11():
    B.akte_tab("rot")
    y = B.doc_head("R-11  ·  AKTE ROT", "Spuren auf dem Steg", "Spurensicherung Samstag 7:40 Uhr · Befragung Siggi Kowalski")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.STEG_INTRO, "Serif", 10.2, 14) - 6
    ph = 170; pw = ph * 1.5
    B.photo("steg_spuren.jpg", B.ML + 5, y - ph, pw, ph, caption="Lichtbild 5: Abdrücke in der Lasur, Stegende")
    tx = B.ML + pw + 26; tw = B.W - B.MR - 40 - tx
    yy = y - 6
    for lab, s in A.STEG_SPUREN:
        c.setFont("FormB", 9); c.drawString(tx, yy, lab.upper())
        yy = B.text(tx, yy - 12, tw, s, "Form", 8.6, 11.4, gap=0) - 7
    y = min(y - ph - 34, yy - 10)
    rule(y + 10)
    c.setFont("SansB", 11); c.drawString(B.ML, y - 6, "Befragung Siggi Kowalski")
    y = head_line(y - 22, A.SIGGI_HEAD, 8.2)
    qa_block(y, A.SIGGI, size=9.2, lead=12.6)
    B.new_page()


def rule(y):
    c.setStrokeGray(0.75); c.setLineWidth(0.6); c.line(B.ML, y, B.W - B.MR - 40, y)


# ---------------- AKTE BLAU ----------------
def b6():
    B.flip(); B.akte_tab("blau")
    y = B.doc_head("B-6  ·  AKTE BLAU", "Aus dem Archiv der Rezeption", "Bodengutachten von 1996 (Auszug)")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.GUTACHTEN_HEAD, "SerifI", 10.2, 14) - 8
    bw = B.W - B.ML - B.MR - 40
    c.setFillColorRGB(0.97, 0.95, 0.88); c.setStrokeGray(0.6)
    rows_h = sum(max(B.lines_h(v, "Mono", 9.4, bw - 150, 13), 13) + 12 for _, v in A.GUTACHTEN) + 110
    c.rect(B.ML, y - rows_h, bw, rows_h, fill=1, stroke=1); c.setFillGray(0)
    c.setFont("MonoB", 10.5); c.drawCentredString(B.ML + bw / 2, y - 24, "INGENIEURBÜRO HARTWIG · SEEBRÜCK")
    c.setFont("Mono", 8.5); c.drawCentredString(B.ML + bw / 2, y - 38, "Baugrund · Altlasten · Gewässer")
    yy = y - 62
    for k, v in A.GUTACHTEN:
        c.setFont("MonoB", 9.2); c.drawString(B.ML + 16, yy, k + ":")
        yy = B.text(B.ML + 130, yy, bw - 150, v, "Mono", 9.4, 13, gap=0) - 10
    c.saveState(); c.translate(B.ML + bw - 210, y - rows_h + 26); c.rotate(4)
    c.setFillColorRGB(0.35, 0.35, 0.38); c.setFont("SerifBI", 12); c.drawString(0, 0, A.GUTACHTEN_NOTE.split(": ", 1)[1])
    c.restoreState(); c.setFillGray(0)
    c.setFont("Sans", 8); c.setFillGray(0.4); c.drawString(B.ML, y - rows_h - 14, A.GUTACHTEN_NOTE.split(":")[0] + " (unten rechts)."); c.setFillGray(0)
    B.new_page()


def b7():
    B.flip(); B.akte_tab("blau")
    y = B.doc_head("B-7  ·  AKTE BLAU", "Anlage 3: Lageplan von 1996", "Von Hand gezeichnet, Ingenieurbüro Hartwig")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.KARTE_INTRO, "Serif", 10.2, 14) - 10
    mw = B.W - B.ML - B.MR - 40; mh = min(y - 80, mw * 0.95)
    x0, y0 = B.ML, y - mh
    c.setFillColorRGB(0.95, 0.92, 0.82); c.setStrokeColorRGB(0.5, 0.42, 0.3); c.setLineWidth(1.2)
    c.rect(x0, y0, mw, mh, fill=1, stroke=1)
    ink = (0.22, 0.2, 0.35)

    def P(u, v):
        return x0 + u * mw, y0 + (1 - v) * mh
    # See (wie im Luftbild: oben rechts)
    pts = [(0.5, 0.11), (0.62, 0.09), (0.8, 0.1), (1.0, 0.12), (1.0, 0.56), (0.9, 0.6), (0.75, 0.56), (0.6, 0.48), (0.52, 0.38), (0.5, 0.25)]
    p = c.beginPath(); p.moveTo(*P(*pts[0]))
    for q in pts[1:]:
        p.lineTo(*P(*q))
    p.close()
    c.setFillColorRGB(0.78, 0.86, 0.9); c.setStrokeColorRGB(*ink); c.setLineWidth(1.1); c.drawPath(p, fill=1, stroke=1)
    # Wellen
    c.setStrokeColorRGB(0.45, 0.6, 0.72); c.setLineWidth(0.6)
    for (u, v) in [(0.72, 0.25), (0.82, 0.4), (0.66, 0.38), (0.9, 0.2)]:
        a, b = P(u, v); c.bezier(a, b, a + 8, b + 4, a + 16, b - 4, a + 24, b)
    # Schilf oben (Nordufer) und Nordostecke
    c.setStrokeColorRGB(0.3, 0.45, 0.25); c.setLineWidth(0.7)
    random.seed(4)
    for k in range(70):
        u = 0.5 + random.random() * 0.5; v = 0.09 + random.random() * 0.05
        a, b = P(u, v); c.line(a, b, a + random.uniform(-2, 2), b + 7)
    for k in range(40):
        u = 0.8 + random.random() * 0.19; v = 0.12 + random.random() * 0.1
        a, b = P(u, v); c.line(a, b, a + random.uniform(-2, 2), b + 7)
    c.setFillColorRGB(*ink); c.setFont("SerifI", 9); c.drawString(*P(0.56, 0.16), "Schilf")
    # Tankstelle + Fasslager (Nordost)
    tx, ty = P(0.84, 0.045)
    c.setStrokeColorRGB(*ink); c.setLineWidth(1); c.setFillColorRGB(0.9, 0.85, 0.72)
    c.rect(tx - 10, ty - 6, 34, 18, fill=1, stroke=1)
    c.setFillColorRGB(*ink); c.setFont("SerifBI", 9); c.drawRightString(tx - 16, ty, "Bootstankstelle (1990–95)")
    fx, fy = P(0.89, 0.18)
    c.setStrokeColorRGB(0.65, 0.1, 0.1); c.setLineWidth(2)
    c.line(fx - 8, fy - 8, fx + 8, fy + 8); c.line(fx - 8, fy + 8, fx + 8, fy - 8)
    c.setFillColorRGB(0.65, 0.1, 0.1); c.setFont("SerifBI", 10); c.drawRightString(fx - 14, fy - 4, "Fasslager im Schilf")
    c.setFont("SerifI", 8); c.drawRightString(fx - 14, fy - 16, "„ca. 12 Fässer – nicht betreten“")
    c.setFillColorRGB(0.3, 0.45, 0.6); c.setFont("SerifBI", 15); c.drawString(*P(0.68, 0.36), "Kiefernsee")
    # Bäume (Wald am Westrand)
    c.setStrokeColorRGB(0.3, 0.45, 0.25); c.setLineWidth(0.7)
    random.seed(7)
    for k in range(26):
        u = random.uniform(0.02, 0.4); v = random.uniform(0.2, 0.36)
        a, b = P(u, v); c.circle(a, b, 5, fill=0, stroke=1)
    # Steg (Westufer des Sees)
    sx, sy = P(0.47, 0.25)
    c.setStrokeColorRGB(*ink); c.setLineWidth(3); c.line(sx, sy, sx + 0.12 * mw, sy)
    c.setFillColorRGB(*ink); c.setFont("SerifI", 9); c.drawString(sx + 4, sy + 6, "Steg")
    # Gaststätte oben links
    gx, gy = P(0.06, 0.1)
    c.setLineWidth(1); c.setFillColorRGB(0.9, 0.85, 0.72); c.rect(gx, gy - 20, 70, 28, fill=1, stroke=1)
    c.setFillColorRGB(*ink); c.setFont("SerifI", 9); c.drawString(gx + 4, gy - 30, "Gaststätte")
    # Badestrand
    c.setFont("SerifI", 9); c.drawString(*P(0.58, 0.62), "Strand")
    # Zeltwiese / Dauercamper links
    c.setFont("SerifI", 9); c.drawString(*P(0.08, 0.45), "Zeltwiese")
    c.setFont("SerifI", 9); c.drawString(*P(0.1, 0.62), "(später Dauerparzellen)")
    # Zufahrt unten links
    c.setStrokeColorRGB(*ink); c.setLineWidth(0.8); c.setDash(4, 3)
    a, b = P(0.18, 1.0); a2, b2 = P(0.18, 0.72); c.line(a, b, a2, b2); c.setDash()
    c.setFont("SerifI", 9); c.drawString(*P(0.2, 0.94), "Zufahrt / Rezeption")
    # Nordpfeil
    nx, ny = P(0.06, 0.92)
    c.setLineWidth(1); c.line(nx, ny - 14, nx, ny + 14)
    p = c.beginPath(); p.moveTo(nx, ny + 18); p.lineTo(nx - 5, ny + 8); p.lineTo(nx + 5, ny + 8); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.setFont("SerifB", 10); c.drawCentredString(nx, ny + 22, "N")
    c.setFont("SerifI", 8); c.drawRightString(x0 + mw - 8, y0 + 8, "Hartwig, März 1996 · nicht maßstäblich")
    c.setFillGray(0)
    B.new_page()


def b8():
    B.flip(); B.akte_tab("blau")
    y = B.doc_head("B-8  ·  AKTE BLAU", "Die Mailbox von Mark Böttcher", "Kriminaltechnik Seebrück")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.MAILBOX_INTRO, "Serif", 10.6, 15) - 12
    # Telefon-Tastenfeld als Zeichnung
    px, pw, ph = B.ML + 10, 200, 330
    py = y - ph
    c.setFillGray(0.12); c.roundRect(px, py, pw, ph, 24, fill=1, stroke=0)
    c.setFillGray(0.97); c.roundRect(px + 10, py + 14, pw - 20, ph - 28, 16, fill=1, stroke=0)
    c.setFillGray(0.85); c.roundRect(px + 22, py + ph - 72, pw - 44, 34, 6, fill=1, stroke=0)
    c.setFillGray(0.35); c.setFont("Mono", 13); c.drawCentredString(px + pw / 2, py + ph - 60, "_ _ _ _  _ _ _  _ _  _ _")
    keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"]
    for i, k in enumerate(keys):
        cx = px + pw / 2 + ((i % 3) - 1) * 52; cy = py + ph - 110 - (i // 3) * 46
        c.setFillGray(0.9); c.circle(cx, cy, 19, fill=1, stroke=0)
        c.setFillGray(0.15); c.setFont("SansB", 14); c.drawCentredString(cx, cy - 5, k)
    c.setFillColorRGB(0.2, 0.6, 0.3); c.circle(px + pw / 2, py + 40, 18, fill=1, stroke=0)
    c.setFillGray(1); c.setFont("SansB", 12); c.drawCentredString(px + pw / 2, py + 36, "☎" if False else "▶"); c.setFillGray(0)
    tx = px + pw + 30; tw = B.W - B.MR - 40 - tx
    c.setFont("SansB", 12); c.drawString(tx, y - 20, "So geht's")
    yy = B.text(tx, y - 40, tw, "1. Akte Rot liest euch die Handynummer von Böttchers Visitenkarte vor (R-7).\n"
                "2. Scannt den Code und tippt die Nummer in der Web-App ein.\n3. Hört die Nachricht ab. Ihr dürft sie Akte Rot vorspielen.",
                "Serif", 10.4, 14.6, gap=5)
    B.qr(tx + (tw - 110) / 2, yy - 130, 110, B.PORTAL + "#b8", "portal")
    B.new_page()


def b9():
    B.flip(); B.akte_tab("blau")
    y = B.doc_head("B-9  ·  AKTE BLAU", "Direktnachrichten @nova.on.wheels", "Vom Handy von Nova Sommer, Bildschirmfotos der Polizei")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.NOVA_INTRO, "SerifI", 10.4, 14.6) - 8
    x0, w0 = B.ML + 50, B.W - B.ML - B.MR - 140
    top = y
    c.setFillColorRGB(0.1, 0.1, 0.12); c.roundRect(x0 - 14, 56, w0 + 28, top - 48, 16, fill=1, stroke=0)
    c.setFillGray(1); c.setFont("SansB", 10); c.drawString(x0, top - 22, "m.lenz.repariert"); c.setFont("Sans", 7.5)
    c.setFillGray(0.7); c.drawString(x0, top - 34, "Hausmeister · repariert alles 🔧".replace(" 🔧", "")); c.setFillGray(0)
    y = top - 52
    for who, t, msg in A.NOVA_DM:
        if t is None:
            c.setFont("SansB", 7.5); c.setFillGray(0.6); c.drawCentredString(x0 + w0 / 2, y - 4, who); c.setFillGray(0)
            y -= 16; continue
        own = who == "nova"
        bw = w0 * 0.78
        msg = B.noemo(msg) or "(Emoji)"
        ls = simpleSplit(msg, "Sans", 9, bw - 20)
        bh = 12 + len(ls) * 11.5
        bx = x0 + (w0 - bw if own else 0)
        c.setFillColorRGB(*((0.45, 0.32, 0.85) if own else (0.24, 0.24, 0.27))); c.roundRect(bx, y - bh, bw, bh, 9, fill=1, stroke=0)
        c.setFillGray(1); yy = y - 13
        for l in ls:
            c.setFont("Sans", 9); c.drawString(bx + 10, yy, l); yy -= 11.5
        c.setFillGray(0.65); c.setFont("Sans", 7); c.drawRightString(bx + bw - 8 if not own else bx - 4, y - bh + 3 if not own else y - 9, "" if own else t)
        if own:
            c.drawRightString(bx - 6, y - 10, t)
        c.setFillGray(0)
        y -= bh + 6
    B.new_page()


def b10():
    B.flip(); B.akte_tab("blau")
    y = B.doc_head("B-10  ·  AKTE BLAU", "Unterlagen der Interessengemeinschaft", "Chronik und Schlüsselliste")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.VEREIN_HEAD, "SerifI", 10, 14) - 8
    bw = B.W - B.ML - B.MR - 40
    bh = y - 70
    c.setFillColorRGB(0.995, 0.995, 0.985); c.setStrokeGray(0.75); c.rect(B.ML, y - bh, bw, bh, fill=1, stroke=1)
    c.setFillColorRGB(0.12, 0.45, 0.25); c.rect(B.ML, y - 34, bw, 34, fill=1, stroke=0)
    c.setFillGray(1); c.setFont("SansB", 11); c.drawString(B.ML + 14, y - 22, "Interessengemeinschaft der Dauercamper am Kiefernsee")
    c.setFillGray(0)
    yy = y - 58
    c.setFont("SansB", 11.5); c.drawString(B.ML + 14, yy, "Unsere Chronik"); yy -= 18
    for j, t in A.CHRONIK:
        c.setFont("MonoB", 9.6); c.drawString(B.ML + 14, yy, j)
        yy = B.text(B.ML + 60, yy, bw - 80, t, "Serif", 9.8, 13, gap=0) - 5
    yy -= 10
    c.setFont("SansB", 11.5); c.drawString(B.ML + 14, yy, "Wer hat welchen Schlüssel?"); yy -= 18
    for k, v in A.SCHLUESSEL:
        c.setFont("FormB", 8.8); c.drawString(B.ML + 14, yy, k.upper())
        yy = B.text(B.ML + 200, yy, bw - 220, v, "Form", 9.4, 12.4, gap=0) - 7
    B.fc(B.INK); c.setFont("SerifBI", 14); c.drawString(B.ML + 14, y - bh + 22, "A. Wohlfahrt"); c.setFillGray(0)
    c.setFont("Form", 8.4); c.drawString(B.ML + 120, y - bh + 22, "Schriftführerin")
    B.new_page()


def b11():
    B.flip(); B.akte_tab("blau")
    y = B.doc_head("B-11  ·  AKTE BLAU", "Chat „Kiefernsee Dauercamper“ – vollständig", "Export vom Handy von Angelika Wohlfahrt")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 40, A.CHAT2_INTRO, "SerifI", 9.8, 13.4) - 4
    x0, w0 = B.ML + 30, B.W - B.ML - B.MR - 100
    c.setFillColorRGB(0.93, 0.90, 0.84); c.roundRect(x0 - 12, 50, w0 + 24, y - 44, 14, fill=1, stroke=0); c.setFillGray(0)
    y -= 10
    for who, t, msg in A.CHAT2:
        if t is None:
            c.setFont("SansB", 7.4); c.setFillGray(0.4); c.drawCentredString(x0 + w0 / 2, y - 4, who); c.setFillGray(0)
            y -= 14; continue
        own = who.startswith("Angelika")
        bw = w0 * 0.84
        deleted = msg.startswith("🚫")
        txt = "Diese Nachricht wurde gelöscht." if deleted else B.noemo(msg)
        ls = simpleSplit(txt, "SansI" if False else "Sans", 8.6, bw - 18)
        bh = 18 + len(ls) * 10.4
        bx = x0 + (w0 - bw if own else 0)
        c.setFillColorRGB(*((0.85, 0.96, 0.78) if own else (1, 1, 1))); c.setStrokeColorRGB(0.8, 0.78, 0.72); c.setLineWidth(0.4)
        c.roundRect(bx, y - bh, bw, bh, 7, fill=1, stroke=1); c.setFillGray(0)
        nmcol = {"Marco": (0.8, 0.45, 0.1), "Siggi": (0.6, 0.2, 0.6), "Mark": (0.1, 0.5, 0.45),
                 "Sven": (0.2, 0.35, 0.75), "Rita": (0.75, 0.2, 0.3)}.get(who.split()[0], (0.2, 0.5, 0.2))
        B.fc(nmcol); c.setFont("SansB", 7.6); c.drawString(bx + 9, y - 10.5, "Ich" if own else who); c.setFillGray(0)
        yy = y - 20
        for l in ls:
            if deleted:
                c.setFillGray(0.45); c.setFont("SerifI", 8.6)
            else:
                c.setFont("Sans", 8.6)
            c.drawString(bx + 9, yy, l); yy -= 10.4
        c.setFillGray(0)
        c.setFont("Sans", 7); c.setFillGray(0.4); c.drawRightString(bx + bw - 8, y - 10.5, t); c.setFillGray(0)
        y -= bh + 3.5
    B.new_page()


# ---------------- Gemeinsam hinten ----------------
def sheet():
    y = B.doc_head("AKT 2  ·  FÜR BEIDE", "Ermittlerbogen", "Wer sagt die Wahrheit – und wer nicht?")
    for h, n in [("Was wir jetzt sicher wissen", 9), ("Wer hatte Zugang zum Schlüsselkasten?", 4), ("Offene Fragen", 8)]:
        c.setFont("SansB", 11); c.setFillGray(0); c.drawString(B.ML, y, h); y -= 10
        for k in range(n):
            y -= 22; c.setStrokeGray(0.6); c.setLineWidth(0.5); c.line(B.ML, y, B.W - B.MR, y)
        y -= 26
    B.new_page()


def solve():
    y = B.doc_head("AKT 2  ·  FÜR BEIDE", "Akt 2 lösen", "Drei Fragen. Ein Scan. Fertig.")
    for q, opts in [(k + " · " + qq, o) for k, qq, o in A.Q]:
        c.setFont("SansB", 11.5); c.setFillGray(0); c.drawString(B.ML, y, q); y -= 21
        for o in opts:
            c.setStrokeGray(0.2); c.setLineWidth(1); c.rect(B.ML + 4, y - 2, 11, 11, fill=0, stroke=1)
            c.setFont("Serif", 10.6); c.drawString(B.ML + 24, y, o); y -= 19
        y -= 12
    y -= 6
    bh = 170; bw = B.W - B.ML - B.MR
    B.fc(B.NIGHT); c.rect(B.ML, y - bh, bw, bh, fill=1, stroke=0)
    c.setFillColorRGB(1, 0.8, 0.35); c.setFont("SansB", 9); c.drawString(B.ML + 18, y - 24, "SO GEHT'S")
    c.setFillGray(1); c.setFont("SansB", 14); c.drawString(B.ML + 18, y - 44, "Einigt euch – dann scannen.")
    yy = y - 70
    for i, t in enumerate(["Kreuzt gemeinsam je eine Antwort an.",
                           "Einer von euch scannt den QR-Code und wählt dort dieselben Antworten aus. Ein Handy reicht.",
                           "Bei „Richtig!“ geht es auf Seite 44 weiter. Jeder Fehlversuch kostet 2 Punkte."], 1):
        c.setFillColorRGB(1, 0.8, 0.35); c.setFont("SansB", 11); c.drawString(B.ML + 18, yy, f"{i}.")
        yy = B.text(B.ML + 36, yy, bw - 36 - 160, t, "Serif", 10.6, 14.6, gray=1, gap=5)
    c.setFillGray(0)
    qx, qy = B.ML + bw - 18 - 118, y - 26 - 118
    c.setFillGray(1); c.roundRect(qx - 7, qy - 27, 132, 153, 4, fill=1, stroke=0); c.setFillGray(0)
    B.qr(qx, qy, 118, B.PORTAL + "#code2", "portal")
    B.new_page()


def help_page():
    y = B.doc_head("AKT 2  ·  FÜR BEIDE", "Ihr steckt fest?", "Hinweise gibt es wie in Akt 1 in der Web-App")
    y = B.text(B.ML, y, B.W - B.ML - B.MR - 150,
               "Zu jeder Frage gibt es drei Stufen: kleiner Tipp, großer Tipp, Lösung. Jede Stufe kostet 1 Punkt. Den Code rechts scannen.", "Serif", 10.6, 15) - 4
    B.qr(B.W - B.MR - 112, y - 30, 104, B.PORTAL + "#hints2", "portal")
    y -= 40
    c.setFont("SansB", 12); c.drawString(B.ML, y, "Und wenn ein Rätsel klemmt?"); y -= 18
    tips = [("UV-Lampe (R-8)", "Leuchten drei verschiedene Tasten, aber der Code hat vier Stellen? Dann kommt eine Ziffer zweimal vor. "
             "Herr Lenz sagt, welches Jahr es ist. Die Chronik in Akte Blau nennt es."),
            ("Alte Karte (R-10)", "Norden ist auf beiden Bildern oben. Sucht auf dem Luftbild dieselbe Ecke des Sees wie auf der Karte."),
            ("Mailbox (B-8)", "Die Nummer hat 11 Ziffern und beginnt mit 0171. Leerzeichen sind egal.")]
    for t, d in tips:
        c.setFont("SansB", 10.8); c.drawString(B.ML, y, t)
        y = B.text(B.ML, y - 15, B.W - B.ML - B.MR - 150, d, "Serif", 10.2, 14, gap=0) - 12
    
    y -= 10
    c.setFillColorRGB(0.99, 0.95, 0.85); c.roundRect(B.ML, y - 72, B.W - B.ML - B.MR, 72, 6, fill=1, stroke=0); c.setFillGray(0)
    c.setFont("SansB", 11.5); c.drawString(B.ML + 14, y - 22, "Wichtig: Nur einer öffnet den Hinweis!")
    B.text(B.ML + 14, y - 40, B.W - B.ML - B.MR - 28,
           "Öffnen beide Handys dieselbe Stufe, werden 2 Punkte abgezogen statt 1. Einer öffnet und liest laut vor.", "Serif", 10.4, 14)
    B.new_page()


def solution():
    y = B.doc_head("AUFLÖSUNG AKT 2", "Wer gelogen hat", "Erst lesen, wenn die Web-App „Richtig!“ zeigt.")
    for h, t in A.SOLUTION:
        B.fc(B.ROT); c.setFont("SansB", 12); c.drawString(B.ML, y, h); c.setFillGray(0)
        y = B.text(B.ML, y - 17, B.W - B.ML - B.MR - 10, t, "Serif", 10.1, 14, gap=0) - 12
    y -= 2
    bh = y - 56
    B.fc(B.NIGHT); c.rect(B.ML, y - bh, B.W - B.ML - B.MR, bh, fill=1, stroke=0); c.setFillGray(1)
    c.setFont("SansB", 9); c.setFillColorRGB(1, 0.8, 0.35); c.drawString(B.ML + 16, y - 22, "WIE ES WEITERGEHT"); c.setFillGray(1)
    c.setFont("SansB", 13); c.drawString(B.ML + 16, y - 40, "Wendland lehnt sich zurück.")
    yy = B.text(B.ML + 16, y - 60, B.W - B.ML - B.MR - 32, A.WENDLAND_END, "SerifI", 10.1, 14, gray=1) - 4
    c.setFillGray(1); c.setFont("SansB", 10.5); c.drawString(B.ML + 16, yy, "Bevor ihr weiterspielt"); yy -= 17
    qtop = yy + 12
    for i, t in enumerate(["Scannt den QR-Code: Jeder versiegelt geheim seinen Hauptverdacht nach Akt 2.",
                           "Akte Blau zeigt den Übergabe-Code, Akte Rot scannt ihn. Das Handy von Akte Rot zeigt eure Punkte.",
                           "Pause! In Akt 3 „Die Wahrheit am Steg“ wird alles aufgedeckt."], 1):
        c.setFillColorRGB(1, 0.8, 0.35); c.setFont("SansB", 10); c.drawString(B.ML + 16, yy, f"{i}.")
        yy = B.text(B.ML + 32, yy, B.W - B.ML - B.MR - 50 - 130, t, "Serif", 9.8, 13.2, gray=1, gap=3)
    qx, qy = B.W - B.MR - 16 - 92, qtop - 92
    c.setFillGray(1); c.roundRect(qx - 7, qy - 27, 106, 127, 4, fill=1, stroke=0); c.setFillGray(0)
    B.qr(qx, qy, 92, B.PORTAL + "#akt", "portal")
    B.new_page()


def build(mod):
    _init(mod)
    B.ACTLABEL[0] = "Akt 2"
    opener()                 # 25
    task(); howto()          # 26 | 27
    r6(); b6()               # 28 | 29
    r7(); b7()               # 30 | 31
    r8(); b8()               # 32 | 33
    r9(); b9()               # 34 | 35
    r10(); b10()             # 36 | 37
    r11(); b11()             # 38 | 39
    sheet(); solve()         # 40 | 41
    help_page(); B.notes_page()   # 42 | 43
    solution()               # 44

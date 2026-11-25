"""Doppelseite 'Die Web-App – so einfach geht's' (zwei Seiten, nach dem Brief)."""
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

APP = None  # Pfad zu den Bildschirmfotos, wird von außen gesetzt


def _crop(name, y0, y1):
    im = Image.open(APP + name).convert("RGB")
    return im.crop((0, y0, im.width, y1))


def phone_img(B, im, x, y, w, h=None, radius=10, border=5):
    """Bildschirmfoto mit dunklem Handyrahmen. (x, y) = links unten der Bildfläche."""
    c = B.c
    if h is None:
        h = w * im.height / im.width
    c.setFillColorRGB(0.08, 0.1, 0.12)
    c.roundRect(x - border, y - border, w + 2 * border, h + 2 * border, radius + border, fill=1, stroke=0)
    c.saveState()
    p = c.beginPath(); p.roundRect(x, y, w, h, radius); c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(im), x, y, w, h)
    c.restoreState()
    return h


def badge(B, x, y, n, r=11, col=None):
    c = B.c
    c.setFillColorRGB(*(col or (0.95, 0.76, 0.2))); c.circle(x, y, r, fill=1, stroke=0)
    c.setStrokeColorRGB(0.07, 0.13, 0.22); c.setLineWidth(1.5); c.circle(x, y, r, fill=0, stroke=1)
    c.setFillColorRGB(0.07, 0.13, 0.22); c.setFont("SansB", r * 1.15); c.drawCentredString(x, y - r * 0.4, str(n))
    c.setFillGray(0)


def step_head(B, x, y, n, verb):
    c = B.c
    B.fc(B.NIGHT); c.circle(x + 15, y + 6, 15, fill=1, stroke=0)
    c.setFillGray(1); c.setFont("SansB", 16); c.drawCentredString(x + 15, y, str(n)); c.setFillGray(0)
    c.setFont("SansB", 16); c.drawString(x + 38, y, verb)


def draw_scan(B, x, y, w, h):
    """Zeichnung: Handy mit Kamera über einem QR-Code."""
    c = B.c
    # Buchseite mit QR-Code
    c.setFillColorRGB(0.97, 0.96, 0.92); c.setStrokeGray(0.6); c.setLineWidth(0.8)
    c.rect(x, y, w * 0.62, h * 0.78, fill=1, stroke=1)
    c.setStrokeGray(0.75)
    for k in range(5):
        c.line(x + 10, y + h * 0.78 - 16 - k * 9, x + w * 0.62 - 10, y + h * 0.78 - 16 - k * 9)
    qs = w * 0.26
    qw = QrCodeWidget("https://natthaphon-lind.github.io/kiefernsee/"); qw.barWidth = qs; qw.barHeight = qs; qw.barBorder = 1
    d = Drawing(qs, qs); d.add(qw); renderPDF.draw(d, c, x + 12, y + 10)
    # Handy schräg darüber
    c.saveState(); c.translate(x + w * 0.66, y + h * 0.12); c.rotate(8)
    pw, ph = w * 0.34, h * 0.86
    c.setFillColorRGB(0.08, 0.1, 0.12); c.roundRect(0, 0, pw, ph, 9, fill=1, stroke=0)
    c.setFillColorRGB(0.85, 0.9, 0.93); c.roundRect(4, 8, pw - 8, ph - 16, 5, fill=1, stroke=0)
    # Sucher-Ecken
    c.setStrokeColorRGB(0.95, 0.76, 0.2); c.setLineWidth(2.2)
    s0, s1, t0, t1 = 10, pw - 10, 20, ph - 34
    L = 9
    for (a, b, da, db) in [(s0, t0, 1, 1), (s1, t0, -1, 1), (s0, t1, 1, -1), (s1, t1, -1, -1)]:
        c.line(a, b, a + da * L, b); c.line(a, b, a, b + db * L)
    # Link-Hinweis
    c.setFillColorRGB(1, 1, 1); c.roundRect(6, ph - 30, pw - 12, 16, 4, fill=1, stroke=0)
    c.setFillColorRGB(0.15, 0.36, 0.63); c.setFont("SansB", 6.5); c.drawCentredString(pw / 2, ph - 25, "Link öffnen")
    c.restoreState(); c.setFillGray(0)


def page_start(B):
    c, W, H, ML, MR = B.c, B.W, B.H, B.ML, B.MR
    y = B.doc_head("SO FUNKTIONIERT DIE WEB-APP", "Bevor ihr startet",
                   "Jeder nimmt sein eigenes Handy. Das dauert nur eine Minute.")
    gap = 18
    cw = (W - ML - MR - gap) / 2
    ch = 252
    steps = [
        (1, "Scannen", "Öffnet die Kamera-App eures Handys und haltet sie über den QR-Code im Brief (Seite 3). "
                       "Tippt dann auf den Link, der erscheint."),
        (2, "Kennwort eingeben", "Das Kennwort steht ganz unten im Brief. Tippt es ein und dann auf "
                                 "„Akte öffnen“."),
        (3, "Namen eintragen", "Vornamen eintragen, „Kommissarin“ oder „Kommissar“ wählen. Schon einen Ermittlerausweis? Dann hier die Dienstnummer eingeben."),
        (4, "Farbe wählen", "Einer tippt auf Akte Rot, der andere auf Akte Blau – jeder auf seinem Handy."),
    ]
    imgs = [None, _crop("1_login.png", 470, 960), _crop("2_rolle.png", 20, 245), _crop("2_rolle.png", 255, 455)]
    for i, (n, verb, txt) in enumerate(steps):
        col, row = i % 2, i // 2
        x = ML + col * (cw + gap)
        top = y - row * (ch + gap)
        c.setStrokeGray(0.8); c.setLineWidth(1); c.roundRect(x, top - ch, cw, ch, 8, fill=0, stroke=1)
        step_head(B, x + 14, top - 32, n, verb)
        ty = B.text(x + 14, top - 52, cw - 28, txt, "Serif", 10.6, 14.6, gap=0)
        area_top = ty - 8
        area_bot = top - ch + 16
        ah = area_top - area_bot
        aw = cw - 40
        if imgs[i] is None:
            draw_scan(B, x + 20, area_bot + 6, aw, ah - 10)
        else:
            im = imgs[i]
            iw = aw; ih = iw * im.height / im.width
            if ih > ah - 10:
                ih = ah - 10; iw = ih * im.width / im.height
            phone_img(B, im, x + 20 + (aw - iw) / 2, area_bot + (ah - ih) / 2, iw, ih, radius=6, border=4)
    # Hinweis Namen
    by = y - 2 * ch - gap - 14
    bh = 64
    c.setFillColorRGB(0.99, 0.95, 0.85); c.roundRect(ML, by - bh, W - ML - MR, bh, 6, fill=1, stroke=0); c.setFillGray(0)
    c.setFont("SansB", 11); c.drawString(ML + 14, by - 20, "Gut zu wissen")
    B.text(ML + 14, by - 36, W - ML - MR - 28,
           "Eure Namen kennt nur die Web-App – im Buch heißt ihr Akte Rot und Akte Blau. Euer Dienstgrad bleibt auf eurem Handy gespeichert und läuft in jedem neuen Fall der Reihe weiter.", "Serif", 10.6, 14)
    B.new_page()


def page_play(B):
    c, W, H, ML, MR = B.c, B.W, B.H, B.ML, B.MR
    y = B.doc_head("SO FUNKTIONIERT DIE WEB-APP", "Während des Spiels",
                   "Alles Wichtige auf einen Blick. Die Nummern findet ihr im Bild wieder.")
    pw = 150
    # --- Bild 1: Kopf, Akten, Punkte
    im1 = _crop("3_menu.png", 20, 625)
    h1 = pw * im1.height / im1.width
    x1 = ML + 6; y1 = y - h1 - 4
    phone_img(B, im1, x1, y1, pw, h1, radius=8, border=5)

    def at(im, h, px, py, x0, y0):  # Pixel im Ausschnitt -> PDF-Koordinate
        return x0 + px / im.width * pw, y0 + h - py / im.height * h
    marks1 = [(1, 368, 40), (2, 368, 112), (3, 368, 330), (4, 368, 553)]
    for n, px, py in marks1:
        bx, byy = at(im1, h1, px, py, x1, y1); badge(B, bx, byy, n)
    items1 = [(1, "Eure Farbe und euer Name", "Oben seht ihr immer, welche Akte ihr habt."),
              (2, "Euer Dienstgrad", "Antippen öffnet euren Ermittlerausweis mit Dienstnummer."),
              (3, "Eure Akten", "Tippt auf R-1, R-2 … bzw. B-1, B-2 … Es sind dieselben Akten wie im Buch – "
                                "dazu Fotos und Tonaufnahmen. Bei Tonaufnahmen tippt ihr auf ▶."),
              (4, "Eure Punkte", "Ihr startet mit 10 Punkten. Die Web-App zieht automatisch ab: 2 Punkte für "
                                 "jeden Fehlversuch, 1 Punkt für jeden Hinweis.")]
    lx = x1 + pw + 26; lw = W - MR - lx
    ly = y - 10
    for n, t, d in items1:
        badge(B, lx + 11, ly - 4, n)
        c.setFont("SansB", 11.5); c.drawString(lx + 30, ly - 8, t)
        ly = B.text(lx + 30, ly - 22, lw - 30, d, "Serif", 9.8, 13, gap=0) - 9
    # --- Bild 2: Für beide
    im2 = _crop("4_beide.png", 0, 392)
    h2 = pw * im2.height / im2.width
    y2 = min(y1, ly + 10) - 18 - h2
    phone_img(B, im2, x1, y2, pw, h2, radius=8, border=5)
    marks2 = [(5, 172, 150), (6, 348, 150), (7, 172, 236), (8, 348, 236), (9, 172, 340)]
    for n, px, py in marks2:
        bx, byy = at(im2, h2, px, py, x1, y2); badge(B, bx, byy, n)
    items2 = [(5, "Akt 1 lösen", "Hier prüft ihr eure drei Antworten."),
              (6, "Hinweise", "Kleiner Tipp, großer Tipp, Lösung. Nur einer öffnet!"),
              (7, "Akt 1 abschließen", "Verdacht versiegeln, Akte Blau übergibt an Akte Rot."),
              (8, "Mein Ausweis", "Dienstgrad, Sterne und Dienstnummer – als Bild speichern."),
              (9, "Neues Spiel", "Löscht den Spielstand. Euer Dienstgrad bleibt.")]
    ly = y2 + h2 + 6
    for n, t, d in items2:
        badge(B, lx + 11, ly - 4, n)
        c.setFont("SansB", 11.5); c.drawString(lx + 30, ly - 8, t)
        ly = B.text(lx + 30, ly - 22, lw - 30, d, "Serif", 9.8, 13, gap=0) - 7
    # --- Wenn etwas nicht klappt
    by = min(y2, ly) - 14
    tips = ["Falsche Farbe gewählt? Oben auf „Akte wechseln“ tippen.",
            "Web-App aus Versehen geschlossen? Einfach wieder einen QR-Code im Buch scannen – alles bleibt gespeichert.",
            "Scannen in der Web-App klappt nicht? Den Code mit der normalen Kamera-App scannen."]
    th = sum(B.lines_h(t, "Serif", 10, W - ML - MR - 44, 13.4) + 6 for t in tips) + 34
    B.fc(B.NIGHT); c.roundRect(ML, by - th, W - ML - MR, th, 6, fill=1, stroke=0)
    c.setFillColorRGB(1, 0.8, 0.35); c.setFont("SansB", 11); c.drawString(ML + 14, by - 20, "Wenn etwas nicht klappt")
    ty = by - 38
    for t in tips:
        c.setFillColorRGB(1, 0.8, 0.35); c.setFont("SansB", 10); c.drawString(ML + 16, ty, "•")
        ty = B.text(ML + 30, ty, W - ML - MR - 44, t, "Serif", 10, 13.4, gray=1, gap=0) - 6
    c.setFillGray(0)
    B.new_page()

import build_farbe as B
from reportlab.pdfgen import canvas
c = canvas.Canvas("/home/claude/mock_1920.pdf", pagesize=(B.W, B.H)); B.c = c
W,H,ML,MR = B.W,B.H,B.ML,B.MR
Q = [("Frage 1 · Wo ist Brandner ins Wasser gekommen?", ["am Badestrand","am Bootssteg","mitten auf dem See, aus dem Tretboot"]),
     ("Frage 2 · Wann ist es passiert?", ["zwischen 21:30 und 23:00 Uhr","zwischen 23:30 und 0:30 Uhr","zwischen 0:30 und 2:00 Uhr","nach 2:00 Uhr"]),
     ("Frage 3 · Was fehlt?", ["sein Handy","seine Brieftasche","seine rote Ledermappe","sein Autoschlüssel"])]
def label(t):
    c.setFillColorRGB(0.85,0.1,0.1); c.setFont("SansB",9); c.drawRightString(W-MR, H-30, t); c.setFillGray(0)
def step(n, x, y, t, w):
    B.fc(B.NIGHT); c.circle(x+11, y+4, 11, fill=1, stroke=0); c.setFillGray(1); c.setFont("SansB",11); c.drawCentredString(x+11, y, str(n)); c.setFillGray(0)
    return B.text(x+32, y+8, w-32, t, "Serif", 11, 15, gap=0)
def box(x,y,s):
    c.setStrokeGray(0.2); c.setLineWidth(1); c.rect(x,y,s,s,fill=0,stroke=1)

# ---------- 19 A ----------
label("VORSCHLAG 19-A · Prüfen in der Web-App")
y = B.doc_head("FÜR BEIDE", "Akt 1 lösen", "Drei Fragen. Ein Scan. Fertig.")
for q, opts in Q:
    c.setFont("SansB", 12); c.drawString(ML, y, q); y -= 20
    for o in opts:
        box(ML+4, y-2, 11); c.setFont("Serif", 11); c.drawString(ML+24, y, o); y -= 18
    y -= 14
y -= 6
bh = 170; bw = W-ML-MR
B.fc(B.NIGHT); c.rect(ML, y-bh, bw, bh, fill=1, stroke=0)
c.setFillColorRGB(1,0.8,0.35); c.setFont("SansB",9); c.drawString(ML+18, y-24, "SO GEHT'S")
c.setFillGray(1); c.setFont("SansB",14); c.drawString(ML+18, y-44, "Einigt euch – dann scannen.")
yy = y-68
for i,t in enumerate(["Kreuzt gemeinsam je eine Antwort an.","Scannt den QR-Code und tippt eure Antworten ein.","Bei „Richtig!“ geht es auf Seite 22 weiter. Bei „Leider falsch“ zeigt die Web-App welche Frage noch nicht passt (kostet 2 Punkte)."],1):
    c.setFillColorRGB(1,0.8,0.35); c.setFont("SansB",11); c.drawString(ML+18, yy, f"{i}.")
    yy = B.text(ML+36, yy, bw-36-150, t, "Serif", 11, 15, gray=1, gap=4)
qx,qy = ML+bw-18-118, y-24-118
c.setFillGray(1); c.roundRect(qx-7,qy-27,132,153,4,fill=1,stroke=0); c.setFillGray(0)
B.qr(qx,qy,118,B.PORTAL+"#code","portal")
c.showPage()

# ---------- 19 B ----------
label("VORSCHLAG 19-B · Lösungswort im Buch (ohne Handy)")
y = B.doc_head("FÜR BEIDE", "Akt 1 lösen", "Jede Antwort hat einen Buchstaben. Die richtigen ergeben ein Wort.")
L = [["P","S","V"],["Q","E","Y","J"],["F","Z","E","W"]]
for (q, opts), ls in zip(Q, L):
    c.setFont("SansB", 12); c.drawString(ML, y, q); y -= 20
    for o, l in zip(opts, ls):
        c.setFillGray(0.92); c.roundRect(ML+2, y-5, 20, 18, 3, fill=1, stroke=0); c.setFillGray(0)
        c.setFont("MonoB" if "MonoB" in c.getAvailableFonts() else "SansB", 12); c.drawCentredString(ML+12, y, l)
        c.setFont("Serif", 11); c.drawString(ML+32, y, o); y -= 18
    y -= 14
y -= 4
c.setFont("SansB", 12); c.drawString(ML, y, "Eure drei Buchstaben:"); 
for k in range(3): box(ML+150+k*46, y-12, 38)
y -= 46
B.fc(B.NIGHT); c.rect(ML, y-96, W-ML-MR, 96, fill=1, stroke=0); c.setFillGray(1)
c.setFont("SansB", 13); c.drawString(ML+18, y-28, "Ergibt sich ein Wort, das zum Fall passt?")
B.text(ML+18, y-50, W-ML-MR-36, "Ja: richtig! Weiter auf Seite 22.\nNein: mindestens eine Antwort stimmt noch nicht. Schaut euch die Spuren noch einmal an.", "Serif", 11, 15, gray=1)
c.setFillGray(0); c.showPage()

# ---------- 20 A ----------
label("VORSCHLAG 20-A · Hinweise in der Web-App")
y = B.doc_head("FÜR BEIDE", "Ihr steckt fest?", "Kein Problem. Holt euch so viel Hilfe, wie ihr braucht.")
y -= 6
stufen = [("1","Schubs","Ein kleiner Tipp, wo ihr hinschauen solltet."),("2","Richtung","Sagt euch, welche Spuren zusammengehören."),("3","Antwort","Verrät die Lösung dieser einen Frage.")]
bw3 = (W-ML-MR-24)/3
for i,(n,t,d) in enumerate(stufen):
    x = ML + i*(bw3+12)
    c.setStrokeGray(0.75); c.setLineWidth(1); c.roundRect(x, y-130, bw3, 130, 6, fill=0, stroke=1)
    B.fc(B.NIGHT); c.circle(x+bw3/2, y-34, 20, fill=1, stroke=0); c.setFillGray(1); c.setFont("SansB",18); c.drawCentredString(x+bw3/2, y-40, n); c.setFillGray(0)
    c.setFont("SansB",13); c.drawCentredString(x+bw3/2, y-74, "Stufe "+n+": "+t)
    B.text(x+12, y-92, bw3-24, d, "Serif", 10, 13.5)
y -= 168
y = step(1, ML, y, "Scannt den QR-Code und tippt bei der Frage, die klemmt, auf „Stufe 1“.", W-ML-MR-160) - 10
y = step(2, ML, y, "Reicht das nicht, öffnet Stufe 2 – und erst ganz zum Schluss Stufe 3.", W-ML-MR-160) - 10
y = step(3, ML, y, "Jede geöffnete Stufe kostet euer Team 1 Punkt. Die Web-App zählt automatisch mit.", W-ML-MR-160) - 10
qy=y+18
B.qr(W-MR-120, qy-110, 110, B.PORTAL+"#hints", "portal")
y = min(y, qy-150)
c.setFillColorRGB(0.99,0.95,0.85); c.roundRect(ML, y-58, W-ML-MR, 58, 6, fill=1, stroke=0); c.setFillGray(0)
c.setFont("SansB",11); c.drawString(ML+14, y-22, "Tipp")
B.text(ML+14, y-38, W-ML-MR-28, "Sprecht euch ab, wer den Hinweis öffnet. Öffnen beide Handys dieselbe Stufe, kostet sie doppelt.", "Serif", 10.5, 14)
c.showPage()

# ---------- 20 B ----------
label("VORSCHLAG 20-B · Hinweise im Buch, übersichtlich")
y = B.doc_head("FÜR BEIDE", "Ihr steckt fest?", "Lest nur das Feld, das ihr braucht. Dreht das Buch dafür um.")
c.setFont("Serif", 11); c.drawString(ML, y, "Die Hinweise stehen auf dem Kopf, damit ihr nicht aus Versehen weiterlest.")
y -= 22
cw = (W-ML-MR-90)/3
for j,t in enumerate(["Stufe 1 · Schubs","Stufe 2 · Richtung","Stufe 3 · Antwort"]):
    c.setFont("SansB",10.5); c.drawCentredString(ML+90+j*cw+cw/2, y, t)
y -= 10
rowsQ = ["Frage 1\nWo?","Frage 2\nWann?","Frage 3\nWas fehlt?"]
for i in range(3):
    rh = 150
    c.setFont("SansB",11)
    for k,ln in enumerate(rowsQ[i].split("\n")): c.drawString(ML, y-60-k*15, ln)
    for j in range(3):
        x = ML+90+j*cw
        c.setStrokeGray(0.5); c.setLineWidth(0.8); c.rect(x, y-rh, cw, rh, fill=0, stroke=1)
        txt = B.HINTS[i*3+j][2]
        c.saveState(); c.translate(x+cw, y-rh); c.rotate(180)
        c.translate(-cw, -rh)  # Ursprung oben links der gedrehten Box
        c.restoreState()
        c.saveState(); c.translate(x+cw/2, y-rh/2); c.rotate(180)
        B.text(-cw/2+8, rh/2-14, cw-16, txt, "Serif", 9.4, 12.6)
        c.restoreState()
    y -= rh
c.setFont("Serif",10.5); c.drawString(ML, y-24, "Hinweise aus dem Buch kosten keine Punkte – die Web-App bekommt davon nichts mit.")
c.showPage(); c.save()

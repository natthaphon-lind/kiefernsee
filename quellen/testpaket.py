"""Testanleitung und Fragebogen für die Testrunde Akt 1 (A4 hoch, 2 Seiten)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = "/home/claude/kiefernsee/quellen/fonts/"
for n, p in [("Sans", "Poppins-Regular.ttf"), ("SansB", "Poppins-Bold.ttf"), ("Serif", "Lora-Regular.ttf"),
             ("SerifI", "Lora-Italic.ttf"), ("SerifB", "Lora-Bold.ttf"), ("Sym", "DejaVuSans-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(n, F + p))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="SerifB", italic="SerifI", boldItalic="SerifB")

NIGHT = colors.HexColor("#15233a"); ROT = colors.HexColor("#a83228"); BLAU = colors.HexColor("#2d5d8c")
GOLD = colors.HexColor("#f2c14e"); PAPER = colors.HexColor("#fcf3dc"); LINE = colors.HexColor("#b9c0c6")

kick = ParagraphStyle("k", fontName="SansB", fontSize=8.5, textColor=colors.HexColor("#6b7680"), leading=11, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="SansB", fontSize=21, leading=25, textColor=NIGHT, spaceAfter=4)
sub = ParagraphStyle("s", fontName="SerifI", fontSize=10.5, leading=14, textColor=colors.HexColor("#4a5560"), spaceAfter=10)
h2 = ParagraphStyle("h2", fontName="SansB", fontSize=12.5, leading=16, textColor=NIGHT, spaceBefore=8, spaceAfter=4)
body = ParagraphStyle("b", fontName="Serif", fontSize=10.3, leading=14.2, spaceAfter=3)
bul = ParagraphStyle("bu", parent=body, leftIndent=14, bulletIndent=2, spaceAfter=2)
small = ParagraphStyle("sm", fontName="Serif", fontSize=9, leading=12, textColor=colors.HexColor("#4a5560"))
q = ParagraphStyle("q", fontName="SansB", fontSize=10, leading=13, textColor=NIGHT)


def box(flow, bg=PAPER, pad=10):
    t = Table([[flow]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("LEFTPADDING", (0, 0), (-1, -1), pad),
                           ("RIGHTPADDING", (0, 0), (-1, -1), pad), ("TOPPADDING", (0, 0), (-1, -1), pad - 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return t


def B(t):
    return Paragraph(t, bul, bulletText="•")


def footer(c, d):
    c.saveState(); c.setFont("Sans", 7.5); c.setFillColor(colors.HexColor("#8a949c"))
    c.drawString(20 * mm, 12 * mm, "Ermittlungsfall Campingplatz · Testrunde Akt 1 · vertraulich – bitte nicht weitergeben")
    c.drawRightString(190 * mm, 12 * mm, f"Seite {d.page}")
    c.restoreState()


def scale(label, left="gar nicht", right="sehr"):
    cells = [Paragraph(label, q)] + [Paragraph(f"<para alignment='center'>{i}</para>", body) for i in range(1, 6)]
    t = Table([cells, ["", left, "", "", "", right]], colWidths=[78 * mm] + [18 * mm] * 5)
    t.setStyle(TableStyle([
        ("BOX", (1, 0), (1, 0), 0.8, LINE), ("BOX", (2, 0), (2, 0), 0.8, LINE), ("BOX", (3, 0), (3, 0), 0.8, LINE),
        ("BOX", (4, 0), (4, 0), 0.8, LINE), ("BOX", (5, 0), (5, 0), 0.8, LINE),
        ("FONT", (0, 1), (-1, 1), "Serif", 7.5), ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#6b7680")),
        ("ALIGN", (1, 1), (1, 1), "CENTER"), ("ALIGN", (5, 1), (5, 1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 1), (-1, 1), 1), ("BOTTOMPADDING", (0, 0), (-1, 0), 4)]))
    return t


def lines(label, n=2):
    rows = [[Paragraph(label, q)]] + [[""] for _ in range(n)]
    t = Table(rows, colWidths=[170 * mm], rowHeights=[None] + [7 * mm] * n)
    st = [("LINEBELOW", (0, i), (0, i), 0.6, LINE) for i in range(1, n + 1)]
    st += [("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (0, 0), 6)]
    t.setStyle(TableStyle(st))
    return t


def choice(label, opts):
    cells = [Paragraph(label, q)] + [Paragraph("<font name='Sym' size='12'>☐</font> " + o, body) for o in opts]
    return Table([cells], colWidths=[62 * mm] + [108 * mm / len(opts)] * len(opts),
                 style=[("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)])


story = []
story += [Paragraph("TESTRUNDE · AKT 1", kick), Paragraph("Ermittlungsfall Campingplatz", h1),
          Paragraph("Das Krimispiel zu zweit – danke, dass ihr als Erste ermittelt!", sub)]
story.append(Paragraph(
    "Ihr testet den ersten Akt meines neuen Buchs. Spielt bitte so, als hättet ihr das Buch gerade gekauft: "
    "Niemand erklärt euch etwas, alles Wichtige steht auf den Seiten. Genau das will ich herausfinden – "
    "ob es ohne Hilfe verständlich ist und ob es Spaß macht.", body))
story.append(Paragraph("Das braucht ihr", h2))
for t in ["Die ausgedruckten Blätter (13 Blätter A4, siehe unten)",
          "Zwei Handys mit Internet – <b>jeder sein eigenes</b>. Ton an, ihr hört Sprachnachrichten.",
          "Einen Stift für Notizen",
          "Ungefähr 60 Minuten Zeit, einen Tisch zum Gegenübersitzen – und gern etwas zu trinken"]:
    story.append(B(t))
story.append(Paragraph("Ausdrucken", h2))
for t in ["Datei „Ermittlungsfall_Testdruck_A4.pdf“ öffnen und <b>einseitig</b> drucken, am besten in <b>Farbe</b>.",
          "Im Druckdialog <b>„Tatsächliche Größe“ bzw. „100 %“</b> wählen, nicht „An Seite anpassen“.",
          "Jedes Blatt ist eine aufgeschlagene Doppelseite des Buchs. Die Schrift ist etwas kleiner als im "
          "fertigen Buch – das ist normal."]:
    story.append(B(t))
story.append(Paragraph("So geht's los", h2))
for t in ["Blätter der Reihe nach stapeln. <b>Das letzte Blatt (Seite 24, „Auflösung“) mit der Schrift nach "
          "unten zur Seite legen</b> – erst umdrehen, wenn die Web-App „Richtig!“ zeigt.",
          "Setzt euch gegenüber. Das oberste Blatt liegt quer zwischen euch. Ab den Akten gehört die linke "
          "Hälfte Akte Rot, die rechte Akte Blau – wer welche Farbe nimmt, entscheidet ihr selbst.",
          "Weiterblättern heißt hier: das nächste Blatt obenauf legen.",
          "Dann einfach mit Blatt 1 anfangen und loslegen. Alles Weitere erklärt das Buch."]:
    story.append(B(t))
story.append(Spacer(1, 8))
story.append(box(Paragraph(
    "<b>Bitte notiert die Uhrzeit, wenn ihr anfangt und wenn ihr fertig seid.</b> Wenn euch etwas unklar ist: "
    "kurz am Rand notieren und weiterspielen – genau diese Stellen sind für mich Gold wert. Nichts googeln, "
    "und den Link oder das Kennwort bitte nicht weitergeben.", body)))
story.append(Spacer(1, 8))
story.append(Paragraph("Nach dem Spiel füllt bitte gemeinsam den Fragebogen auf der nächsten Seite aus und schickt "
                       "mir ein Foto davon – oder antwortet einfach per Nachricht. Ehrliche Kritik hilft mir am meisten!",
                       body))
story.append(PageBreak())

story += [Paragraph("FRAGEBOGEN", kick), Paragraph("Wie war's?", h1),
          Paragraph("Bitte nach dem Spiel gemeinsam ausfüllen. Es gibt keine falschen Antworten.", sub)]
tt = Table([[Paragraph("Start:", q), "", Paragraph("Ende:", q), "", Paragraph("Punkte am Ende:", q), ""]],
           colWidths=[16 * mm, 30 * mm, 15 * mm, 30 * mm, 33 * mm, 46 * mm])
tt.setStyle(TableStyle([("LINEBELOW", (1, 0), (1, 0), 0.6, LINE), ("LINEBELOW", (3, 0), (3, 0), 0.6, LINE),
                        ("LINEBELOW", (5, 0), (5, 0), 0.6, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
story += [tt, Spacer(1, 6)]
story.append(choice("Handys:", ["2× iPhone", "2× Android", "gemischt"]))
story.append(Spacer(1, 4))
story.append(Paragraph("Ankreuzen von 1 bis 5", ParagraphStyle("h2b", parent=h2, spaceBefore=4)))
for lab, l, r in [("Hat es Spaß gemacht?", "gar nicht", "sehr"),
                  ("Wie schwer war der Fall?", "zu leicht", "zu schwer"),
                  ("War die Web-App-Anleitung (Seite 4 | 5) verständlich?", "gar nicht", "sofort klar"),
                  ("Klappte das Lesen gegenüber (Blau kopfüber)?", "schlecht", "sehr gut"),
                  ("Wie gut haben euch Fotos und Tonaufnahmen gefallen?", "gar nicht", "sehr")]:
    story += [scale(lab, l, r), Spacer(1, 1)]
story.append(Paragraph("Kurze Fragen", h2))
story.append(choice("Kennwort und Farbwahl geklappt?", ["ja", "mit Mühe", "nein"]))
story.append(choice("Sprachnachrichten abgespielt?", ["ja", "nur eine", "nein"]))
story.append(choice("QR-Übergabe am Ende:", ["in der Web-App", "Kamera-App", "ging nicht"]))
story.append(choice("Würdet ihr Akt 2 spielen?", ["ja, sofort", "vielleicht", "eher nicht"]))
story.append(Spacer(1, 2))
story.append(lines("Wo seid ihr hängen geblieben oder wart unsicher, was zu tun ist?", 2))
story.append(lines("Was hat euch am besten gefallen?", 2))
story.append(lines("Was würdet ihr ändern?", 2))
story.append(lines("Würdet ihr das Buch kaufen oder verschenken? Was dürfte es kosten?", 1))
story.append(Spacer(1, 6))
story.append(Paragraph("Danke! Und bitte verratet niemandem die Lösung.", small))

doc = BaseDocTemplate("/home/claude/fall/Testrunde_Akt1_Anleitung_und_Fragebogen.pdf", pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                      title="Ermittlungsfall Campingplatz – Testrunde Akt 1", author="Natthaphon Lind")
fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f", leftPadding=0, rightPadding=0)
doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=footer)])
doc.build(story)
print("ok")

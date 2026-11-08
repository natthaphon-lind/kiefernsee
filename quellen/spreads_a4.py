from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from reportlab.pdfgen import canvas
import io
SRC="Kiefernsee_Akt1_Prototyp_Farbe.pdf"
r=PdfReader(SRC); n=len(r.pages)
pw,ph=612,792
A4W,A4H=842,595
s=min((A4W-28)/(2*pw),(A4H-34)/ph)
x0=(A4W-2*pw*s)/2; y0=(A4H-ph*s)/2+4
pairs=[(None,0)]+[(i,i+1 if i+1<n else None) for i in range(1,n,2)]
w=PdfWriter()
for k,(L,R) in enumerate(pairs):
    pg=PageObject.create_blank_page(width=A4W,height=A4H)
    # Hintergrund: Buchkante, Mittelfalz, Beschriftung
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(A4W,A4H))
    c.setStrokeGray(0.75); c.setLineWidth(0.6)
    c.rect(x0+(0 if L is not None else pw*s),y0,(2*pw*s if (L is not None and R is not None) else pw*s),ph*s,fill=0,stroke=1)
    if L is not None and R is not None:
        c.setStrokeGray(0.55); c.setDash(2,2); c.line(x0+pw*s,y0,x0+pw*s,y0+ph*s); c.setDash()
    lab=" | ".join(str(p+1) for p in (L,R) if p is not None)
    c.setFont("Helvetica",7); c.setFillGray(0.5)
    c.drawCentredString(A4W/2,8,f"Testdruck · Buchseiten {lab} · so liegt das Buch aufgeschlagen vor euch")
    c.save(); buf.seek(0)
    pg.merge_page(PdfReader(buf).pages[0])
    for idx,off in ((L,0),(R,pw*s)):
        if idx is None: continue
        src=r.pages[idx]
        pg.merge_transformed_page(src,Transformation().scale(s).translate(x0+off,y0))
    w.add_page(pg)
w.add_metadata({"/Title":"Ausverkauf am Kiefernsee – Akt 1 – Testdruck A4 (Doppelseiten)","/Author":"Natthaphon Lind"})
w.write("Kiefernsee_Akt1_Testdruck_A4_Doppelseiten.pdf")
print(len(pairs),"Blätter, Maßstab",round(s*100),"%")

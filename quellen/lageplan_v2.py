from PIL import Image, ImageDraw, ImageFont
F="/home/claude/kiefernsee/quellen/fonts/"
im=Image.open("/home/claude/fall/img/lageplan_v2.png").convert("RGBA")
S=2  # hochskalieren für saubere Schrift
im=im.resize((im.width*S, im.height*S), Image.LANCZOS)
W,H=im.size
ov=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
fB=ImageFont.truetype(F+"Poppins-Bold.ttf",30*S); fS=ImageFont.truetype(F+"Poppins-Medium.ttf",22*S); fL=ImageFont.truetype(F+"Lora-BoldItalic.ttf",44*S)
def P(u,v): return (u*W, v*H)
def pill(u,v,txt,font=fB,bg=(255,255,255,235),fg=(20,28,35,255),anchor="mm",dot=None):
    x,y=P(u,v)
    b=d.textbbox((0,0),txt,font=font); tw,th=b[2]-b[0],b[3]-b[1]
    px,py=12*S,7*S
    if anchor=="mm": x0,y0=x-tw/2-px,y-th/2-py
    elif anchor=="lm": x0,y0=x,y-th/2-py
    elif anchor=="rm": x0,y0=x-tw-2*px,y-th/2-py
    if dot:
        dx,dy=P(*dot); d.line([((x0+x0+tw+2*px)/2,(y0+y0+th+2*py)/2),(dx,dy)],fill=(255,255,255,230),width=3*S)
        d.ellipse([dx-7*S,dy-7*S,dx+7*S,dy+7*S],fill=(255,255,255,255),outline=(20,28,35,255),width=2*S)
    d.rounded_rectangle([x0,y0,x0+tw+2*px,y0+th+2*py],radius=8*S,fill=bg,outline=(20,28,35,120),width=S)
    d.text((x0+px-b[0],y0+py-b[1]),txt,font=font,fill=fg)
# See
x,y=P(0.79,0.42); d.text((x,y),"Kiefernsee",font=fL,fill=(255,255,255,235),anchor="mm")
pill(0.72,0.035,"Schilfgürtel")
fx,fy=P(0.86,0.115); r=16*S
d.line([fx-r,fy-r,fx+r,fy+r],fill=(210,30,30,255),width=8*S); d.line([fx-r,fy+r,fx+r,fy-r],fill=(210,30,30,255),width=8*S)
pill(0.86,0.17,"Fundort",bg=(200,30,30,240),fg=(255,255,255,255))
pill(0.60,0.315,"Bootssteg",dot=(0.53,0.25))
pill(0.80,0.29,"Tretboote „Kevin“ + „Chantal“",font=fS,dot=(0.64,0.245))
pill(0.69,0.585,"Badestrand",dot=(0.60,0.535))
pill(0.015,0.045,"Gaststätte Seeklause",anchor="lm",dot=(0.09,0.17))
pill(0.10,0.335,"mit Wetterstation",font=fS)
pill(0.31,0.12,"Mietchalets C1–C4",font=fS)
for k,u in enumerate([0.229,0.283,0.337,0.392]):
    pill(u,0.248,f"C{k+1}",font=fS)
pill(0.413,0.468,"P3",bg=(255,214,90,240))
pill(0.231,0.605,"P7",bg=(255,214,90,240))
pill(0.385,0.738,"P14",bg=(255,214,90,240))
pill(0.43,0.795,"Dauercamper-Parzellen",font=fS)
pill(0.32,0.935,"Rezeption + Kiosk",dot=(0.32,0.86))
pill(0.015,0.815,"Schranke / Einfahrt",font=fS,anchor="lm",dot=(0.19,0.864))
pill(0.705,0.80,"G1",font=fS)
pill(0.82,0.775,"G2 · Nova",dot=(0.815,0.86))
pill(0.74,0.96,"Gaststellplätze G1 / G2",font=fS)
pill(0.885,0.64,"Spielplatz",dot=(0.85,0.70))
# Kompass
cx,cy=P(0.945,0.90); s=26*S
d.ellipse([cx-s*1.5,cy-s*1.6,cx+s*1.5,cy+s*1.4],fill=(255,255,255,220))
d.polygon([(cx,cy-s),(cx-s*0.55,cy+s*0.7),(cx,cy+s*0.35),(cx+s*0.55,cy+s*0.7)],fill=(20,28,35,255))
d.text((cx,cy-s*1.25),"N",font=fS,fill=(20,28,35,255),anchor="mm")
out=Image.alpha_composite(im,ov).convert("RGB")
out.save("/home/claude/fall/img/lageplan_beschriftet_v2.jpg",quality=90)
out.resize((1200,1200),Image.LANCZOS).save("/home/claude/lp_web_v2.jpg",quality=82,optimize=True,progressive=True)
out.resize((900,900)).save("/home/claude/lp_check.jpg",quality=85)

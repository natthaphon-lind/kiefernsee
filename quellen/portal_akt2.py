"""Web-App-Teil für Akt 2: Karten, Rätsel (UV-Lampe, Karte, Mailbox), Prüfen und Hinweise."""
import html, json
import akt2_data as A

E = html.escape


def card(id_, lab, title, body, kind):
    tag = {"rot": "AKTE ROT", "blau": "AKTE BLAU", "alle": "FÜR BEIDE"}[kind]
    return (f'<section id="v-{id_}" class="card {kind}" hidden><span class="lab"><span class="tag {kind}">{tag}</span> {E(lab)}</span>'
            f'<h2>{E(title)}</h2>{body}</section>')


def photo(src, alt, cap):
    return (f'<figure class="photo"><a href="bilder/{src}" target="_blank" rel="noopener">'
            f'<img src="bilder/{src}" alt="{E(alt)}" loading="lazy"></a><figcaption>{E(cap)}</figcaption></figure>')


def qa(rows):
    return '<div class="qa mono">' + "".join(f'<p class="{"f" if w == "F" else "a"}"><b>{w}:</b> {E(t)}</p>' for w, t in rows) + "</div>"


def rows_table(rows):
    return '<dl class="form">' + "".join(f"<dt>{E(a)}</dt><dd><p>{E(b)}</p></dd>" for a, b in rows) + "</dl>"


def chat(rows, own_prefix):
    out = []
    for who, t, msg in rows:
        if t is None:
            out.append(f'<div class="day">{E(who)}</div>'); continue
        own = who.startswith(own_prefix)
        cls = " own" if own else ""
        if msg.startswith("🚫"):
            msg_html = '<p class="deleted">🚫 Diese Nachricht wurde gelöscht.</p>'
        else:
            msg_html = f"<p>{E(msg)}</p>"
        out.append(f'<div class="bub{cls}"><b>{"Ich" if own else E(who)}</b><span class="t">{t}</span>{msg_html}</div>')
    return f'<div class="chat">{"".join(out)}</div>'


def sealed_note(txt):
    return f'<p class="msg"><b>🔒 Versiegelt.</b> {E(txt)}</p>'


S = {}
# ---------------- ROT ----------------
S["r6"] = card("r6", "R-6 · " + A.MARCO_HEAD.split(". Personalien")[0], "Vernehmung Marco Lenz",
               f'<p class="small mono">{E(A.MARCO_HEAD)}</p>' + qa(A.MARCO)
               + '<div class="voice"><span class="mono small">Tonaufnahme der Vernehmung · Ausschnitt · 0:29</span>'
                 '<audio controls preload="metadata" src="audio/vernehmung-marco-r6.mp3">Euer Browser kann die Aufnahme nicht abspielen.</audio></div>'
                 '<p class="small">Ihr dürft die Aufnahme Akte Blau vorspielen.</p><p class="sig">M. Lenz</p>', "rot")

n, t1, t2, t3 = A.VISITENKARTE
S["r7"] = card("r7", "R-7 · " + A.BOETTCHER_HEAD, "Vernehmung Mark Böttcher",
               qa(A.BOETTCHER)
               + f'<div class="vcard"><b>{E(n)}</b><span>{E(t1)}</span><span class="small">{E(t2)}</span><b class="mono">{E(t3)}</b></div>'
                 '<p class="small">Lest Akte Blau die Handynummer vor – damit öffnet sie seine Mailbox (B-8).</p>', "rot")

fund = "".join(f'<li><b class="mono">{E(f)}</b> <span>{E(s)}</span></li>' for f, s in A.KASTEN_FUND)
log = "".join(f"<tr><td>{E(d)}</td><td>{E(t)}</td><td>{E(c)}</td><td>{E(f)}</td></tr>" for d, t, c, f in A.KASTEN_LOG)
S["r8"] = card("r8", "R-8 · Flur der Rezeption · Spurensicherung, Samstag, 26.09.", "Der Schlüsselkasten",
               "".join(f"<p>{E(p)}</p>" for p in A.KASTEN_INTRO.split("\n"))
               + photo("kasten.jpg", "Grauer Schlüsselkasten mit Zahlenfeld, daneben gelber Spurenmarker 1",
                       "Lichtbild 4: Schlüsselkasten im Flur der Rezeption")
               + f'<h3>Inhalt am Samstag, 8:47 Uhr</h3><ol class="assv">{fund}</ol>'
               + '<h3>Protokoll auslesen</h3>'
                 '<p>Fahrt mit dem Finger die UV-Lampe über das Zahlenfeld. Welche Tasten werden oft gedrückt? '
                 'Die Reihenfolge verrät euch Herr Lenz (R-6) zusammen mit der Chronik in Akte Blau (B-10).</p>'
                 '<div class="uvwrap"><canvas id="uv" width="300" height="400" aria-label="Zahlenfeld des Schlüsselkastens unter UV-Licht"></canvas></div>'
                 '<form id="uvForm" class="pinrow"><label for="uvPin">Code (4 Ziffern)</label>'
                 '<input id="uvPin" type="text" inputmode="numeric" maxlength="4" autocomplete="off" placeholder="_ _ _ _">'
                 '<button type="submit">Code eingeben</button></form><div id="uvMsg" class="msg" hidden></div>'
               + f'<div id="uvOpen" hidden style="display:flex;flex-direction:column;gap:10px"><div class="msg ok">Der Kasten piept. Das Protokoll öffnet sich.</div>'
                 f'<div class="scroll"><table class="mono"><thead><tr><th>Datum</th><th>Uhrzeit</th><th>Zugang</th><th>Aktion</th></tr></thead><tbody>{log}</tbody></table></div>'
                 f'<p class="small mono">{E(A.KASTEN_LOG_NOTE)}</p></div>', "rot")

zettel = "<br>".join(E(z) for z in A.ZETTEL)
S["r9"] = card("r9", "R-9 · Asservat Nr. 9, Spurensicherung, Samstag, 26.09.", "Fundstück aus Mietchalet 3",
               f"<p>{E(A.ZETTEL_INTRO)}</p>"
               f'<div class="zettel"><span class="zrest">{E(A.ZETTEL_REST)}</span><p>{zettel}</p></div>'
               f'<p class="small mono">{E(A.ZETTEL_KT)}</p>', "rot")

S["r10"] = card("r10", "R-10 · Suche am Fundort, Samstag, 26.09.", "Taucherbericht der Feuerwehr",
                f"<p>{E(A.TAUCHER_INTRO)}</p>"
                '<p><b>Tippt im Luftbild auf die Stelle, an der früher das Fasslager war.</b> Norden ist oben.</p>'
                '<div class="tapmap" id="tapMap"><img src="bilder/lageplan.jpg" width="1200" height="1200" alt="Luftbild des Campingplatzes"><span id="tapDot" hidden></span></div>'
                '<div id="tapMsg" class="msg" hidden></div>'
                '<div id="tapOpen" hidden style="display:flex;flex-direction:column;gap:12px"><div class="msg ok">Treffer. Der Bericht ist entsiegelt.</div>'
                + rows_table(A.TAUCHER)
                + photo("taucher.jpg", "Verrostete Stahlfässer im Schilf, Ölfilm auf dem Wasser, gelber Marker 4", A.TAUCHER_PHOTO_CAP)
                + "</div>", "rot")

spuren = "".join(f'<li><b class="mono">{E(a)}</b> <span>{E(b)}</span></li>' for a, b in A.STEG_SPUREN)
S["r11"] = card("r11", "R-11 · Spurensicherung Samstag 7:40 Uhr · Befragung Siggi Kowalski", "Spuren auf dem Steg",
                f"<p>{E(A.STEG_INTRO)}</p>"
                + photo("steg_spuren.jpg", "Grau lasierter Steg mit Fußabdrücken und Pfoten, gelbe Marker A bis D",
                        "Lichtbild 5: Abdrücke in der Lasur, Stegende")
                + f'<ol class="assv">{spuren}</ol><h3>Befragung Siggi Kowalski</h3><p class="small mono">{E(A.SIGGI_HEAD)}</p>' + qa(A.SIGGI), "rot")

# ---------------- BLAU ----------------
S["b6"] = card("b6", "B-6 · Aus dem Archiv der Rezeption", "Bodengutachten von 1996 (Auszug)",
               f'<p class="small">{E(A.GUTACHTEN_HEAD)}</p><div class="paper"><p class="mono" style="text-align:center"><b>INGENIEURBÜRO HARTWIG · SEEBRÜCK</b></p>'
               + rows_table(A.GUTACHTEN) + f'<p class="pencil">{E(A.GUTACHTEN_NOTE.split(": ", 1)[1])}</p></div>'
               f'<p class="small">{E(A.GUTACHTEN_NOTE.split(":")[0])} (unten rechts).</p>', "blau")

S["b7"] = card("b7", "B-7 · Von Hand gezeichnet, Ingenieurbüro Hartwig", "Anlage 3: Lageplan von 1996",
               f"<p>{E(A.KARTE_INTRO)}</p>" + photo("karte1996.jpg", "Handgezeichneter Lageplan von 1996 mit Fasslager", "Tippt auf die Karte, um sie groß zu sehen."), "blau")

S["b8"] = card("b8", "B-8 · Kriminaltechnik Seebrück", "Die Mailbox von Mark Böttcher",
               f"<p>{E(A.MAILBOX_INTRO)}</p>"
               '<div class="phone"><div id="dial" class="dial mono">&nbsp;</div><div class="keys" id="keys"></div>'
               '<div class="hrow" style="justify-content:center"><button type="button" id="dialDel" class="ghost">⌫ Löschen</button>'
               '<button type="button" id="dialCall" class="call">📞 Anrufen</button></div></div>'
               '<div id="dialMsg" class="msg" hidden></div>'
               f'<div id="mailOpen" hidden class="voice"><span class="mono small">{E(A.MAILBOX_HEAD)}</span>'
               '<audio id="mailAudio" controls preload="metadata" src="audio/mailbox-b8.mp3">Euer Browser kann die Aufnahme nicht abspielen.</audio>'
               f'<details><summary>Abschrift anzeigen</summary><p>{E(A.MAILBOX)}</p></details>'
               '<p class="small">Ihr dürft die Nachricht Akte Rot vorspielen.</p></div>', "blau")

dm = []
for who, t, msg in A.NOVA_DM:
    if t is None:
        dm.append(f'<div class="day">{E(who)}</div>'); continue
    own = who == "nova"
    dm.append(f'<div class="dm{" own" if own else ""}"><p>{E(msg)}</p><span class="t">{t}</span></div>')
S["b9"] = card("b9", "B-9 · Vom Handy von Nova Sommer, Bildschirmfotos der Polizei", "Direktnachrichten @nova.on.wheels",
               f'<p><i>{E(A.NOVA_INTRO)}</i></p><div class="dmbox"><b>m.lenz.repariert</b><span class="small">Hausmeister · repariert alles</span>{"".join(dm)}</div>', "blau")

chron = "".join(f'<li><b class="mono">{E(j)}</b><span>{E(t)}</span></li>' for j, t in A.CHRONIK)
S["b10"] = card("b10", "B-10 · Chronik und Schlüsselliste", "Unterlagen der Interessengemeinschaft",
                f'<p class="small">{E(A.VEREIN_HEAD)}</p><div class="paper"><div class="ighead">Interessengemeinschaft der Dauercamper am Kiefernsee</div>'
                f'<h3>Unsere Chronik</h3><ol class="chron">{chron}</ol><h3>Wer hat welchen Schlüssel?</h3>' + rows_table(A.SCHLUESSEL)
                + '<p class="sig">A. Wohlfahrt</p><p class="small">Schriftführerin</p></div>', "blau")

S["b11"] = card("b11", "B-11 · Export vom Handy von Angelika Wohlfahrt", "Chat „Kiefernsee Dauercamper“ – vollständig",
                f'<p class="small">{E(A.CHAT2_INTRO)}</p>' + chat(A.CHAT2, "Angelika"), "blau")

S["lock2"] = card("lock2", "Akt 2 · Wer lügt?", "Noch versiegelt",
                  '<p>Diese Akte gehört zu Akt 2. Sie öffnet sich auf diesem Handy, sobald ihr Akt 1 gelöst und euren Verdacht unter '
                  '„Akt 1 abschließen“ versiegelt habt.</p><button type="button" data-view="akt">Zu „Akt abschließen“</button>', "alle")

ROT_NAV2 = [("r6", "R-6", "Vernehmung Marco Lenz"), ("r7", "R-7", "Vernehmung Böttcher"), ("r8", "R-8", "Schlüsselkasten 🔒"),
            ("r9", "R-9", "Zettel aus Chalet 3"), ("r10", "R-10", "Taucherbericht 🔒"), ("r11", "R-11", "Spuren auf dem Steg")]
BLAU_NAV2 = [("b6", "B-6", "Gutachten 1996"), ("b7", "B-7", "Karte von 1996"), ("b8", "B-8", "Mailbox 🔒"),
             ("b9", "B-9", "Novas Nachrichten"), ("b10", "B-10", "Chronik der IG"), ("b11", "B-11", "Chat vollständig")]
ALL_NAV2 = [("code2", "Akt 2 lösen", "Antworten prüfen"), ("hints2", "Hinweise Akt 2", "Hilfe in drei Stufen")]
VIEWS2 = [k for k, _a, _b in ROT_NAV2 + BLAU_NAV2 + ALL_NAV2]

opts = lambda o: "".join(f'<option value="{i}">{i} · {E(t)}</option>' for i, t in enumerate(o, 1))
CODE2 = (f'''<section id="v-code2" class="card alle" hidden>
<span class="lab"><span class="tag alle">FÜR BEIDE</span> Akt 2 · Wer lügt?</span><h2>Antworten prüfen</h2>
<form id="codeForm2" style="display:flex;flex-direction:column;gap:14px">'''
         + "".join(f'<div class="q"><label for="q2{i}">{E(k)}: {E(q)}</label><select id="q2{i}"><option value="">bitte wählen</option>{opts(o)}</select></div>'
                   for i, (k, q, o) in enumerate(A.Q, 1))
         + '''<button type="submit">Antwort prüfen</button><div id="codeMsg2" class="msg" hidden></div></form>
<div id="codeLock2" class="msg" hidden>Akt 2 ist auf diesem Handy versiegelt. Prüfen und Hinweise sind geschlossen.</div>
<p class="small">Jede falsche Antwort kostet euer Team 2 Punkte.</p></section>
<section id="v-hints2" class="card alle" hidden>
<span class="lab"><span class="tag alle">FÜR BEIDE</span> Akt 2 · Hinweise</span><h2>Hilfe in drei Stufen</h2>
<p class="small">Stufe 1 ist ein kleiner Tipp, Stufe 2 ein großer Tipp, Stufe 3 verrät die Lösung. Jede geöffnete Stufe kostet euer Team einen Punkt. Öffnen beide Handys dieselbe Stufe, zählt sie doppelt.</p>
<div class="hints" id="hintBox2"></div></section>''')

CSS = r"""
.vcard{align-self:flex-start;display:flex;flex-direction:column;gap:2px;background:#fff;color:#1d2428;border-top:8px solid #1e5a38;border-radius:3px;padding:14px 18px;box-shadow:0 3px 10px rgba(0,0,0,.18);transform:rotate(-1.5deg);min-width:240px}
.vcard b{font-size:18px} .vcard .mono{font-size:16px;margin-top:8px}
.uvwrap{display:flex;justify-content:center}
#uv{width:100%;max-width:300px;height:auto;border-radius:8px;touch-action:none;background:#111;cursor:crosshair}
.pinrow{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:end} .pinrow label{grid-column:1/-1}
.pinrow input{font-family:var(--f-mono);font-size:22px;letter-spacing:.3em;text-align:center}
.zettel{position:relative;align-self:center;max-width:360px;width:100%;background:#fbfbf6 repeating-linear-gradient(0deg,transparent 0 17px,#cbd8e4 17px 18px),#fbfbf6;
 background-image:repeating-linear-gradient(0deg,transparent 0 17px,#cbd8e4 17px 18px),repeating-linear-gradient(90deg,transparent 0 17px,#cbd8e4 17px 18px);
 color:#1a2f8c;font-family:var(--f-mono);font-weight:600;font-size:17px;line-height:1.9;padding:34px 20px 20px;transform:rotate(1.2deg);box-shadow:0 4px 12px rgba(0,0,0,.2)}
.zrest{position:absolute;top:6px;left:10px;color:#1e7340;font-family:var(--f-display);font-weight:700;font-size:13px}
.tapmap{position:relative;line-height:0;border-radius:4px;overflow:hidden;cursor:crosshair}
.tapmap img{width:100%;height:auto;display:block}
#tapDot{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border:3px solid #fff;border-radius:50%;background:rgba(168,50,42,.75);box-shadow:0 0 0 2px #a8322a}
.paper{background:#f6f1e1;color:#2a2a2a;border:1px solid #d8cfb2;border-radius:3px;padding:14px;display:flex;flex-direction:column;gap:10px}
.paper dl.form dt{color:#6b6450} .paper dl.form dd{color:#2a2a2a}
.pencil{font-family:Georgia,serif;font-style:italic;font-weight:700;color:#55565c;transform:rotate(3deg);align-self:flex-end}
.ighead{background:#1e7340;color:#fff;font-family:var(--f-display);font-weight:700;padding:8px 10px;border-radius:2px}
ol.chron{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:6px} ol.chron li{display:grid;grid-template-columns:52px 1fr;gap:8px}
.phone{align-self:center;background:#1b1b1e;border-radius:26px;padding:18px;display:flex;flex-direction:column;gap:14px;width:100%;max-width:290px}
.dial{background:#f2f2f2;color:#111;border-radius:8px;padding:10px;text-align:center;font-size:20px;min-height:48px;letter-spacing:.06em;word-break:break-all}
.keys{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.keys button{background:#e8e8ea;color:#111;border-radius:50%;aspect-ratio:1;font-size:24px;padding:0}
.phone .ghost{color:#fff;border-color:#555} button.call{background:#2f8a43;color:#fff}
.dmbox{background:#18181b;color:#fff;border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:6px}
.dmbox .small{color:#a7a7ad}
.dm{background:#3b3b40;border-radius:12px;padding:6px 10px;max-width:82%;font-size:14px;display:flex;flex-direction:column}
.dm.own{background:#6c4bd8;align-self:flex-end} .dm .t{font-size:11px;opacity:.7;align-self:flex-end}
.dmbox .day{text-align:center;font-size:11px;font-weight:700;color:#a7a7ad;margin:6px 0}
.deleted{font-style:italic;color:#6b7378}
"""

JS = r'''<script>
(function(){
  var $=function(id){return document.getElementById(id)}, G=window.__kgame;
  var SFX=((location.search.match(/[?&]slot=(\w+)/)||[])[1]||""); SFX=SFX?"-"+SFX:"";
  var PKEY="kiefernsee-raetsel"+SFX;
  function getP(){try{return JSON.parse(localStorage.getItem(PKEY)||"{}")}catch(e){return {}}}
  function setP(k){var p=getP();p[k]=1;try{localStorage.setItem(PKEY,JSON.stringify(p))}catch(e){}}

  // ---------- UV-Lampe (R-8) ----------
  var cv=$("uv"), cx=cv.getContext("2d"), KEYS=["1","2","3","4","5","6","7","8","9","*","0","#"], GLOW={"1":1,"9":1,"6":1};
  var lamp=null;
  function keyPos(i){return {x:60+(i%3)*90, y:95+Math.floor(i/3)*80}}
  function draw(){
    cx.fillStyle="#141416"; cx.fillRect(0,0,300,400);
    cx.fillStyle="#2a2a2e"; cx.fillRect(18,40,264,340);
    KEYS.forEach(function(k,i){ var p=keyPos(i);
      cx.fillStyle="#3a3a3e"; cx.beginPath(); cx.roundRect?cx.roundRect(p.x-32,p.y-26,64,52,8):cx.rect(p.x-32,p.y-26,64,52); cx.fill();
      cx.fillStyle="#77777c"; cx.font="bold 26px system-ui,sans-serif"; cx.textAlign="center"; cx.textBaseline="middle"; cx.fillText(k,p.x,p.y) });
    if(lamp){
      cx.save(); cx.beginPath(); cx.arc(lamp.x,lamp.y,70,0,Math.PI*2); cx.clip();
      cx.fillStyle="rgba(70,20,140,.55)"; cx.fillRect(0,0,300,400);
      KEYS.forEach(function(k,i){ var p=keyPos(i);
        if(GLOW[k]){ var g=cx.createRadialGradient(p.x+4,p.y+3,2,p.x+4,p.y+3,30); g.addColorStop(0,"rgba(190,255,250,.95)"); g.addColorStop(.6,"rgba(120,230,255,.55)"); g.addColorStop(1,"rgba(120,230,255,0)");
          cx.fillStyle=g; cx.beginPath(); cx.ellipse(p.x+4,p.y+3,28,22,.4,0,Math.PI*2); cx.fill();
          cx.strokeStyle="rgba(210,255,255,.5)"; cx.lineWidth=1; for(var r=6;r<22;r+=4){cx.beginPath(); cx.ellipse(p.x+4,p.y+3,r,r*.75,.4,0,Math.PI*2); cx.stroke()} }
        cx.fillStyle="#c9b8ff"; cx.font="bold 26px system-ui,sans-serif"; cx.fillText(k,p.x,p.y) });
      cx.restore();
      var gl=cx.createRadialGradient(lamp.x,lamp.y,50,lamp.x,lamp.y,74); gl.addColorStop(0,"rgba(150,90,255,0)"); gl.addColorStop(1,"rgba(150,90,255,.6)");
      cx.strokeStyle=gl; cx.lineWidth=6; cx.beginPath(); cx.arc(lamp.x,lamp.y,71,0,Math.PI*2); cx.stroke();
    } else { cx.fillStyle="#9a9aa0"; cx.font="15px system-ui,sans-serif"; cx.textAlign="center"; cx.fillText("Finger hier drüberziehen",150,22) }
  }
  function pos(e){var r=cv.getBoundingClientRect(),t=e.touches?e.touches[0]:e;return {x:(t.clientX-r.left)*300/r.width,y:(t.clientY-r.top)*400/r.height}}
  function mv(e){var q=pos(e);if(!isFinite(q.x)||!isFinite(q.y))return;lamp=q;draw();if(e.cancelable)e.preventDefault()}
  cv.addEventListener("pointerdown",function(e){cv.setPointerCapture&&cv.setPointerCapture(e.pointerId);mv(e)});
  cv.addEventListener("pointermove",function(e){if(e.pointerType==="mouse"||e.buttons||e.pressure)mv(e)});
  cv.addEventListener("pointerup",function(){});
  draw();
  function uvOpen(){ $("uvOpen").hidden=false; $("uvForm").hidden=true; $("uvMsg").hidden=true }
  $("uvForm").addEventListener("submit",function(e){ e.preventDefault(); var v=($("uvPin").value||"").replace(/\D/g,""), m=$("uvMsg"); m.hidden=false;
    if(v==="'''+A.KASTEN_CODE+r'''"){ setP("uv"); uvOpen(); return }
    m.className="msg bad"; m.textContent = v.length!==4 ? "Der Code hat genau 4 Ziffern." : "Der Kasten piept zweimal. Falscher Code. Welches Jahr meint Herr Lenz? Fragt Akte Blau nach der Chronik."; });
  if(getP().uv) uvOpen();

  // ---------- Karte antippen (R-10) ----------
  var map=$("tapMap");
  function tapOpen(){ $("tapOpen").hidden=false; $("tapMsg").className="msg ok"; $("tapMsg").hidden=true }
  map.addEventListener("click",function(e){ if(!$("tapOpen").hidden) return; var r=map.getBoundingClientRect(), x=(e.clientX-r.left)/r.width, y=(e.clientY-r.top)/r.height;
    var d=$("tapDot"); d.hidden=false; d.style.left=(x*100)+"%"; d.style.top=(y*100)+"%"; var m=$("tapMsg"); m.hidden=false;
    if(x>=0.62&&y<=0.27){ setP("map"); tapOpen(); $("tapOpen").scrollIntoView({behavior:"smooth",block:"start"}); return }
    m.className="msg bad"; m.textContent="Hier haben die Taucher nichts gefunden. Fragt Akte Blau noch einmal genau: An welchem Ufer, in welcher Ecke des Sees?"; });
  if(getP().map) tapOpen();

  // ---------- Mailbox wählen (B-8) ----------
  var num="", NR="'''+A.MAILBOX_NUMBER+r'''";
  function showNum(){ var s=num.replace(/^(\d{4})(\d{0,3})(\d{0,2})(\d{0,2})$/,function(a,b,c,d,e){return [b,c,d,e].filter(Boolean).join(" ")}); $("dial").textContent=s||" " }
  ["1","2","3","4","5","6","7","8","9","*","0","#"].forEach(function(k){ var b=document.createElement("button"); b.type="button"; b.textContent=k;
    b.addEventListener("click",function(){ if(num.length<14){num+=k; showNum()} }); $("keys").appendChild(b) });
  $("dialDel").addEventListener("click",function(){ num=num.slice(0,-1); showNum() });
  function mailOpen(){ $("mailOpen").hidden=false; $("dialMsg").hidden=true }
  $("dialCall").addEventListener("click",function(){ var m=$("dialMsg"); m.hidden=false;
    if(num===NR){ setP("mail"); mailOpen(); m.hidden=true; try{$("mailAudio").play()}catch(e){} return }
    m.className="msg bad"; m.textContent = num.length<11 ? "Die Nummer ist zu kurz. Akte Rot hat sie auf der Visitenkarte (R-7)." : "Kein Anschluss unter dieser Nummer. Lasst sie euch von Akte Rot noch einmal vorlesen."; });
  if(getP().mail) mailOpen();

  // ---------- Akt 2 prüfen ----------
  var RIGHT='''+json.dumps(list(A.RIGHT))+r''', WRONG='''+json.dumps(A.WRONG, ensure_ascii=False)+r''';
  $("codeForm2").addEventListener("submit",function(e){ e.preventDefault();
    var a=[+$("q21").value,+$("q22").value,+$("q23").value], m=$("codeMsg2"); m.hidden=false;
    if(!a[0]||!a[1]||!a[2]){ m.className="msg bad"; m.textContent="Bitte alle drei Fragen beantworten."; return }
    if(G&&G.sealed(2)){ m.className="msg"; m.textContent="Akt 2 ist schon versiegelt."; return }
    for(var i=0;i<3;i++){ if(a[i]!==RIGHT[i]){ if(G) G.wrong(2); m.className="msg bad"; m.textContent="Hauptkommissarin Wendland schüttelt den Kopf. "+WRONG[i]+" (−2 Punkte)"; return } }
    if(G) G.right(2);
    m.className="msg ok"; m.textContent='''+json.dumps(A.RIGHT_MSG.replace("Lest jetzt die Auflösung von Akt 2 im Buch.", "Lest jetzt die Auflösung von Akt 2 im Buch (Seite 44). Danach versiegelt jeder unter „Akt abschließen“ seinen Hauptverdacht."), ensure_ascii=False)+r''';
  });
  var H='''+json.dumps([list(h) for h in A.HINTS], ensure_ascii=False)+r''', box=$("hintBox2");
  H.forEach(function(h,qi){
    var d=document.createElement("div"); d.className="card"; d.style.padding="14px";
    var t=document.createElement("b"); t.textContent=h[0]; d.appendChild(t);
    var row=document.createElement("div"); row.className="hrow"; d.appendChild(row);
    var out=document.createElement("div"); out.className="hints"; d.appendChild(out);
    [1,2,3].forEach(function(s){
      var b=document.createElement("button"); b.type="button"; b.className="ghost"; b.textContent="Stufe "+s+" · "+["","Kleiner Tipp","Großer Tipp","Lösung"][s]+" · −1";
      var id="A2-"+qi+"-"+s;
      function reveal(){ b.disabled=true; var p=document.createElement("div"); p.className="msg"; p.textContent=["","Kleiner Tipp","Großer Tipp","Lösung"][s]+": "+h[s]; out.appendChild(p) }
      b.addEventListener("click",function(){ if(b.disabled) return; if(G&&!G.openHint(id,2)) return; reveal() });
      if(G&&G.hintOpened(id)){ setTimeout(reveal,0) } else if(G&&G.sealed(2)){ b.disabled=true }
      row.appendChild(b);
    });
    box.appendChild(d);
  });
  if(G) G.refresh();
})();
</script>'''

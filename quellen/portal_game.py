"""Spielstand-Teil der Web-App: Punkte, Verdacht versiegeln, Übergabe Blau -> Rot."""
import html

E = html.escape


def game_html(suspects):
    opts = "".join(f'<option value="{i}">{E(n)}</option>' for i, n in enumerate(suspects))
    return f'''<section id="v-akt" class="card alle" hidden>
<span class="lab"><span class="tag alle">FÜR BEIDE</span> Akt 1 · Abschluss</span><h2>Akt 1 abschließen</h2>
<div id="aktLocked" class="msg">Zuerst löst ihr gemeinsam die <a href="#code">Code-Prüfung</a>. Danach versiegelt hier jeder seinen Hauptverdacht.</div>
<div id="aktOpen" hidden style="display:flex;flex-direction:column;gap:12px">
<p>Wer steckt eurer Meinung nach hinter allem? Jeder wählt <b>geheim auf seinem eigenen Handy</b> einen Hauptverdacht. Zeigt dem anderen nicht euren Bildschirm.</p>
<label for="sus">Mein Hauptverdacht nach Akt 1</label>
<select id="sus"><option value="">bitte wählen</option>{opts}</select>
<button id="sealBtn" type="button">Verdacht versiegeln</button>
<div id="sealAsk" class="confirm" hidden><span><b>Sicher?</b> Nach dem Versiegeln kannst du deinen Verdacht für Akt 1 nicht mehr ändern. Auch Code-Prüfung und Hinweise für Akt 1 sind danach geschlossen.</span>
<button id="sealYes" type="button">Ja, versiegeln</button><button id="sealNo" type="button" class="ghost">Abbrechen</button></div>
</div>
<div id="aktSealed" hidden style="display:flex;flex-direction:column;gap:12px">
<div class="seal"><span class="sealIcon" aria-hidden="true">🔒</span><div><b>Verdacht für Akt 1 versiegelt</b><span id="sealTime" class="small"></span></div></div>
<div id="blueGive" hidden style="display:flex;flex-direction:column;gap:10px;align-items:center;text-align:center">
<h3>An die Spielleitung übergeben</h3>
<p class="small">Akte Rot ist die Spielleitung. Akte Rot öffnet in der eigenen Web-App „Akt 1 abschließen“ und tippt auf „QR-Code scannen“. Der Code verrät euren Verdacht nicht.</p>
<div id="giveQr" class="qrbox"></div>
<p class="small" id="giveDed"></p></div>
<div id="redTake" hidden style="display:flex;flex-direction:column;gap:10px">
<h3>Spielstand von Akte Blau einlesen</h3>
<p class="small">Akte Blau zeigt nach dem Versiegeln einen QR-Code. Scannt ihn am besten hier in der Web-App.</p>
<button id="scanBtn" type="button">QR-Code scannen</button>
<div id="scanBox" hidden class="scanbox"><video id="scanVid" playsinline muted></video><button id="scanStop" type="button" class="ghost">Abbrechen</button></div>
<p class="small"><b>Scannen klappt hier nicht?</b> Dann scannt den Code einfach mit der normalen Kamera-App eures Handys – genau wie die QR-Codes im Buch. Der Spielstand wird trotzdem übernommen.</p>
<div id="takeMsg" class="msg" hidden></div></div>
<div id="teamSum" hidden class="msg ok"></div>
</div>
</section>
<section id="v-neu" class="card alle" hidden>
<span class="lab"><span class="tag alle">FÜR BEIDE</span> Einstellungen</span><h2>Neues Spiel starten</h2>
<p>Löscht auf diesem Handy alle Punkte, versiegelten Verdachte, die gewählte Akte und deinen Namen. Das Kennwort bleibt gespeichert.</p>
<p class="small">Spielt ihr zu zweit von vorn, macht das bitte auf beiden Handys.</p>
<button id="resetBtn" type="button" class="ghost">Spielstand löschen</button>
<div id="resetAsk" class="confirm" hidden><span><b>Wirklich alles löschen?</b> Das lässt sich nicht rückgängig machen.</span>
<button id="resetYes" type="button">Ja, löschen</button><button id="resetNo" type="button" class="ghost">Abbrechen</button></div>
</section>'''


GAME_CSS = r"""
.score{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:8px 14px;border:1px solid var(--line);border-radius:4px;background:var(--paper);font-size:14px}
.score b{font-family:var(--f-display);font-size:20px;letter-spacing:.04em}
.seal{display:flex;gap:12px;align-items:center;padding:12px 14px;border:2px solid var(--stamp);border-radius:4px;color:var(--stamp)}
.seal b{display:block;font-family:var(--f-display);font-size:18px;letter-spacing:.04em}
.sealIcon{font-size:32px}
h3{font-family:var(--f-display);font-size:18px;margin:4px 0 0}
.qrbox{background:#fff;padding:10px;border-radius:6px;line-height:0}
.qrbox svg{width:220px;height:220px;display:block}
.bigcode{font-size:28px;font-weight:600;letter-spacing:.12em;margin:0}
.scanbox{display:flex;flex-direction:column;gap:8px}
.scanbox video{width:100%;max-height:60vh;background:#000;border-radius:6px;object-fit:cover}
button:disabled{opacity:.45;cursor:not-allowed}
"""


def game_js(suspects, portal):
    import json
    return r'''<script>
(function(){
  var SUS=''' + json.dumps(suspects, ensure_ascii=False) + r''', PORTAL=''' + json.dumps(portal) + r''';
  var SFX=((location.search.match(/[?&]slot=(\w+)/)||[])[1]||""); SFX=SFX?"-"+SFX:"";
  var GKEY="kiefernsee-spiel"+SFX, RKEY="kiefernsee-rolle"+SFX, NKEY="kiefernsee-name"+SFX, ACT=1, START=10;
  var $=function(id){return document.getElementById(id)};
  function load(){try{var s=JSON.parse(localStorage.getItem(GKEY)||"null");if(s&&s.v===1)return s}catch(e){}return {v:1,ded:{},hints:{},solved:{},seal:{},blue:{}}}
  var G=load();
  function save(){try{localStorage.setItem(GKEY,JSON.stringify(G))}catch(e){}}
  function role(){try{return localStorage.getItem(RKEY)}catch(e){return null}}
  function myName(){try{return localStorage.getItem(NKEY)||""}catch(e){return ""}}
  function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
  function who(kind,n){return "Akte "+kind+(n?" ("+n+")":"")}
  function ded(a){var d=G.ded[a]||{c:0,h:0};return d.c*2+d.h}
  function sealed(a){return !!G.seal[a]}

  // ---------- Übergabe-Code: 6 Zeichen, nicht lesbar ----------
  var AB="ABCDEFGHJKLMNPQRSTUVWXYZ23456789", M=0x3FFFFFFF, MUL=0x2f1b3a7, INV=0x26fbc417, XK=0x15A3C96E&M;
  function chk(x){var h=2166136261;for(var i=0;i<3;i++){h^=(x>>>(i*6))&63;h=Math.imul(h,16777619)>>>0}return (h^(h>>>12))&0xFFF}
  function enc(a,s,d){var salt=Math.floor(Math.random()*128),x=(((a&3)<<16)|((s&7)<<13)|((Math.min(d,63))<<7)|salt)&0x3FFFF;
    var v=((x<<12)|chk(x))&M; v=(Math.imul(v,MUL)&M)^XK; var o="";for(var i=0;i<6;i++){o=AB[v&31]+o;v=v>>>5}return o}
  function dec(str){str=(str||"").toUpperCase().replace(/[^A-Z0-9]/g,"").replace(/O/g,"0");if(str.length!==6)return null;var v=0;
    for(var i=0;i<6;i++){var k=AB.indexOf(str[i]);if(k<0)return null;v=v*32+k}
    v=Math.imul((v^XK)&M,INV)&M; var x=v>>>12; if(chk(x)!==(v&0xFFF))return null;
    return {a:(x>>>16)&3,s:(x>>>13)&7,d:(x>>>7)&63}}
  window.__kcode={enc:enc,dec:dec};

  // ---------- Punkteanzeige ----------
  function score(){
    var r=role(), el=$("scoreTxt"), sub=$("scoreSub"); if(!el) return;
    if(r==="rot"){ var b=G.blue[ACT]; var t=START-ded(ACT)-(b?b.d:0);
      el.textContent=t+" Punkte"; sub.textContent=b?"Teamstand, "+who("Blau",b.n)+" ist eingerechnet":"Teamstand · Abzüge von Akte Blau kommen am Ende des Akts dazu"; }
    else { el.textContent=(ded(ACT)?"−"+ded(ACT):"0")+" Punkte"; sub.textContent="Eure Abzüge auf diesem Handy · gehen am Ende an Akte Rot"; }
  }

  // ---------- Code-Prüfung und Hinweise anbinden ----------
  window.__kgame={
    wrong:function(){ if(sealed(ACT)) return; G.ded[ACT]=G.ded[ACT]||{c:0,h:0}; G.ded[ACT].c++; save(); score() },
    right:function(){ G.solved[ACT]=1; save(); refresh() },
    hintOpened:function(id){ return !!G.hints[id] },
    openHint:function(id){ if(G.hints[id]||sealed(ACT)) return false; G.hints[id]=1; G.ded[ACT]=G.ded[ACT]||{c:0,h:0}; G.ded[ACT].h++; save(); score(); return true },
    sealed:function(){ return sealed(ACT) },
    solved:function(){ return !!G.solved[ACT] },
    refresh:function(){ refresh() },
    importCode:function(c,n){ return take(c,n) }
  };

  function hhmm(){var d=new Date();return ("0"+d.getHours()).slice(-2)+":"+("0"+d.getMinutes()).slice(-2)}

  function refresh(){
    score();
    var r=role(), s=G.seal[ACT];
    $("aktLocked").hidden=!!G.solved[ACT]||!!s; $("aktOpen").hidden=!G.solved[ACT]||!!s; $("aktSealed").hidden=!s;
    if(s){ $("sealTime").textContent=" um "+s.t+" Uhr. "+(myName()?myName()+", dein":"Dein")+" Verdacht bleibt bis zur Auflösung geheim."; }
    $("blueGive").hidden=!(s&&r==="blau"); $("redTake").hidden=(r!=="rot");
    if(r==="rot"){ $("aktSealed").hidden=false; if(!s){ $("aktSealed").querySelector(".seal").hidden=true } else { $("aktSealed").querySelector(".seal").hidden=false } }
    if(s&&r==="blau"){
      if(!s.code){ s.code=enc(ACT,s.s,ded(ACT)); save() }
      $("giveDed").textContent="Übergeben werden: euer versiegelter Verdacht und eure Abzüge ("+(ded(ACT)?"−"+ded(ACT):"0")+" Punkte).";
      try{var q=qrcode(0,"M");q.addData(PORTAL+"#k="+s.code+(myName()?"&n="+encodeURIComponent(myName()):""));q.make();$("giveQr").innerHTML=q.createSvgTag({cellSize:6,margin:2,scalable:true})}catch(e){$("giveQr").textContent=""}
    }
    var b=G.blue[ACT], ts=$("teamSum");
    if(r==="rot"&&b){ ts.hidden=false;
      ts.innerHTML="🔒 Verdacht von "+esc(who("Blau",b.n))+" für Akt 1 gespeichert.<br>Punkte nach Akt 1: "+START+" − "+esc(myName()||"Rot")+" "+ded(ACT)+" − "+esc(b.n||"Blau")+" "+b.d+" = <b>"+(START-ded(ACT)-b.d)+" Punkte</b>"+
        (s?"<br>Beide Verdachte sind versiegelt. Die Siegel öffnen sich bei der großen Auflösung im letzten Akt. Akt 2 „Wer lügt?“ folgt im fertigen Buch.":"<br>Jetzt noch deinen eigenen Verdacht oben versiegeln.");
    } else ts.hidden=true;
    // Code-Prüfung und Hinweise nach dem Versiegeln sperren
    var lock=sealed(ACT); document.querySelectorAll("#codeForm select,#codeForm button,#hintBox button").forEach(function(el){ if(lock) el.disabled=true });
    var cl=$("codeLock"); if(cl) cl.hidden=!lock;
  }

  // ---------- Versiegeln ----------
  $("sealBtn").addEventListener("click",function(){ if($("sus").value===""){ $("sus").focus(); return } $("sealAsk").hidden=false });
  $("sealNo").addEventListener("click",function(){ $("sealAsk").hidden=true });
  $("sealYes").addEventListener("click",function(){ var v=+$("sus").value; G.seal[ACT]={s:v,t:hhmm()}; save(); $("sealAsk").hidden=true; $("sus").value=""; refresh(); $("v-akt").scrollIntoView({block:"start"}) });

  // ---------- Einlesen bei Rot ----------
  function msg(ok,t){var m=$("takeMsg");m.hidden=false;m.className="msg "+(ok?"ok":"bad");m.textContent=t}
  function take(c,n){
    if(role()!=="rot"){ return false }
    var p=dec(c); if(!p){ msg(false,"Dieser QR-Code gehört nicht zum Spiel. Bitte den Code von Akte Blau scannen."); return false }
    if(p.a!==ACT){ msg(false,"Dieser Code gehört zu Akt "+p.a+", nicht zu Akt "+ACT+"."); return false }
    if(G.blue[ACT]){ msg(true,"Der Spielstand von Akte Blau für Akt "+ACT+" ist schon gespeichert."); return true }
    G.blue[ACT]={s:p.s,d:p.d,n:(n||"").slice(0,20)}; save(); $("takeMsg").hidden=true; refresh(); return true
  }

  var stream=null, raf=0;
  function stopScan(){ if(raf) cancelAnimationFrame(raf); raf=0; if(stream){stream.getTracks().forEach(function(t){t.stop()})} stream=null; $("scanBox").hidden=true; $("scanBtn").hidden=false }
  function loadJsQR(cb){ if(window.jsQR) return cb(); var s=document.createElement("script"); s.src="js/jsQR.js"; s.onload=cb; s.onerror=function(){msg(false,"Der Scanner konnte nicht geladen werden. Scannt den Code mit der normalen Kamera-App.")}; document.head.appendChild(s) }
  $("scanBtn").addEventListener("click",function(){
    if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){ msg(false,"Dieses Handy erlaubt hier keinen Kamerazugriff. Scannt den Code mit der normalen Kamera-App."); return }
    loadJsQR(function(){
      navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"}}).then(function(st){
        stream=st; var v=$("scanVid"); v.srcObject=st; v.setAttribute("playsinline",""); v.play(); $("scanBox").hidden=false; $("scanBtn").hidden=true;
        var cv=document.createElement("canvas"), cx=cv.getContext("2d",{willReadFrequently:true});
        (function tick(){ if(!stream) return;
          if(v.readyState===v.HAVE_ENOUGH_DATA){ var w=v.videoWidth,h=v.videoHeight,sc=Math.min(1,640/Math.max(w,h)); cv.width=w*sc; cv.height=h*sc; cx.drawImage(v,0,0,cv.width,cv.height);
            var r=jsQR(cx.getImageData(0,0,cv.width,cv.height).data,cv.width,cv.height,{inversionAttempts:"dontInvert"});
            if(r&&r.data){ var m=r.data.match(/#k=([A-Z0-9]{6})(?:&n=([^&#]*))?/i); var c=m?m[1]:r.data, nn=""; try{nn=m&&m[2]?decodeURIComponent(m[2]):""}catch(e){} stopScan(); take(c,nn); return } }
          raf=requestAnimationFrame(tick) })();
      }).catch(function(){ msg(false,"Kein Zugriff auf die Kamera. Scannt den Code einfach mit der normalen Kamera-App.") });
    });
  });
  $("scanStop").addEventListener("click",stopScan);

  // ---------- Neues Spiel ----------
  $("resetBtn").addEventListener("click",function(){ $("resetAsk").hidden=false });
  $("resetNo").addEventListener("click",function(){ $("resetAsk").hidden=true });
  $("resetYes").addEventListener("click",function(){ try{localStorage.removeItem(GKEY);localStorage.removeItem(RKEY);localStorage.removeItem(NKEY)}catch(e){} location.hash=""; location.reload() });

  // Link aus Blaus QR-Code mit der normalen Kamera geöffnet
  function hashImport(){ var m=(location.hash||"").match(/^#k=([A-Z0-9]{6})(?:&n=([^&#]*))?$/i); if(!m) return;
    var nn=""; try{nn=m[2]?decodeURIComponent(m[2]):""}catch(e){}
    if(role()==="rot"&&!$("app").hidden){ take(m[1],nn); history.replaceState(null,"",location.pathname+location.search+"#akt"); window.dispatchEvent(new HashChangeEvent("hashchange")) } }
  window.addEventListener("hashchange",hashImport);
  window.__kgame.hashImport=hashImport;
  refresh();
})();
</script>'''

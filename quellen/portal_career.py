"""Ermittler-Laufbahn für alle Bände der Reihe: Profil, Dienstgrade, Dienstnummer, Dienstausweis.

Das Profil liegt unter dem Schlüssel „ermittler-profil“ – gleiche Adresse (natthaphon-lind.github.io)
für alle Bände, deshalb übernimmt jedes neue Buch den Rang automatisch auf demselben Handy.
"""
import json

# Fälle der Reihe: Bit-Nummer -> Name. Neue Bände hier ergänzen, Bits nie umnummerieren!
CASES = {0: "Kiefernsee"}
CASE_ID = 0

SETUP_HTML = '''<div id="welcomeBack" class="msg ok" hidden></div>
<fieldset class="anrede"><legend>Wie soll euch die Web-App ansprechen?</legend>
<label><input type="radio" name="anrede" value="w"> Kommissarin</label>
<label><input type="radio" name="anrede" value="m"> Kommissar</label></fieldset>
<details id="dnBox"><summary>Schon einen Ermittlerausweis aus einem anderen Fall? Dienstnummer eingeben</summary>
<p class="small">Die Dienstnummer steht auf eurem Ausweis und hinten im Buch eures letzten Falls.</p>
<input id="dnIn" type="text" autocomplete="off" autocapitalize="characters" placeholder="DN-XXXX-XXXX" maxlength="14">
<div id="dnMsg" class="msg" hidden></div></details>'''

VIEW_HTML = '''<section id="v-ausweis" class="card alle" hidden>
<span class="lab"><span class="tag alle">PERSÖNLICH</span> Eure Laufbahn</span><h2>Mein Ermittlerausweis</h2>
<p>Mit jedem gelösten Fall der Reihe sammelt ihr Sterne und werdet befördert. Die Beförderungen gibt es am Ende des Falls – nach Akt 3.</p>
<div id="idCard"></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><button id="idSave" type="button">Ausweis als Bild speichern</button>
<button id="idCopy" type="button" class="ghost">Dienstnummer kopieren</button></div>
<div id="idMsg" class="msg" hidden></div>
<h3>So steigt ihr auf</h3>
<ul class="small" style="margin:0;padding-left:18px;line-height:1.7">
<li>Euer Verdacht stimmt schon nach Akt 1: 3 Sterne · nach Akt 2: 2 Sterne · nach Akt 3: 1 Stern</li>
<li>Fall gelöst: +1 Stern · Team hat am Ende noch mindestens 7 Punkte: +1 Stern</li>
<li>Jeder Fall zählt einmal. Neues Handy? Einfach die Dienstnummer eingeben.</li></ul>
<div id="rankList" class="small"></div>
</section>'''

CSS = r"""
.anrede{border:0;padding:0;margin:0;display:flex;gap:18px;flex-wrap:wrap;align-items:center}
.anrede legend{font-weight:600;margin-bottom:6px;font-size:14px}
.anrede label{display:flex;gap:6px;align-items:center;font-size:15px}
details#dnBox summary{cursor:pointer;font-size:14px;color:var(--ink-soft, #445)}
details#dnBox{display:flex;flex-direction:column;gap:8px}
.idc{background:#fbf7ec;color:#2c2c2a;border:1px solid #c9b98f;border-radius:12px;overflow:hidden;max-width:420px}
.idc .h{background:#15233a;color:#f3ead2;padding:9px 14px;font-size:12px;letter-spacing:.12em;font-weight:600;display:flex;justify-content:space-between}
.idc .b{padding:14px;display:grid;grid-template-columns:64px 1fr;gap:12px;font-size:13px;line-height:1.45}
.idc .ph{width:64px;height:80px;border-radius:6px;background:#e8dfc6;border:1px solid #c9b98f;display:flex;align-items:center;justify-content:center;font-size:30px}
.idc .k{font-size:11px;color:#6b6248}
.idc .n{font-size:18px;font-weight:700}
.idc .r{font-weight:700;color:#a83228}
.idc .f{padding:0 14px 10px;font-size:12px;line-height:1.6}
.idc .f div{display:flex;justify-content:space-between;gap:8px}
.idc .sig{font-style:italic;font-family:Georgia,serif;color:#15233a;font-size:14px}
.idc .ft{background:#e8dfc6;color:#6b6248;font-size:11px;text-align:center;padding:5px}
.rankchip{text-align:left;font-size:14px;padding:8px 12px;background:#fbf7ec;color:#7a2a22;border:1px solid #c9b98f;border-radius:4px;cursor:pointer;font-weight:600}
.rankrow{display:flex;justify-content:space-between;padding:5px 8px;border-bottom:1px solid #d8d2c4}
.rankrow.me{background:#f6e3df;color:#a83228;font-weight:700}
"""


def js(portal):
    return r'''<script>
(function(){
  var SFX=((location.search.match(/[?&]slot=(\w+)/)||[])[1]||""); SFX=SFX?"-"+SFX:"";
  var PKEY="ermittler-profil"+SFX, NKEY="kiefernsee-name"+SFX;
  var CASES=''' + json.dumps({str(k): v for k, v in CASES.items()}, ensure_ascii=False) + r''', CASE_ID=''' + str(CASE_ID) + r''';
  var $=function(id){return document.getElementById(id)};
  var RANKS=[[0,"Kommissaranwärter","Kommissaranwärterin"],[3,"Kriminalkommissar","Kriminalkommissarin"],
    [6,"Kriminaloberkommissar","Kriminaloberkommissarin"],[10,"Kriminalhauptkommissar","Kriminalhauptkommissarin"],
    [15,"Erster Kriminalhauptkommissar","Erste Kriminalhauptkommissarin"],[21,"Kriminalrat","Kriminalrätin"]];
  function load(){try{var p=JSON.parse(localStorage.getItem(PKEY)||"null");if(p&&p.v===1)return p}catch(e){}return null}
  function save(p){try{localStorage.setItem(PKEY,JSON.stringify(p))}catch(e){}}
  function rankIdx(st){var i=0;for(var k=0;k<RANKS.length;k++)if(st>=RANKS[k][0])i=k;return i}
  function title(i,form){var r=RANKS[i];return form==="w"?r[2]:form==="m"?r[1]:r[1]+"/in"}
  function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}

  // ---------- Dienstnummer: 40 Bit, 8 Zeichen ----------
  var AB="ABCDEFGHJKLMNPQRSTUVWXYZ23456789", M40=(1n<<40n)-1n, MUL=0x9e3779b97n, INV=0xe54e4c9427n, XK=0x5A3C96E1B7n;
  function chk(x){var h=2166136261>>>0;for(var i=0;i<4;i++){h^=Number((x>>BigInt(i*7))&127n);h=Math.imul(h,16777619)>>>0}return BigInt((h^(h>>>14))&0x3FFF)}
  function enc(p){var f=p.form==="w"?1n:p.form==="m"?2n:0n;
    var x=(1n<<24n)|(f<<22n)|(BigInt(Math.min(p.stars,63))<<16n)|BigInt(p.cases&0xFFFF);
    var v=(x<<14n)|chk(x); v=((v*MUL)&M40)^XK; var o="";for(var i=0;i<8;i++){o=AB[Number(v&31n)]+o;v>>=5n}
    return "DN-"+o.slice(0,4)+"-"+o.slice(4)}
  function dec(s){s=(s||"").toUpperCase().replace(/^DN/,"").replace(/[^A-Z0-9]/g,"").replace(/O/g,"0").replace(/I/g,"1");
    if(s.length!==8)return null;var v=0n;for(var i=0;i<8;i++){var k=AB.indexOf(s[i]);if(k<0)return null;v=v*32n+BigInt(k)}
    v=((v^XK)*INV)&M40;var x=v>>14n;if(chk(x)!==(v&0x3FFFn))return null;if((x>>24n)!==1n)return null;
    var f=Number((x>>22n)&3n);return {form:f===1?"w":f===2?"m":"",stars:Number((x>>16n)&63n),cases:Number(x&0xFFFFn)}}
  window.__dn={enc:enc,dec:dec};

  // ---------- Einrichtung ----------
  function fill(){
    var p=load(); if(!p) return;
    if(p.name&&!$("pname").value) $("pname").value=p.name;
    document.querySelectorAll('input[name=anrede]').forEach(function(r){r.checked=(r.value===p.form)});
    var w=$("welcomeBack"); w.hidden=false; w.textContent="Willkommen zurück, "+title(rankIdx(p.stars),p.form)+(p.name?" "+p.name:"")+"! Euer Dienstgrad ist gespeichert.";
    $("dnBox").hidden=true;
  }
  function fromSetup(){
    var p=load()||{v:1,name:"",form:"",stars:0,cases:0};
    var dn=($("dnIn").value||"").trim(), m=$("dnMsg");
    if(dn){ var d=dec(dn); if(!d){ m.hidden=false; m.className="msg bad"; m.textContent="Diese Dienstnummer stimmt nicht. Bitte genau abschreiben – sie beginnt mit DN-."; $("dnBox").open=true; return false }
      p.stars=Math.max(p.stars,d.stars); p.cases=p.cases|d.cases; if(d.form) p.form=d.form; m.hidden=true; $("dnIn").value="" }
    var nm=($("pname").value||"").trim().slice(0,20); if(nm) p.name=nm;
    var a=document.querySelector('input[name=anrede]:checked'); if(a) p.form=a.value;
    save(p); try{ if(p.name) localStorage.setItem(NKEY,p.name) }catch(e){}
    return true
  }

  // ---------- Ausweis ----------
  function caseList(c){var o=[];for(var k in CASES){if(c&(1<<+k))o.push(CASES[k])}return o}
  function render(){
    var p=load()||{v:1,name:"",form:"",stars:0,cases:0}, i=rankIdx(p.stars), cs=caseList(p.cases);
    $("idCard").innerHTML='<div class="idc"><div class="h"><span>KRIPO SEEBRÜCK · ERMITTLERAUSWEIS</span><span>★</span></div>'+
      '<div class="b"><div class="ph" aria-hidden="true">🕵</div><div><div class="k">Name</div><div class="n">'+esc(p.name||"ohne Namen")+'</div>'+
      '<div class="k">Dienstgrad</div><div class="r">'+esc(title(i,p.form))+'</div><div>'+"★".repeat(Math.min(p.stars,10))+' <span class="k">'+p.stars+' Sterne</span></div></div></div>'+
      '<div class="f"><div><span class="k">Gelöste Fälle</span><span>'+esc(cs.length?cs.join(", "):"noch keiner")+'</span></div>'+
      '<div><span class="k">Dienstnummer</span><b style="font-family:monospace">'+enc(p)+'</b></div>'+
      '<div style="align-items:end"><span class="sig">J. Wendland, EKHK’in</span><span class="k">Spielausweis</span></div></div>'+
      '<div class="ft">Spielausweis · Ermittlungsfall-Reihe von Natthaphon Lind · kein amtliches Dokument</div></div>';
    var h="";for(var k=RANKS.length-1;k>=0;k--){h+='<div class="rankrow'+(k===i?" me":"")+'"><span>'+esc(title(k,p.form))+'</span><span>ab '+RANKS[k][0]+' Sternen</span></div>'}
    $("rankList").innerHTML=h;
    var s=$("rankLine"); if(s) s.textContent=title(i,p.form)+(p.name?" "+p.name:"")+" · "+p.stars+" Sterne · Mein Ausweis";
  }
  function toImage(){
    var p=load()||{v:1,name:"",form:"",stars:0,cases:0}, i=rankIdx(p.stars), cs=caseList(p.cases);
    var W=900,H=560,c=document.createElement("canvas");c.width=W;c.height=H;var x=c.getContext("2d");
    x.fillStyle="#fbf7ec";x.fillRect(0,0,W,H);x.strokeStyle="#c9b98f";x.lineWidth=4;x.strokeRect(2,2,W-4,H-4);
    x.fillStyle="#15233a";x.fillRect(0,0,W,70);x.fillStyle="#f3ead2";x.font="bold 26px sans-serif";x.fillText("KRIPO SEEBRÜCK · ERMITTLERAUSWEIS",30,45);
    x.fillStyle="#f2c14e";x.fillText("★",W-60,45);
    x.fillStyle="#e8dfc6";x.fillRect(30,100,140,175);x.strokeStyle="#c9b98f";x.lineWidth=2;x.strokeRect(30,100,140,175);
    x.font="80px sans-serif";x.fillText("🕵",55,215);
    function lab(t,y){x.fillStyle="#6b6248";x.font="20px sans-serif";x.fillText(t,200,y)}
    lab("Name",120);x.fillStyle="#2c2c2a";x.font="bold 40px sans-serif";x.fillText(p.name||"ohne Namen",200,162);
    lab("Dienstgrad",200);x.fillStyle="#a83228";x.font="bold 32px sans-serif";x.fillText(title(i,p.form),200,238);
    x.fillStyle="#b8860b";x.font="30px sans-serif";x.fillText("★".repeat(Math.min(p.stars,10))+"  ",200,282);
    x.fillStyle="#6b6248";x.font="20px sans-serif";x.fillText(p.stars+" Sterne",200+Math.min(p.stars,10)*30+(p.stars?10:0),280);
    x.strokeStyle="#c9b98f";x.setLineDash([8,6]);x.beginPath();x.moveTo(30,310);x.lineTo(W-30,310);x.stroke();x.setLineDash([]);
    function row(k,v,y,mono){x.fillStyle="#6b6248";x.font="22px sans-serif";x.fillText(k,30,y);x.fillStyle="#2c2c2a";x.font=(mono?"bold 26px monospace":"24px sans-serif");var w=x.measureText(v).width;x.fillText(v,W-30-w,y)}
    row("Gelöste Fälle",cs.length?cs.join(", "):"noch keiner",350);row("Dienstnummer",enc(p),395,true);
    x.fillStyle="#15233a";x.font="italic 28px Georgia, serif";x.fillText("J. Wendland, EKHK’in",30,455);
    x.fillStyle="#a83228";x.beginPath();x.arc(W-70,440,38,0,7);x.fill();x.fillStyle="#fbf7ec";x.font="bold 30px sans-serif";x.fillText("★",W-82,451);
    x.fillStyle="#e8dfc6";x.fillRect(0,H-60,W,60);x.fillStyle="#6b6248";x.font="20px sans-serif";
    var t="Spielausweis · Ermittlungsfall-Reihe von Natthaphon Lind · kein amtliches Dokument";x.fillText(t,(W-x.measureText(t).width)/2,H-24);
    return c;
  }
  $("idSave").addEventListener("click",function(){
    var c=toImage(), m=$("idMsg");
    c.toBlob(function(b){
      var f=null; try{ f=new File([b],"ermittlerausweis.png",{type:"image/png"}) }catch(e){}
      if(f&&navigator.canShare&&navigator.canShare({files:[f]})){ navigator.share({files:[f],title:"Mein Ermittlerausweis"}).catch(function(){}) ; return }
      var a=document.createElement("a"); a.href=URL.createObjectURL(b); a.download="ermittlerausweis.png"; document.body.appendChild(a); a.click(); a.remove();
      m.hidden=false; m.className="msg ok"; m.textContent="Der Ausweis wurde als Bild gespeichert.";
    },"image/png");
  });
  $("idCopy").addEventListener("click",function(){
    var p=load()||{v:1,name:"",form:"",stars:0,cases:0}, t=enc(p), m=$("idMsg"); m.hidden=false;
    if(navigator.clipboard){ navigator.clipboard.writeText(t).then(function(){ m.className="msg ok"; m.textContent="Kopiert: "+t }).catch(function(){ m.className="msg"; m.textContent="Eure Dienstnummer: "+t }) }
    else { m.className="msg"; m.textContent="Eure Dienstnummer: "+t }
  });

  // ---------- Beförderung am Ende eines Falls (wird ab Akt 3 aufgerufen) ----------
  function award(stars){
    var p=load()||{v:1,name:"",form:"",stars:0,cases:0}, bit=1<<CASE_ID, before=rankIdx(p.stars);
    if(p.cases&bit) return {already:true,before:before,after:before,stars:0};
    p.stars=Math.min(63,p.stars+stars); p.cases|=bit; save(p); render();
    return {already:false,before:before,after:rankIdx(p.stars),stars:stars,title:title(rankIdx(p.stars),p.form),name:p.name};
  }
  window.__career={fromSetup:fromSetup,fill:fill,render:render,award:award,profile:load,title:function(){var p=load();return p?title(rankIdx(p.stars),p.form):title(0,"")}};
  fill(); render();
})();
</script>'''

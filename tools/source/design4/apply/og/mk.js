const {chromium}=require('playwright');const fs=require('fs');
const F='<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=IBM+Plex+Sans+KR:wght@600;700&family=Noto+Sans+Lao:wght@600;700&family=Noto+Sans+Thai:wght@600;700&family=Noto+Sans+Khmer:wght@600;700&display=swap" rel="stylesheet">';
const A=[
 {n:'kao',bg:'url(kao-bg.jpg) center/cover',ov:'linear-gradient(90deg,rgba(14,40,92,.95) 0,rgba(26,63,134,.85) 48%,rgba(26,63,134,.25) 100%)',ic:'kao-ic.png',name:'PhasaKAO',h1:'한국어 배우기',s1:'ຮຽນພາສາເກົາຫຼີຕາມຫົວຂໍ້ ງ່າຍໆ ທຸກມື້',s2:'라오스 학습자를 위한 한국어',ch:'kao-ch.webp',acc:'#F5C04A',pc:'#1A3F86'},
 {n:'lao',bg:'url(lao-bg.jpg) center/cover',ov:'linear-gradient(90deg,rgba(60,32,12,.95) 0,rgba(92,52,20,.82) 48%,rgba(92,52,20,.2) 100%)',ic:'lao-ic.png',name:'PhasaLAO',h1:'ຮຽນ ພາສາລາວ',s1:'라오스어, 주제별로 공부하기',s2:'라오어 문장 · 단어 · 원어민 음성',ch:'lao-ch.webp',acc:'#F2B541',pc:'#8A4B16',lo:1},
 {n:'hotel',bg:'url(hotel-bg.jpg) center/cover',ov:'linear-gradient(90deg,rgba(14,28,58,.95) 0,rgba(20,40,80,.82) 50%,rgba(20,40,80,.2) 100%)',ic:'hotel-ic.png',name:'HotelEng',h1:'호텔서비스 영어',s1:'Hotel Service English',s2:'호텔 현장에서 바로 쓰는 영어, 주제별로 쉽게',ch:'hotel-ch.png',acc:'#F0A040',pc:'#1E3A70'},
 {n:'thai',svg:'thai-hd.svg',ic:'thai-ic.png',name:'THAI Lang',h1:'เรียนภาษาไทย',s1:'태국어, 주제별로 공부하기',s2:'문장 · 단어 · 원어민 음성',acc:'#FFD37A',pc:'#7A1F3D',th:1},
 {n:'khmer',svg:'khmer-hd.svg',ic:'khmer-ic.png',name:'KHMER Lang',h1:'រៀនភាសាខ្មែរ',s1:'캄보디아어(크메르어) 첫걸음',s2:'문장 · 단어 · 원어민 음성',acc:'#FFD37A',pc:'#5B2A86',km:1},
 {n:'rwanda',svg:'rwanda-hd.svg',ic:'rwanda-ic.png',name:'RWANDA Lang',h1:'Kinyarwanda',s1:'르완다어, 주제별로 공부하기',s2:'문장 · 단어 · 원어민 음성',acc:'#FFE27A',pc:'#0B6E8A'},
 {n:'swahili',svg:'swahili-hd.svg',ic:'swahili-ic.png',name:'SWAHILI Lang',h1:'Kiswahili',s1:'스와힐리어, 주제별로 공부하기',s2:'문장 · 단어 · 원어민 음성',acc:'#FFE27A',pc:'#1E6B3A'}];
(async()=>{const b=await chromium.launch();
for(const a of A){
 const back=a.svg?`<div class="bg" style="background:url(${a.svg}) right center/auto 630px no-repeat"></div><div class="ov" style="background:linear-gradient(90deg,rgba(0,0,0,.55) 0,rgba(0,0,0,.35) 45%,rgba(0,0,0,0) 75%)"></div>`:`<div class="bg" style="background:${a.bg}"></div><div class="ov" style="background:${a.ov}"></div>`;
 const hf=a.lo?'"Noto Sans Lao"':a.th?'"Noto Sans Thai"':a.km?'"Noto Sans Khmer"':'"IBM Plex Sans KR"';
 const html=`<!doctype html><meta charset="utf-8">${F}<style>html,body{margin:0}.c{width:1200px;height:630px;position:relative;overflow:hidden;font-family:"IBM Plex Sans KR","Noto Sans Lao",sans-serif;color:#fff;background:#222}
 .bg,.ov{position:absolute;inset:0}.c:after{content:"";position:absolute;left:0;right:0;bottom:0;height:14px;background:${a.acc}}
 .t{position:absolute;left:72px;top:${a.svg?120:96}px;width:${a.ch?640:900}px;text-shadow:0 2px 12px rgba(0,0,0,.25)}
 .pill{display:inline-flex;align-items:center;gap:14px;background:#fff;color:${a.pc};border-radius:999px;padding:10px 28px 10px 12px;font:700 42px "Space Grotesk",sans-serif;text-shadow:none}
 .pill img{width:56px;height:56px;border-radius:14px}
 h1{font-family:${hf},"IBM Plex Sans KR";font-size:${a.lo||a.th||a.km?88:84}px;line-height:1.2;margin:34px 0 16px;font-weight:700}
 .s1{font-family:"IBM Plex Sans KR","Noto Sans Lao";font-size:34px;font-weight:600;opacity:.95}.s2{font-size:30px;color:${a.acc};margin-top:18px;font-weight:600}
 .ch{position:absolute;right:${a.n=='hotel'?40:70}px;bottom:40px;height:${a.n=='hotel'?380:430}px;filter:drop-shadow(0 8px 24px rgba(0,0,0,.35))}</style>
 <div class="c">${back}<div class="t"><span class="pill"><img src="${a.ic}">${a.name}</span><h1>${a.h1}</h1><div class="s1">${a.s1}</div><div class="s2">${a.s2}</div></div>${a.ch?`<img class="ch" src="${a.ch}">`:''}</div>`;
 fs.writeFileSync(a.n+'.html',html);const p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/'+a.n+'.html');await p.waitForTimeout(2500);await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:'og-'+a.n+'.png'});await p.close()}
await b.close()})();

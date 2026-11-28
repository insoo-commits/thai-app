
// v3.30 RYU: 아래로 읽을 때 대분류 메뉴를 화면 맨 위에 고정 (호텔서비스 영어 v1.51과 같은 방식)
(function(){
  const st=document.getElementById("stick"),mb=document.querySelector(".menubox"),sg=document.getElementById("stickG"),g=document.getElementById("groups");
  if(!st||!mb||!sg||!g||!("IntersectionObserver" in window))return;
  const title=()=>{const o=document.querySelector("#bsel option:checked");return o?(o.dataset.ko||o.textContent||"").trim():""};
  const sync=()=>{sg.innerHTML=g.innerHTML;sg.querySelectorAll(".glide").forEach(x=>x.remove());sg.querySelectorAll("[data-part]").forEach(b=>b.removeAttribute("data-part"));document.getElementById("stickT").textContent=title();const on=sg.querySelector('[aria-pressed="true"]');if(on&&!st.hidden)on.scrollIntoView({block:"nearest",inline:"center"})};
  new IntersectionObserver(es=>{const e=es[0];const show=!e.isIntersecting&&e.boundingClientRect.bottom<0;if(show===!st.hidden)return;st.hidden=!show;if(show)sync()}).observe(mb);
  new MutationObserver(()=>{if(!st.hidden)sync()}).observe(g,{childList:true,subtree:true,attributes:true});
  const band=document.getElementById("band");if(band)new MutationObserver(()=>{if(!st.hidden)sync()}).observe(band,{childList:true,subtree:true});
  sg.addEventListener("click",e=>{const t=e.target.closest(".group");if(!t)return;e.stopPropagation();const i=[...sg.querySelectorAll(".group")].indexOf(t);const o=g.querySelectorAll(".group")[i];if(o)o.click();document.querySelector(".search").scrollIntoView({block:"start"})});
  document.getElementById("stickQ").addEventListener("click",e=>{e.stopPropagation();window.scrollTo(0,0);document.getElementById("q").focus()});
})();

// v3.31 RYU: PC - 대분류 위에 마우스를 올리면 연한 바탕과 밑줄이 따라 움직임 (호텔서비스 영어 v1.55)
(function(){
  if(!matchMedia("(hover:hover) and (pointer:fine)").matches)return;
  for(const id of ["groups","stickG"]){const nav=document.getElementById(id);if(!nav)continue;
    const gl=()=>{let e=nav.querySelector(".glide");if(!e){e=document.createElement("span");e.className="glide";e.setAttribute("aria-hidden","true");nav.appendChild(e)}return e};
    const at=(e,t)=>{e.style.left=t.offsetLeft+"px";e.style.width=t.offsetWidth+"px";e.style.top=t.offsetTop+"px";e.style.height=t.offsetHeight+"px"};
    nav.addEventListener("mouseover",ev=>{const t=ev.target.closest(".group");if(!t||!nav.contains(t))return;const e=gl();if(e.style.opacity!=="1"){e.style.transition="none";at(e,t);e.offsetWidth;e.style.transition=""}at(e,t);e.style.opacity="1"});
    nav.addEventListener("mouseleave",()=>{const e=nav.querySelector(".glide");if(e)e.style.opacity="0"});
  }
})();
// v3.31 RYU: PC - 한 줄에 다 안 들어가는 메뉴 줄 끝에 둥근 화살표 버튼, 마우스 휠로도 옆으로 이동 (호텔서비스 영어 v1.57)
(function(){
  if(!matchMedia("(hover:hover) and (pointer:fine)").matches)return;
  const chev=d=>{const b=document.createElement("button");b.className="hsb "+(d<0?"l":"r");b.type="button";b.setAttribute("aria-label",d<0?"왼쪽 메뉴 보기":"오른쪽 메뉴 보기");b.hidden=true;
    b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="'+(d<0?"m15 5-7 7 7 7":"m9 5 7 7-7 7")+'"/></svg>';return b};
  for(const id of ["groups","subs","stickG"]){const nav=document.getElementById(id);if(!nav)continue;
    const w=document.createElement("div");w.className="hs";nav.parentNode.insertBefore(w,nav);w.appendChild(nav);
    const l=chev(-1),r=chev(1);w.append(l,r);
    const upd=()=>{const m=nav.scrollWidth-nav.clientWidth,x=nav.scrollLeft;l.hidden=!(m>2&&x>2);r.hidden=!(m>2&&x<m-2);w.classList.toggle("ml",!l.hidden);w.classList.toggle("mr",!r.hidden)};
    const mv=d=>nav.scrollBy({left:d*Math.max(120,nav.clientWidth*.6),behavior:"smooth"});
    l.addEventListener("click",e=>{e.stopPropagation();mv(-1)});r.addEventListener("click",e=>{e.stopPropagation();mv(1)});
    nav.addEventListener("scroll",upd,{passive:true});
    nav.addEventListener("wheel",e=>{if(nav.scrollWidth-nav.clientWidth<3||Math.abs(e.deltaY)<=Math.abs(e.deltaX))return;e.preventDefault();nav.scrollLeft+=e.deltaY},{passive:false});
    addEventListener("resize",upd);
    new MutationObserver(()=>requestAnimationFrame(upd)).observe(nav,{childList:true,subtree:true,attributes:true,attributeFilter:["aria-pressed","aria-selected"]});
    if("ResizeObserver" in window)new ResizeObserver(upd).observe(nav);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(upd);
    upd();
  }
})();

// 당겨서 새로고침 (RYU 2026-11-27): 폰·패드에서 화면 맨 위에서 아래로 당겼다 놓으면 새로고침. 설치한 앱(홈 화면)에도 동작.
(function(){
  if(window.__ptr)return;window.__ptr=1;
  if(!("ontouchstart" in window)&&!(navigator.maxTouchPoints>0))return;
  var TH=70,MAX=110,de=document.documentElement;
  var css=document.createElement("style");
  css.textContent="html,body{overscroll-behavior-y:contain}"+
   "#ptr{position:fixed;left:50%;top:0;z-index:2147483000;width:40px;height:40px;margin-left:-20px;border-radius:50%;"+
   "background:rgba(40,44,52,.88);color:#fff;display:flex;align-items:center;justify-content:center;"+
   "box-shadow:0 2px 10px rgba(0,0,0,.25);transform:translateY(-52px);opacity:0;pointer-events:none}"+
   "#ptr svg{width:22px;height:22px;transition:transform .15s}#ptr.go{background:rgba(26,115,232,.95)}"+
   "#ptr.spin svg{animation:ptrs .8s linear infinite}@keyframes ptrs{to{transform:rotate(360deg)}}";
  (document.head||de).appendChild(css);
  var el=null;
  function mk(){if(el)return el;el=document.createElement("div");el.id="ptr";el.setAttribute("aria-hidden","true");
   el.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 1 1-2.34-5.66"/><path d="M20 4v5h-5"/></svg>';
   document.body.appendChild(el);return el}
  function top0(){return (window.scrollY||de.scrollTop||0)<=0}
  function blocked(t){
    if(!t||!t.closest)return false;
    if(t.closest("input,select,textarea,[contenteditable=''],[contenteditable=true],#player,.player,[role=slider]"))return true;
    for(var n=t;n&&n!==document.body&&n!==de;n=n.parentElement){
      if(n.scrollTop>0){var oy=getComputedStyle(n).overflowY;if(oy==="auto"||oy==="scroll")return true}
    }
    return false}
  var sx=0,sy=0,on=false,pull=false,d=0,busy=false;
  function show(){var e=mk(),y=Math.min(d,MAX);e.style.transition="none";e.style.opacity=Math.min(1,y/40);
    e.style.transform="translateY("+(y-46)+"px)";e.querySelector("svg").style.transform="rotate("+(y/TH*270)+"deg)";
    e.classList.toggle("go",y>=TH)}
  function hide(){if(!el)return;el.style.transition="transform .2s,opacity .2s";el.style.transform="translateY(-52px)";el.style.opacity="0";el.classList.remove("go")}
  function refresh(){busy=true;var e=mk();e.classList.add("spin");e.style.transition="transform .2s";e.style.transform="translateY("+(TH-46)+"px)";
    var go=function(){location.reload()};
    try{var sw=navigator.serviceWorker;if(sw&&sw.getRegistration){
      Promise.race([sw.getRegistration().then(function(r){return r&&r.update()}),new Promise(function(r){setTimeout(r,1500)})]).then(go,go);return}}catch(_){}
    setTimeout(go,150)}
  document.addEventListener("touchstart",function(e){on=pull=false;d=0;
    if(busy||e.touches.length!==1||!top0()||blocked(e.target))return;
    try{var s=getSelection();if(s&&String(s).length)return}catch(_){}
    sx=e.touches[0].clientX;sy=e.touches[0].clientY;on=true},{passive:true});
  document.addEventListener("touchmove",function(e){if(!on)return;
    if(e.touches.length!==1){on=false;if(pull){pull=false;hide()}return}
    var dx=e.touches[0].clientX-sx,dy=e.touches[0].clientY-sy;
    if(!pull){if(dy<=0||!top0()){on=false;return}
      if(dy<12)return;
      if(Math.abs(dx)>dy*0.7){on=false;return}
      pull=true;sy=e.touches[0].clientY}
    dy=e.touches[0].clientY-sy;
    if(dy<=0){d=0;show();return}
    if(e.cancelable)e.preventDefault();
    d=dy*0.5;show()},{passive:false});
  function end(){if(!on)return;on=false;if(!pull)return;pull=false;if(d>=TH)refresh();else hide();d=0}
  document.addEventListener("touchend",end,{passive:true});
  document.addEventListener("touchcancel",function(){on=false;if(pull){pull=false;hide()}d=0},{passive:true});
})();

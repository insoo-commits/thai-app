/* v1.20 RYU: phone swipe left/right = next/previous bundle. Decided during touchmove (no wait for touchend): 60px, within 1s, sideways > 1.5x vertical; >40px vertical = scroll, ignore; one bundle per swipe; change at once, new bundle slides in. Tables count only when they scroll sideways. (Lao v3.23, Korean app v2.51) */
(function(){let sx=0,sy=0,st=0,ok=false;
 const hscroll=el=>{for(;el&&el!==document.body;el=el.parentElement){if(el.scrollWidth>el.clientWidth+4){const o=getComputedStyle(el).overflowX;if(o==="auto"||o==="scroll")return true}}return false};
 document.addEventListener("touchstart",e=>{ok=false;if(e.touches.length!==1)return;const t=e.touches[0],w=innerWidth;if(t.clientX<24||t.clientX>w-24)return;/* leave screen edges to the browser back/forward gesture */
  const el=e.target;if(el.closest&&el.closest("input,select,textarea,#player,.gal,.bsel,#groups,#subs,.subs,.tabs"))return;if(hscroll(el))return;sx=t.clientX;sy=t.clientY;st=Date.now();ok=true},{passive:true});
 const go=dx=>{const b=document.querySelector(dx<0?".nextbun:not(.prevbun)":".nextbun.prevbun");if(!b)return;b.click();
  const s2=document.getElementById("sheet");if(s2){s2.style.transition="none";s2.style.transform="translateX("+(dx<0?36:-36)+"px)";s2.style.opacity=".4";requestAnimationFrame(()=>requestAnimationFrame(()=>{s2.style.transition="transform .16s ease-out,opacity .16s";s2.style.transform="";s2.style.opacity=""}))}};
 document.addEventListener("touchmove",e=>{if(!ok)return;const t=e.touches[0],dx=t.clientX-sx,dy=t.clientY-sy;
  if(Math.abs(dy)>40||Date.now()-st>1000){ok=false;return}
  if(Math.abs(dx)>=60&&Math.abs(dx)>Math.abs(dy)*1.5){ok=false;try{const s=getSelection();if(s&&String(s).length)return}catch(_){}go(dx)}},{passive:true});
 document.addEventListener("touchend",()=>{ok=false},{passive:true});
 document.addEventListener("touchcancel",()=>{ok=false},{passive:true})})();

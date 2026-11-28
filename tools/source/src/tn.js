/* Thai tone marks (5 tones): syllables and tones come from the build (tltk g2p), per known word; text is split into known words */
const TN=(()=>{const W=__TNW__;let MX=0;for(const k in W)if(k.length>MX)MX=k.length;
const seg=(t)=>{const n=t.length,best=new Array(n+1).fill(null);best[n]={c:0,k:0,p:[]};
  for(let i=n-1;i>=0;i--){let b={c:best[i+1].c,k:best[i+1].k,p:best[i+1].p};
    for(let L=Math.min(MX,n-i);L>=1;L--){const w=t.substr(i,L),d=W[w];if(!d)continue;const nx=best[i+L],c=nx.c+L,k=nx.k+d.length;
      if(c>b.c||c===b.c&&k<b.k)b={c:c,k:k,p:d.map(([a,m,ci,cl,tn])=>({i:i+a,n:m,ci:ci,ini:w.substr(a+ci,cl),tn:"t"+tn})).concat(nx.p)}}
    best[i]=b}
  return best[0].p};
const tone=y=>y.tn;
const MK={t1:'M2 6H14',t2:'M2 8.5Q8 9.5 14 10.5',t3:'M2 4Q6 0.5 14 10.5',t4:'M2 3.5Q9 3.5 14 1',t5:'M2 6.5Q7 11.5 14 1.5'};
return {seg:seg,tone:tone,MK:MK}})();

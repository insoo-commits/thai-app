/* Thai: words with several meanings show the one that fits the sentence (rules on the Korean translation; first match wins) */
const NUMW=/(หนึ่ง|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า|สิบ|ยี่สิบ|ร้อย|พัน|หมื่น|แสน|ล้าน|กี่|[0-9])\s*$/;
const NOW=a=>/^\s*$/.test(a);
const NSENSE={};
const nmean0=(t,lo)=>NDICT[t];
const nmean=(t,lo,ko)=>{const r=NSENSE[t];if(r&&ko!==undefined){const i=lo.indexOf(t),b=i<0?"":lo.slice(0,i),a=i<0?"":lo.slice(i+t.length);for(const [f,m] of r){if(typeof f==="function"?f(ko,b,a,lo):f.test(ko))return m}}return nmean0(t,lo)};

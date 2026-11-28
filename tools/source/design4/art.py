import math
def head(body): return '<svg class="hart" viewBox="0 0 340 124" preserveAspectRatio="xMaxYMax meet" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 122h340"/>'+body+'</svg>'
def prang(x,b,h,w):
    s=f'<path d="M{x-w} {b}C{x-w*.9} {b-h*.5} {x-w*.35} {b-h*.82} {x} {b-h}C{x+w*.35} {b-h*.82} {x+w*.9} {b-h*.5} {x+w} {b}"/>'
    for k in (0.25,0.45,0.62,0.76): yy=b-h*k; ww=w*(1-k*.95); s+=f'<path d="M{x-ww:.1f} {yy:.1f}h{2*ww:.1f}" stroke-width=".8"/>'
    return s+f'<path d="M{x} {b-h}v-8"/>'
TH = head(
  # Wat Arun: base terraces + central prang + two side prangs
  '<path d="M96 122v-10h112v10M106 112v-9h92v9M116 103v-8h72v8"/>'+prang(152,95,78,20)+prang(104,103,40,10)+prang(200,103,40,10)
  # sala roof with chofa
  +'<path d="M232 122V96h40v26M228 96l24-22 24 22M236 86l16-16 16 16M226 96q-4-2-4-8M278 96q4-2 4-8M252 70v-8M248 64h8"/><path d="M240 104h24M244 104v18M260 104v18" stroke-width=".9"/>'
  # long-tail boat + water
  +'<path d="M286 110h44l-6 6h-34zM296 110v-6M330 110l8-8" /><path d="M280 120q6-3 12 0t12 0t12 0t12 0t12 0" stroke-width=".9"/>'
  # palm left
  +'<path d="M42 122c2-20 4-36 1-54M43 68c-9-6-19-5-26 2M43 68c-6-9-16-12-24-10M43 68c5-9 14-12 22-8M43 68c9-4 19 0 25 8M43 68c1-8 5-14 10-17"/>')
rays=''.join(f'<path d="M{276+16*math.cos(math.radians(a)):.1f} {34+16*math.sin(math.radians(a)):.1f}L{276+24*math.cos(math.radians(a)):.1f} {34+24*math.sin(math.radians(a)):.1f}" stroke-width=".9"/>' for a in range(0,360,15))
RW = head(
  '<circle cx="276" cy="34" r="10"/>'+rays
  # rolling hills
  +'<path d="M0 104q40-30 90-12t90-8 80 4 80-14" stroke-width="1.1"/><path d="M60 122q50-34 110-18t100 0 70-10"/>'
  # tea terraces
  +''.join(f'<path d="M{150+i*16} {114-i*4}q14-4 28 0" stroke-width=".8"/>' for i in range(5))
  # King's palace beehive hut
  +'<path d="M30 122c0-26 14-46 34-50 20 4 34 24 34 50M64 72v-12M58 62q6-6 12 0M52 122v-14a12 12 0 0 1 24 0v14"/><path d="M40 98q24-8 48 0M36 110q28-8 56 0" stroke-width=".8"/>'
  # banana plant
  +'<path d="M248 122v-30M248 92c-14-4-22 2-26 10M248 92c-4-14 2-22 12-26M248 92c12-6 22-2 26 6M248 92c-12-12-22-12-30-6"/>'
  # drum (ingoma)
  +'<path d="M296 122l-4-18h24l-4 18zM292 104q12-4 24 0"/>')
KM = head(
  # Angkor Wat 5 towers
  '<path d="M70 122v-12h150v12M84 110v-10h122v10"/>'
  +''.join(f'<path d="M{x-w} 100C{x-w} {100-h*.55} {x-w*.4} {100-h*.86} {x} {100-h}C{x+w*.4} {100-h*.86} {x+w} {100-h*.55} {x+w} 100"/><path d="M{x-w*.8} {100-h*.3}h{w*1.6}M{x-w*.6} {100-h*.55}h{w*1.2}" stroke-width=".8"/>' for x,h,w in ((100,44,9),(122,56,11),(145,80,14),(168,56,11),(190,44,9)))
  +'<path d="M140 110v-6h10v6" stroke-width=".9"/>'
  # reflecting pond lines + lotus
  +'<path d="M228 116q10-3 20 0t20 0t20 0" stroke-width=".9"/><path d="M256 112c-4-6-4-12 0-16 4 4 4 10 0 16zM256 112c-8-2-12-8-12-12 6 0 10 6 12 12zM256 112c8-2 12-8 12-12-6 0-10 6-12 12z"/><path d="M256 112v10"/>'
  # sugar palms
  +''.join(f'<path d="M{x} 122c1-22 2-40 0-{h}"/>'+''.join(f'<path d="M{x} {122-h-18}l{dx} {dy}"/>' for dx,dy in ((-14,6),(14,6),(-12,-6),(12,-6),(0,-12),(-8,10),(8,10))) for x,h in ((36,40),(300,46),(318,32)))
  )
SW = head(
  # Kilimanjaro
  '<path d="M60 122L130 64q20-12 40 0l80 58"/><path d="M118 74l8 4 8-6 10 6 10-6 8 6 10-4" stroke-width=".9"/>'
  # acacia
  +'<path d="M226 122l-2-26-8-12M224 96l10-14M196 82q34-14 66 0q-32 6-66 0z"/>'
  # giraffe
  +'<path d="M272 122v-22M286 122v-22M270 100h20l1-2M288 100l4-34 8-4M292 66l2-6M298 62l2-6M270 100q-4 6-2 14"/><path d="M276 92h4M284 90h3M290 80h2" stroke-width=".8"/>'
  # dhow on sea
  +'<path d="M20 112h40l-6 8H26zM40 112V74l22 34M40 78l-18 28h18"/><path d="M8 120q6-3 12 0t12 0t12 0t12 0t12 0" stroke-width=".9"/>'
  # sun
  +'<circle cx="310" cy="30" r="10"/>')
ART={'th':TH,'rw':RW,'km':KM,'sw':SW}

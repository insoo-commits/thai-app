import sys, json, re
sys.path.insert(0,'/mnt/project-files/lao-app/src/v3')
import pics
from pics import svg, r, c, ln, W, H, INK
import subpics as S
FF = "font-family=\"'Noto Sans Thai','Noto Sans Khmer','Noto Sans KR',sans-serif\""
def fix(s): return re.sub(r'font-family="[^"]*"', FF, s.replace("font-family=\"'Lao Local','Noto Sans Lao Looped','Noto Sans Lao',sans-serif\"", FF))
def skin(a,b): pics.SKIN, pics.SKIN2 = a, b
def wai(x, foot, shirt, pants, hair, female, s=1.0):
    sk = pics.SKIN
    o = pics.person(x, foot, shirt, pants, hair, female=female)
    sh = foot - 114
    o += ln([(x-15, sh+6), (x-13, sh+30), (x-3, sh+16)], shirt, 10) + ln([(x+15, sh+6), (x+13, sh+30), (x+3, sh+16)], shirt, 10)
    o += f'<ellipse cx="{x}" cy="{sh+8}" rx="5" ry="11" fill="{sk}"/>'
    return o
def hills(cols):
    return "".join(f'<path d="M0,{y} Q{a},{y-h} {b},{y} T{W},{y-10} V{H} H0 Z" fill="{col}"/>' for (y,a,b,h,col) in cols)
def prang(x, foot, s=1.0):
    o = r(x-46*s, foot-16*s, 92*s, 16*s, "#e9d3ae") + r(x-36*s, foot-30*s, 72*s, 14*s, "#f1dfbd")
    o += f'<path d="M{x-26*s},{foot-30*s} C{x-22*s},{foot-80*s} {x-8*s},{foot-118*s} {x},{foot-150*s} C{x+8*s},{foot-118*s} {x+22*s},{foot-80*s} {x+26*s},{foot-30*s} Z" fill="#f4e6c8" stroke="#c98b4a" stroke-width="2"/>'
    for k in range(1,5): yy=foot-30*s-k*24*s; ww=26*s*(1-k*.2); o += ln([(x-ww, yy), (x+ww, yy)], "#d9723a", 2.4)
    o += ln([(x, foot-150*s), (x, foot-166*s)], "#d49a2e", 2.5)
    for dx in (-62,62):
        o += f'<path d="M{x+dx*s-12*s},{foot-16*s} C{x+dx*s-9*s},{foot-50*s} {x+dx*s-3*s},{foot-66*s} {x+dx*s},{foot-80*s} C{x+dx*s+3*s},{foot-66*s} {x+dx*s+9*s},{foot-50*s} {x+dx*s+12*s},{foot-16*s} Z" fill="#f4e6c8" stroke="#c98b4a" stroke-width="1.6"/>'
    return o
def angkor(x, foot, s=1.0, col="#c9a46a", col2="#b08a52"):
    o = r(x-90*s, foot-22*s, 180*s, 22*s, col2) + r(x-70*s, foot-40*s, 140*s, 18*s, col)
    for dx,hh in ((-56,58),(-28,72),(0,96),(28,72),(56,58)):
        cx=x+dx*s; b=foot-40*s
        o += f'<path d="M{cx-12*s},{b} C{cx-12*s},{b-hh*.5*s} {cx-5*s},{b-hh*.85*s} {cx},{b-hh*s} C{cx+5*s},{b-hh*.85*s} {cx+12*s},{b-hh*.5*s} {cx+12*s},{b} Z" fill="{col}" stroke="{col2}" stroke-width="1.5"/>'
    return o
def sugarpalm(x, foot, h=120):
    top=foot-h; o=[ln([(x,foot),(x+3,top)], "#7a5a3a", 6)]
    for a in range(0,360,30):
        import math; dx=34*math.cos(math.radians(a)); dy=22*math.sin(math.radians(a))
        o.append(ln([(x+3,top),(x+3+dx,top+dy)], "#4f7f46", 5))
    return "".join(o)
def lotus(x,y,col="#e98aa6"):
    return "".join(f'<ellipse cx="{x+dx}" cy="{y}" rx="5" ry="11" fill="{col}" transform="rotate({dx*3} {x+dx} {y})"/>' for dx in (-7,0,7)) + f'<ellipse cx="{x}" cy="{y+9}" rx="14" ry="3" fill="#5f9a5a"/>'
def kili(x, foot, s=1.0):
    return (f'<path d="M{x-150*s},{foot} L{x-40*s},{foot-80*s} Q{x},{foot-92*s} {x+40*s},{foot-80*s} L{x+150*s},{foot} Z" fill="#7d95ad"/>'
            f'<path d="M{x-52*s},{foot-70*s} L{x-40*s},{foot-80*s} Q{x},{foot-92*s} {x+40*s},{foot-80*s} L{x+54*s},{foot-68*s} L{x+30*s},{foot-72*s} L{x+14*s},{foot-64*s} L{x-6*s},{foot-73*s} L{x-24*s},{foot-64*s} Z" fill="#ffffff"/>')
def acacia(x, foot, s=1.0):
    return ln([(x,foot),(x-4*s,foot-50*s),(x-16*s,foot-74*s)],"#6b4a2e",5*s)+ln([(x-4*s,foot-50*s),(x+14*s,foot-76*s)],"#6b4a2e",4*s)+f'<ellipse cx="{x}" cy="{foot-82*s}" rx="{58*s}" ry="{12*s}" fill="#5e8a3a"/>'
def banana(x, foot):
    o=[ln([(x,foot),(x,foot-70)],"#6f8f3a",8)]
    for dx,dy in ((-40,-96),(38,-100),(-30,-118),(24,-122),(0,-128)):
        o.append(f'<path d="M{x},{foot-66} Q{x+dx*.5},{foot+dy-6} {x+dx},{foot+dy+16}" stroke="#5fa04a" stroke-width="12" fill="none" stroke-linecap="round"/>')
    return "".join(o)
two = S.two_talk
OUT = {}
# Thai: wai greeting, Wat Arun
skin("#ecbd96","#d9a47c")
bg = S.sky("#f9d9b8","#fbeedd",200,"#c9b48a")
OUT["th"] = svg(bg + prang(330,200,.8) + S.palm(42,200,96) + wai(140,236,"#f1e3c6","#8e1f3b",S.HAIR,True) + wai(262,236,"#5b7fa6","#3b4a5a",S.HAIR2,False)
   + S.bubble(70,24,"สวัสดีค่ะ",112,18) + S.bubble(200,62,"สวัสดีครับ",120,18,tail="r"))
# Khmer: sampeah, Angkor
skin("#e2ad84","#cf9a70")
bg = S.sky("#f3c9d4","#f8e6dc",206,"#8fb7a8")
OUT["km"] = svg(bg + angkor(312,206,.7) + sugarpalm(36,206,110) + lotus(200,224) + lotus(372,230,"#f2a7bb") + wai(138,240,"#f6c453","#5b3a8c",S.HAIR,True) + wai(264,240,"#ffffff","#3b4a5a",S.HAIR2,False)
   + S.bubble(56,22,"ជំរាបសួរ",112,18) + S.bubble(206,58,"សួស្តី បាទ",116,18,tail="r"))
# Rwanda: hills, handshake
skin("#8a5a3c","#774b30")
bg = S.sky("#bfe6f6","#eaf6ee",190,"#7fb35a") + hills([(200,90,200,60,"#9cc76a"),(214,260,400,50,"#6fa44d")]) + "".join(ln([(250+i*10,186-i*2),(390,186-i*2-6)],"#5d8f3e",2) for i in range(4))
OUT["rw"] = svg(bg + banana(46,214) + c(330,52,20,"#fad201") + S.W_(5,True,140,240,arms=[[(0,0),(18,22),(42,24)]]) + S.W_(1,False,262,240,arms=[[(0,0),(-18,22),(-40,24)]])
   + S.bubble(40,24,"Muraho!",96,18) + S.bubble(196,60,"Amakuru?",108,18,tail="r"))
# Swahili: Kilimanjaro, acacia
bg = S.sky("#ffd9a0","#fbeccf",196,"#d8b46a")
OUT["sw"] = svg(bg + kili(250,196,.9) + acacia(352,200,.9) + S.W_(4,True,140,238,arms=[[(0,0),(18,22),(42,24)]]) + S.W_(6,False,262,238,arms=[[(0,0),(-18,22),(-40,24)]])
   + S.bubble(40,22,"Habari?",96,18) + S.bubble(206,58,"Nzuri!",88,18,tail="r"))
OUT = {k: fix(v) for k,v in OUT.items()}
json.dump(OUT, open('pics.json','w'), ensure_ascii=False)
print({k:len(v) for k,v in OUT.items()})

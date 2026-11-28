# Sub-category pictures for the Thai, Rwanda, Khmer and Swahili apps (RYU 2026-11-24: "라오앱을 참고해서 그대로 적용").
# Same flat style as the Lao app (lao-app/src/v3/subpics.py); scenes take the target language's text.
import sys, json, math, re
sys.path.insert(0, '/mnt/project-files/lao-app/src/v3')
import pics, subpics as S
from pics import svg as _svg, r, c, ln, W, H, INK
from subpics import sky, room, cloud, sun, table, bowl, desk, board, card, waves, tone_curve
LF = "font-family=\"'Lao Local','Noto Sans Lao Looped','Noto Sans Lao',sans-serif\""
FF = "font-family=\"'Thai Local','Khmer Local','Noto Sans Thai','Noto Sans Khmer','Pretendard','Noto Sans KR',sans-serif\""
TEAK = "#8a4a16"; GOLD = "#d49a2e"
L = {}  # current locale
def svg(body, bg="#eef3f6"): return _svg(body, bg).replace(LF, FF)
def t(x, y, s, size=16, fill=INK, w="700"): return S.t(x, y, s, size, fill, lao=True, w=w)
def tk(x, y, s, size=16, fill=INK, w="600"): return S.t(x, y, s, size, fill, lao=False, w=w)
COMB = re.compile('[ัิ-ฺ็-๎ិ-ួំ-៓៝]')
def tw(s, size): n = len(COMB.sub('', s)); n -= s.count('្'); return n * size * (0.56 if L.get('latin') else 0.62)
def fit(s, size, maxw): return min(size, size * maxw / max(1, tw(s, size)))
def bub(x, y, s, size=16, tail="l", maxw=150):
    size = fit(s, size, maxw); w = max(44, tw(s, size) + 6)
    if tail == "r": x = min(x, W - w - 24)
    return S.bubble(x, y, s, w, size, tail=tail)
def P(i, female=None, x=0, foot=0, **k):
    shirt = S.SHIRT[(i if female else i + 2) % len(S.SHIRT)]
    if female: return pics.person(x, foot, shirt, S.SINH[i % len(S.SINH)], S.HAIR, female=True, **k)
    return pics.person(x, foot, shirt, "#3b4a5a", S.HAIR2 if i % 2 else S.HAIR, **k)
def two(a, b, bg, ia=0, ib=1, fa=True, fb=False, extra="", size=17):
    return (bg + extra + P(ia, fa, 130, 236, arms=[[(0, 0), (16, 20), (30, 28)]]) + P(ib, fb, 270, 236, arms=[[(0, 0), (-16, 20), (-30, 28)]])
            + bub(30, 34, a, size, maxw=170) + bub(220, 74, b, size, "r", maxw=170))
# ---------- landmarks per country
def prang(x, foot, s=1.0):
    o = r(x-46*s, foot-16*s, 92*s, 16*s, "#e9d3ae") + r(x-36*s, foot-30*s, 72*s, 14*s, "#f1dfbd")
    o += f'<path d="M{x-26*s},{foot-30*s} C{x-22*s},{foot-80*s} {x-8*s},{foot-118*s} {x},{foot-150*s} C{x+8*s},{foot-118*s} {x+22*s},{foot-80*s} {x+26*s},{foot-30*s} Z" fill="#f4e6c8" stroke="#c98b4a" stroke-width="2"/>'
    for k in range(1, 5): yy = foot-30*s-k*24*s; ww = 26*s*(1-k*.2); o += ln([(x-ww, yy), (x+ww, yy)], "#d9723a", 2.4)
    for dx in (-62, 62):
        o += f'<path d="M{x+dx*s-12*s},{foot-16*s} C{x+dx*s-9*s},{foot-50*s} {x+dx*s-3*s},{foot-66*s} {x+dx*s},{foot-80*s} C{x+dx*s+3*s},{foot-66*s} {x+dx*s+9*s},{foot-50*s} {x+dx*s+12*s},{foot-16*s} Z" fill="#f4e6c8" stroke="#c98b4a" stroke-width="1.6"/>'
    return o + ln([(x, foot-150*s), (x, foot-166*s)], GOLD, 2.5)
def angkor(x, foot, s=1.0, col="#c9a46a", col2="#b08a52"):
    o = r(x-90*s, foot-22*s, 180*s, 22*s, col2) + r(x-70*s, foot-40*s, 140*s, 18*s, col)
    for dx, hh in ((-56, 58), (-28, 72), (0, 96), (28, 72), (56, 58)):
        cx = x+dx*s; b = foot-40*s
        o += f'<path d="M{cx-12*s},{b} C{cx-12*s},{b-hh*.5*s} {cx-5*s},{b-hh*.85*s} {cx},{b-hh*s} C{cx+5*s},{b-hh*.85*s} {cx+12*s},{b-hh*.5*s} {cx+12*s},{b} Z" fill="{col}" stroke="{col2}" stroke-width="1.5"/>'
    return o
def sugarpalm(x, foot, h=110):
    top = foot-h; o = [ln([(x, foot), (x+3, top)], "#7a5a3a", 6)]
    for a in range(0, 360, 30): o.append(ln([(x+3, top), (x+3+34*math.cos(math.radians(a)), top+22*math.sin(math.radians(a)))], "#4f7f46", 5))
    return "".join(o)
def banana(x, foot, h=100):
    o = [ln([(x, foot), (x, foot-h*.7)], "#6f8f3a", 8)]
    for dx, dy in ((-40, -.96), (38, -1.0), (-30, -1.18), (24, -1.22), (0, -1.28)):
        o.append(f'<path d="M{x},{foot-h*.66} Q{x+dx*.5},{foot+dy*h-6} {x+dx},{foot+dy*h+16}" stroke="#5fa04a" stroke-width="12" fill="none" stroke-linecap="round"/>')
    return "".join(o)
def acacia(x, foot, h=100):
    s = h/90
    return ln([(x, foot), (x-4*s, foot-50*s), (x-16*s, foot-74*s)], "#6b4a2e", 5*s) + ln([(x-4*s, foot-50*s), (x+14*s, foot-76*s)], "#6b4a2e", 4*s) + f'<ellipse cx="{x}" cy="{foot-82*s}" rx="{58*s}" ry="{12*s}" fill="#5e8a3a"/>'
def kili(x, foot, s=1.0):
    return (f'<path d="M{x-150*s},{foot} L{x-40*s},{foot-80*s} Q{x},{foot-92*s} {x+40*s},{foot-80*s} L{x+150*s},{foot} Z" fill="#8aa0b6"/>'
            f'<path d="M{x-52*s},{foot-70*s} L{x-40*s},{foot-80*s} Q{x},{foot-92*s} {x+40*s},{foot-80*s} L{x+54*s},{foot-68*s} L{x+30*s},{foot-72*s} L{x+14*s},{foot-64*s} L{x-6*s},{foot-73*s} L{x-24*s},{foot-64*s} Z" fill="#ffffff"/>')
def hills(foot):
    return f'<path d="M0,{foot} Q80,{foot-60} 170,{foot-16} T340,{foot-30} T420,{foot-10} V{foot} Z" fill="#8cbf62"/>' + "".join(ln([(200+i*14, foot-14-i*3), (360, foot-22-i*3)], "#5d8f3e", 2) for i in range(4))
def hut(x, foot, s=1.0):  # Rwanda royal beehive hut
    return (f'<path d="M{x-46*s},{foot} C{x-46*s},{foot-56*s} {x-20*s},{foot-92*s} {x},{foot-96*s} C{x+20*s},{foot-92*s} {x+46*s},{foot-56*s} {x+46*s},{foot} Z" fill="#c9a46a" stroke="#9a7a42" stroke-width="2"/>'
            + "".join(f'<path d="M{x-40*s+i*2*s},{foot-20*s-i*16*s} Q{x},{foot-28*s-i*16*s} {x+40*s-i*2*s},{foot-20*s-i*16*s}" stroke="#9a7a42" stroke-width="1.5" fill="none"/>' for i in range(4))
            + r(x-10*s, foot-30*s, 20*s, 30*s, "#6b4a2e", 8) + ln([(x, foot-96*s), (x, foot-116*s)], "#6b4a2e", 3*s))
def brick_house(x, foot, s=1.0, wall="#d98b5f", roof="#8f9aa3"):
    return (r(x-60*s, foot-70*s, 120*s, 70*s, wall) + f'<path d="M{x-72*s},{foot-68*s} L{x},{foot-112*s} L{x+72*s},{foot-68*s} Z" fill="{roof}"/>'
            + r(x-12*s, foot-40*s, 24*s, 40*s, "#6b4a2e", 2) + r(x-46*s, foot-52*s, 22*s, 18*s, "#cfe6ef", 2) + r(x+24*s, foot-52*s, 22*s, 18*s, "#cfe6ef", 2))
def bus(x, y, col="#2f8a5a"):
    return (r(x-20, y-64, 170, 56, col, 10) + "".join(r(x-8+i*30, y-56, 24, 20, "#cfe6ef", 3) for i in range(5)) + r(x-20, y-30, 170, 6, "#f6c453")
            + c(x+10, y-4, 12, INK) + c(x+116, y-4, 12, INK))
def lanterns():
    return "".join(c(40+i*46, 30+(i % 2)*10, 6, ["#e0503a", "#f6c453", "#6cbf5a", "#4a8ad6"][i % 4]) for i in range(9))
LOC = {
 'th': dict(skin=("#ecbd96", "#d9a47c"), land=lambda x, f, s: prang(x, f, s*.8), temple=S.temple, tree=S.palm, house=S.stilt_house, veh=S.tuk, cur="฿", sky=("#d8ecf2", "#f7ecd8"), ground="#b9cf8f"),
 'km': dict(skin=("#e2ad84", "#cf9a70"), land=lambda x, f, s: angkor(x, f, s*.7), temple=lambda x, f, s: angkor(x, f, s*.6), tree=sugarpalm, house=S.stilt_house, veh=S.tuk, cur="៛", sky=("#f3d6dd", "#f8ebe0"), ground="#9fc39a"),
 'rw': dict(skin=("#8a5a3c", "#774b30"), land=lambda x, f, s: hut(x, f, s*.9), temple=lambda x, f, s: hut(x, f, s*.9), tree=banana, house=lambda x, f, s: brick_house(x, f, s), veh=lambda x, y: bus(x, y, "#1a7fb0"), cur="FRw", sky=("#c4e7f6", "#eef6e8"), ground="#8cbf62", latin=True, hills=True),
 'sw': dict(skin=("#7d4f33", "#6c432a"), land=lambda x, f, s: kili(x, f, s*.8), temple=lambda x, f, s: kili(x, f, s*.7), tree=acacia, house=lambda x, f, s: brick_house(x, f, s, "#f1e3c6", "#b07a45"), veh=lambda x, y: bus(x, y, "#2f8a5a"), cur="TSh", sky=("#ffe1b0", "#fbefd6"), ground="#d8b46a", latin=True),
}
def use(k):
    global L
    L = LOC[k]; pics.SKIN, pics.SKIN2 = L['skin']; S.SKIN, S.SKIN2 = L['skin']
def outside(y=200, top=None, bot=None, ground=None):
    b = sky(top or L['sky'][0], bot or L['sky'][1], y, ground or L['ground'])
    if L.get('hills'): b += hills(y)
    return b
# ---------- scenes (one per kind of sub; texts in the target language)
def greet(a, b): return svg(two(a, b, outside(200), extra=L['land'](330, 200, .7) + L['tree'](40, 200, 100)))
def clock(nums, cards):
    o = [room(), c(200, 92, 64, "#ffffff", f'stroke="{TEAK}" stroke-width="6"')]
    for i in range(12): o.append(t(200+50*math.sin(i*math.pi/6), 92-50*math.cos(i*math.pi/6)+5, nums[i], 12, INK))
    o += [ln([(200, 92), (200, 56)], INK, 4), ln([(200, 92), (228, 104)], INK, 4), c(200, 92, 4, INK)]
    for i, s in enumerate(cards): o.append(card([30, 90, 258, 318][i], 190, s, 52, 46, "#fff4dc", fit(s, 24, 46)))
    return svg("".join(o))
def restaurant(menu, order):
    return svg("".join([room("#f6e6cc", "#b98d5e", 196), r(30, 30, 110, 70, "#fffaf0", 4, f'stroke="{TEAK}" stroke-width="3"'), t(85, 58, menu, fit(menu, 18, 96), TEAK),
        r(46, 70, 78, 4, "#c9b79c"), r(46, 80, 60, 4, "#c9b79c"), table(70, 168, 200), bowl(120, 168, food="#f3e2b3"), bowl(170, 168), bowl(220, 168, food="#6e9a64"),
        P(1, False, 60, 250, arms=[[(0, 0), (20, 10), (36, 2)]], scale=.9), P(0, True, 320, 250, arms=[[(0, 0), (-24, 14), (-40, 10)]], scale=.95), bub(196, 34, order, 16, "r")]))
def market(q):
    return svg("".join([sky("#f3e2c3", "#f6ecdc", 200, "#c9ab84"), '<path d="M30,60 L370,60 L350,30 L50,30 Z" fill="#c25e4f"/>', "".join(r(50+i*64, 30, 32, 30, "#f3e2c3") for i in range(5)),
        r(40, 140, 320, 14, TEAK, 3), r(50, 154, 10, 46, TEAK), r(340, 154, 10, 46, TEAK),
        "".join(c(80+i*18, 132, 9, "#f2b134") for i in range(4)), "".join(c(180+i*16, 130, 10, "#e0503a") for i in range(4)), "".join(c(272+i*16, 132, 9, "#7cae3f") for i in range(4)),
        P(0, True, 200, 140, scale=.7), P(5, False, 330, 252, arms=[[(0, 0), (-18, 12), (-32, 4)]], scale=.9), bub(232, 70, q, 16, "r")]))
def transport(q):
    return svg("".join([outside(196, ground="#bfb19a"), r(0, 216, W, 10, "#f3efe4"), L['veh'](150, 228), L['tree'](360, 196, 100), cloud(50, 50), cloud(260, 40, .8),
        P(4, False, 60, 250, arms=[[(0, 0), (16, -22), (28, -46)]], scale=.9), bub(90, 60, q, 16)]))
def tboard(lines, bw=250, extra=""):
    return svg("".join([room("#efe4cf", "#c9ab84", 205), board(110, 26, bw, 120, [(s, fit(s, z, bw-20), True) for s, z in lines]), P(3, True, 66, 236, arms=[[(0, 0), (20, -20), (40, -46)]]), extra]))
def school(lines): return tboard(lines, extra="".join([desk(250, 200, 110, 40), r(270, 186, 30, 14, "#e9a15b", 2), r(306, 190, 40, 6, "#5b7fa6", 2)]))
def lesson(a, b):
    return svg("".join([room("#efe4cf", "#c9ab84", 205), board(30, 24, 200, 100, [(a, fit(a, 24, 180), True), (b, fit(b, 18, 180), True)]),
        desk(250, 170, 130, 40), r(262, 150, 36, 20, "#c25e4f", 2), r(304, 154, 30, 16, "#5b7fa6", 2), r(340, 140, 8, 30, "#f2b134", 2),
        P(6, False, 150, 250, arms=[[(0, 0), (14, -24), (22, -52)]], scale=.85), P(1, True, 220, 250, scale=.85)]))
def home(): return svg("".join([outside(200, ground="#9cbf7a"), L['house'](150, 200, 1.0), L['tree'](330, 200, 110), r(280, 170, 40, 30, "#5b7fa6", 4), P(0, True, 260, 246, arms=[[(0, 0), (18, 6), (28, -10)]], scale=.85)]))
def hospital(pain):
    return svg("".join([room("#eef3f1", "#c3d0cc", 200), r(30, 30, 60, 60, "#ffffff", 6), r(54, 38, 12, 44, "#d9534f"), r(38, 54, 44, 12, "#d9534f"),
        r(250, 150, 120, 30, "#ffffff", 6, 'stroke="#c3d0cc" stroke-width="2"'), pics.person(180, 236, "#ffffff", "#5b7fa6", S.HAIR, female=True, arms=[[(0, 0), (20, 14), (36, 12)]]),
        ln([(190, 150), (206, 168), (214, 190)], INK, 2), c(214, 192, 5, "#9aa7b1"), P(3, False, 300, 236, arms=[[(0, 0), (-14, -18), (-6, -40)]]), bub(280, 40, pain, 16, "r")]))
def bank(name):
    return svg("".join([room("#eef0f2", "#c9c0b2", 200), r(0, 20, W, 26, "#2f4f66"), t(200, 39, name, fit(name, 16, 300), "#f3e2b3"),
        r(40, 60, 150, 76, "#d9e6ea", 3), P(1, True, 110, 198, scale=.9), r(30, 140, 340, 60, "#8a6a4a", 4), r(226, 104, 76, 34, "#7cae3f", 3), tk(264, 127, L['cur'], fit(L['cur'], 18, 66), "#ffffff"),
        r(314, 96, 28, 44, INK, 5), r(318, 102, 20, 28, "#9fd0e6", 2), P(5, False, 340, 262, back=True)]))
def weather():
    return svg("".join([sky("#bfe0ee", "#eaf4f2", 186, "#86b16a"), sun(320, 58, 30), cloud(60, 60), cloud(170, 40, .9, "#e3ebf0"),
        "".join(ln([(80+i*14, 86), (74+i*14, 104)], "#5b9ed6", 3) for i in range(5)), '<path d="M0,186 Q100,150 200,170 T400,160 V186 Z" fill="#6e9a5a"/>', L['tree'](330, 186, 80),
        "".join(r(40+i*46, 220, 34, 18, col, 4) for i, col in enumerate(["#d9534f", "#f2b134", "#f6e04b", "#6cbf5a", "#4a8ad6", "#7a5ab8", "#ffffff", INK]))]))
def festival():
    return svg("".join([sky("#f3c98b", "#f7e7c8", 200, "#c9ab84"), L['temple'](200, 200, 1.0), lanterns(),
        P(0, True, 70, 250, arms=[[(0, 0), (12, -20), (4, -40)]], scale=.85), P(4, True, 330, 250, arms=[[(0, 0), (-12, -20), (-4, -40)]], scale=.85)]))
def office():
    return svg("".join([room("#eef0f2", "#c9c0b2", 200), r(40, 26, 120, 80, "#d9e6ea", 3, 'stroke="#9aa7b1" stroke-width="4"'), desk(150, 160, 200, 50),
        r(210, 120, 72, 40, "#3d4a55", 4), r(214, 124, 64, 30, "#9fd0e6", 2), r(196, 158, 100, 4, "#56646f"), r(300, 136, 18, 24, "#ffffff", 3, f'stroke="{INK}"'),
        P(5, False, 110, 246, arms=[[(0, 0), (24, 8), (46, 8)]]), P(3, True, 340, 246, arms=[[(0, 0), (-16, 10), (-30, 4)]], scale=.9)]))
def airport(line1):
    return svg("".join([room("#eef0f2", "#c9c0b2", 200), r(30, 30, 210, 70, "#24323f", 6), tk(135, 60, line1, fit(line1, 15, 190), "#f6c453"), tk(135, 86, "→ 08:30", 15, "#9fd0e6"),
        '<path d="M300,40 l60,20 l-60,20 l10,-20 z" fill="#c25e4f"/>', P(5, False, 120, 250, back=True), r(150, 210, 36, 40, "#5b7fa6", 5), P(2, True, 300, 250, arms=[[(0, 0), (-16, 10), (-28, 0)]], scale=.9)]))
def phone_scene(word):
    return svg("".join([room("#eef0f2", "#c9c0b2", 200), r(150, 40, 100, 150, INK, 14), r(158, 52, 84, 120, "#9fd0e6", 4), t(200, 100, word, fit(word, 18, 76), INK), c(200, 180, 5, "#56646f"),
        P(1, True, 70, 250, arms=[[(0, 0), (16, -20), (8, -44)]], scale=.85), waves(260, 110, "#3d4a55")]))
def help_scene(a, b): return svg(two(a, b, outside(200), ia=4, ib=2, fa=False, fb=True, extra=r(330, 120, 50, 80, "#ffffff", 6, 'stroke="#d9534f" stroke-width="3"') + r(349, 130, 12, 40, "#d9534f") + r(335, 144, 40, 12, "#d9534f")))
def family():
    return svg("".join([room("#f6ecdc", "#c9ab84", 205), P(0, True, 90, 246), pics.person(200, 246, "#ffffff", "#6a3d7a", "#b8b8b8", female=True), P(5, False, 300, 246, scale=.75), P(2, True, 350, 246, scale=.6)]))
def signs(a, b):
    return svg("".join([outside(205, ground="#bfb19a"), r(30, 70, 160, 135, "#f3e8d6"), r(210, 50, 160, 155, "#e9dcc4"),
        r(36, 40, 148, 34, "#c25e4f", 4), t(110, 64, a, fit(a, 18, 136), "#ffffff"), r(216, 20, 148, 34, "#2f6a8a", 4), t(290, 44, b, fit(b, 18, 136), "#ffffff"),
        r(70, 120, 80, 85, TEAK, 3), r(250, 110, 80, 95, TEAK, 3), P(1, True, 200, 252, arms=[[(0, 0), (14, -18), (28, -34)]], scale=.9)]))
def names(a, b, c_): return svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(card(30+i*120, 70, s, 100, 60, "#ffffff", fit(s, 20, 90)) for i, s in enumerate([a, b, c_])), t(200, 190, "Aa", 30, TEAK), t(200, 230, "A · B · C", 16, "#7a6a5a")]), "#f6ecdc")
def letters(cards, bg="#f6ecdc"):
    o = [r(0, 0, W, H, bg)]
    n = len(cards); cols = 4 if n > 6 else 3
    for i, (s, sub) in enumerate(cards):
        x = 30 + (i % cols) * (340 // cols); y = 26 + (i // cols) * 112
        o.append(card(x, y, s, 340 // cols - 12, 96, "#ffffff", fit(s, 34, 340 // cols - 24), sub=sub))
    return svg("".join(o), bg)
def pronouns(a, b, c_):
    return svg("".join([room("#f6ecdc", "#c9ab84", 205), P(0, True, 90, 246, arms=[[(0, 0), (-10, 26), (0, 40)], [(0, 0), (10, 26), (0, 40)]]), pics.person(200, 246, "#ffffff", "#6a3d7a", "#b8b8b8", female=True),
        P(5, False, 310, 246, scale=.75), bub(30, 40, a, 17, maxw=110), bub(150, 40, b, 16, maxw=110), bub(270, 80, c_, 17, "r", maxw=100)]))
def counters(a, b, c_, top):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), table(30, 196, 340), "".join(c(70+i*30, 184, 12, "#f2b134") for i in range(3)), t(100, 146, a, fit(a, 20, 110), TEAK),
        "".join(r(190+i*16, 150, 10, 46, "#5b7fa6", 3) for i in range(3)), t(214, 136, b, fit(b, 20, 100), TEAK), "".join(r(282+i*24, 170, 20, 26, "#c25e4f", 4) for i in range(3)), t(316, 156, c_, fit(c_, 20, 100), TEAK),
        t(200, 50, top, fit(top, 26, 340), INK)]), "#f6ecdc")
def directions(lft, rgt, up, dn):
    return svg("".join([outside(196, ground="#9cbf7a"), sun(70, 60, 24), L['house'](200, 196, .8), f'<path d="M290,120 h60 l-14,-14 M350,120 l-14,14" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>',
        f'<path d="M110,120 h-60 l14,-14 M50,120 l14,14" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>', t(80, 160, lft, fit(lft, 20, 110), TEAK), t(320, 160, rgt, fit(rgt, 20, 110), TEAK),
        t(200, 28, up, fit(up, 18, 200), TEAK), t(200, 250, dn, fit(dn, 18, 200), TEAK)]))
def bigsmall(a, b):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), r(40, 40, 140, 180, "#ffffff", 10, f'stroke="{INK}" stroke-width="1.5"'), r(220, 40, 140, 180, "#ffffff", 10, f'stroke="{INK}" stroke-width="1.5"'),
        c(110, 120, 46, "#e0503a"), c(290, 130, 20, "#e0503a"), t(110, 204, a, fit(a, 22, 126), TEAK), t(290, 204, b, fit(b, 22, 126), TEAK)]), "#f6ecdc")
def givetake(a, b):
    return svg("".join([room("#f3e8d6", "#c9ab84", 205), P(0, True, 110, 246, arms=[[(0, 0), (30, 14), (60, 10)]]), P(5, False, 290, 246, arms=[[(0, 0), (-30, 14), (-60, 10)]]),
        r(180, 100, 40, 32, "#c25e4f", 4), ln([(200, 100), (200, 132)], "#f6c453", 4), ln([(180, 116), (220, 116)], "#f6c453", 4), bub(30, 26, a, 18, maxw=130), bub(260, 40, b, 18, "r", maxw=120)]))
def politeeat(a, b):
    return svg("".join([room("#f6e6cc", "#b98d5e", 200), table(80, 176, 240), bowl(150, 176, food="#f3e2b3"), bowl(200, 176), bowl(250, 176, food="#6e9a64"),
        pics.person(90, 246, "#ffffff", "#6a3d7a", "#b8b8b8", female=True, scale=.9), P(5, False, 320, 246, arms=[[(0, 0), (-10, -16), (-2, -34)], [(0, 0), (10, -16), (2, -34)]], scale=.9),
        bub(30, 34, a, 17, maxw=120), bub(230, 40, b, 16, "r", maxw=140)]))
def quant(a, b, line):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(c(60+i*36, 120, 14, "#f2b134") for i in range(4)), t(110, 170, a, fit(a, 20, 150), TEAK),
        "".join(r(240+i*40, 100, 28, 40, "#5b7fa6", 6) for i in range(3)), t(300, 170, b, fit(b, 20, 150), TEAK), t(200, 230, line, fit(line, 20, 340), INK), tk(200, 50, "?", 40, "#c25e4f", "700")]), "#f6ecdc")
def verbs(line, cur=True):
    return svg("".join([room(), P(0, True, 110, 246, arms=[[(0, 0), (30, 14), (60, 10)]]), P(5, False, 290, 246, arms=[[(0, 0), (-30, 14), (-60, 10)]]),
        r(176, 104, 48, 28, "#fff4dc", 4, f'stroke="{INK}"'), tk(200, 124, L['cur'] if cur else "★", fit(L['cur'], 15, 42), TEAK, "700"), bub(120, 30, line, 15, maxw=200)]))
def want(a, b):
    return svg("".join([outside(205, "#e3eef0", "#f6ecdc", "#c9ab84"), P(2, True, 120, 246, arms=[[(0, 0), (14, -20), (6, -40)]]), c(250, 80, 50, "#ffffff", f'stroke="{INK}" stroke-width="1.5"'),
        c(196, 140, 8, "#ffffff", f'stroke="{INK}"'), c(184, 158, 5, "#ffffff", f'stroke="{INK}"'), t(250, 76, a, fit(a, 22, 88), TEAK), t(250, 104, b, fit(b, 16, 88), INK)]))
def speaklisten(a, b):
    return svg("".join([room("#f3e8d6"), P(0, True, 110, 246, arms=[[(0, 0), (16, 20), (30, 28)]]), waves(140, 110), P(5, False, 290, 246, arms=[[(0, 0), (-18, -30), (-16, -64)]]),
        bub(30, 30, a, 18, maxw=120), bub(230, 40, b, 16, "r", maxw=140)]))
def timeline(a, b, c_, top):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), ln([(40, 140), (360, 140)], TEAK, 5), "".join(c(80+i*120, 140, 14, ["#e0503a", "#f2b134", "#6cbf5a"][i]) for i in range(3)),
        t(80, 186, a, fit(a, 20, 110), TEAK), t(200, 186, b, fit(b, 20, 110), TEAK), t(320, 186, c_, fit(c_, 20, 110), TEAK), t(200, 80, top, fit(top, 20, 340), INK)]), "#f6ecdc")
def connect(a, b, mid, line):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), card(40, 90, a, 90, 60, "#ffffff", fit(a, 22, 80)), card(270, 90, b, 90, 60, "#ffffff", fit(b, 22, 80)),
        r(150, 98, 100, 44, "#f2b134", 22), t(200, 128, mid, fit(mid, 22, 90), "#ffffff"), t(200, 210, line, fit(line, 20, 340), TEAK)]), "#f6ecdc")
def happy(word):
    return svg("".join([sky("#f3d9a8", "#f7ecd8", 205, "#c9ab84"), sun(320, 50, 26), P(0, True, 140, 246, arms=[[(0, 0), (14, -24), (20, -50)], [(0, 0), (-14, -24), (-20, -50)]]),
        P(5, False, 260, 246, arms=[[(0, 0), (14, -24), (20, -50)], [(0, 0), (-14, -24), (-20, -50)]]), bub(150, 26, word, 18, maxw=140)]))
def degree(a, b, top):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(r(50+i*80, 200-(i+1)*36, 50, (i+1)*36, ["#f6d58a", "#f2b134", "#d9822b", "#b5442e"][i], 4) for i in range(4)),
        t(75, 224, a, fit(a, 16, 90), TEAK), t(315, 224, b, fit(b, 16, 90), TEAK), t(200, 40, top, fit(top, 20, 340), INK), ln([(40, 206), (360, 206)], INK, 2)]), "#f6ecdc")
def fullempty(a, b):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), r(60, 70, 90, 130, "#e8f1f6", 8, 'stroke="#9fb3c1" stroke-width="3"'), r(64, 90, 82, 106, "#5b9ed6", 6), t(105, 230, a, fit(a, 20, 120), TEAK),
        r(250, 70, 90, 130, "#e8f1f6", 8, 'stroke="#9fb3c1" stroke-width="3"'), r(254, 186, 82, 10, "#5b9ed6", 4), t(295, 230, b, fit(b, 20, 120), TEAK)]), "#f6ecdc")
def compare(a, b, line):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), c(110, 110, 34, "#f2b134"), c(290, 110, 34, "#f2b134"), tk(200, 118, "=", 40, TEAK, "700"),
        t(110, 190, a, fit(a, 20, 140), TEAK), t(290, 190, b, fit(b, 20, 140), TEAK), t(200, 240, line, fit(line, 20, 340), INK)]), "#f6ecdc")
def duo(a, b, ia=0, ib=1, fa=True, fb=False): return svg(two(a, b, outside(205, "#e3eef0", "#f6ecdc", "#c9ab84"), ia, ib, fa, fb, extra=L['tree'](360, 205, 90)))
def openclose(line):
    return svg("".join([room(), r(240, 50, 100, 155, TEAK, 4), r(250, 60, 80, 140, "#a5825c", 3), c(262, 130, 5, GOLD), P(5, False, 180, 246, arms=[[(0, 0), (40, -4), (74, -6)]]), bub(30, 40, line, 16, maxw=180)]))
def think(word):
    return svg("".join([room("#efe4cf"), desk(120, 180, 200, 30), r(160, 160, 70, 20, "#fffaf0", 2, f'stroke="{INK}"'), ln([(196, 160), (196, 180)], INK, 1.5),
        P(1, True, 200, 250, arms=[[(0, 0), (14, 26), (20, 34)]], scale=.9), c(270, 70, 38, "#ffffff", f'stroke="{INK}"'), t(270, 76, word, fit(word, 22, 66), TEAK), c(236, 116, 6, "#ffffff", f'stroke="{INK}"')]))
def looks(a, b, c_):
    return svg("".join([outside(205, "#e3eef0", "#f6ecdc", "#c9ab84"), P(0, True, 90, 246), P(5, False, 200, 246, scale=1.1), P(3, True, 310, 246, scale=.8),
        t(90, 40, a, fit(a, 20, 110), TEAK), t(200, 30, b, fit(b, 20, 110), TEAK), t(310, 60, c_, fit(c_, 18, 110), TEAK)]))
def measure(a, b):
    return svg("".join([outside(200), P(0, True, 50, 236, scale=.8), L['house'](330, 200, .6), ln([(80, 150), (290, 150)], TEAK, 3), '<path d="M80,150 l12,-7 v14 z M290,150 l-12,-7 v14 z" fill="#8a4a16"/>',
        t(185, 136, a, fit(a, 20, 200), TEAK), t(185, 180, b, fit(b, 16, 200), INK)]))
def lost(word):
    return svg("".join([room("#f3e8d6"), P(2, True, 140, 246, arms=[[(0, 0), (14, -20), (20, -44)], [(0, 0), (-14, -20), (-20, -44)]]), r(240, 170, 90, 50, "#c9b79c", 6), tk(285, 140, "?", 44, "#c25e4f", "700"), bub(30, 40, word, 18, maxw=150)]))
# roots: word card + picture
PIC = {
 'work': lambda: P(5, False, 285, 220, arms=[[(0, 0), (24, 10), (40, 2)], [(0, 0), (-24, 10), (-40, 2)]], scale=.9) + r(250, 196, 70, 10, TEAK, 2),
 'car': lambda: L['veh'](232, 176) if not L.get('latin') else bus(230, 176),
 'water': lambda: r(255, 70, 60, 110, "#e8f1f6", 10, 'stroke="#9fb3c1" stroke-width="3"') + r(259, 110, 52, 66, "#5b9ed6", 8),
 'rice': lambda: bowl(285, 150, food="#ffffff") + c(285, 128, 8, "#ffffff"),
 'day': lambda: sun(285, 100, 34) + "".join(r(214+i*24, 170, 20, 20, "#f3e2c3" if i != 3 else "#e0503a", 3) for i in range(7)),
 'people': lambda: P(1, True, 250, 220, scale=.85) + P(5, False, 320, 220, scale=.85),
 'child': lambda: P(1, True, 250, 220, scale=.95) + P(4, False, 320, 220, scale=.6),
 'building': lambda: r(220, 70, 130, 130, "#e9dcc4", 3) + '<path d="M210,74 L285,36 L360,74 Z" fill="#b5442e"/>' + "".join(r(236+(i % 3)*40, 90+(i // 3)*40, 22, 22, "#9fd0e6", 2) for i in range(6)) + r(270, 170, 30, 30, TEAK),
 'machine': lambda: r(222, 90, 120, 80, "#3d4a55", 6) + r(230, 98, 104, 60, "#9fd0e6", 3) + r(266, 170, 32, 14, "#56646f") + r(250, 184, 64, 6, "#56646f", 3),
 'most': lambda: "".join(r(220+i*36, 200-(i+1)*30, 28, (i+1)*30, "#f2b134" if i < 3 else "#b5442e", 4) for i in range(4)) + tk(328, 64, "★", 22, GOLD, "700"),
 'book': lambda: r(225, 80, 120, 90, "#fffaf0", 4, f'stroke="{INK}" stroke-width="2"') + ln([(285, 80), (285, 170)], INK, 2) + "".join(r(236, 96+i*16, 40, 4, "#c9b79c") for i in range(4)) + "".join(r(296, 96+i*16, 40, 4, "#c9b79c") for i in range(4)),
 'eye': lambda: f'<ellipse cx="285" cy="120" rx="60" ry="32" fill="#ffffff" stroke="{INK}" stroke-width="3"/>' + c(285, 120, 22, "#6a4a2e") + c(285, 120, 10, INK) + c(293, 112, 4, "#ffffff"),
 'heart': lambda: '<path d="M285,190 C200,130 230,60 285,100 C340,60 370,130 285,190 Z" fill="#e0503a"/>',
 'sky': lambda: sun(250, 90, 26) + cloud(270, 120, .9) + "".join(ln([(250+i*14, 160), (244+i*14, 180)], "#5b9ed6", 3) for i in range(5)),
 'song': lambda: f'<path d="M260,170 V80 L330,66 V150" stroke="{INK}" stroke-width="6" fill="none"/>' + c(250, 172, 14, INK) + c(320, 152, 14, INK) + r(220, 196, 130, 10, GOLD, 3),
 'three': lambda: "".join(P(i, i % 2 == 0, 235+i*50, 220, scale=.6) for i in range(3)),
 'food': lambda: table(214, 170, 140) + bowl(250, 170, food="#f3e2b3") + bowl(300, 170, food="#6e9a64"),
 'door': lambda: r(245, 50, 80, 150, TEAK, 4) + r(253, 58, 64, 136, "#a5825c", 3) + c(262, 128, 5, GOLD) + tk(340, 120, "🔑" if False else "", 1),
}
def root(word, meaning, pic):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), r(20, 20, 150, 220, "#ffffff", 14, f'stroke="{GOLD}" stroke-width="3"'), t(95, 120, word, fit(word, 40, 130), TEAK), S.t(95, 164, meaning, fit(meaning, 16, 136), "#7a6a5a", lao=False, w="600"),
                        r(190, 20, 190, 220, "#fffaf0", 14, 'stroke="#e1d3bb" stroke-width="2"'), PIC[pic]()]), "#f6ecdc")
def wordform(a, plus, b, res):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), card(30, 70, a, 120, 60, "#f6d58a", fit(a, 22, 110)), tk(170, 108, plus, 26, TEAK, "700"), card(190, 70, b, 180, 60, "#ffffff", fit(b, 22, 170)),
        tk(200, 168, "↓", 26, TEAK, "700"), t(200, 222, res, fit(res, 26, 340), TEAK)]), "#f6ecdc")
def sounds(cards, curves=None, bg="#f6ecdc"):
    o = [r(0, 0, W, H, bg), P(2, True, 64, 250, arms=[[(0, 0), (14, 18), (26, 22)]]), waves(100, 110)]
    for i, (s, sub) in enumerate(cards):
        x = 140 + (i % 3) * 84; y = 30 + (i // 3) * 110
        o.append(card(x, y, s, 74, 64, "#ffffff", fit(s, 28, 66), sub=sub))
        if curves: o.append(tone_curve(x+8, y+88, 58, curves[i % len(curves)], ["#e0503a", "#f2b134", "#4a8ad6", "#6cbf5a", "#7a5ab8", TEAK][i % 6]))
    return svg("".join(o), bg)

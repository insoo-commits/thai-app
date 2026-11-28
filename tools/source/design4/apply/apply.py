# Apply Lao v3.30-v3.34 design (sticky bar, new skin, glide/arrows, no scrollbar, tight gaps, sub pictures) to the 4 apps.
import json, re, sys
sys.path.insert(0, '/mnt/project-files/design4')
import os
_cwd = os.getcwd(); os.chdir('/mnt/project-files/design4')
from art import ART
from build import D as MOCK
os.chdir(_cwd)
HERE = '/mnt/project-files/design4/apply/'
lao = open(HERE + 'lao_index_v334.html').read().split('\n')
CSS = lao[516:611]          # lines 517..611
assert CSS[0].startswith('/* v3.30') and CSS[-1].startswith('/* v3.34'), (CSS[0][:30], CSS[-1][:30])
assert CSS[2].startswith('/* 시안 B') and CSS[3].startswith(':root{--L-bg')
TAIL = open(HERE + 'lao_tail.js').read()
PICS = json.load(open(HERE + 'subpics4.json'))
APPS = {  # repo: (mock id, art key, name in sticky bar, old ver, new ver, shell prefix, storage prefix)
 'thai-app': ('thai', 'th', 'THAI Lang'), 'rwanda-app': ('rwanda', 'rw', 'RWANDA Lang'),
 'khmer-app': ('khmer', 'km', 'KHMER Lang'), 'swahili-app': ('swahili', 'sw', 'SWAHILI Lang')}
def palette(c, name):
    return [f'/* {name} */',
      f':root{{--L-bg:{c["bg"]};--L-line:{c["line"]};--L-line2:{c["line2"]};--L-tint:{c["tint"]};--L-now:{c["soft"]};--L-segbg:{c["line"]};--L-a1:{c["a1"]};--L-a2:{c["a2"]};--L-soft:{c["soft"]};',
      f'  --T1:{c["T1"]};--T2:{c["T2"]};--T3:{c["T3"]};--G1a:{c["G1a"]};--G1b:{c["G1b"]};--G2:{c["G2"]};--Ttitle:{c["Tt"]};--Tart:{c["Ta"]};',
      f'  --D-bg:{c["dbg"]};--D-sheet:{c["dsheet"]};--D-line:{c["dline"]};--D-line2:{c["dline2"]};--D-tint:{c["dtint"]};--D-now:{c["dsoft"]};--D-acc:{c["dacc"]};--D-soft:{c["dsoft"]}}}']
def run(repo, newv=None, d=None):
    mid, ak, nm = APPS[repo]
    m = next(x for x in MOCK if x['id'] == mid)
    d = (d.rstrip('/') + '/') if d else f'/home/user/{repo}/'
    ix = open(d + 'index.html').read(); js = open(d + 'app.js').read(); sw = open(d + 'sw.js').read()
    oldv = re.search(r'AV="app\.js\?v=([\d.]+)"', ix).group(1)
    css = CSS[:2] + palette(m['c'], f'{m["ko"]} 앱: {m["pal"]}') + CSS[6:]
    css = [l.replace('v3.30 RYU', 'RYU (라오 v3.30)').replace('v3.31 RYU: 시안 B 황금 사원', f'RYU (라오 v3.31): 새 디자인 {m["pal"]}').replace('v3.32 RYU', 'RYU (라오 v3.32)').replace('v3.33 RYU', 'RYU (라오 v3.33)').replace('v3.34 RYU', 'RYU (라오 v3.34)') for l in css]
    assert '/* RYU (라오 v3.30)' not in ix, 'already applied'
    h = ix.index('</head>'); k = ix.rindex('</style>', 0, h)
    ix = ix[:k] + '\n' + '\n'.join(css) + '\n' + ix[k:]
    assert 'RYU (라오 v3.30)' in ix
    ix = ix.replace('<header>', '<header>' + ART[ak], 1)
    stick = f'<div class="stick" id="stick" hidden><div class="stin"><div class="strow"><b>{nm}</b><span id="stickT"></span><button type="button" id="stickQ" aria-label="검색"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></button></div><nav class="groups" id="stickG" aria-label="대분류"></nav></div></div>'
    k = ix.index('<section class="sheet" id="sheet">')
    ix = ix[:k] + stick + '\n  ' + ix[k:]
    if newv:
        ix = ix.replace(f'v{oldv} · Claude', f'v{newv} · Claude').replace(f'app.js?v={oldv}"', f'app.js?v={newv}"')
        ix = re.sub(r'<div class="ver">\d{4}-\d\d-\d\d ', '<div class="ver">2026-11-24 ', ix)
        sw = re.sub(r'(SHELL="[a-z]+-shell-v)[\d.]+"', lambda mm: mm.group(1) + newv + '"', sw)
    else: newv = oldv
    # app.js: pictures + band layout + sticky/glide/arrows
    sp = PICS[repo]
    js = js.replace('function renderBand(){', '/* RYU (라오 v3.34): 소분류마다 그림 하나 (design4/apply/specs.py) */\nconst SUBPIC=' + json.dumps(sp, ensure_ascii=False) + ';\nfunction renderBand(){', 1)
    old = re.search(r'\$\("#band"\)\.innerHTML=`<select id="bsel" class="bsel bigsel" aria-label="묶음 고르기"></select>\$\{bb&&bb\.i\?`<p class="bintro">\$\{laoWrap\(bb\.i\)\}</p>`:""\}\$\{bb&&bb\.tp\.length\?`<div class="box">\$\{bb\.tp\.map\(t=>`<p>\$\{laoWrap\(t\)\}</p>`\)\.join\(""\)\}</div>`:""\}`;', js)
    assert old, repo + ' band line'
    new = '/* RYU (라오 v3.34): 소분류 그림 왼쪽, 설명 오른쪽 */const _txt=`${bb&&bb.i?`<p class="bintro">${laoWrap(bb.i)}</p>`:""}${bb&&bb.tp.length?`<div class="box">${bb.tp.map(t=>`<p>${laoWrap(t)}</p>`).join("")}</div>`:""}`,_pic=SUBPIC[s.id];$("#band").innerHTML=`<div class="brow"><select id="bsel" class="bsel bigsel" aria-label="묶음 고르기"></select></div>${_pic&&_txt?`<div class="bandrow"><div class="bandpic" aria-hidden="true">${_pic}</div><div class="bandtxt">${_txt}</div></div>`:_txt}`;'
    js = js[:old.start()] + new + js[old.end():]
    js = js.rstrip('\n') + '\n\n' + TAIL.replace('v3.30 RYU', 'RYU (라오 v3.30)').replace('v3.31 RYU', 'RYU (라오 v3.31)')
    open(d + 'index.html', 'w').write(ix); open(d + 'app.js', 'w').write(js); open(d + 'sw.js', 'w').write(sw)
    print(repo, oldv, '->', newv, 'pics', len(sp))
    import og; og.inject(repo, d)   # RYU 2026-11-28: link preview card (og.py)
if __name__ == '__main__':
    # apply.py <repo> <newver>            : patch the clone in /home/user/<repo> and bump the version
    # apply.py <repo> --out <built dir>   : patch a fresh make.sh build (version already set by the build)
    if len(sys.argv) > 3 and sys.argv[2] == '--out': run(sys.argv[1], None, sys.argv[3])
    else: run(sys.argv[1], sys.argv[2])

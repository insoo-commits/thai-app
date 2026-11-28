# RYU 2026-11-24 (Lao v3.35-3.37): description text sized like the hotel English app (intro 14.5 / tips 14, tablet 21.5 / 20.5),
# Lao/Thai/... words inside 1.1em, bullet list with hanging indent. Idempotent: python3 patch_band.py <app dir>
import sys, re
d = sys.argv[1]
s = open(f'{d}/app.js').read()
old = 'bb.tp.map(t=>`<p>${laoWrap(t)}</p>`)'
if old in s:
    s = s.replace(old, 'bb.tp.map(t=>/^•\\s*/.test(t)?`<p class="bl">${laoWrap(t.replace(/^•\\s*/,""))}</p>`:`<p>${laoWrap(t)}</p>`)')
    open(f'{d}/app.js', 'w').write(s)
h = open(f'{d}/index.html').read()
h = h.replace('\n/* RYU 2026-11-24: bullet list with hanging indent (wrapped lines start under the text) */\n#band .box p.bl{position:relative;padding-left:1em}\n#band .box p.bl::before{content:"•";position:absolute;left:.15em;top:0}\n', '')
for a, b in [('#band .bandtxt .bintro{font-size:13px!important', '#band .bandtxt .bintro{font-size:14.5px!important'),
             ('#band .bandtxt .box{font-size:12.5px!important', '#band .bandtxt .box{font-size:14px!important'),
             ('#band .bandtxt .box p{font-size:12.5px!important', '#band .bandtxt .box p{font-size:14px!important'),
             ('#band .bandtxt .box,#band .bandtxt .box p{font-size:13px!important}', '#band .bandtxt .box,#band .bandtxt .box p{font-size:14px!important}')]:
    h = h.replace(a, b)
M = '/* band-v2 RYU 2026-11-24 */'
if M not in h:
    i = h.rfind('#band .bandtxt .box p{font-size'); j = h.index('</style>', i)
    add = (M + '\nhtml.tab #band .bandtxt .bintro{font-size:21.5px!important}\nhtml.tab #band .bandtxt .box,html.tab #band .bandtxt .box p{font-size:20.5px!important}\n'
           'html.tab .bandpic{flex-basis:360px!important}\n#band .bandtxt .lo,#band .bandtxt .tip-lo{font-size:1.1em!important;line-height:1}\n'
           '#band .box p.bl{position:relative;padding-left:1em}\n#band .box p.bl::before{content:"•";position:absolute;left:.15em;top:0}\n')
    h = h[:j] + add + h[j:]
open(f'{d}/index.html', 'w').write(h)
M2 = '/* seg-wide */'
if M2 not in h:
    j = h.rfind('</style>', 0, h.index(M) + 10**6) if False else h.index('</style>', h.index(M))
    h = h[:j] + M2 + '\n' + '/* RYU 2026-11-24: phone: 문장·단어·퀴즈 tabs fill the free width beside the repeat/speed boxes */\n@media (max-width:600px){.controls .seg{flex:1 1 auto;margin-right:10px!important}.controls .seg button{flex:1 1 0;text-align:center;display:inline-flex;justify-content:center;align-items:center}}\n' + h[j:]
    open(f'{d}/index.html', 'w').write(h)
print(d, 'ok')

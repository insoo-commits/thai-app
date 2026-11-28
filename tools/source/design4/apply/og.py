# Link-preview card (KakaoTalk, Facebook, LINE …) for the 4 language apps (RYU 2026-11-28).
# og.py <repo> <site dir>: copies og/<repo>.jpg to <dir>/og.jpg and puts og/twitter meta tags in <dir>/index.html.
# Called by apply.py run(); images made by og/mk.js (Playwright render of the app header art).
import sys, os, shutil, re, html
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
OG = {'thai-app': ('THAI Lang · 태국어 배우기', '태국어, 주제별로 공부하기 · 문장 · 단어 · 원어민 음성'),
      'khmer-app': ('KHMER Lang · 캄보디아어 배우기', '캄보디아어(크메르어) 첫걸음 · 문장 · 단어 · 원어민 음성'),
      'rwanda-app': ('RWANDA Lang · 르완다어 배우기', '르완다어, 주제별로 공부하기 · 문장 · 단어 · 원어민 음성'),
      'swahili-app': ('SWAHILI Lang · 스와힐리어 배우기', '스와힐리어, 주제별로 공부하기 · 문장 · 단어 · 원어민 음성')}
def inject(repo, d):
    d = d.rstrip('/') + '/'; t, desc = OG[repo]; url = f'https://insoo-commits.github.io/{repo}/'
    shutil.copyfile(HERE + f'og/{repo}.jpg', d + 'og.jpg')
    ix = open(d + 'index.html').read()
    ix = re.sub(r'\n?<!-- link preview -->.*?<!-- /link preview -->', '', ix, flags=re.S)
    e = html.escape
    tags = (f'\n<!-- link preview --><meta property="og:type" content="website"><meta property="og:site_name" content="{e(repo)}"><meta property="og:url" content="{url}">'
            f'<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:image" content="{url}og.jpg?v=1"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{url}og.jpg?v=1"><!-- /link preview -->')
    k = ix.index('</title>') + len('</title>')
    open(d + 'index.html', 'w').write(ix[:k] + tags + ix[k:])
    print(repo, 'og ok')
if __name__ == '__main__': inject(sys.argv[1], sys.argv[2])

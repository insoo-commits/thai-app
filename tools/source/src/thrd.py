"""Thai -> Korean reading (한글 독음) and tone/syllable data, from tltk g2p.
Rules (follow the Lao app where the sounds match):
  onsets  ก ㄲ, ข ค ㅋ, จ ㅉ, ฉ ช ㅊ, ซ ส ㅆ, ด ㄷ, ต ㄸ, ถ ท ㅌ, บ ㅂ, ป ㅃ, ผ พ ฟ ฝ ㅍ, ง 응, ย/ญ y-glide, ว w-glide, ร ล ㄹ, อ ㅇ
  clusters ปล 쁠라 (C + 으 + ㄹ받침 + ㄹ), ครับ 크랍 (C + 으 + ㄹ), กว/ขว 꽈/콰
  vowels  ɔ ㅓ (ขอ 커), ɛ ㅐ, ɯ ㅡ, ə open ㅓ (เธอ 터) / closed ㅡ (เงิน 응은, เดิน 든), ia 이아, ɯa 으아, ua 우아; length not shown
  finals  k ㄱ, t ㅅ, p ㅂ, ŋ ㅇ, w 우 (แล้ว 래우, เที่ยว 티아우) but aw 아오 (เรา 라오), j 이 (ใจ 짜이)
  intervocalic ล inside one word: ㄹ받침 on the syllable before (เกาหลี 까올리)
Tones (tltk numbering): 0 mid 1 low 2 falling 3 high 4 rising  ->  app t1..t5 = 평성 1, 2 낮은, 3 떨어지는, 4 높은, 5 올라가는.
"""
import re,functools
from tltk import nlp

ON={'p':'ㅃ','ph':'ㅍ','t':'ㄸ','th':'ㅌ','k':'ㄲ','kh':'ㅋ','c':'ㅉ','ch':'ㅊ','b':'ㅂ','d':'ㄷ','f':'ㅍ','s':'ㅆ','h':'ㅎ',
    'm':'ㅁ','n':'ㄴ','N':'ㅇ','l':'ㄹ','r':'ㄹ','w':'ㅇ','j':'ㅇ','?':'ㅇ','':'ㅇ'}
CHO='ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
JUNG='ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
JONG=['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
def H(c,v,f=''): return chr(0xAC00+(CHO.index(c)*21+JUNG.index(v))*28+JONG.index(f))
FIN={'p':'ㅂ','t':'ㅅ','k':'ㄱ','m':'ㅁ','n':'ㄴ','N':'ㅇ','':''}
# vowel -> list of jamo vowels (multi-part for diphthongs)
VW={'a':['ㅏ'],'i':['ㅣ'],'U':['ㅡ'],'u':['ㅜ'],'e':['ㅔ'],'x':['ㅐ'],'o':['ㅗ'],'O':['ㅓ'],'@':['ㅓ'],
    'ia':['ㅣ','ㅏ'],'Ua':['ㅡ','ㅏ'],'ua':['ㅜ','ㅏ']}
GW={'ㅏ':'ㅘ','ㅐ':'ㅙ','ㅔ':'ㅞ','ㅣ':'ㅟ','ㅓ':'ㅝ','ㅗ':'ㅝ','ㅜ':'ㅜ','ㅡ':'ㅢ'}   # w-glide
GJ={'ㅏ':'ㅑ','ㅐ':'ㅒ','ㅔ':'ㅖ','ㅓ':'ㅕ','ㅗ':'ㅛ','ㅜ':'ㅠ','ㅣ':'ㅣ','ㅡ':'ㅡ'}   # y-glide
SY=re.compile(r"^(ph|th|kh|ch|[ptkcbdfshmnNlrwj?])?([lrw])?(iia|ia|UUa|Ua|uua|ua|aa|a|ii|i|UU|U|uu|u|ee|e|xx|x|oo|o|OO|O|@@|@)([ptkmnNwj])?(\d)$")
def parse(s):
    m=SY.match(s)
    if not m: raise ValueError('syl '+s)
    on,cl,v,f,t=m.groups();on=on or ''
    vv={'iia':'ia','UUa':'Ua','uua':'ua'}.get(v,v);vv=vv[0] if len(vv)==2 and vv[0]==vv[1] else vv
    return dict(on=on,cl=cl or '',v=vv,long=len(v)>len(vv) or v in('iia','UUa','uua'),f=f or '',t=int(t))
def hangul(sy):
    """one phonological syllable -> list of Hangul syllables"""
    on,cl,v,f=sy['on'],sy['cl'],sy['v'],sy['f']
    out=[]
    if on=='N': out.append('응');c='ㅇ'
    else: c=ON[on]
    vs=list(VW[v])
    if cl in('l','r'):
        out.append(H(c,'ㅡ','ㄹ' if cl=='l' else ''));c='ㄹ'
    if cl=='w' or on=='w':
        if on=='w' and v=='o': vs[0]='ㅝ'
        else: vs[0]=GW.get(vs[0],vs[0])
        if on=='w' and v=='u': c='ㅇ';vs[0]='ㅜ'
    if on=='j': vs[0]=GJ.get(vs[0],vs[0])
    # closed ə = ㅡ (RYU Lao rule), open ə = ㅓ
    if v=='@' and f in FIN and f: vs[0]='ㅡ' if vs[0]=='ㅓ' else vs[0]
    fj=''
    tail=[]
    if f=='w':
        if v=='a': tail=['오']
        else: tail=['우']
    elif f=='j': tail=['이']
    else: fj=FIN[f]
    for k,vv in enumerate(vs):
        last=k==len(vs)-1
        out.append(H(c if k==0 else 'ㅇ',vv,fj if last else ''))
    out+=tail
    return out
# disk cache: tltk g2p / syl_segment cost ~0.08 s per word; keep results between builds
import json as _json,os as _os,atexit as _atexit
_CF=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'g2pcache.json')
try: _C=_json.load(open(_CF,encoding='utf-8'))
except Exception: _C={'g':{},'s':{}}
_N=[0]
@_atexit.register
def _save():
    if _N[0]:
        tmp='/tmp/g2pcache.tmp';_json.dump(_C,open(tmp,'w',encoding='utf-8'),ensure_ascii=False)
        import shutil;shutil.copyfile(tmp,_CF)
def syl(w):
    if w not in _C['s']: _C['s'][w]=nlp.syl_segment(w);_N[0]+=1
    return _C['s'][w]
def g2p(w):
    if w not in _C['g']:
        r=nlp.g2p(w)
        _C['g'][w]=r.split('<tr/>')[1].split('<s/>')[0].rstrip('|');_N[0]+=1
    return _C['g'][w]
@functools.lru_cache(None)
def word(w):
    """-> syllables = list of dicts with tone. If g2p drops syllables (สิบเอ็ด -> si1), read each written syllable alone."""
    seg=g2p(w)
    groups=[g for g in re.split(r'[~|]',seg) if g]
    orth=[g for g in syl(w).split('~') if g and g!='<s/>']
    if (len(groups)<len(orth) and len(orth)>1) or any(not g.strip("'") for g in groups):
        raise ValueError('g2p dropped syllables: '+w+' '+seg)
    sys_=[]
    for g in groups:
        for s in g.split("'"):
            if s: sys_.append(parse(s))
    return sys_
def reading(sys_,lrule=True):
    hs=[hangul(s) for s in sys_]
    # intervocalic l inside one word -> ㄹ받침 on the syllable before
    for k in range(1,len(sys_) if lrule else 1):
        if sys_[k]['on']=='l' and not sys_[k]['cl'] and hs[k-1]:
            last=hs[k-1][-1];c=ord(last)-0xAC00
            if 0<=c<11172 and c%28==0: hs[k-1][-1]=chr(ord(last)+JONG.index('ㄹ'))
    return ''.join(''.join(h) for h in hs)
FALLBACK=set()
TONE={0:'t1',1:'t2',2:'t3',3:'t4',4:'t5'}
if __name__=='__main__':
    import sys
    for w in sys.argv[1:]:
        s=word(w);print(w,g2p(w),reading(s),[TONE[x['t']] for x in s])

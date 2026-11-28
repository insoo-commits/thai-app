"""Build the Thai PWA (THAI Lang) from the Lao app code (src/base = insoo-commits/lao-app v2.53) + content files content/c*.txt.
Usage: python3 build.py <out_dir> [version]
Content DSL (one sub per file, ' | ' separates fields):
  # P5-K | 기초 회화                      sub id | name
  @ 1-01-01 | 첫인사 | สวัสดี·ขอบคุณ | intro   bundle id | Korean title | Thai label | intro
  w thai | hint | meaning [| reading]     word (hint '=' = meaning); reading is automatic unless given
  e thai | ko                              example of the last word (2nd example = male voice)
  tp text / nx text / qz q | a
  pr thai | ko || thai | ko                pair sentences
  dl who | thai | ko                       dialog (even lines female, odd lines male)
  sm thai | ko                             one-line summary sentence
  x thai | meaning [| reading]             note-dictionary word
  rd thai | reading                        global reading override
"""
import json,sys,os,glob,base64,re,shutil,datetime
here=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,here)
import thrd
out=sys.argv[1] if len(sys.argv)>1 else None; VER=sys.argv[2] if len(sys.argv)>2 else "0.1"
DATE=datetime.date.today().isoformat()
TH=re.compile('[ก-๛]')
subs=[];B={};BLAB={};X={};RDO={};SUBNAME={};NODICT=set();SAYO={}
def P_(rest): return [x.strip() for x in rest.split(' | ')]
for f in sorted(glob.glob(here+'/content/c*.txt')):
    cur=None;sid=None
    for n,line in enumerate(open(f,encoding='utf-8'),1):
        line=line.rstrip('\n').strip()
        if not line or line.startswith('//'): continue
        tag,_,rest=line.partition(' ');P=P_(rest)
        try:
            if tag=='#':
                sid=P[0];SUBNAME[sid]=P[1]
                if not any(s["id"]==sid for s in subs): subs.append({"id":sid,"name":P[1].replace(' ',''),"b":[]})
            elif tag=='@':
                assert len(P)==4,P
                cur={"t":P[1],"h":"","i":P[3],"w":[],"tp":[],"nx":[],"pr":[],"dl":[],"sm":["","",""],"qz":[]}
                assert P[0] not in B,('dup bundle',P[0]);B[P[0]]=cur;BLAB[P[0]]=[P[1],P[2]]
                [s for s in subs if s["id"]==sid][0]["b"].append(P[0])
            elif tag=='w':
                assert len(P) in (3,4),P
                cur["w"].append([P[0],P[2] if P[1]=='=' else P[1],P[3] if len(P)==4 else None,P[2],[]])
            elif tag=='e': assert len(P)==2,P;cur["w"][-1][4].append([P[0],None,P[1]])
            elif tag=='tp': cur["tp"].append('• '+rest.strip())
            elif tag=='nx': cur["nx"].append(rest.strip())
            elif tag=='pr':
                a,b2=[[y.strip() for y in x.split(' | ')] for x in rest.split(' || ')];assert len(a)==2 and len(b2)==2,(a,b2)
                cur["pr"].append([[a[0],None,a[1]],[b2[0],None,b2[1]]])
            elif tag=='dl': assert len(P)==3,P;cur["dl"].append([P[0],P[1],None,P[2]])
            elif tag=='sm': assert len(P)==2,P;cur["sm"]=[P[0],None,P[1]]
            elif tag=='qz': assert len(P)==2,P;cur["qz"].append(P)
            elif tag=='x': assert len(P) in (2,3),P;X[P[0]]=P[1];(len(P)==3 and RDO.__setitem__(P[0],P[2]))
            elif tag=='rd': assert len(P)==2,P;RDO[P[0]]=P[1]
            elif tag=='sy': assert len(P)==2,P;SAYO[P[0]]=P[1]
            elif tag=='nd': NODICT.update(rest.split())
            else: raise ValueError('tag '+tag)
        except Exception as ex: raise SystemExit(f'{f}:{n}: {line} ({ex!r})')
for s in subs: s["b"].sort()
for k,b in B.items():
    b["h"]=" · ".join(w[0] for w in b["w"])
    for w in b["w"]: assert len(w[4])>=2,(k,w[0],'needs 2+ examples')
    for w in b["w"]:
        if w[2]: RDO.setdefault(w[0],w[2])
# 글자(P6): a letter card 'ก ไก่' is spoken by its name 'กอ ไก่'
for k,b in B.items():
    if not k.startswith('6-'): continue
    for w in b["w"]:
        m=re.fullmatch(r'([ก-ฮ]) (\S+)',w[0])
        if m: SAYO.setdefault(w[0],m.group(1)+'อ '+m.group(2))
# ---------- '원래 x-xx-xx' references (GPT review 2026-11-19): point each copy at a bundle that really holds the word, else drop it
def _hw(x): return re.sub(r'\s*\([^)]*\)\s*$','',x).replace('…','').strip()
_ORIG={}
for bid,b in B.items():
    for w in b["w"]:
        if '원래' not in w[1]: _ORIG.setdefault(_hw(w[0]),[]).append(bid)
REFFIX=[]
for bid,b in B.items():
    for w in b["w"]:
        m=re.search(r'\s*·?\s*원래 (\d-\d{2}-\d{2})',w[1])
        if not m: continue
        ref=m.group(1);hw=_hw(w[0])
        if ref in B and ref!=bid and any(_hw(x[0])==hw for x in B[ref]["w"]): continue
        cand=[c for c in _ORIG.get(hw,[]) if c!=bid]
        if cand: w[1]=w[1][:m.start()]+(' · ' if m.group(0).lstrip().startswith('·') else ' ')+'원래 '+cand[0]+w[1][m.end():];REFFIX.append((bid,hw,ref,cand[0]))
        else: w[1]=(w[1][:m.start()]+w[1][m.end():]).strip(' ·');REFFIX.append((bid,hw,ref,None))
    for i,x in enumerate(b["nx"]):
        for r in re.findall(r'\d-\d{2}-\d{2}',x):
            if r not in B: REFFIX.append((bid,'nx',r,'MISSING'))
# ---------- readings
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_words
from pythainlp.util import Trie, num_to_thaiword
HW=set()
for b in B.values():
    for w in b["w"]:
        k=w[0].replace('…','').replace('~','').strip()
        if k and ' ' not in k and TH.search(k): HW.add(k)
DICTW=(set(thai_words())-NODICT)|HW|set(X)|set(RDO)
TRIE=Trie(DICTW)
BADRD=[];SPLITRD=[]
CUR=HW|set(X)|set(RDO)
def _tok0(t): return word_tokenize(t,custom_dict=TRIE,engine='newmm',keep_whitespace=True)
def tok(t):
    """newmm, then re-cut each Thai run by dictionary DP: newmm's TCC rule glues a consonant to a following ละ/ว
    (ชามละ → ชา+มละ, แล้วจะ → แล้+วจะ, เมตรละ → เม+ตรละ). Fewest unknown letters first, then fewest pieces."""
    out=[];run=[]
    def flush():
        if not run: return
        if len(run)==1: out.append(run[0]);run.clear();return
        s=''.join(run);n=len(s);spans={}
        p=0
        for r in run: spans.setdefault(p,[]).append(p+len(r));p+=len(r)
        INF=(10**9,0,0);best=[INF]*(n+1);back=[None]*(n+1);best[n]=(0,0,0)
        for i in range(n-1,-1,-1):
            for j in range(i+1,min(n,i+30)+1):
                if best[j]==INF: continue
                w=s[i:j];known=w in DICTW
                if not known and j not in spans.get(i,[]): continue
                c=(best[j][0]+(0 if known else len(w)),best[j][1]+1,best[j][2]+(0 if w in CUR else 1))
                if c<best[i]: best[i]=c;back[i]=j
        i=0
        while i<n: j=back[i];out.append(s[i:j]);i=j
        run.clear()
    for x in _tok0(t):
        if TH.search(x) and not x.isspace() and re.fullmatch('[\u0E01-\u0E4E]+',x): run.append(x)
        else: flush();out.append(x)
    flush();return out
if os.environ.get('TOKTEST'):
    for b in B.values():
        for w in b['w']:
            for e in w[4]:
                T=tok(e[0])
                for q in os.environ['TOKTEST'].split(','):
                    if q in T: print(q,'|',e[0],'|',' '.join(T))
    sys.exit()
def rdw(t):
    if t in RDO: return RDO[t]
    if re.fullmatch(r'[\d,]+',t):
        try: return rdw_th(num_to_thaiword(int(t.replace(',',''))))
        except Exception: return t
    return rdw_th(t)
def rdw_th(t):
    if t in RDO: return RDO[t]
    try: return thrd.reading(thrd.word(t),not decomposable(t))
    except Exception as e:
        ps=pieces(t)
        if len(ps)>1:
            SPLITRD.append(t);return ''.join(rdw_th(p) for p in ps)
        BADRD.append(t);return '?'
TOKS={}
_TW=set(thai_words())-NODICT
import functools
@functools.lru_cache(None)
def _W(): return _TW|HW|set(X)
@functools.lru_cache(None)
def pieces(t):
    """split a word into 2+ dictionary words, fewest pieces (สิบเอ็ด = สิบ + เอ็ด); [t] if impossible"""
    W=_W();n=len(t);best=[None]*(n+1);best[n]=[]
    for i in range(n-1,-1,-1):
        for j in range(i+1,n+1):
            if (i==0 and j==n) or best[j] is None or t[i:j] not in W: continue
            c=[t[i:j]]+best[j]
            if best[i] is None or len(c)<len(best[i]): best[i]=c
    return tuple(best[0]) if best[0] else (t,)
@functools.lru_cache(None)
def decomposable(t):
    """a phrase made of dictionary words (ใช่แล้ว = ใช่ + แล้ว): no ㄹ받침 across its pieces"""
    W=_W();n=len(t);ok=[False]*(n+1);ok[n]=True
    for i in range(n-1,-1,-1):
        ok[i]=any(ok[j] and t[i:j] in W for j in range(i+1,n+1) if not (i==0 and j==n))
    return ok[0]
def rd(t):
    t=t.replace('…',' … ')
    outp=[];prev=None
    for tk in tok(t):
        if tk.isspace(): continue
        if tk=='ๆ':
            # repeat the shortest known word right before ๆ (ฝนตกปรอยๆ → …쁘러이쁘러이), not the whole token
            if outp:
                last=prev if prev else ''
                ps=pieces(last) if last else ()
                outp[-1]=outp[-1]+(rdw(ps[-1]) if len(ps)>1 else outp[-1].split(' ')[-1])
            continue
        prev=tk if TH.search(tk) else None
        if TH.search(tk) or re.fullmatch(r'[\d,]+',tk):
            if TH.search(tk): TOKS[tk]=TOKS.get(tk,0)+1
            outp.append(rdw(tk))
        else:
            s=tk.strip()
            if s in ('?','!','.',',','…'):
                if outp: outp[-1]+=s
            elif s: outp.append(s)
    r=' '.join(outp)
    return re.sub(r'\s+',' ',r).strip()
def rdhead(t):
    t=re.sub(r'\s*\([^)]*[\uac00-\ud7a3][^)]*\)','',t)
    if t in RDO: return RDO[t]
    k=t.replace('…','').strip()
    if k in RDO: return RDO[k]+('…' if t.endswith('…') else '')
    return rd(t)
for b in B.values():
    for w in b["w"]:
        w[2]=rdhead(w[0])
        for e in w[4]: e[1]=rd(e[0])
    for pr in b["pr"]:
        for x in pr: x[1]=rd(x[0])
    for x in b["dl"]: x[2]=rd(x[1])
    if b["sm"][0]: b["sm"][1]=rd(b["sm"][0])
# ---------- 말소리(P1, ids 5-): spelling hint § = consonant class + tone mark; tip line '소리 높이' from the g2p tone
HIC=set('ขฃฉฐถผฝศษสห');MIC=set('กจฎฏดตบปอ');SONO=set('งญนมยรลว');STOP=set('กขคฆดตถทธจชซศษสฎฏฐฑฒบปพฟภ')
MKN={'\u0e48':'◌่','\u0e49':'◌้','\u0e4a':'◌๊','\u0e4b':'◌๋'}
TNAME={0:'평성(가운데에서 평평)',1:'1성(낮게)',2:'2성(높았다가 떨어짐)',3:'3성(높게)',4:'4성(낮게 내려갔다 올라감)'}
def p1hint(w):
    w=re.sub(r'\s*\([^)]*\)','',w)
    cs=[i for i,ch in enumerate(w) if 'ก'<=ch<='ฮ']
    i=cs[0];c=w[i]
    if c=='ห' and i+1<len(w) and w[i+1] in SONO: cls,desc='높은','ห + '+w[i+1]+' (높은 자음처럼)'
    elif c=='อ' and i+1<len(w) and w[i+1]=='ย': cls,desc='가운데','อ + ย (가운데 자음처럼)'
    else:
        cls='높은' if c in HIC else '가운데' if c in MIC else '낮은';desc=c
        if cls!='낮은' or True:
            pass
    mk=[MKN[ch] for ch in w if ch in MKN]
    out=f"{cls} 자음 {desc}" if not desc.startswith('ห + ') and not desc.startswith('อ + ') else desc
    out+=' + '+mk[0] if mk else ', 부호 없음'
    if not mk:
        body=w.rstrip('์')
        fin=[ch for ch in body[i+1:] if 'ก'<=ch<='ฮ']
        if body.endswith('ะ') or w.endswith('็'): out+=' · 짧은 모음'
        elif fin and fin[-1] in STOP and not (len(fin)==1 and fin[0] in 'อ'): out+=' · 받침 '+{'ก':'ก','ข':'ก','ค':'ก','ฆ':'ก','บ':'บ','ป':'บ','พ':'บ','ฟ':'บ','ภ':'บ'}.get(fin[-1],'ด')
    return out
for k,b in B.items():
    if not k.startswith(('5-','6-10-')): continue
    parts=[]
    for w in b["w"]:
        if '§' in w[1]: w[1]=w[1].replace('§',p1hint(w[0]))
        hw=re.sub(r'\s*\([^)]*\)','',w[0])
        try: ts=[x['t'] for x in thrd.word(hw)]
        except Exception: ts=[]
        if len(ts)==1: parts.append(f"{hw} {TNAME[ts[0]]}")
    if parts and not any(t.startswith('• 소리 높이') for t in b["tp"]):
        b["tp"].insert(1 if b["tp"] else 0,'• 소리 높이: '+' / '.join(parts))
# front text: Thai phrase in intro/tips gets its reading in parentheses (as in the Khmer app)
def addrd(t):
    def f(m):
        run,par=m.group(1),m.group(3)
        if not re.search('[ก-ฮ]',run): return m.group(0)   # a bare tone mark ◌่ has no reading
        if ' ' in run and all(len(x)==1 for x in run.split()): return m.group(0)   # a list of letters (ก จ ฎ ฏ …)
        if (m.start()>0 and m.string[m.start()-1]=='◌') or m.string[m.end(1):m.end(1)+1]=='◌': return m.group(0)   # a vowel pattern (◌อ, เ◌ือ) is not a word
        r=rd(run)
        if par is not None:
            sq=lambda x:re.sub(r'[\s,?·]','',x)
            if sq(par).startswith(sq(r)): return m.group(0)
            return f'{run}({r} · {par})'
        return f'{run}({r})'
    return re.sub(r'([ก-๛…~]+(?: [ก-๛…~]+)*)(\(([^()]*)\))?',f,t)
for b in B.values():
    b["i"]=addrd(b["i"]);b["tp"]=[addrd(t) for t in b["tp"]];b["qz"]=[[q,addrd(a)] for q,a in b["qz"]]
PMETA=[("P5","기초회화","학교·식당·시장·병원 등 장면별 단어와 문장"),("P6","문자학습","태국 글자: 자음 44자, 모음, 받침, 성조 부호와 성조 규칙"),("P7","문장규칙","어순·부정·의문·시제·분류사·끝말 등 문장을 만드는 기초 문법"),("P4","짝말비교","반대말·분류사·높임말 짝"),("P3","비슷한말","뜻은 비슷하지만 쓰임이 다른 말"),("P2","단어가족","뿌리가 같은 말. 앞뒤에 붙는 말로 뜻이 넓어지는 단어 가족"),("P1","발음구별","한글로 쓰면 같거나 비슷해서 헷갈리는 소리. 성조, 짧은·긴 모음, 된소리·거센소리, 받침")]
DATA={"P":[{"id":p,"ko":k,"desc":d,"subs":[x for x in subs if x["id"].startswith(p+'-')]} for p,k,d in PMETA],"B":B}
DATA["P"]=[p for p in DATA["P"] if p["subs"]]
# ---------- note dictionary
ND={};NR={}
for b in B.values():
    for w in b["w"]:
        k=w[0].replace("…","").replace("?","").strip()
        if " " in k or not TH.search(k): continue
        ND.setdefault(k,re.split(r"[;(]",w[3])[0].strip());NR.setdefault(k,w[2])
for k,mn in X.items(): ND[k]=mn;NR[k]=rdw(k)
alltxt=" ".join(e[0] for b in B.values() for w in b["w"] for e in w[4])
NF={k:alltxt.count(k) for k in ND}
# tokens in sentences with no meaning in the note dictionary
NOMEAN=sorted([t for t in TOKS if t not in ND and len(t)>=2],key=lambda t:-TOKS[t])
# ---------- tones: syllables of every dictionary word / headword
def sylinfo(w,top=True):
    r=sylinfo1(w)
    if r is None and top:
        ps=pieces(w)
        if len(ps)>1:
            r=[];pos=0
            for p in ps:
                q=sylinfo(p,False)
                if q is None: return None
                r+=[[a+pos,b,c,d,t] for a,b,c,d,t in q];pos+=len(p)
    return r
def sylinfo1(w):
    """orthographic anchor of each phonological syllable: [i, n, ci, cl, tone]"""
    try:
        seg=thrd.g2p(w);thrd.word(w)
    except Exception: return None
    groups=[g for g in re.split(r'[~|]',seg) if g]
    orth=[g for g in thrd.syl(w).split('~') if g and g!='<s/>']
    if ''.join(orth)!=w or len(orth)!=len(groups): return None
    res=[];pos=0
    for og,pg in zip(orth,groups):
        ph=[thrd.parse(s) for s in pg.split("'") if s]
        cons=[k for k,ch in enumerate(og) if 'ก'<=ch<='ฮ']
        if not cons: return None
        lead=0
        # first anchor = first consonant; ห/อ leading a sonorant counts as one cluster
        anchors=[]
        start=cons[0]
        cl=2 if og[start] in 'หอ' and start+1<len(og) and og[start+1] in 'งญนมยรลว' and len(ph)>=1 and ph[0]['on'] not in ('h','?') else 1
        anchors.append((start,cl))
        prev=start+cl-1
        for p in ph[1:]:
            nxt=[k for k in cons if k>prev]
            # doubled consonant (ราช|ชะ): the final of the previous syllable may start the next one
            if p['on'] and nxt: k=nxt[0]
            elif nxt: k=nxt[0]
            else: k=cons[-1]
            anchors.append((k,1));prev=k
        for j,(p,(a,c)) in enumerate(zip(ph,anchors)):
            e=anchors[j+1][0] if j+1<len(anchors) else len(og)
            if j==0: s0=0
            else: s0=a
            res.append([pos+s0,e-s0,a-s0,c,p['t']])
        pos+=len(og)
    return res
TNW={}
for k in set(ND)|HW:
    if TH.search(k) and not re.search(r'[\s…~]',k):
        si=sylinfo(k)
        if si: TNW[k]=[[a,b,c,d,t+1] for a,b,c,d,t in si]
J=lambda o:json.dumps(o,ensure_ascii=False,separators=(",",":"))
# ---------- lint: polite particles must match the voice
def gender_lint():
    bad=[]
    FEM=re.compile('ครับ|(?<![ก-ฮ])ผม(?!ห)');MAL=re.compile('ค่ะ|คะ|ดิฉัน|(?<!ฉั)ฉัน')
    for k,b in B.items():
        for w in b["w"]:
            for i,e in enumerate(w[4]):
                if i==1 and MAL.search(e[0]): bad.append((k,'male ex',e[0]))
                if i!=1 and FEM.search(e[0]): bad.append((k,'female ex',e[0]))
        for i,x in enumerate(b["dl"]):
            if i%2 and MAL.search(x[1]): bad.append((k,'male dl',x[1]))
            if not i%2 and FEM.search(x[1]): bad.append((k,'female dl',x[1]))
        for pr in b["pr"]:
            for x in pr:
                if FEM.search(x[0]): bad.append((k,'female pr',x[0]))
        if b["sm"][0] and FEM.search(b["sm"][0]): bad.append((k,'female sm',b["sm"][0]))
    return bad
# ---------- voices: position decides (2nd example, odd dialog lines = male) unless the words say it (ครับ/ผม male, ค่ะ/คะ/ฉัน female)
def gender(t):
    """particles decide (ครับ male; ค่ะ คะ จ้ะ female), else pronouns (ผม male; ฉัน ดิฉัน หนู female); token-based so คะแนน/ผมร่วง don't count"""
    T=set(tok(t))
    m,f='ครับ' in T or 'นะครับ' in T,bool(T&{'ค่ะ','คะ','นะคะ','จ้ะ','จ้า','จ๊ะ'})
    if m!=f: return 'm' if m else 'f'
    if m and f: return None
    m,f='ผม' in T,bool(T&{'ฉัน','ดิฉัน'})
    return 'm' if m and not f else 'f' if f and not m else None
def akey(t):
    t=re.sub(r'\s+',' ',t).strip();h=0x811c9dc5
    for ch in t.encode('utf-16-le').decode('utf-16-le'):
        for cu in ([ord(ch)] if ord(ch)<0x10000 else [0xD800+((ord(ch)-0x10000)>>10),0xDC00+((ord(ch)-0x10000)&0x3FF)]):
            h^=cu;h=(h*0x01000193)&0xFFFFFFFF
    d='0123456789abcdefghijklmnopqrstuvwxyz';o=''
    while True:
        o=d[h%36]+o;h//=36
        if not h: break
    return o
def kosay(t):
    t=re.sub('[\u2460-\u2473]','',t);t=re.sub(r'\s*\([^)]*\)','',t);t=re.sub('[;·]',',',t);t=re.sub(r'\s+',' ',t).strip()
    return t.replace('—',',')
LF={};LM={};LK={};MV=set();FV=set()
def say(t):
    if t in SAYO: return SAYO[t]
    t=re.sub(r'\s*\([^)]*[\uac00-\ud7a3][^)]*\)','',t)  # 'ตัว (동물)' -> TTS reads only the Thai
    t=re.sub(r'[\uac00-\ud7a3]+','',t).replace('+',' ')  # 'กี่ + 분류사' -> 'กี่'
    return re.sub(r'\s+',' ',t.replace('…',' ').replace('—',' ')).strip()
def clip(t,pos_m):
    if not t: return
    g=gender(t)
    if g=='m': MV.add(t)
    if g=='f': FV.add(t)
    male=(g=='m') or (g is None and pos_m)
    (LM.__setitem__('m_'+akey(t),say(t)) if male else LF.__setitem__(akey(t),say(t)))
def kclip(t):
    if t: LK['k_'+akey(t)]=kosay(t)
for b in B.values():
    for w in b["w"]:
        clip(w[0],False);kclip(w[3])
        for i,e in enumerate(w[4]): clip(e[0],i==1);kclip(e[2])
    for pr in b["pr"]:
        for x in pr: clip(x[0],False);kclip(x[2])
    for i,x in enumerate(b["dl"]): clip(x[1],i%2==1);kclip(x[3])
    if b["sm"][0]: clip(b["sm"][0],False);kclip(b["sm"][2])
if __name__=='__main__' and out is None:
    print(len(B),'bundles'); sys.exit()
os.makedirs(out+'/audio',exist_ok=True)
GLINT=[]
for k,bb in B.items():
    sp={}
    for i,x in enumerate(bb["dl"]):
        g=gender(x[1]);v=g if g else ('m' if i%2 else 'f')
        sp.setdefault(x[0],set()).add(v)
    for s,v in sp.items():
        if len(v)>1: GLINT.append((k,'speaker '+s+' has both voices'))
    for t in [e[0] for w in bb["w"] for e in w[4]]+[x[1] for x in bb["dl"]]:
        T=set(tok(t))
        if ('ครับ' in T) and (T&{'ค่ะ','คะ','นะคะ'}): GLINT.append((k,t))
json.dump({"badrd":sorted(set(BADRD)),"splitrd":sorted(set(SPLITRD)),"reffix":REFFIX,"nomean":NOMEAN,"nomean_unc":[[t,TOKS[t]] for t in NOMEAN if not (len(pieces(t))>1 and all(p in ND for p in pieces(t)))],"gender":GLINT,"notone":sorted(k for k in set(ND)|HW if k not in TNW and TH.search(k))},open(out+'/../lint.json','w'),ensure_ascii=False,indent=0)
# ---------- app.js from the Lao base
L=open(here+'/base/app.js',encoding='utf-8').read().split('\n')
def find(prefix,start=0):
    for i in range(start,len(L)):
        if L[i].startswith(prefix): return i
    raise SystemExit('marker not found: '+prefix)
code=list(L)
def setline(prefix,new):
    i=find(prefix);code[i]=new
# bundle ids follow the tab order (sub code = tab position in the app): content files keep their own numbers
# 1 주제별, 6 글자 → 2, 7 문법 → 3, 2 짝말 → 4, 3 닮은말 → 5, 4 말뿌리 → 6, 5 말소리 → 7
IDP={'1':'1','6':'2','7':'3','2':'4','3':'5','4':'6','5':'7'}
_IDRE=re.compile(r'(?<![\d\-])([1-7])-(\d{2})(-\d{2})?(?![\d\-])')
def _rid(x):
    if isinstance(x,str): return _IDRE.sub(lambda m:IDP[m.group(1)]+'-'+m.group(2)+(m.group(3) or ''),x)
    if isinstance(x,list): return [_rid(y) for y in x]
    if isinstance(x,dict): return {_rid(k):_rid(v) for k,v in x.items()}
    return x
DATA=_rid(DATA);BLAB=_rid(BLAB)
DATA["B"]=dict(sorted(DATA["B"].items()))
# ---------- 태국 탭 (P8): info pages like the Lao app's 라오스 tab (v2.63/2.64). No words, audio, quiz or totals.
def _info():
    import importlib.util
    sp=importlib.util.spec_from_file_location('thai_info',here+'/info/thai_info.py');ti=importlib.util.module_from_spec(sp);sp.loader.exec_module(ti)
    exec(open(here+'/info/thai_more.py',encoding='utf-8').read(),ti.__dict__)
    assert set(ti.M)<=set(ti.B) and len(ti.M)==len(ti.B),(set(ti.B)-set(ti.M))
    try: CR=json.load(open(here+'/info/credits.json',encoding='utf-8'))
    except Exception: CR={}
    used=[]
    def ph(m):
        k,cap=m.group(1),m.group(2);c=CR.get(k)
        if not c or not os.path.exists(here+'/info/img/'+k+'.jpg'): return ''
        used.append(k)
        return f'<figure class="ph"><img src="img/th/{k}.jpg" width="{c["w"]}" height="{c["h"]}" loading="lazy" alt=""><figcaption>{cap}<small>사진: {c["a"]} · {c["lic"]} · Wikimedia Commons</small></figcaption></figure>'
    IB={};IL={}
    for bid,(t,th,html) in ti.B.items():
        if bid in ti.M:  # v1.18 RYU: 더 알아보기 + 이럴 때 이렇게 말해요 (info/thai_more.py)
            cs,ps=ti.M[bid]
            html+='<h3 class="more">더 알아보기</h3><div class="cards">'+''.join(f'<div class="card"><h4>{h}</h4>{c}</div>' for h,c in cs)+'</div>'
            html+='<div class="phr"><div class="ph-t">이럴 때 이렇게 말해요</div>'+''.join(f'<div><span class="lo">{x}</span> <span class="r">{r}</span><span class="m">{m}</span></div>' for x,r,m in ps)+'</div>'
        html=re.sub(r'@@PHOTO:([a-z0-9]+):(.*?)@@',ph,html)
        html=re.sub(r'<span class="lo">([^<]*)</span> <span class="r">@RD@</span>',lambda m:f'<span class="lo">{m.group(1)}</span> <span class="r">{rdhead(m.group(1))}</span>',html)
        # "방콕 กรุงเทพฯ 끄룽텝": drop the reading when the Korean name just before says the same
        html=re.sub(r'((?:[가-힣]+ )?[가-힣]+) (<span class="lo">[^<]*</span>) <span class="r">([^<]*)</span>',lambda m:(m.group(1)+' '+m.group(2)) if m.group(1).replace(' ','')==m.group(3).replace(' ','') or m.group(1).split(' ')[-1]==m.group(3) else m.group(0),html)
        html=html.replace('<div class="top2"><div></div><div>','<div class="top1"><div>')
        IB[bid]=dict(t=t,h=th,i="",w=[],tp=[],nx=[],pr=[],dl=[],sm=None,qz=[],info=f'<h2>{t}</h2><div class="sub2 lo">{th}</div>'+html)
        IL[bid]=[t,th]
    subs=[dict(id=sid,name=nm,b=[k for k in ti.B if k.startswith('8-%02d-'%(n+1))]) for n,(sid,nm) in enumerate(ti.SUBS)]
    DATA["P"].append(dict(id='P8',ko='태국',desc='태국을 이해하기 위한 자료',subs=[x for x in subs if x['b']]))
    DATA["B"].update(IB);BLAB.update(IL)
    bad=[k for k,v in IB.items() if '?' in re.sub(r'<[^>]+>','',v['info']).replace('?)','').replace('까?','')]
    print('태국 탭:',len(IB),'pages,',len(used),'photos; pages with ? in a reading:',bad[:8])
    return used
INFO_IMG=_info()
exec(open(here+'/titles.py',encoding='utf-8').read())
for _pi,_p in enumerate(DATA["P"]):
    for _si,_x in enumerate(_p["subs"]):
        _c=f'{_pi+1}-{_si+1:02d}'
        if _c in SUBREN: _x["name"]=SUBREN.pop(_c)
for _k,_v in list(BUNREN.items()):
    _b=DATA["B"].get(_k)
    if not _b: continue
    if _b.get('info'): _b['info']=_b['info'].replace('<h2>'+_b['t']+'</h2>','<h2>'+_v+'</h2>',1)
    _b['t']=_v
    if _k in BLAB: BLAB[_k][0]=_v
    del BUNREN[_k]
assert not SUBREN and not BUNREN,(SUBREN,BUNREN)
exec(open(here+'/info/thai_help.py',encoding='utf-8').read())
code[0]="const DATA=JSON.parse("+json.dumps(J(DATA),ensure_ascii=False)+");"
i4=find('const NDICT=');code[i4]=f"const NDICT={J(ND)},NRD={J(NR)},NFREQ={J(NF)},NSTOP=new Set([]);"
for i in range(i4+1,find('function notesOf')):
    if code[i].startswith('Object.assign(NDICT') or code[i].startswith('/*') and 'Object.assign(NDICT' in code[i]: code[i]=''
# IDMAP blocks: a new app has nothing to migrate
a=find('let known=store.get(');b2=find('let S={')
for i in range(a,b2): code[i]=''
code[a]='let known=store.get("tha-known",{});const saved=store.get("tha-sel",{});'
code[find('const BLAB=')]="const BLAB="+J(BLAB)+";"
# tone block
a=find('const TN=(()=>');b2=find('return {seg:seg,tone:tone,MK:MK}})();')
code[a]=open(here+'/tn.js',encoding='utf-8').read().replace('__TNW__',J(TNW)).rstrip('\n')
for i in range(a+1,b2+1): code[i]=''
setline('const PARTEN=','const PARTEN={P1:"SOUND",P2:"ROOT",P3:"MEANING",P4:"PAIR",P5:"SCENE",P6:"LETTER",P7:"GRAMMAR",P8:"THAILAND",PH:"HELP"};')
setline('const TLEG=','const TLEG=[["t1","평성 가운데"],["t2","1성 낮게"],["t3","2성 떨어짐"],["t4","3성 높게"],["t5","4성 올라감"]];')
# sense rules
a=find('const HCL=');b2=find('const nmean0=')
code[a]=open(here+'/nsense.js',encoding='utf-8').read().rstrip('\n')
for i in range(a+1,b2+1): code[i]=''
a=find('const SWATCH=');code[a]=open(here+'/swatch.js',encoding='utf-8').read().rstrip('\n')
# last line: Lao clip refresh
a=find('(function(){var KEYS=');code[a]=''
s="\n".join(code)+"\n"
# RYU 2026-11-21 (Thai v1.6): Lao app v2.75-2.78 (key badges, key info line, K = Korean on/off, short pause between repeats, no review pass after word cards, flat header)
LH=json.load(open(here+'/lao_v278.json',encoding='utf-8'))
for _i,(_a,_b) in enumerate(LH['app.js']):
    if _i==8: continue
    _a=_a.replace('function stopPlay(){P.rel=0;P.token++;','function stopPlay(){P.token++;');_b=_b.replace('function stopPlay(){P.rel=0;P.token++;','function stopPlay(){P.token++;')
    assert s.count(_a)==1,('lao hunk',_i,s.count(_a));s=s.replace(_a,_b)
def rp(a,b,n=None):
    global s
    c=s.count(a)
    assert c>0 and (n is None or c==n),(a[:80],c)
    s=s.replace(a,b)
# notes: Thai letters, marks that cannot start a word, leading vowels that cannot end one
rp('const bad=/^[\\u0EB1\\u0EB4-\\u0EBC\\u0EC8-\\u0ECD]/;','const bad=/^[\\u0E30-\\u0E3A\\u0E45-\\u0E4E]/;',1)
rp('for(const run of lo.match(/[\\u0E80-\\u0EFF]+/g)||[])','for(const run of lo.match(/[\\u0E01-\\u0E4E]+/g)||[])',1)
rp('(b>0&&/[\\u0EC0-\\u0EC4]/.test(run[b-1]))','(b>0&&/[\\u0E40-\\u0E44]/.test(run[b-1]))',1)
rp('/* ທຸ່ມ (night hours) always gets a note, even on its own card */if(lo.includes("ທຸ່ມ")&&!out.includes("ທຸ່ມ")){out.unshift("ທຸ່ມ")}','',1)
rp('out.filter(t=>t!=="ທຸ່ມ")','out.slice()',1)
# RYU 2026-11-19 (Thai v1.1): word cards show the Korean reading under the Thai on the FRONT too
rp('</span><span class="hint">${hintHtml(hint)}</span></span><span class="bk"','</span><span class="rd frd">${esc(rd)}</span><span class="hint">${hintHtml(hint)}</span></span><span class="bk"',1)
# RYU 2026-11-19 (Thai v1.1): 이전·다음 묶음 keeps the current mode (단어공부 stays 단어공부); goto() alone switches to 예문보기
rp('if(t.dataset.next){if(P.active)stopPlay();goto(t.dataset.next);','if(t.dataset.next){if(P.active)stopPlay();{const m=S.mode;goto(t.dataset.next);if(m!=="dlg"){S.mode=m;S.flipped={};save();render()}}',1)
rp('const m=/[\\u0E80-\\u0EFF]+/g;','const m=/[\\u0E01-\\u0E4E]+/g;',1)
rp('if(/[\\u0EB0-\\u0EBC\\u0EC8-\\u0ECD]/.test(nx)||/[\\u0EC0-\\u0EC4]/.test(pv))return true;','if(/[\\u0E30-\\u0E3A\\u0E45-\\u0E4E]/.test(nx)||/[\\u0E40-\\u0E44]/.test(pv))return true;',1)
rp('!/[\\u0EB0-\\u0EBC\\u0EC8-\\u0ECD]/.test(e[i+L]||"")','!/[\\u0E30-\\u0E3A\\u0E45-\\u0E4E]/.test(e[i+L]||"")',1)
rp("/([຀-໿][຀-໿\\s◌]*)/g","/([\\u0E01-\\u0E5B][\\u0E01-\\u0E5B\\s◌…~]*)/g",1)
# ๆ: the Thai voice reads it itself, so the text goes to the voice as written
a=s.index('function rep(t){');b2=s.index('function utterOf')
s=s[:a]+'function rep(t){return t}\n'+s[b2:]
rp('/^lo([-_]|$)/i','/^th([-_]|$)/i',1); rp('"lo-LA"','"th-TH"'); rp('Intl.Segmenter("lo"','Intl.Segmenter("th"',1)
rp('(id==="2-04-10"||id==="2-04-11")&&SWATCH[lo]','SWATCH[lo]',1)
rp('라오스어','태국어'); rp('LAO Lang','THAI Lang'); rp('lao-','tha-')
left=[l[:80] for l in s.split('\n')[1:] if re.search('[຀-໿]',l)]
print('code lines still holding Lao letters:',len(left));[print('  ',x) for x in left[:12]]
# 태국 탭 (P8): info pages have no words; skip them in 연속 재생, totals and the sub line; render them as an article
rp('const L=PARTS.flatMap(p=>p.subs.flatMap(x=>x.b)),cur=','const L=PARTS.flatMap(p=>p.subs.flatMap(x=>x.b)).filter(x=>!B[x].info),cur=',1)
rp('const all=Object.values(B),nw=','const all=Object.values(B).filter(b=>!b.info),nw=',1)
rp('${cs.b.length}묶음 ${nwd.toLocaleString()}단어 ${nsb.toLocaleString()}문장`}','${cs.b.length}묶음`+(B[cs.b[0]].info?"":` ${nwd.toLocaleString()}단어 ${nsb.toLocaleString()}문장`)}',1)
rp('if(S.q.trim()){renderSearch();return}','if(S.q.trim()){renderSearch();return}\n  /* 태국 탭: info page, no controls */{const ib=B[curBun()];if(ib&&ib.info){$("#controls").hidden=true;renderBand();$("#view").innerHTML=`<article class="info">${ib.info}</article>`+nextRow(curBun());snapLater();return}}',1)
# RYU 2026-11-20 (Thai v1.5): keyboard shortcuts from the Lao app v2.71-2.74 (src/kbd.js)
rp('function stopPlay(){P.token++;','function stopPlay(){P.rel=0;P.token++;',1)
rp('function advQ(){if(P.hold!=null){P.i=P.hold;P.k++;return}const it=P.queue[P.i];if(!it){P.i++;return}if(P.i<it.ge){P.i++;return}','function advQ(){if(P.hold!=null){P.i=P.hold;P.k++;return}const it=P.queue[P.i];if(!it){P.i++;return}/* Enter released the loop: go on to the next item */if(P.rel){P.rel=0;P.k=0;P.i=it.ge+1;return}if(P.i<it.ge){P.i++;return}',1)
_g='S.quiz=null;save();render();window.scrollTo({top:0})}\n'
assert s.count('function goto(id){')==1
_a=s.index('function goto(id){');_b=s.index(_g,_a)+len(_g)
s=s[:_b]+open(here+'/kbd.js',encoding='utf-8').read()+s[_b:]
_a,_b=LH['app.js'][8];assert s.count(_a)==1,'lao hunk 8';s=s.replace(_a,_b)
# RYU 2026-11-21 (Thai v1.9): Lao app v2.79-2.85 UI: follow scroll only outside the middle area, speed 0.7-2.0 by 0.1, tighter lists
rp('d=(r.top+r.height/2)-(innerHeight-ph)/2;if(Math.abs(d)>24)window.scrollBy({top:d,behavior:"smooth"})','H=innerHeight-ph,c=r.top+r.height/2,d=r.height>H*.5?r.top-H*.05:c-H*.25;/* v1.14 RYU: when it must move, put the item at ~25% from the top (play goes downward) *//* move only when the item leaves the middle area (25%..75%) or is cut off */if(c<H*.25||c>H*.75||(r.top<0&&r.height<H)||(r.bottom>H&&r.height<H))window.scrollBy({top:d,behavior:"smooth"})',1)
rp('let RATE=store.get("tha-rate",1);if(![0.8,1,1.2,1.5,2].includes(RATE))RATE=1;','let RATE=store.get("tha-rate",1);if(!(RATE>=0.7&&RATE<=2))RATE=1;RATE=Math.round(RATE*10)/10;',1)
rp("'.ddl button .ck{width:1em","/* tighter 횟수·배속 lists */'.ddl button:not(.ctr){padding:.22em 1em;line-height:1.25}'+'.ddl button .ck{width:1em",1)
# moved bundles (v1.9): 5-11-02 -> 4-06-08, 5-17-01 -> 3-06-03, word บาท 1-02-08 -> 1-10-05; learned marks follow
rp('let known=store.get("tha-known",{});const saved=store.get("tha-sel",{});','let known=store.get("tha-known",{});const saved=store.get("tha-sel",{});/* Thai v1.9: moved bundles keep their learned marks */{const IDM={"5-11-02":"4-06-08","5-17-01":"3-06-03"};if(store.get("tha-idv",0)<1){const k2={};for(const k in known){const m=/^(\\d-\\d{2}-\\d{2})::/.exec(k);let nk=m&&IDM[m[1]]?IDM[m[1]]+k.slice(m[1].length):k;if(nk==="1-02-08::บาท")nk="1-10-05::บาท";k2[nk]=known[k]}known=k2;store.set("tha-known",known);if(saved.bun)for(const k in saved.bun)if(IDM[saved.bun[k]])saved.bun[k]=IDM[saved.bun[k]];if(saved.sub==="P3-Z"){saved.sub="P7-F";saved.part="P7";if(saved.bun&&saved.bun["P3-Z"])saved.bun["P7-F"]=saved.bun["P3-Z"]}if(saved.lastSub&&saved.lastSub.P3==="P3-Z")delete saved.lastSub.P3;store.set("tha-sel",saved);store.set("tha-idv",1)}}',1)
# voice by the words: male-only texts use the male clip, female-only texts the female clip, wherever they stand
rp('function keyOf(it){if(!AUD||it.noAud)return null;let k=akey(it.text);if(it.ko)k="k_"+k;else if(it.m&&AUD["m_"+k])k="m_"+k;','const MVS=new Set('+J(sorted(MV))+'),FVS=new Set('+J(sorted(FV))+');\nfunction keyOf(it){if(!AUD||it.noAud)return null;let k=akey(it.text);if(it.ko)k="k_"+k;else if(!FVS.has(it.text)&&(it.m||MVS.has(it.text))&&AUD["m_"+k])k="m_"+k;',1)
_a='document.addEventListener("click",function(e){if(e.target.closest&&e.target.closest(".ddl,.ddbg"))return;';assert s.count(_a)==1,'dd click';s=s.replace(_a,_a+'if(!e.isTrusted)return;/* v1.20: only a real tap opens the bundle list (swipe calls .click() on 다음 묶음) */')
s+='\n'+open(here+'/swipe.js',encoding='utf-8').read()+'\n'  # v1.18 RYU: phone swipe = next/previous bundle (Lao v3.23)
open(out+'/app.js','w',encoding='utf-8').write(s)
os.makedirs(out+'/../lists',exist_ok=True)
for n,o in (('f',LF),('m',LM),('k',LK)): json.dump(o,open(out+f'/../lists/{n}.json','w'),ensure_ascii=False)
# ---------- index.html
h=open(here+'/base/index.html',encoding='utf-8').read()
font=base64.b64encode(open(here+'/base/th.woff2','rb').read()).decode()
h,n=re.subn(r'@font-face\{font-family:"Lao Local";.*?\}','@font-face{font-family:"Thai Local";src:url(data:font/woff2;base64,'+font+') format("woff2");font-weight:100 900;font-display:swap;unicode-range:U+0E01-0E5B,U+200C-200D,U+25CC}',h,count=1,flags=re.S);assert n==1
def hp(a,b):
    global h
    assert a in h,a
    h=h.replace(a,b)
hp('"Lao Local","Noto Sans Lao Looped","Phetsarath OT","Saysettha OT","Lao UI"','"Thai Local","Noto Sans Thai Looped","Thonburi","Leelawadee UI","Tahoma"')
hp('"Lao Local"','"Thai Local"')
hp('라오스어, 주제별로 공부하기','태국어, 주제별로 공부하기')
hp('ຮຽນ ພາສາລາວ','เรียนภาษาไทย')
hp('라오스어, 독음, 뜻으로 검색 (예: ໝາກ, 막, 과일)','태국어, 독음, 뜻으로 검색 (예: น้ำ, 남, 물)')
nw=sum(len(b["w"]) for b in B.values());ns=sum(sum(len(w[4]) for w in b["w"])+len(b["pr"])*2+len(b["dl"])+(1 if b["sm"][0] else 0) for b in B.values())
h,n=re.subn(r'<span><b>[\d,]+</b>묶음</span><span><b>[\d,]+</b>단어</span><span><b>[\d,]+</b>문장</span>',f'<span><b>{len(B)}</b>묶음</span><span><b>{nw:,}</b>단어</span><span><b>{ns:,}</b>문장</span>',h);assert n==1
h,n=re.subn(r'\d{4}-\d\d-\d\d v[\d.]+ · Claude',f'{DATE} v{VER} · Claude',h);assert n>=1,'ver'
h,n=re.subn(r'app\.js\?v=[\d.]+"',f'app.js?v={VER}"',h);assert n>=1
for _a,_b in LH['index.html'][:2]:
    assert h.count(_a)==1,'lao html hunk';h=h.replace(_a,_b)
hp('<span><kbd class="kc">Esc</kbd>재생 정지</span>','<span><kbd class="kc">Space</kbd>일시정지/재개</span><span><kbd class="kc">Esc</kbd>재생 정지</span>')
hp('<option value="0.8">x 0.8</option><option value="1">x 1.0</option><option value="1.2">x 1.2</option><option value="1.5">x 1.5</option><option value="2">x 2.0</option>',''.join(f'<option value="{v:g}">x {v:.1f}</option>' for v in [x/10 for x in range(7,21)]))
hp('  <nav class="groups" id="groups" aria-label="대분류"></nav>\n  <nav class="subs" id="subs" role="tablist" aria-label="소분류"></nav>\n  <div class="sinfo" id="sinfo"></div>\n','  <div class="menubox">\n  <nav class="groups" id="groups" aria-label="대분류"></nav>\n  <nav class="subs" id="subs" role="tablist" aria-label="소분류"></nav>\n  <div class="sinfo" id="sinfo"></div>\n  </div>\n')
h=h.replace('LAO Lang','THAI Lang').replace('lao-','tha-').replace('라오스어','태국어')
h=h.replace('</head>','<style>'+open(here+'/extra.css',encoding='utf-8').read()+'</style></head>',1)
assert not re.search('[຀-໿]',h),"Lao text left in html: "+re.search('.{40}[຀-໿].{40}',h).group()
open(out+'/index.html','w',encoding='utf-8').write(h)
sw=open(here+'/base/sw.js').read();_a,_b=LH['sw.js'][1];assert sw.count(_a)==1,'lao sw hunk';sw=sw.replace(_a,_b);sw=re.sub(r'lao-shell-v[\d.]+',f'tha-shell-v{VER}',sw).replace('lao-','tha-');open(out+'/sw.js','w').write(sw)
mf=json.load(open(here+'/base/manifest.webmanifest'));mf["name"]=mf["short_name"]="THAI Lang";json.dump(mf,open(out+'/manifest.webmanifest','w'),ensure_ascii=False)
for f in ('header.svg','header-day.svg','icon-180.png','icon-192.png','icon-512.png'):
    src=here+'/art/'+f if os.path.exists(here+'/art/'+f) else here+'/base/'+f
    if os.path.exists(src): shutil.copyfile(src,out+'/'+f)
for f in ('_gap150.mp3','_gap450.mp3','_gap900.mp3'): shutil.copyfile(here+'/base/'+f,out+'/audio/'+f)
if INFO_IMG:
    os.makedirs(out+'/img/th',exist_ok=True)
    for k in INFO_IMG: shutil.copyfile(here+'/info/img/'+k+'.jpg',out+'/img/th/'+k+'.jpg')
open(out+'/.nojekyll','w').write('')
print('built',len(B),'bundles',nw,'words',ns,'sentences; tokens without note meaning:',len(NOMEAN),'; reading failures:',len(set(BADRD)),'; male',len(LM),'female',len(LF),'korean',len(LK))

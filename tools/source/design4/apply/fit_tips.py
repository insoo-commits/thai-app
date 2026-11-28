# RYU 2026-11-24: at most 3 tips (●) per bundle description next to the 소분류 picture ("동그라미가 최대 3개"). Removed tips stay in fit_removed.json, so they can be put back.
#
# Usage: python3 fit_tips.py <app.js> <fit_removed.json>
import json, re, sys
p, rp = sys.argv[1], sys.argv[2]
s = open(p, encoding="utf8").read()
m = re.search(r'const DATA=JSON\.parse\((".*?(?<!\\)")\)', s)
d = json.loads(json.loads(m.group(1)))
R = json.load(open(rp, encoding="utf8")); n = 0
for k, gone in R.items():
    b = d["B"].get(k)
    if not b: continue
    tp = [t for t in b["tp"] if t not in gone]
    if len(tp) < len(b["tp"]): n += len(b["tp"]) - len(tp); b["tp"] = tp
lit = json.dumps(json.dumps(d, ensure_ascii=False, separators=(",", ":")), ensure_ascii=False)
s = s[:m.start(1)] + lit + s[m.end(1):]
open(p, "w", encoding="utf8").write(s)
print("tips removed", n)

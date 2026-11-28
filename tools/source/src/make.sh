#!/bin/bash
# Full build: bash make.sh [version]. Needs pythainlp, edge-tts, ffmpeg. Audio is kept in ../audio_all.tar (16 kbps; RYU 2026-11-26: one tar instead of ~20,000 loose files, see /mnt/project-files/tools/mp3tar.py), only clips in use go to ../pwa/audio.
set -e; H=$(cd "$(dirname "$0")"; pwd); V=${1:-0.1}; OUT=${OUT:-$H/../pwa}; W=$(mktemp -d)
python3 $H/build.py $W/out $V
A=$(python3 /mnt/project-files/tools/mp3tar.py path $H/../audio_all.tar)   # unpacked to local disk
(cd $W && python3 $H/tts_gen.py lists/f.json $A th-TH-PremwadeeNeural && python3 $H/tts_gen.py lists/m.json $A th-TH-NiwatNeural && python3 $H/tts_gen.py lists/k.json $A ko-KR-SunHiNeural) | grep -v '^todo 0' || true
python3 /mnt/project-files/tools/mp3tar.py save $A $H/../audio_all.tar   # new clips go back into the tar
python3 - $W $H $A <<'P'
import json,sys,os,shutil
W,H,A=sys.argv[1:4];ks=[];AV=json.load(open(f'{H}/aver.json'))
for n in 'fmk': ks+=list(json.load(open(f'{W}/lists/{n}.json')))
miss=[k for k in ks if not os.path.exists(f'{A}/{k}.mp3')];assert not miss,miss[:20]
os.makedirs(f'{W}/out/audio',exist_ok=True)
for k in ks: shutil.copyfile(f'{A}/{k}.mp3',f'{W}/out/audio/{k}.mp3')
open(f'{W}/out/audio/index.js','w').write('window.AUDIO_INDEX='+json.dumps({k:AV.get(k,1) for k in sorted(ks)},separators=(',',':'))+';')
print('audio clips',len(ks))
P
rm -rf $OUT; mkdir -p $OUT; cp -r $W/out/. $OUT/; rm -rf $W

# RYU 2026-11-24: new design (Lao v3.30-v3.34 look) + sub pictures, then fit tips to the picture height
python3 /mnt/project-files/design4/apply/apply.py thai-app --out $OUT
python3 /mnt/project-files/design4/apply/fit_tips.py $OUT/app.js $H/fit_removed.json
python3 /mnt/project-files/design4/apply/patch_band.py $OUT

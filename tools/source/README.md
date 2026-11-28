# 원본 도구 (2026-11-28 프로젝트 "웹앱/ 다국어" 공유 폴더에서 옮김)

이 폴더는 앱 화면에 쓰이지 않습니다. 앱을 만들던 원본 도구를 저장소에 보관한 것입니다.

- `src/` = 예전 공유 폴더 `thai-app/src` 그대로 (build.py, make.sh, content/, base/ 등). 빌드: `bash src/make.sh <ver>` (메모 기준, 경로는 /mnt/project-files/thai-app/ 를 가정하므로 쓸 때 경로 확인).
- `design4/` = 네 앱(태국·르완다·크메르·스와힐리) 공용 디자인 적용 스크립트 (apply.py, xpics.py, specs.py …). `lao_pics/pics.py` = design4가 import하는 라오 앱 src/v3/pics.py 사본.
- 넣지 않은 것: 음성 원본 묶음(audio_all.tar 등). 같은 mp3는 저장소 `audio/`에 있음.

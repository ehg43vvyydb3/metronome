# metronome

> Two standalone metronomes you open straight in a browser — a simple one, and one that highlights measures on a guitar tab PDF as it plays.

[English](#english) · [한국어](#한국어)

---

## English

Two independent single-file HTML metronomes. No build step, no server — just double-click the HTML file.

### simple.html

A basic metronome.

- BPM control (number input / -5, -1, +1, +5 buttons / Space to start·stop)
- Beats per measure, subdivision (quarter/eighth/sixteenth notes)
- Click a beat to toggle its accent on/off
- Save/load presets (localStorage)

### score-player.html

A practice metronome that pages through a guitar tab PDF, highlighting one measure at a time in sync with the click.

#### Workflow

1. **Load**: click "PDF 변환해서 불러오기" (convert PDF and load) and pick a PDF — it's converted to page images right in the browser.
   In Chrome/Edge, picking a folder also saves `page-N.png` files and settings (`meta.json`) into it, so next time you can reopen it in one click from the "최근 열기" (recent) list.
   (To pre-convert from the terminal instead, see `pdf_to_png.py` below.)
2. **Mark measures** (once per song): drag to mark one TAB line — the start/end are picked up automatically, you only click the boundaries that divide it into measures. Dragging again outside the box you're editing automatically starts the next line. Draw as many lines as you like, then save them all at once with "페이지 확정" (confirm page).
   - Drag the blue dots on a box's corners to resize it
   - Click a line to select it (orange), Backspace to delete
3. **Play**: set BPM, time signature, lead-in count-in, and section looping, then press start — the metronome clicks while highlighting the current measure, and the 3-line window slides smoothly two lines at a time. Click a measure on the score, or type a number into the measure box, to jump straight to it. Space toggles play/stop.

#### Limitations

- Repeat signs (D.C., "Play 2x", etc.) aren't recognized. Playback always follows the order drawn on the page (top to bottom, page by page); for a repeated section you need to mark that line's measures a second time and splice it into the sequence where it belongs.
- Remembering the song's folder, saving `meta.json` inside it, and auto-saving PNGs all require the File System Access API — Chrome/Edge only. Other browsers (Firefox, etc.) need the file picker every time, and settings are kept in `localStorage` only.

#### pdf_to_png.py

For pre-converting a PDF to images from the terminal, without the browser.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 pdf_to_png.py "song.pdf"              # scores/song/page-1.png ...
python3 pdf_to_png.py "song.pdf" out_dir 200  # custom output dir / DPI
```

`scores/` can end up holding copyrighted sheet-music images, so it's excluded from git (see `.gitignore`).

---

## 한국어

브라우저에서 바로 여는 간단한 메트로놈 두 가지. 빌드 과정도, 서버도 없다 — HTML 파일을 더블클릭하면 끝.

### simple.html

기본 메트로놈.

- BPM 조절 (숫자 입력 / -5, -1, +1, +5 버튼 / 스페이스바로 재생·정지)
- 박 수, 음표 쪼개기(4분/8분/16분음표)
- 박마다 클릭해서 강세 on/off
- 프리셋 저장/불러오기 (localStorage)

### score-player.html

기타 탭 악보(PDF)를 넘기면서 마디마다 하이라이트해주는 연습용 메트로놈.

#### 사용 흐름

1. **불러오기**: "PDF 변환해서 불러오기"로 PDF를 고르면 브라우저 안에서 바로 페이지 이미지로 변환됩니다.
   Chrome/Edge에서는 폴더를 고르면 그 안에 `page-N.png`와 설정(`meta.json`)까지 저장되어, 다음에 "최근 열기" 목록에서 한 번에 다시 불러올 수 있습니다.
   (터미널에서 미리 변환해두고 싶다면 아래 `pdf_to_png.py` 참고)
2. **마디 지정** (곡마다 처음 한 번만): 드래그로 TAB 한 줄을 지정하면 시작/끝은 자동으로 잡히고, 마디를 나누는 경계만 클릭하면 됩니다. 편집 중인 박스 바깥에서 다시 드래그하면 자동으로 다음 줄이 시작됩니다. 여러 줄을 그린 뒤 "페이지 확정" 한 번으로 저장됩니다.
   - 박스 모서리의 파란 점을 드래그하면 크기 조정
   - 줄을 클릭하면 선택(주황), Backspace로 삭제
3. **재생**: BPM, 박자, 준비마디(카운트인), 구간 반복을 설정하고 시작하면 메트로놈이 돌아가며 마디마다 하이라이트되고, 3줄 창이 두 줄씩 부드럽게 넘어갑니다. 악보를 클릭하거나 마디 번호 입력창에 숫자를 입력해 원하는 마디로 바로 이동할 수 있습니다. 스페이스바로 재생/정지.

#### 제한사항

- 반복 기호(D.C., Play 2x 등)는 인식하지 않습니다. 악보에 그려진 순서(위→아래, 페이지순)대로만 재생하며, 반복 구간은 해당 줄을 다시 한번 마디 지정해서 순서에 끼워 넣어야 합니다.
- 곡 폴더 기억, 폴더 안 `meta.json` 저장, PNG 자동 저장은 File System Access API를 지원하는 Chrome/Edge에서만 동작합니다. 그 외 브라우저(Firefox 등)에서는 매번 파일 선택 창으로 폴더를 다시 골라야 하고, 설정은 `localStorage`에만 저장됩니다.

#### pdf_to_png.py

브라우저 없이 터미널에서 PDF를 미리 이미지로 변환해두고 싶을 때 사용합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 pdf_to_png.py "악보.pdf"              # scores/악보/page-1.png ...
python3 pdf_to_png.py "악보.pdf" out_dir 200   # 출력 폴더, DPI 직접 지정
```

`scores/`에는 저작권이 있는 악보 이미지가 생길 수 있어 git에는 포함하지 않습니다(`.gitignore` 참고).

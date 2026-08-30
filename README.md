# metronome

> Standalone practice tools you open straight in a browser — a simple metronome, one that highlights measures on a guitar tab PDF as it plays, and one that does the same in sync with a backing track.

[English](#english) · [한국어](#한국어)

---

## English

Independent single-file HTML tools. No build step, no server — just double-click the HTML file.

### simple.html

A basic metronome.

- BPM control (number input / -5, -1, +1, +5 buttons / Space to start·stop)
- Beats per measure, subdivision (quarter/eighth/sixteenth notes)
- Click a beat to toggle its accent on/off
- Save/load presets (localStorage)

### score-player.html

A practice metronome that pages through a guitar tab PDF, highlighting one measure at a time in sync with the click.

#### Workflow

1. **Convert**: PDFs are never converted inside the browser. Pre-convert a PDF to page images first — either `pdf_to_png_gui.command` (double-click, pick a PDF in a native dialog) or `pdf_to_png.py` from the terminal (see below). Either way it writes `scores/<song>/page-N.png`.
2. **Load**: in score-player.html, click "폴더 불러오기" (load folder) and pick that folder — works in any browser, since it's a plain file picker. The song name is remembered in `localStorage` so it shows up under "최근 열기" (recent) next time, though you'll still need to re-pick the folder (browsers don't let a page silently reopen a folder on its own).
3. **Mark measures** (once per song): drag to mark one TAB line — the start/end are picked up automatically, you only click the boundaries that divide it into measures. Dragging again outside the box you're editing automatically starts the next line. Draw as many lines as you like, then save them all at once with "페이지 확정" (confirm page).
   - Drag the blue dots on a box's corners to resize it
   - Click a line to select it (orange), Backspace to delete
4. **Play**: set BPM, time signature, lead-in count-in, and section looping, then press start — the metronome clicks while highlighting the current measure, and the 3-line window slides smoothly two lines at a time. Click a measure on the score, or type a number into the measure box, to jump straight to it. Space toggles play/stop.

Measure positions, BPM, and other settings auto-save to `localStorage`, keyed by song (folder) name — no server, no browser-specific API involved.

#### Limitations

- Repeat signs (D.C., "Play 2x", etc.) aren't recognized. Playback always follows the order drawn on the page (top to bottom, page by page); for a repeated section you need to mark that line's measures a second time and splice it into the sequence where it belongs.

#### pdf_to_png.py / pdf_to_png_gui.command

Convert a PDF to page images before loading it in score-player.html.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 pdf_to_png.py "song.pdf"              # scores/song/page-1.png ...
python3 pdf_to_png.py "song.pdf" out_dir 200  # custom output dir / DPI
```

Or double-click `pdf_to_png_gui.command` for a small tkinter window with a single "pick a PDF" button — same conversion, no terminal needed. It reuses `pdf_to_png.py`'s `convert()` directly. Homebrew's Python doesn't ship tkinter by default, so this needs `brew install python-tk@<your version>` once.

`scores/` can end up holding copyrighted sheet-music images, so it's excluded from git (see `.gitignore`).

### backing-track-sync-editor.html

Same measure-by-measure tab practice as score-player.html, but the measures follow a **real backing track** instead of a synthesized click. score-player.html stays as it is — use that when you're practicing to a click alone.

#### Workflow

1. **Prepare the folder**: put the page images *and* the audio file in the same folder — `scores/<song>/page-N.png` (from `pdf_to_png.py`, as above) plus any audio file (`.mp3`, `.wav`, `.m4a`, …) copied in from wherever you keep it. One "load folder" then picks up both at once.
2. **Audio sync**: set the BPM and click the waveform to mark the point where measure 1 actually begins. If the recording already has a count-in, set "준비박 개수" (count-in beats) to how many beats it holds — the start point still marks the *first real beat*, after the count-in. Optionally pre-analyze the BPM (see below). The waveform zooms in and out for precise placement.
3. **Mark measures**: identical to score-player.html.
4. **Play**: the backing track drives everything — measures highlight and the 3-line window slides in time with the audio. Under each tab line the matching slice of the waveform is drawn, stretched to each measure's own width so the bar lines always line up with the audio. "전체화면 연습" (fullscreen practice) hides every setting and leaves just play/stop plus the tab and waveform, scaled up to the window.

Practice speed is adjustable ("연습 BPM"), defaulting to the track's own BPM.

#### Limitations

- Repeat signs aren't recognized, same as score-player.html.
- Slowing down or speeding up shifts the **pitch** as well — it uses `playbackRate`, and pitch-preserving time-stretching would need an external library, which this project deliberately avoids.

#### analyze_audio.py

Estimates a track's BPM with [librosa](https://librosa.org/) so you don't have to tap it in.

```bash
source .venv/bin/activate
pip install -r requirements.txt

python3 analyze_audio.py "scores/song/"   # writes scores/song/audio_meta.json
```

The editor reads `audio_meta.json` when you load the folder and fills in the BPM (it won't overwrite settings you've already saved for that song — use the "분석값 적용" button for that). The **start point is deliberately not auto-detected**: estimating it kept landing a beat or two off, and it takes one click on the waveform to place exactly.

---

## 한국어

브라우저에서 바로 여는 연습 도구들. 빌드 과정도, 서버도 없다 — HTML 파일을 더블클릭하면 끝.

### simple.html

기본 메트로놈.

- BPM 조절 (숫자 입력 / -5, -1, +1, +5 버튼 / 스페이스바로 재생·정지)
- 박 수, 음표 쪼개기(4분/8분/16분음표)
- 박마다 클릭해서 강세 on/off
- 프리셋 저장/불러오기 (localStorage)

### score-player.html

기타 탭 악보(PDF)를 넘기면서 마디마다 하이라이트해주는 연습용 메트로놈.

#### 사용 흐름

1. **변환**: PDF는 브라우저 안에서 변환하지 않습니다. `pdf_to_png_gui.command`(더블클릭 후 PDF 선택) 또는 터미널의 `pdf_to_png.py`(아래 참고)로 미리 변환해두면 `scores/곡이름/page-N.png`가 생깁니다.
2. **불러오기**: score-player.html에서 "폴더 불러오기"로 그 폴더를 고르면 됩니다 — 일반 파일 선택창이라 브라우저를 가리지 않습니다. 곡 이름은 `localStorage`에 남아 "최근 열기" 목록에 뜨지만, 브라우저가 폴더를 자동으로 다시 열어주지는 않으므로 폴더는 매번 다시 선택해야 합니다.
3. **마디 지정** (곡마다 처음 한 번만): 드래그로 TAB 한 줄을 지정하면 시작/끝은 자동으로 잡히고, 마디를 나누는 경계만 클릭하면 됩니다. 편집 중인 박스 바깥에서 다시 드래그하면 자동으로 다음 줄이 시작됩니다. 여러 줄을 그린 뒤 "페이지 확정" 한 번으로 저장됩니다.
   - 박스 모서리의 파란 점을 드래그하면 크기 조정
   - 줄을 클릭하면 선택(주황), Backspace로 삭제
4. **재생**: BPM, 박자, 준비마디(카운트인), 구간 반복을 설정하고 시작하면 메트로놈이 돌아가며 마디마다 하이라이트되고, 3줄 창이 두 줄씩 부드럽게 넘어갑니다. 악보를 클릭하거나 마디 번호 입력창에 숫자를 입력해 원하는 마디로 바로 이동할 수 있습니다. 스페이스바로 재생/정지.

마디 위치, BPM 등 설정은 곡(폴더) 이름을 기준으로 `localStorage`에 자동 저장됩니다 — 서버도, 브라우저별 API도 필요 없습니다.

#### 제한사항

- 반복 기호(D.C., Play 2x 등)는 인식하지 않습니다. 악보에 그려진 순서(위→아래, 페이지순)대로만 재생하며, 반복 구간은 해당 줄을 다시 한번 마디 지정해서 순서에 끼워 넣어야 합니다.

#### pdf_to_png.py / pdf_to_png_gui.command

score-player.html에 불러오기 전에 PDF를 페이지 이미지로 변환해둡니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 pdf_to_png.py "악보.pdf"              # scores/악보/page-1.png ...
python3 pdf_to_png.py "악보.pdf" out_dir 200   # 출력 폴더, DPI 직접 지정
```

터미널 대신 `pdf_to_png_gui.command`를 더블클릭하면 "PDF 선택해서 변환" 버튼 하나짜리 작은 tkinter 창이 뜹니다 — 내부적으로 `pdf_to_png.py`의 `convert()`를 그대로 재사용합니다. Homebrew Python에는 tkinter가 기본 포함되어 있지 않아 한 번은 `brew install python-tk@<버전>`이 필요합니다.

`scores/`에는 저작권이 있는 악보 이미지가 생길 수 있어 git에는 포함하지 않습니다(`.gitignore` 참고).

### backing-track-sync-editor.html

score-player.html과 같은 마디 단위 탭 연습이지만, 합성 클릭 대신 **실제 배킹트랙**에 맞춰 마디가 넘어갑니다. score-player.html은 그대로 두었으니 클릭만으로 연습할 때는 계속 그걸 쓰면 됩니다.

#### 사용 흐름

1. **폴더 준비**: 페이지 이미지와 오디오 파일을 같은 폴더에 둡니다 — `scores/곡이름/page-N.png`(위의 `pdf_to_png.py`로 변환) + 오디오 파일(`.mp3`, `.wav`, `.m4a` 등)을 원본에서 복사해 넣기만 하면 됩니다. "폴더 불러오기" 한 번으로 둘 다 읽어옵니다.
2. **오디오 싱크**: BPM을 맞추고, 파형을 클릭해 마디 1이 실제로 시작하는 지점을 찍습니다. 녹음에 이미 준비박이 들어있다면 "준비박 개수"에 그 박 수를 넣으세요 — 시작점은 준비박이 *끝난 뒤* 진짜 첫 박을 가리킵니다. BPM은 미리 분석해둘 수도 있습니다(아래 참고). 파형은 확대/축소해서 정확히 찍을 수 있습니다.
3. **마디 지정**: score-player.html과 동일합니다.
4. **재생**: 배킹트랙이 모든 걸 이끕니다 — 오디오에 맞춰 마디가 하이라이트되고 3줄 창이 넘어갑니다. 각 탭 줄 아래에는 그 구간의 파형이 마디별 폭에 맞춰 그려져서 마디선과 파형이 항상 일치합니다. "전체화면 연습"을 누르면 설정 UI가 전부 사라지고 재생/정지 버튼과 탭·파형만 화면 가득 남습니다.

연습 속도("연습 BPM")도 조절할 수 있고, 기본값은 그 트랙의 BPM입니다.

#### 제한사항

- 반복 기호를 인식하지 않는 건 score-player.html과 동일합니다.
- 속도를 바꾸면 **음정도 같이 변합니다** — `playbackRate`를 쓰기 때문이고, 음정을 유지하려면 외부 라이브러리가 필요해서 의도적으로 넣지 않았습니다.

#### analyze_audio.py

[librosa](https://librosa.org/)로 트랙의 BPM을 추정해줍니다(탭 템포로 직접 찍지 않아도 되도록).

```bash
source .venv/bin/activate
pip install -r requirements.txt

python3 analyze_audio.py "scores/곡이름/"   # scores/곡이름/audio_meta.json 생성
```

폴더를 불러올 때 `audio_meta.json`을 읽어 BPM을 채웁니다(이미 저장해둔 설정이 있으면 덮어쓰지 않고, 그때는 "분석값 적용" 버튼을 누르면 됩니다). **시작점은 일부러 자동 추정하지 않습니다** — 추정값이 자꾸 한두 박씩 어긋났고, 파형을 한 번 클릭하면 정확히 찍히기 때문입니다.

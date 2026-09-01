# metronome

> Standalone practice tools you open straight in a browser — a simple metronome, a rhythm-pattern builder, one that highlights measures on a guitar tab PDF as it plays, and one that does the same in sync with a backing track.

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

### rhythm.html

Write out a rhythm and hear it — for drilling a pattern you can't yet read at sight.

- Set BPM, time signature (n/2, n/4, n/8) and how many measures
- Fill measures from a palette of notes and rests (whole through 16th, dotted optional); ties carry over into the next measure
- Play once or on a loop, with count-in measures and an optional metronome click over the top

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
2. **Audio sync**: set the BPM and the time signature (both numerator and denominator — BPM always means ♩, so ♩=120 makes a 4/4 bar 2.0s and a 6/8 bar 1.5s), then click the waveform to mark the point where measure 1 actually begins (the *first real beat* — if the recording opens with a count-in, mark the beat after it). Optionally pre-analyze the BPM (see below). The waveform zooms in and out for precise placement.
3. **Mark measures**: identical to score-player.html.
4. **Play**: the backing track drives everything — measures highlight and the 3-line window slides in time with the audio. Under each tab line the matching slice of the waveform is drawn, stretched to each measure's own width so the bar lines always line up with the audio. Section looping and partial ranges work as in score-player.html, and Space toggles play/stop. "준비박 세기" (count-in), on by default, gives you one bar — as many beats as the beats-per-bar set in audio sync — before playback reaches the measure you started from, counted off in the beat boxes above the tab — the same boxes that light up beat by beat while playing, and they stay visible in fullscreen practice. It applies wherever you start, so what you hear during the count is the track's own preceding bar; loop repeats skip it so the loop doesn't break. If the count-in needs more room than there is before the start point, playback simply starts that much later — the audio file is never padded or rewritten. Past the last measure the track keeps playing to the end of the file, so the song's ending isn't cut off (unless looping is on, which restarts right away). "전체화면 연습" (fullscreen practice) hides every setting and leaves just play/stop, "처음으로" (back to the section's first measure), the beat boxes, and the tab plus waveform, scaled up to the window.

Practice speed can be dropped to whatever slowed-down versions you prepared with `stretch_audio.py` (see below) — **the pitch stays put**, so the track is still in tune with your guitar. Each button shows the resulting BPM.

#### Limitations

- Repeat signs aren't recognized, same as score-player.html.
- Only the speeds you pre-rendered are selectable — the browser can't stretch audio on the fly without shifting pitch.

#### analyze_audio.py

Estimates a track's BPM with [librosa](https://librosa.org/) so you don't have to tap it in.

```bash
source .venv/bin/activate
pip install -r requirements.txt

python3 analyze_audio.py "scores/song/"   # writes scores/song/audio_meta.json
```

The editor reads `audio_meta.json` when you load the folder and fills in the BPM (it won't overwrite settings you've already saved for that song — use the "분석값 적용" button for that). The **start point is deliberately not auto-detected**: estimating it kept landing a beat or two off, and it takes one click on the waveform to place exactly.

#### stretch_audio.py

Renders slowed-down copies of the track **without changing pitch**, so you can practice under tempo and still play in tune.

```bash
python3 stretch_audio.py "scores/song/"           # 50–95% in 5% steps (10 files)
python3 stretch_audio.py "scores/song/" 60 75     # or pick your own
```

It writes `scores/song/speed-70.mp3` etc. next to the original; the editor picks them up on the next folder load and turns them into practice-speed buttons. **Copies keep the original's format**, so an MP3 source stays MP3 rather than ballooning into WAV. (M4A/AAC can't be encoded by libsndfile, so those fall back to MP3.) The copies are longer than the original — a 50% copy runs twice as long — so the full default set lands around 15× the original file's size.

---

## 한국어

브라우저에서 바로 여는 연습 도구들. 빌드 과정도, 서버도 없다 — HTML 파일을 더블클릭하면 끝.

### simple.html

기본 메트로놈.

- BPM 조절 (숫자 입력 / -5, -1, +1, +5 버튼 / 스페이스바로 재생·정지)
- 박 수, 음표 쪼개기(4분/8분/16분음표)
- 박마다 클릭해서 강세 on/off
- 프리셋 저장/불러오기 (localStorage)

### rhythm.html

리듬을 직접 적어 넣고 들어보는 도구 — 눈으로 바로 안 읽히는 패턴을 익힐 때 씁니다.

- BPM, 박자표(n/2, n/4, n/8), 마디 수 설정
- 음표·쉼표 팔레트(온음표~16분음표, 점음표 옵션)로 마디를 채우고, 붙임줄은 다음 마디까지 이어집니다
- 1번 재생 또는 반복 재생, 준비마디와 메트로놈 클릭을 같이 켤 수 있습니다

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
2. **오디오 싱크**: BPM과 박자(분자/분모)를 맞추고 — BPM은 언제나 ♩ 기준이라 ♩=120이면 4/4 마디는 2.0초, 6/8 마디는 1.5초입니다 — 파형을 클릭해 마디 1이 실제로 시작하는 지점을 찍습니다(녹음 앞에 카운트인이 들어있다면 그 *다음* 진짜 첫 박). BPM은 미리 분석해둘 수도 있습니다(아래 참고). 파형은 확대/축소해서 정확히 찍을 수 있습니다.
3. **마디 지정**: score-player.html과 동일합니다.
4. **재생**: 배킹트랙이 모든 걸 이끕니다 — 오디오에 맞춰 마디가 하이라이트되고 3줄 창이 넘어갑니다. 각 탭 줄 아래에는 그 구간의 파형이 마디별 폭에 맞춰 그려져서 마디선과 파형이 항상 일치합니다. 구간 반복·일부 재생은 score-player.html과 같고, 스페이스바로 재생/정지합니다. 기본으로 켜져 있는 "준비박 세기"는 시작한 마디에 도달하기 전 1마디(= 오디오 싱크의 박자만큼)를 세어주고, 그동안 탭 위의 박자박스가 한 칸씩 켜집니다 — 재생 중 박자 표시와 같은 박스이고, 전체화면 연습에서도 보입니다. 어느 마디에서 시작하든 붙기 때문에 곡 중간에서 시작하면 그 직전 마디의 실제 오디오가 리드인으로 들리고, 구간 반복으로 되돌아갈 때는 루프가 끊기지 않도록 붙지 않습니다. 시작점 앞에 준비박이 들어갈 공간이 모자라면 그만큼 재생을 늦게 시작할 뿐, 오디오 파일을 손대거나 무음을 덧붙이지 않습니다. 마지막 마디를 지나도 파일 끝까지 계속 재생해서 곡의 끝맺음이 잘리지 않습니다(구간 반복이 켜져 있으면 바로 처음으로 되돌아갑니다). "전체화면 연습"을 누르면 설정 UI가 전부 사라지고 재생/정지·처음으로 버튼과 박자박스, 탭·파형만 화면 가득 남습니다.

연습 속도는 `stretch_audio.py`(아래 참고)로 미리 만들어둔 느린 버전 중에서 고를 수 있습니다 — **음정은 그대로 유지되므로** 기타 튜닝과 어긋나지 않습니다. 버튼마다 그 속도에서의 BPM이 표시됩니다.

#### 제한사항

- 반복 기호를 인식하지 않는 건 score-player.html과 동일합니다.
- 미리 변환해둔 속도만 고를 수 있습니다 — 브라우저에서 즉석으로 늘이면 음정이 변하기 때문입니다.

#### analyze_audio.py

[librosa](https://librosa.org/)로 트랙의 BPM을 추정해줍니다(탭 템포로 직접 찍지 않아도 되도록).

```bash
source .venv/bin/activate
pip install -r requirements.txt

python3 analyze_audio.py "scores/곡이름/"   # scores/곡이름/audio_meta.json 생성
```

폴더를 불러올 때 `audio_meta.json`을 읽어 BPM을 채웁니다(이미 저장해둔 설정이 있으면 덮어쓰지 않고, 그때는 "분석값 적용" 버튼을 누르면 됩니다). **시작점은 일부러 자동 추정하지 않습니다** — 추정값이 자꾸 한두 박씩 어긋났고, 파형을 한 번 클릭하면 정확히 찍히기 때문입니다.

#### stretch_audio.py

**음정은 그대로 두고** 속도만 늦춘 사본을 만들어줍니다. 느리게 연습해도 기타 튜닝과 맞습니다.

```bash
python3 stretch_audio.py "scores/곡이름/"          # 50~95%를 5% 단위로 (10개)
python3 stretch_audio.py "scores/곡이름/" 60 75    # 원하는 속도만 지정
```

원본 옆에 `scores/곡이름/speed-70.mp3` 같은 파일이 생기고, 다음에 폴더를 불러오면 자동으로 연습 속도 버튼이 됩니다. **사본은 원본과 같은 포맷으로 저장**하므로 mp3 원본이 WAV로 부풀지 않습니다(m4a/aac는 libsndfile이 인코딩을 지원하지 않아 mp3로 저장). 사본은 원본보다 길어지므로(50%면 두 배) 기본 10개를 다 만들면 원본 파일의 약 15배 정도가 됩니다.

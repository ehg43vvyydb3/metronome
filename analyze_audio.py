import re
import sys
import os
import json

import numpy as np
import librosa

# backing-track-sync-editor.html의 AUDIO_EXT_RE와 같은 목록이어야 한다.
# 한쪽에만 추가하면 앱은 읽는데 스크립트는 "오디오 파일이 없습니다"가 된다.
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".aiff", ".aif")
# stretch_audio.py가 만들어둔 느린 사본. 원본 후보에서 빼지 않으면 파일명 정렬 순서에 따라
# (원본 이름이 "speed-"보다 뒤면) 사본이 원본으로 뽑혀서, 이미 늘린 음원을 또 늘리게 된다.
SPEED_FILE_RE = re.compile(r"^speed-\d+\.", re.IGNORECASE)


def find_audio_file(folder):
    candidates = sorted(
        f
        for f in os.listdir(folder)
        if f.lower().endswith(AUDIO_EXTS) and not SPEED_FILE_RE.match(f)
    )
    return candidates[0] if candidates else None


def analyze(path):
    if os.path.isdir(path):
        folder = path
        name = find_audio_file(folder)
        if not name:
            raise FileNotFoundError(f"{folder} 안에 오디오 파일이 없습니다.")
        audio_path = os.path.join(folder, name)
    else:
        audio_path = path
        folder = os.path.dirname(audio_path) or "."

    y, sr = librosa.load(audio_path, sr=None, mono=True)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.atleast_1d(tempo)[0])

    # 시작점은 여기서 추정하지 않는다 — 준비박 유무·박자 어긋남 등으로
    # 자동 추정이 자꾸 한두 박씩 밀리는 문제가 있어서, BPM만 자동으로 잡고
    # 시작점은 backing-track-sync-editor.html에서 파형을 직접 클릭해
    # 지정하는 쪽이 더 정확하고 간단하다.
    meta = {
        "sourceFile": os.path.basename(audio_path),
        "bpm": round(bpm, 1),
    }
    os.makedirs(folder, exist_ok=True)
    out_path = os.path.join(folder, "audio_meta.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return out_path, meta


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 analyze_audio.py <scores/곡이름 폴더 또는 오디오 파일 경로>")
        sys.exit(1)
    out_path, meta = analyze(sys.argv[1])
    print(f"BPM: {meta['bpm']}")
    print(out_path)

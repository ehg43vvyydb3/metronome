import sys
import os
import json

import numpy as np
import librosa

AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac")


def find_audio_file(folder):
    candidates = sorted(
        f for f in os.listdir(folder) if f.lower().endswith(AUDIO_EXTS)
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

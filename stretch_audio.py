import sys
import os

import librosa
import soundfile as sf

from analyze_audio import find_audio_file

# 만들어진 파일은 scores/곡이름/speed-80.wav 처럼 저장된다.
# backing-track-sync-editor.html이 이 이름 규칙으로 느린 버전을 찾아
# 연습 속도 버튼을 만들고, 재생할 때 원본 대신 이 파일을 쓴다.
OUT_PREFIX = "speed-"


def stretch(path, percents):
    if os.path.isdir(path):
        folder = path
        name = find_audio_file(folder)
        if not name:
            raise FileNotFoundError(f"{folder} 안에 오디오 파일이 없습니다.")
        audio_path = os.path.join(folder, name)
    else:
        audio_path = path
        folder = os.path.dirname(audio_path) or "."

    # mono=False로 원본 채널 수를 유지한다(스테레오면 (채널, 샘플) 모양).
    y, sr = librosa.load(audio_path, sr=None, mono=False)

    out_paths = []
    for pct in percents:
        if not (10 <= pct <= 200):
            raise ValueError(f"속도는 10~200(%) 사이여야 합니다: {pct}")
        if pct == 100:
            continue
        rate = pct / 100.0
        stretched = librosa.effects.time_stretch(y, rate=rate)
        # soundfile은 (샘플, 채널) 모양을 기대하므로 스테레오면 전치한다.
        data = stretched.T if stretched.ndim > 1 else stretched
        out_path = os.path.join(folder, f"{OUT_PREFIX}{pct}.wav")
        sf.write(out_path, data, sr)
        out_paths.append(out_path)
    return out_paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 stretch_audio.py <scores/곡이름 폴더 또는 오디오 파일> [속도%...]")
        print("  예: python3 stretch_audio.py scores/곡이름/ 70 80 90")
        print("  속도를 안 주면 70 80 90 을 만든다. 음정은 그대로 두고 속도만 바꾼다.")
        sys.exit(1)
    path = sys.argv[1]
    percents = [int(a) for a in sys.argv[2:]] or [70, 80, 90]
    for out_path in stretch(path, percents):
        print(out_path)

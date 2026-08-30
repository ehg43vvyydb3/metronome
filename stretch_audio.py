import sys
import os

import librosa
import soundfile as sf

from analyze_audio import find_audio_file

# 만들어진 파일은 scores/곡이름/speed-80.mp3 처럼 저장된다(확장자는 아래 규칙대로 원본을 따른다).
# backing-track-sync-editor.html이 이 이름 규칙으로 느린 버전을 찾아
# 연습 속도 버튼을 만들고, 재생할 때 원본 대신 이 파일을 쓴다.
OUT_PREFIX = "speed-"

# 속도를 안 주면 만드는 기본 목록: 50~95%를 5% 단위로.
DEFAULT_PERCENTS = list(range(50, 100, 5))

# 사본은 원본과 같은 포맷으로 저장한다. 원본이 mp3인데 WAV로 뽑으면
# 사본 하나가 원본의 10배가 넘어서(10개면 수백 MB) 감당이 안 된다.
# libsndfile이 인코딩할 수 있는 포맷만 여기 있고, m4a/aac는 지원하지 않아
# 브라우저가 항상 읽을 수 있는 mp3로 대신 저장한다.
WRITABLE_FORMATS = {
    ".wav": "WAV",
    ".mp3": "MP3",
    ".flac": "FLAC",
    ".ogg": "OGG",
    ".aiff": "AIFF",
    ".aif": "AIFF",
}
FALLBACK_EXT, FALLBACK_FORMAT = ".mp3", "MP3"


def output_format(audio_path):
    ext = os.path.splitext(audio_path)[1].lower()
    if ext in WRITABLE_FORMATS:
        return ext, WRITABLE_FORMATS[ext]
    return FALLBACK_EXT, FALLBACK_FORMAT


def stretch(path, percents):
    # 오디오를 읽기 전에 먼저 검사한다 — 잘못된 값이 섞여 있으면 긴 디코딩 뒤에
    # 실패하거나, 파일을 반만 만들어놓고 멈추게 된다.
    for pct in percents:
        if not (10 <= pct <= 200):
            raise ValueError(f"속도는 10~200(%) 사이여야 합니다: {pct}")

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
    ext, fmt = output_format(audio_path)
    if ext != os.path.splitext(audio_path)[1].lower():
        print(f"※ {os.path.splitext(audio_path)[1]}는 인코딩을 지원하지 않아 {ext}로 저장합니다.")

    out_paths = []
    for pct in percents:
        if pct == 100:
            continue
        rate = pct / 100.0
        stretched = librosa.effects.time_stretch(y, rate=rate)
        # soundfile은 (샘플, 채널) 모양을 기대하므로 스테레오면 전치한다.
        data = stretched.T if stretched.ndim > 1 else stretched
        out_path = os.path.join(folder, f"{OUT_PREFIX}{pct}{ext}")
        sf.write(out_path, data, sr, format=fmt)
        out_paths.append(out_path)
    return out_paths


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 stretch_audio.py <scores/곡이름 폴더 또는 오디오 파일> [속도%...]")
        print("  예: python3 stretch_audio.py scores/곡이름/ 70 80 90")
        print(f"  속도를 안 주면 {DEFAULT_PERCENTS[0]}~{DEFAULT_PERCENTS[-1]}%를 5% 단위로 만든다"
              f"({len(DEFAULT_PERCENTS)}개). 음정은 그대로 두고 속도만 바꾼다.")
        sys.exit(1)
    path = sys.argv[1]
    percents = [int(a) for a in sys.argv[2:]] or DEFAULT_PERCENTS
    for out_path in stretch(path, percents):
        print(out_path)

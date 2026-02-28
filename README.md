# Scriba

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org)

Simple CLI tool that transcribes audio files to text using OpenAI's [Whisper](https://github.com/openai/whisper). Point it at an audio file, pick a model, and get a clean `.txt` transcription — no setup beyond `pip install`.

## Quick start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** You may need the correct PyTorch wheel for your OS/CUDA version.
> See [pytorch.org/get-started](https://pytorch.org/get-started/locally/).

3. Transcribe:

```bash
python scriba.py interview.mp3
python scriba.py lecture.wav -m large
python scriba.py ep1.mp3 ep2.mp3 ep3.mp3        # batch
python scriba.py call.ogg -l es                  # force Spanish
```

## Usage

```
usage: scriba [-h] [-m {tiny,base,small,medium,large}] [-l LANGUAGE] audio [audio ...]

Simple transcription helper powered by Whisper.

positional arguments:
  audio                 path(s) to the audio file(s) to transcribe

options:
  -h, --help            show this help message and exit
  -m, --model {tiny,base,small,medium,large}
                        Whisper model size (default: small)
  -l, --language LANGUAGE
                        language code, e.g. 'en', 'es', 'fr' (default: auto-detect)
```

## Models

| Model  | Speed   | Quality | VRAM   |
|--------|---------|---------|--------|
| tiny   | Fastest | Low     | ~1 GB  |
| base   | Fast    | Fair    | ~1 GB  |
| small  | Medium  | Good    | ~2 GB  |
| medium | Slow    | Great   | ~5 GB  |
| large  | Slowest | Best    | ~10 GB |

## Example

```
$ python scriba.py meeting.mp3 -m small
⚙️  Using device: CUDA
⏳ Loading Whisper model 'small'... (this may take a while the first time)
🎤 Processing 'meeting.mp3'... Please wait.
[00:00.000 --> 00:04.320]  Welcome everyone to the weekly standup.
[00:04.320 --> 00:08.640]  Let's start with a quick round of updates.

========================================
✅ Done! Transcription saved to:
📄 meeting_transcription.txt
========================================
```

## License

[MIT](LICENSE)

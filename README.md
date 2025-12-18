# Scriba — simple transcription helper

This repository contains a small Python script named `scriba.py` to transcribe audio using Whisper.

Quick start (recommended):

1. Create a virtual environment and activate it (zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip and install dependencies.

Note: Installing `torch` may require selecting the correct wheel for your OS and CUDA version. For CPU-only or to get the right command, visit https://pytorch.org/get-started/locally/.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the script:

```bash
python scriba.py path/to/audio.mp3 [model]
```

Models: `tiny`, `base`, `small`, `medium`, `large`. Default is `small`.

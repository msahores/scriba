import argparse
import os
import warnings

warnings.filterwarnings("ignore")

import torch
import whisper

MODELS = ["tiny", "base", "small", "medium", "large"]


def load_model(model_size, device):
    print(f"⏳ Loading Whisper model '{model_size}'... (this may take a while the first time)")
    try:
        return whisper.load_model(model_size, device=device)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None


def transcribe_audio(file_path, model, language=None):
    print(f"\n🎤 Processing '{file_path}'... Please wait.")
    opts = {"verbose": True}
    if language:
        opts["language"] = language
    result = model.transcribe(file_path, **opts)

    base_name = os.path.splitext(file_path)[0]
    output_name = f"{base_name}_transcription.txt"

    try:
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print("\n" + "=" * 40)
        print(f"✅ Done! Transcription saved to:")
        print(f"📄 {output_name}")
        print("=" * 40)

    except IOError as e:
        print(f"❌ Error saving file: {e}")


def main():
    parser = argparse.ArgumentParser(
        prog="scriba",
        description="Simple transcription helper powered by Whisper.",
    )
    parser.add_argument(
        "audio",
        nargs="+",
        help="path(s) to the audio file(s) to transcribe",
    )
    parser.add_argument(
        "-m", "--model",
        choices=MODELS,
        default="small",
        help="Whisper model size (default: small)",
    )
    parser.add_argument(
        "-l", "--language",
        default=None,
        help="language code, e.g. 'en', 'es', 'fr' (default: auto-detect)",
    )

    args = parser.parse_args()

    missing = [f for f in args.audio if not os.path.exists(f)]
    if missing:
        parser.error(f"file(s) not found: {', '.join(missing)}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"⚙️  Using device: {device.upper()}")
    if device == "cpu":
        print("⚠️  Warning: Using CPU can be slow. If you have an NVIDIA GPU, make sure CUDA drivers are installed.")

    model = load_model(args.model, device)
    if model is None:
        return

    for file_path in args.audio:
        transcribe_audio(file_path, model, args.language)


if __name__ == "__main__":
    main()

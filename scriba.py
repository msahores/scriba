import argparse
import os
import warnings

warnings.filterwarnings("ignore")

import torch
import whisper

MODELS = ["tiny", "base", "small", "medium", "large"]


def transcribe_audio(file_path, model_size="small"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"⚙️  Using device: {device.upper()}")
    if device == "cpu":
        print("⚠️  Warning: Using CPU can be slow. If you have an NVIDIA GPU, make sure CUDA drivers are installed.")

    print(f"⏳ Loading Whisper model '{model_size}'... (this may take a while the first time)")
    try:
        model = whisper.load_model(model_size, device=device)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    print(f"🎤 Processing '{file_path}'... Please wait.")
    result = model.transcribe(file_path, verbose=True)

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
    parser.add_argument("audio", help="path to the audio file to transcribe")
    parser.add_argument(
        "-m", "--model",
        choices=MODELS,
        default="small",
        help="Whisper model size (default: small)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.audio):
        parser.error(f"file not found: {args.audio}")

    transcribe_audio(args.audio, args.model)


if __name__ == "__main__":
    main()

import whisper
import sys
import os
import torch
import warnings

# Filter irrelevant warnings to keep the terminal clean
warnings.filterwarnings("ignore")

def transcribe_audio(file_path, model_size="small"):
    # 1. Validate that the file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: The file '{file_path}' does not exist.")
        return

    # 2. Detect device (GPU is much faster)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"⚙️  Using device: {device.upper()}")
    if device == "cpu":
        print("⚠️  Warning: Using CPU can be slow. If you have an NVIDIA GPU, make sure CUDA drivers are installed.")

    # 3. Load the model
    print(f"⏳ Loading Whisper model '{model_size}'... (this may take a while the first time)")
    try:
        model = whisper.load_model(model_size, device=device)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return

    # 4. Transcribe
    print(f"🎤 Processing '{file_path}'... Please wait.")

    # verbose=True prints segments with timestamps in real time
    result = model.transcribe(file_path, verbose=True)

    # 5. Save the result to a text file
    base_name = os.path.splitext(file_path)[0]
    output_name = f"{base_name}_transcription.txt"

    try:
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print("\n" + "="*40)
        print(f"✅ Done! Transcription saved to:")
        print(f"📄 {output_name}")
        print("="*40)

    except IOError as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python scriba.py <audio_file> [model]")
        print("Example: python scriba.py interview.mp3 medium")
        sys.exit(1)

    audio_file = sys.argv[1]

    # If the user specifies a model (tiny, base, small, medium, large), use it.
    # Otherwise, default to 'small' (good speed/quality balance).
    model = sys.argv[2] if len(sys.argv) > 2 else "small"

    transcribe_audio(audio_file, model)

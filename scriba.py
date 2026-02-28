import argparse
import os
import warnings

warnings.filterwarnings("ignore")

import torch
import whisper
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

MODELS = ["tiny", "base", "small", "medium", "large"]
FORMATS = ["txt", "srt", "vtt"]

console = Console()


def format_timestamp(seconds, fmt):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if fmt == "srt":
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def write_txt(segments, f):
    text = " ".join(seg["text"].strip() for seg in segments)
    f.write(text)


def write_srt(segments, f):
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg["start"], "srt")
        end = format_timestamp(seg["end"], "srt")
        f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")


def write_vtt(segments, f):
    f.write("WEBVTT\n\n")
    for seg in segments:
        start = format_timestamp(seg["start"], "vtt")
        end = format_timestamp(seg["end"], "vtt")
        f.write(f"{start} --> {end}\n{seg['text'].strip()}\n\n")


WRITERS = {"txt": write_txt, "srt": write_srt, "vtt": write_vtt}


def load_model(model_size, device):
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        progress.add_task(f"Loading Whisper model '{model_size}'...", total=None)
        try:
            return whisper.load_model(model_size, device=device)
        except Exception as e:
            console.print(f"[bold red]Error loading model:[/] {e}")
            return None


def transcribe_audio(file_path, model, language=None, formats=None):
    if formats is None:
        formats = ["txt"]

    console.rule(f"[bold]{file_path}")
    console.print(f"[dim]Transcribing...[/]")

    opts = {"verbose": False}
    if language:
        opts["language"] = language

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        progress.add_task("Transcribing audio...", total=None)
        result = model.transcribe(file_path, **opts)

    segments = result["segments"]
    detected = result.get("language", "unknown")
    console.print(f"[dim]Detected language:[/] [bold]{detected}")

    base_name = os.path.splitext(file_path)[0]
    saved = []

    for fmt in formats:
        output_name = f"{base_name}_transcription.{fmt}"
        try:
            with open(output_name, "w", encoding="utf-8") as f:
                WRITERS[fmt](segments, f)
            saved.append(output_name)
        except IOError as e:
            console.print(f"[bold red]Error saving {output_name}:[/] {e}")

    if saved:
        file_list = "\n".join(f"  [green]{f}[/]" for f in saved)
        console.print(Panel(file_list, title="Saved", border_style="green"))


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
    parser.add_argument(
        "-f", "--format",
        choices=FORMATS,
        nargs="+",
        default=["txt"],
        help="output format(s): txt, srt, vtt (default: txt)",
    )

    args = parser.parse_args()

    missing = [f for f in args.audio if not os.path.exists(f)]
    if missing:
        parser.error(f"file(s) not found: {', '.join(missing)}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        console.print("[yellow]Using CPU — this may be slow. Install CUDA for GPU acceleration.[/]")
    else:
        console.print(f"[green]Using device: {device.upper()}[/]")

    model = load_model(args.model, device)
    if model is None:
        return

    for file_path in args.audio:
        transcribe_audio(file_path, model, args.language, args.format)

    console.print("\n[bold green]All done![/]")


if __name__ == "__main__":
    main()

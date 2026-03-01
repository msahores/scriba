import os
import warnings
from enum import Enum
from typing import List, Optional

warnings.filterwarnings("ignore")

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()
app = typer.Typer(help="Simple transcription helper powered by Whisper.")


class ModelSize(str, Enum):
    tiny = "tiny"
    base = "base"
    small = "small"
    medium = "medium"
    large = "large"


class OutputFormat(str, Enum):
    txt = "txt"
    srt = "srt"
    vtt = "vtt"


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
    import whisper

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


@app.command()
def main(
    audio: List[str] = typer.Argument(help="Path(s) to the audio file(s) to transcribe"),
    model: ModelSize = typer.Option(ModelSize.small, "--model", "-m", help="Whisper model size"),
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Language code, e.g. 'en', 'es', 'fr' (default: auto-detect)"),
    format: List[OutputFormat] = typer.Option([OutputFormat.txt], "--format", "-f", help="Output format(s): txt, srt, vtt"),
):
    """Simple transcription helper powered by Whisper."""
    missing = [f for f in audio if not os.path.exists(f)]
    if missing:
        console.print(f"[bold red]File(s) not found:[/] {', '.join(missing)}")
        raise typer.Exit(1)

    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        console.print("[yellow]Using CPU — this may be slow. Install CUDA for GPU acceleration.[/]")
    else:
        console.print(f"[green]Using device: {device.upper()}[/]")

    whisper_model = load_model(model.value, device)
    if whisper_model is None:
        raise typer.Exit(1)

    fmt_values = [f.value for f in format]
    for file_path in audio:
        transcribe_audio(file_path, whisper_model, language, fmt_values)

    console.print("\n[bold green]All done![/]")


if __name__ == "__main__":
    app()

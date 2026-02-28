# TODO

## Prioridad alta

- [x] Reemplazar `sys.argv` por `argparse` (con `--help`, `--model`, `--language`, `--output`)
- [x] Agregar archivo `LICENSE` (MIT o similar)
- [ ] Mejorar el README: explicar el valor agregado de Scriba, agregar badges, ejemplo de output
- [x] Eliminar `numpy` de `requirements.txt` (ya es dependencia de `openai-whisper`)

## Features nuevas

- [x] Soporte para múltiples archivos (batch processing)
- [x] Selección de idioma (`--language`)
- [x] Output en múltiples formatos: `.txt`, `.srt`, `.vtt`
- [x] Interfaz más visual con `rich` (progress bar, colores, tablas)

## Nice to have

- [ ] Migrar CLI a `typer` (basado en `rich`, auto-genera `--help` bonito)
- [ ] Agregar un `pyproject.toml` y hacer el paquete instalable con `pip install .`
- [ ] Tests básicos con `pytest`
- [ ] CI con GitHub Actions (lint + tests)

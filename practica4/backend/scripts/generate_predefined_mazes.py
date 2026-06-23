"""
Script de un solo uso: genera los 5 laberintos predefinidos del proyecto.

No forma parte de la API en tiempo de ejecución — se ejecuta manualmente
una vez para producir los archivos estáticos en ``backend/data/mazes/``.
Usa una semilla fija por laberinto para que el resultado sea reproducible
y quede versionado igual siempre, tal como exige el documento de la
práctica ("el sistema deberá incluir al menos 5 laberintos predefinidos").

Uso:
    cd backend/
    source venv/bin/activate
    python scripts/generate_predefined_mazes.py
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.domain.maze_generator import MazeGenerator  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "mazes"

# (archivo, id, nombre, dificultad, cols, rows, semilla)
DEFINICIONES = [
    ("maze_01.json", "claro-del-bosque", "Claro del Bosque", "facil", 6, 6, 101),
    ("maze_02.json", "sendero-del-rio", "Sendero del Río", "facil", 8, 8, 202),
    ("maze_03.json", "cueva-de-musgo", "Cueva de Musgo", "media", 10, 10, 303),
    ("maze_04.json", "bosque-profundo", "Bosque Profundo", "dificil", 14, 14, 404),
    ("maze_05.json", "laberinto-ancestral", "Laberinto Ancestral", "experto", 18, 18, 505),
]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generator = MazeGenerator()

    for filename, maze_id, nombre, dificultad, cols, rows, seed in DEFINICIONES:
        random.seed(seed)
        maze = generator.generate(cols=cols, rows=rows)

        data = {
            "id": maze_id,
            "nombre": nombre,
            "dificultad": dificultad,
            "grid": maze.grid,
            "start": {"row": maze.start.row, "col": maze.start.col},
            "goal": {"row": maze.goal.row, "col": maze.goal.col},
        }

        destino = OUTPUT_DIR / filename
        destino.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Generado {destino} ({maze.rows}x{maze.cols}, dificultad={dificultad})")


if __name__ == "__main__":
    main()

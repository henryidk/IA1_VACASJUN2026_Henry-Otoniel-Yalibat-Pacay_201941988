"""
Dominio: repositorio de laberintos predefinidos.

Carga los laberintos estáticos almacenados en ``backend/data/mazes/``
(un archivo JSON por laberinto) y los expone como objetos de dominio.
No hay base de datos: los laberintos predefinidos viven como archivos
versionados en el propio repositorio.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .maze import Maze, Position

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "mazes"


@dataclass(frozen=True)
class PredefinedMaze:
    """Laberinto predefinido junto con sus metadatos descriptivos."""

    id: str
    nombre: str
    dificultad: str
    maze: Maze


class MazeRepository:
    """Carga y expone los laberintos predefinidos desde disco."""

    def __init__(self, data_dir: Path = _DATA_DIR) -> None:
        self._data_dir = data_dir

    def list_all(self) -> list[PredefinedMaze]:
        """Carga y devuelve todos los laberintos predefinidos, ordenados por archivo."""
        archivos = sorted(self._data_dir.glob("*.json"))
        return [self._load(archivo) for archivo in archivos]

    def get(self, maze_id: str) -> PredefinedMaze | None:
        """Busca un laberinto predefinido por su id; ``None`` si no existe."""
        for predefinido in self.list_all():
            if predefinido.id == maze_id:
                return predefinido
        return None

    @staticmethod
    def _load(path: Path) -> PredefinedMaze:
        data = json.loads(path.read_text(encoding="utf-8"))
        maze = Maze(
            grid=data["grid"],
            start=Position(row=data["start"]["row"], col=data["start"]["col"]),
            goal=Position(row=data["goal"]["row"], col=data["goal"]["col"]),
        )
        return PredefinedMaze(
            id=data["id"],
            nombre=data["nombre"],
            dificultad=data["dificultad"],
            maze=maze,
        )

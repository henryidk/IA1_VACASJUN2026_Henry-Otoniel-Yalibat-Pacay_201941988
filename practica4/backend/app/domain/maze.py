"""
Dominio: entidad Maze.

Representa un laberinto como una cuadrícula bidimensional de celdas abiertas (0)
y muros (1), con una posición de inicio y una de meta.
"""

from __future__ import annotations
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Posición en la cuadrícula
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Position:
    """
    Coordenadas de una celda dentro del laberinto.

    Atributos:
        row: Fila (0 = fila superior).
        col: Columna (0 = columna izquierda).

    Es inmutable y hasheable, por lo que puede usarse en conjuntos
    y como clave de diccionario (útil para los algoritmos de búsqueda).
    """

    row: int
    col: int

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"


# ---------------------------------------------------------------------------
# Laberinto
# ---------------------------------------------------------------------------

class Maze:
    """
    Laberinto representado como una cuadrícula 2-D.

    Convención del grid:
        0 → celda abierta / transitable
        1 → muro / obstáculo

    El origen de coordenadas es la esquina superior-izquierda: (row=0, col=0).
    Los ejes crecen hacia abajo (filas) y hacia la derecha (columnas).

    Ejemplo de grid 5×5::

        1 1 1 1 1
        1 0 0 0 1
        1 0 1 0 1
        1 0 0 0 1
        1 1 1 1 1

    Attributes:
        rows:  Número total de filas de la cuadrícula (incluyendo muros).
        cols:  Número total de columnas de la cuadrícula (incluyendo muros).
        start: Posición de inicio del agente.
        goal:  Posición objetivo.
    """

    # Direcciones ortogonales (arriba, abajo, izquierda, derecha)
    _DIRECTIONS: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(
        self,
        grid: list[list[int]],
        start: Position,
        goal: Position,
    ) -> None:
        """
        Inicializa el laberinto y valida la consistencia de los datos.

        Args:
            grid:  Cuadrícula 2-D de enteros (0 = abierta, 1 = muro).
            start: Posición de inicio.
            goal:  Posición de meta.

        Raises:
            ValueError: Si la cuadrícula está vacía, no es rectangular,
                        o si inicio/meta están fuera de rango o sobre un muro.
        """
        self._validate_grid(grid)

        # Copia defensiva para que modificaciones externas no afecten al objeto
        self._grid: list[list[int]] = [row[:] for row in grid]
        self.rows: int = len(grid)
        self.cols: int = len(grid[0])
        self.start: Position = start
        self.goal: Position = goal

        self._validate_position(start, "inicio")
        self._validate_position(goal, "meta")

        if start == goal:
            raise ValueError(
                "La posición de inicio y la meta no pueden ser la misma celda."
            )

    # ------------------------------------------------------------------
    # Validaciones internas
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_grid(grid: list[list[int]]) -> None:
        if not grid or not grid[0]:
            raise ValueError("La cuadrícula del laberinto no puede estar vacía.")
        expected_cols = len(grid[0])
        if any(len(row) != expected_cols for row in grid):
            raise ValueError(
                "Todas las filas del laberinto deben tener el mismo número de columnas."
            )

    def _validate_position(self, pos: Position, label: str) -> None:
        if not self.in_bounds(pos):
            raise ValueError(
                f"La posición de {label} {pos} está fuera de los límites "
                f"del laberinto ({self.rows} filas × {self.cols} columnas)."
            )
        if self.is_wall(pos):
            raise ValueError(
                f"La posición de {label} {pos} es un muro y no es transitable."
            )

    # ------------------------------------------------------------------
    # Interfaz pública — consultas sobre celdas
    # ------------------------------------------------------------------

    @property
    def grid(self) -> list[list[int]]:
        """Devuelve una copia de la cuadrícula interna."""
        return [row[:] for row in self._grid]

    def in_bounds(self, pos: Position) -> bool:
        """Devuelve True si pos está dentro de los límites de la cuadrícula."""
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def is_wall(self, pos: Position) -> bool:
        """Devuelve True si la celda en pos es un muro."""
        return self._grid[pos.row][pos.col] == 1

    def is_passable(self, pos: Position) -> bool:
        """Devuelve True si pos está dentro de límites y no es un muro."""
        return self.in_bounds(pos) and not self.is_wall(pos)

    def neighbors(self, pos: Position) -> list[Position]:
        """
        Devuelve los vecinos ortogonales transitables de pos
        (arriba, abajo, izquierda, derecha; sin diagonales).
        """
        result: list[Position] = []
        for dr, dc in self._DIRECTIONS:
            neighbor = Position(pos.row + dr, pos.col + dc)
            if self.is_passable(neighbor):
                result.append(neighbor)
        return result

    # ------------------------------------------------------------------
    # Representación
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Maze(rows={self.rows}, cols={self.cols}, "
            f"start={self.start}, goal={self.goal})"
        )

    def to_ascii(self) -> str:
        """
        Devuelve una representación ASCII del laberinto, útil para depuración.

        Leyenda:
            █  muro
            ·  celda abierta
            S  inicio
            G  meta
        """
        symbols = {0: "· ", 1: "█ "}
        lines: list[str] = []
        for r, row in enumerate(self._grid):
            line_parts: list[str] = []
            for c, cell in enumerate(row):
                pos = Position(r, c)
                if pos == self.start:
                    line_parts.append("S ")
                elif pos == self.goal:
                    line_parts.append("G ")
                else:
                    line_parts.append(symbols[cell])
            lines.append("".join(line_parts))
        return "\n".join(lines)

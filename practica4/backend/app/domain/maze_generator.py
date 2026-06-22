"""
Dominio: generador de laberintos aleatorios.

Implementa el algoritmo de *recursive backtracker* (versión iterativa con pila)
para producir laberintos perfectos: toda celda es alcanzable desde cualquier
otra celda, lo que garantiza que siempre existe un camino entre inicio y meta.

Referencia del algoritmo:
    https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search
"""

from __future__ import annotations
import random

from .maze import Maze, Position
from ..core.config import MAZE_MIN_SIZE, MAZE_MAX_SIZE


class MazeGenerator:
    """
    Genera laberintos aleatorios usando el algoritmo iterativo de
    *recursive backtracker* (DFS con pila y «talla» de muros).

    Dimensiones internas del grid:
        - El usuario especifica `cols` y `rows` como el número de celdas
          transitables en cada eje.
        - El grid real tiene dimensiones (2·rows + 1) × (2·cols + 1),
          donde las celdas transitables ocupan posiciones impares y los
          muros las posiciones pares.

    Ejemplo para cols=2, rows=2 (grid 5×5)::

        Celda lógica (0,0) → posición real (1,1)
        Celda lógica (0,1) → posición real (1,3)
        Celda lógica (1,0) → posición real (3,1)
        Celda lógica (1,1) → posición real (3,3)
        Muro entre (0,0)↔(0,1) → posición real (1,2)
        Muro entre (0,0)↔(1,0) → posición real (2,1)

    Start real: (1, 1)  — esquina superior-izquierda
    Goal real : (2·rows−1, 2·cols−1) — esquina inferior-derecha
    """

    def generate(self, cols: int, rows: int) -> Maze:
        """
        Genera y devuelve un laberinto aleatorio perfecto.

        Args:
            cols: Número de celdas transitables en el eje horizontal (5–30).
            rows: Número de celdas transitables en el eje vertical   (5–30).

        Returns:
            Instancia de ``Maze`` con la cuadrícula generada, inicio en la
            esquina superior-izquierda y meta en la esquina inferior-derecha.

        Raises:
            ValueError: Si ``cols`` o ``rows`` están fuera del rango permitido.
        """
        self._validate_size(cols, rows)
        grid = self._carve(cols, rows)

        start = Position(row=1, col=1)
        goal  = Position(row=2 * rows - 1, col=2 * cols - 1)

        return Maze(grid=grid, start=start, goal=goal)

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_size(cols: int, rows: int) -> None:
        for value, name in [(cols, "ancho (cols)"), (rows, "alto (rows)")]:
            if not (MAZE_MIN_SIZE <= value <= MAZE_MAX_SIZE):
                raise ValueError(
                    f"El {name} debe estar entre {MAZE_MIN_SIZE} y "
                    f"{MAZE_MAX_SIZE} celdas; se recibió {value}."
                )

    @staticmethod
    def _carve(cols: int, rows: int) -> list[list[int]]:
        """
        Ejecuta el algoritmo de talla (*carving*) sobre una cuadrícula
        inicialmente llena de muros y devuelve el grid resultante.

        Pasos del algoritmo:
        1. Inicializar el grid con todo 1s (muros).
        2. Abrir la celda de inicio (1, 1).
        3. Empujar (0, 0) en la pila de celdas lógicas visitadas.
        4. Mientras la pila no esté vacía:
           a. Obtener la celda en el tope de la pila.
           b. Listar sus vecinos lógicos no visitados.
           c. Si hay vecinos: elegir uno al azar, «tallar» el muro
              intermedio y la celda vecina, marcarla como visitada
              y empujarla.
           d. Si no hay vecinos: hacer pop (retroceder).
        """
        grid_rows = 2 * rows + 1
        grid_cols = 2 * cols + 1

        # Todo muros
        grid: list[list[int]] = [[1] * grid_cols for _ in range(grid_rows)]

        # Abrir la celda lógica inicial
        grid[1][1] = 0

        visited: set[tuple[int, int]] = {(0, 0)}
        stack:   list[tuple[int, int]] = [(0, 0)]

        # Direcciones ortogonales en el espacio lógico
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            cr, cc = stack[-1]

            # Vecinos lógicos no visitados dentro del rango
            unvisited = [
                (cr + dr, cc + dc)
                for dr, dc in directions
                if 0 <= cr + dr < rows
                and 0 <= cc + dc < cols
                and (cr + dr, cc + dc) not in visited
            ]

            if unvisited:
                nr, nc = random.choice(unvisited)

                # Posición real de la celda vecina
                real_nr = 2 * nr + 1
                real_nc = 2 * nc + 1

                # Posición real del muro entre la celda actual y la vecina
                wall_r = 2 * cr + 1 + (nr - cr)   # cr*2+1 ± 1
                wall_c = 2 * cc + 1 + (nc - cc)   # cc*2+1 ± 1

                # Tallar: abrir el muro y la celda vecina
                grid[wall_r][wall_c] = 0
                grid[real_nr][real_nc] = 0

                visited.add((nr, nc))
                stack.append((nr, nc))
            else:
                stack.pop()

        return grid

"""
Dominio: patrón Strategy para algoritmos de búsqueda.

Define el contrato común (interfaz) que deben implementar todos los
algoritmos de búsqueda (BFS, DFS, y cualquier otro que se agregue en
el futuro). Gracias a este patrón, la capa de servicio puede intercambiar
algoritmos sin conocer sus detalles internos.

Diagrama::

    SearchStrategy (ABC)
    ├── BFSStrategy   → algorithms/bfs.py
    └── DFSStrategy   → algorithms/dfs.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .maze import Maze, Position


# ---------------------------------------------------------------------------
# Resultado de una búsqueda
# ---------------------------------------------------------------------------

@dataclass
class SearchResult:
    """
    Datos producidos por un algoritmo de búsqueda tras ejecutarse.

    Attributes:
        path:
            Lista ordenada de posiciones que forman el camino desde el
            inicio hasta la meta, ambos inclusive.
            ``None`` si no existe ningún camino válido.
        explored:
            Lista de posiciones **en el orden en que fueron visitadas**
            por el algoritmo. Usada por el frontend para animar la
            exploración celda a celda.
        nodes_explored:
            Número total de nodos visitados (equivale a ``len(explored)``).
            Se guarda por separado para facilitar la serialización.
    """

    path:           list[Position] | None
    explored:       list[Position] = field(default_factory=list)
    nodes_explored: int = 0


# ---------------------------------------------------------------------------
# Interfaz común (Strategy)
# ---------------------------------------------------------------------------

class SearchStrategy(ABC):
    """
    Interfaz abstracta para los algoritmos de búsqueda en el laberinto.

    Cada implementación concreta recibe un ``Maze`` y devuelve un
    ``SearchResult`` con la ruta encontrada (si existe) y la secuencia
    de nodos explorados.

    Reglas de implementación:
    - Los algoritmos **no** miden su propio tiempo de ejecución; esa
      responsabilidad recae en la capa de servicio (MazeService).
    - Los algoritmos **no** modifican el ``Maze`` recibido.
    - Si no existe un camino de ``maze.start`` a ``maze.goal``,
      ``SearchResult.path`` debe ser ``None`` (no se lanza excepción).
    """

    @abstractmethod
    def search(self, maze: Maze) -> SearchResult:
        """
        Ejecuta el algoritmo de búsqueda sobre el laberinto dado.

        Args:
            maze: Laberinto sobre el que se ejecuta la búsqueda.
                  Contiene la cuadrícula, la posición de inicio y la meta.

        Returns:
            ``SearchResult`` con la ruta encontrada (o ``None``) y la
            secuencia de nodos explorados.
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre identificador del algoritmo (p. ej. ``'BFS'``)."""

    # ------------------------------------------------------------------
    # Utilidad compartida (heredada por BFS y DFS)
    # ------------------------------------------------------------------

    @staticmethod
    def _reconstruct_path(
        parent: dict[Position, Position | None],
        goal: Position,
    ) -> list[Position]:
        """
        Reconstruye el camino desde el inicio hasta ``goal`` siguiendo
        el diccionario de padres hacia atrás.

        Args:
            parent: Mapeo nodo → predecesor en el árbol de búsqueda.
                    El nodo raíz (inicio) tiene ``None`` como predecesor.
            goal:   Nodo destino desde el que se inicia la reconstrucción.

        Returns:
            Lista de posiciones ordenada de inicio a meta (ambos inclusive).
        """
        path: list[Position] = []
        current: Position | None = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

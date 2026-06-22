"""
Algoritmo de búsqueda: Breadth-First Search (BFS).

BFS explora el laberinto nivel por nivel usando una cola FIFO.
Garantiza encontrar el **camino más corto** (en número de celdas)
entre el inicio y la meta en grafos no ponderados como este laberinto.

Complejidad:
    Tiempo:  O(V + E)  donde V = celdas transitables, E = conexiones entre ellas.
    Espacio: O(V)      para la cola, el conjunto de visitados y el diccionario de padres.
"""

from __future__ import annotations

from collections import deque

from ..domain.maze import Maze, Position
from ..domain.search_strategy import SearchResult, SearchStrategy


class BFSStrategy(SearchStrategy):
    """
    Implementación de Breadth-First Search como estrategia de búsqueda.

    Proceso:
    1. Encolar el nodo de inicio; marcarlo como visitado.
    2. Mientras la cola no esté vacía:
       a. Desencolar el nodo actual; añadirlo a ``explored``.
       b. Si es la meta → reconstruir y devolver el camino.
       c. Para cada vecino transitable no visitado:
          - Marcarlo como visitado.
          - Registrar su predecesor en ``parent``.
          - Encolarlo.
    3. Si la cola se vacía sin encontrar la meta → devolver ``path=None``.

    Propiedad clave: al usar una cola FIFO, el primer camino encontrado
    hasta la meta es siempre el de menor longitud.
    """

    @property
    def name(self) -> str:
        return "BFS"

    def search(self, maze: Maze) -> SearchResult:
        """
        Ejecuta BFS desde ``maze.start`` hasta ``maze.goal``.

        Args:
            maze: Laberinto sobre el que se realiza la búsqueda.

        Returns:
            ``SearchResult`` con:
            - ``path``: camino más corto de inicio a meta, o ``None``.
            - ``explored``: nodos visitados en orden de exploración BFS.
            - ``nodes_explored``: total de nodos visitados.
        """
        start: Position = maze.start
        goal:  Position = maze.goal

        # Cola FIFO
        queue: deque[Position] = deque([start])

        # Nodos ya visitados (evita procesar el mismo nodo dos veces)
        visited: set[Position] = {start}

        # Predecesor de cada nodo en el árbol BFS; inicio tiene None
        parent: dict[Position, Position | None] = {start: None}

        # Secuencia de exploración para la animación del frontend
        explored: list[Position] = []

        while queue:
            current = queue.popleft()
            explored.append(current)

            if current == goal:
                path = self._reconstruct_path(parent, goal)
                return SearchResult(
                    path=path,
                    explored=explored,
                    nodes_explored=len(explored),
                )

            for neighbor in maze.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        # Cola vacía: no existe camino entre inicio y meta
        return SearchResult(
            path=None,
            explored=explored,
            nodes_explored=len(explored),
        )

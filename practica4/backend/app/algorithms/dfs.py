"""
Algoritmo de búsqueda: Depth-First Search (DFS).

DFS explora el laberinto en profundidad usando una pila LIFO.
**No** garantiza encontrar el camino más corto, pero generalmente
explora menos nodos que BFS en laberintos con caminos largos y
pocos ramales.

Implementación iterativa (pila explícita) para evitar el límite
de recursión de Python en laberintos grandes.

Complejidad:
    Tiempo:  O(V + E)  donde V = celdas transitables, E = conexiones.
    Espacio: O(V)      para la pila, el conjunto de visitados y los padres.
"""

from __future__ import annotations

from ..domain.maze import Maze, Position
from ..domain.search_strategy import SearchResult, SearchStrategy


class DFSStrategy(SearchStrategy):
    """
    Implementación de Depth-First Search como estrategia de búsqueda.

    La pila almacena tuplas ``(posición, padre)`` para poder reconstruir
    el camino correcto incluso cuando un nodo es alcanzado por múltiples
    rutas antes de ser visitado.

    Proceso:
    1. Apilar ``(inicio, None)``; conjunto de visitados vacío.
    2. Mientras la pila no esté vacía:
       a. Desapilar ``(actual, padre)``.
       b. Si ``actual`` ya fue visitado → saltar (puede estar duplicado).
       c. Marcar ``actual`` como visitado; registrar su padre; añadirlo
          a ``explored``.
       d. Si es la meta → reconstruir y devolver el camino.
       e. Apilar todos los vecinos transitables no visitados (con ``actual``
          como padre), sin marcarlos como visitados todavía.
    3. Si la pila se vacía sin encontrar la meta → devolver ``path=None``.

    Nota sobre el orden de exploración:
        En DFS iterativo, el vecino que se desapila primero es el **último**
        que se apiló. Para conservar el orden natural (arriba, abajo,
        izquierda, derecha definido en ``Maze._DIRECTIONS``), los vecinos
        se apilan en **orden inverso** de forma que el primero de la lista
        sea el primero en desapilarse.
    """

    @property
    def name(self) -> str:
        return "DFS"

    def search(self, maze: Maze) -> SearchResult:
        """
        Ejecuta DFS desde ``maze.start`` hasta ``maze.goal``.

        Args:
            maze: Laberinto sobre el que se realiza la búsqueda.

        Returns:
            ``SearchResult`` con:
            - ``path``: camino encontrado de inicio a meta, o ``None``.
            - ``explored``: nodos visitados en orden de exploración DFS.
            - ``nodes_explored``: total de nodos visitados.
        """
        start: Position = maze.start
        goal:  Position = maze.goal

        # Pila LIFO; cada elemento es (posición, padre)
        stack: list[tuple[Position, Position | None]] = [(start, None)]

        # Nodos ya visitados (procesados al desapilar)
        visited: set[Position] = set()

        # Predecesor de cada nodo en el árbol DFS
        parent: dict[Position, Position | None] = {}

        # Secuencia de exploración para la animación del frontend
        explored: list[Position] = []

        while stack:
            current, par = stack.pop()

            # Un nodo puede estar en la pila más de una vez;
            # lo ignoramos si ya fue procesado
            if current in visited:
                continue

            visited.add(current)
            parent[current] = par
            explored.append(current)

            if current == goal:
                path = self._reconstruct_path(parent, goal)
                return SearchResult(
                    path=path,
                    explored=explored,
                    nodes_explored=len(explored),
                )

            # Apilar vecinos en orden inverso para que el «primero natural»
            # sea el primero en desapilarse (comportamiento DFS predecible)
            for neighbor in reversed(maze.neighbors(current)):
                if neighbor not in visited:
                    stack.append((neighbor, current))

        # Pila vacía: no existe camino entre inicio y meta
        return SearchResult(
            path=None,
            explored=explored,
            nodes_explored=len(explored),
        )

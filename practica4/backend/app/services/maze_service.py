"""
Capa de servicio: orquestación de búsquedas en laberintos.

MazeService actúa como intermediario entre la capa API y los algoritmos
de búsqueda. Sus responsabilidades son:

1. Seleccionar la estrategia de búsqueda correcta (BFS o DFS) según lo
   que pida el cliente.
2. Medir el tiempo de ejecución con alta precisión (time.perf_counter).
3. Empaquetar el resultado en un objeto uniforme que la API pueda
   serializar sin conocer los detalles internos de cada algoritmo.
4. Manejar explícitamente el caso «sin ruta válida» con un mensaje
   descriptivo en lugar de lanzar una excepción genérica.

El servicio es independiente del transporte HTTP: no conoce FastAPI,
requests ni responses — solo trabaja con objetos de dominio (Maze,
Position) y devuelve dataclasses serializables.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from ..algorithms.bfs import BFSStrategy
from ..algorithms.dfs import DFSStrategy
from ..domain.maze import Maze, Position
from ..domain.search_strategy import SearchStrategy


# ---------------------------------------------------------------------------
# Resultado del servicio
# ---------------------------------------------------------------------------

@dataclass
class BusquedaResult:
    """
    Resultado completo de una ejecución de búsqueda, listo para serializar.

    Attributes:
        algoritmo:       Nombre del algoritmo usado (``'BFS'`` o ``'DFS'``).
        encontrado:      ``True`` si existe una ruta de inicio a meta.
        ruta:            Lista ordenada de posiciones del camino encontrado,
                         o ``None`` si no existe camino.
        explorados:      Posiciones en el **orden exacto** en que fueron
                         visitadas por el algoritmo (usado para animación).
        nodos_explorados: Número total de nodos visitados.
        tiempo_ms:       Tiempo de ejecución del algoritmo en milisegundos.
        mensaje:         Descripción legible del resultado (útil para la UI).
    """

    algoritmo:        str
    encontrado:       bool
    ruta:             list[Position] | None
    explorados:       list[Position]   = field(default_factory=list)
    nodos_explorados: int              = 0
    tiempo_ms:        float            = 0.0
    mensaje:          str              = ""


# ---------------------------------------------------------------------------
# Servicio
# ---------------------------------------------------------------------------

# Algoritmos disponibles (instanciados una sola vez; son stateless)
_STRATEGIES: dict[str, SearchStrategy] = {
    "BFS": BFSStrategy(),
    "DFS": DFSStrategy(),
}

# Nombres válidos como conjunto para validación rápida
ALGORITMOS_DISPONIBLES: frozenset[str] = frozenset(_STRATEGIES)


class MazeService:
    """
    Servicio de búsqueda de rutas en laberintos.

    Orquesta la selección del algoritmo, la ejecución cronometrada y
    el empaquetado del resultado — incluyendo el caso «sin ruta válida».
    """

    # ------------------------------------------------------------------
    # Búsqueda individual
    # ------------------------------------------------------------------

    def buscar(self, maze: Maze, algoritmo: str) -> BusquedaResult:
        """
        Ejecuta el algoritmo indicado sobre el laberinto y devuelve el resultado.

        Args:
            maze:      Laberinto con cuadrícula, inicio y meta ya definidos.
            algoritmo: Nombre del algoritmo a usar: ``'BFS'`` o ``'DFS'``.

        Returns:
            ``BusquedaResult`` con ruta (o ``None``), nodos explorados,
            tiempo de ejecución y mensaje descriptivo.

        Raises:
            ValueError: Si ``algoritmo`` no es un valor reconocido.
        """
        strategy = self._seleccionar_estrategia(algoritmo)

        # --- Cronometraje de alta precisión ---
        t_inicio = time.perf_counter()
        search_result = strategy.search(maze)
        t_fin = time.perf_counter()

        tiempo_ms = round((t_fin - t_inicio) * 1_000, 4)

        # --- Construir resultado ---
        encontrado = search_result.path is not None
        mensaje = (
            f"Ruta encontrada: {len(search_result.path)} celdas."
            if encontrado
            else self._diagnosticar_sin_ruta(maze)
        )

        return BusquedaResult(
            algoritmo=algoritmo,
            encontrado=encontrado,
            ruta=search_result.path,
            explorados=search_result.explored,
            nodos_explorados=search_result.nodes_explored,
            tiempo_ms=tiempo_ms,
            mensaje=mensaje,
        )

    # ------------------------------------------------------------------
    # Comparación BFS vs DFS
    # ------------------------------------------------------------------

    def comparar(self, maze: Maze) -> dict[str, BusquedaResult]:
        """
        Ejecuta BFS y DFS sobre el mismo laberinto y devuelve ambos resultados.

        Ambos algoritmos reciben exactamente el mismo ``Maze``, de manera
        que los números de nodos explorados y tiempos son comparables.

        Args:
            maze: Laberinto sobre el que se ejecutan ambos algoritmos.

        Returns:
            Diccionario ``{'BFS': BusquedaResult, 'DFS': BusquedaResult}``.
        """
        return {alg: self.buscar(maze, alg) for alg in ("BFS", "DFS")}

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    @staticmethod
    def _diagnosticar_sin_ruta(maze: Maze) -> str:
        """
        Genera un mensaje descriptivo cuando el algoritmo no encontró ruta.

        Inspecciona el laberinto para distinguir entre tres casos:
        - El inicio no tiene vecinos transitables (rodeado de muros).
        - La meta no tiene vecinos transitables (rodeada de muros).
        - Existe camino desde el inicio pero no llega a la meta
          (laberinto desconectado por obstáculos manuales).

        Args:
            maze: Laberinto sobre el que falló la búsqueda.

        Returns:
            Mensaje descriptivo del motivo por el que no se encontró ruta.
        """
        if not maze.neighbors(maze.start):
            return (
                f"La posición de inicio {maze.start} está rodeada de muros "
                "y no tiene ninguna celda adyacente transitable."
            )
        if not maze.neighbors(maze.goal):
            return (
                f"La posición de meta {maze.goal} está rodeada de muros "
                "y no tiene ninguna celda adyacente transitable."
            )
        return (
            "No existe una ruta válida entre el inicio y la meta. "
            "Los obstáculos colocados desconectan ambas posiciones."
        )

    @staticmethod
    def _seleccionar_estrategia(algoritmo: str) -> SearchStrategy:
        """
        Devuelve la estrategia correspondiente al nombre dado.

        Raises:
            ValueError: Si el nombre no corresponde a ningún algoritmo registrado.
        """
        key = algoritmo.upper()
        if key not in _STRATEGIES:
            disponibles = ", ".join(sorted(_STRATEGIES))
            raise ValueError(
                f"Algoritmo '{algoritmo}' no reconocido. "
                f"Opciones disponibles: {disponibles}."
            )
        return _STRATEGIES[key]

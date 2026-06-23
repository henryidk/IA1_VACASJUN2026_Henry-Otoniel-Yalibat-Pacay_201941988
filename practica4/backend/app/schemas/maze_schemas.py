"""
Schemas Pydantic para request/response de laberintos y búsquedas.

Define los modelos de entrada y salida que FastAPI usa para validar
y serializar los datos entre el cliente y la API.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from ..core.config import (
    MAZE_DEFAULT_HEIGHT,
    MAZE_DEFAULT_WIDTH,
    MAZE_MAX_SIZE,
    MAZE_MIN_SIZE,
)


# ---------------------------------------------------------------------------
# Modelos compartidos
# ---------------------------------------------------------------------------

class PositionSchema(BaseModel):
    """Coordenadas de una celda en la cuadrícula del laberinto."""

    row: int = Field(..., description="Índice de fila (0 = fila superior).")
    col: int = Field(..., description="Índice de columna (0 = columna izquierda).")


# ---------------------------------------------------------------------------
# Generación de laberintos
# ---------------------------------------------------------------------------

class MazeRandomRequest(BaseModel):
    """
    Parámetros para generar un laberinto aleatorio.

    `cols` y `rows` representan el número de **celdas transitables**
    en cada eje — no el tamaño total del grid con muros.
    El grid real tendrá dimensiones (2·rows + 1) × (2·cols + 1).
    """

    cols: int = Field(
        default=MAZE_DEFAULT_WIDTH,
        ge=MAZE_MIN_SIZE,
        le=MAZE_MAX_SIZE,
        description=(
            f"Número de celdas transitables en el eje horizontal "
            f"({MAZE_MIN_SIZE}–{MAZE_MAX_SIZE})."
        ),
    )
    rows: int = Field(
        default=MAZE_DEFAULT_HEIGHT,
        ge=MAZE_MIN_SIZE,
        le=MAZE_MAX_SIZE,
        description=(
            f"Número de celdas transitables en el eje vertical "
            f"({MAZE_MIN_SIZE}–{MAZE_MAX_SIZE})."
        ),
    )


class MazeResponse(BaseModel):
    """
    Representación completa de un laberinto lista para enviar al cliente.

    Attributes:
        grid:  Cuadrícula 2-D (0 = abierta, 1 = muro).
        start: Posición de inicio del agente en el grid real.
        goal:  Posición objetivo en el grid real.
        rows:  Número de filas del grid real (incluyendo muros).
        cols:  Número de columnas del grid real (incluyendo muros).
    """

    grid:  list[list[int]]
    start: PositionSchema
    goal:  PositionSchema
    rows:  int
    cols:  int


# ---------------------------------------------------------------------------
# Búsqueda de rutas
# ---------------------------------------------------------------------------

class SearchRequest(BaseModel):
    """
    Parámetros para ejecutar un algoritmo de búsqueda sobre un laberinto.

    El cliente envía la cuadrícula completa junto con las posiciones de
    inicio y meta, y selecciona el algoritmo que desea ejecutar.
    """

    grid:      list[list[int]] = Field(..., description="Cuadrícula 2-D del laberinto (0=abierta, 1=muro).")
    start:     PositionSchema  = Field(..., description="Posición de inicio del agente.")
    goal:      PositionSchema  = Field(..., description="Posición objetivo.")
    algoritmo: Literal["BFS", "DFS"] = Field(
        ...,
        description="Algoritmo de búsqueda a usar: 'BFS' (anchura) o 'DFS' (profundidad).",
    )


class SearchResponse(BaseModel):
    """
    Resultado de la ejecución de un algoritmo de búsqueda.

    Attributes:
        algoritmo:        Nombre del algoritmo ejecutado.
        encontrado:       ``True`` si existe ruta de inicio a meta.
        ruta:             Lista de posiciones del camino, o ``None``.
        explorados:       Nodos visitados en orden de exploración (para animación).
        nodos_explorados: Total de nodos visitados.
        tiempo_ms:        Tiempo de ejecución en milisegundos.
        mensaje:          Descripción legible del resultado.
    """

    algoritmo:        str
    encontrado:       bool
    ruta:             list[PositionSchema] | None
    explorados:       list[PositionSchema]
    nodos_explorados: int
    tiempo_ms:        float
    mensaje:          str


# ---------------------------------------------------------------------------
# Comparación BFS vs DFS
# ---------------------------------------------------------------------------

class CompareRequest(BaseModel):
    """
    Parámetros para comparar BFS y DFS sobre el mismo laberinto.

    Igual que ``SearchRequest`` pero sin campo ``algoritmo``,
    ya que el endpoint ejecuta ambos automáticamente.
    """

    grid:  list[list[int]] = Field(..., description="Cuadrícula 2-D del laberinto (0=abierta, 1=muro).")
    start: PositionSchema  = Field(..., description="Posición de inicio del agente.")
    goal:  PositionSchema  = Field(..., description="Posición objetivo.")


class CompareResponse(BaseModel):
    """
    Resultado de ejecutar BFS y DFS sobre el mismo laberinto.

    Permite comparar directamente las métricas de ambos algoritmos:
    longitud de ruta, nodos explorados y tiempo de ejecución.
    """

    bfs: SearchResponse
    dfs: SearchResponse

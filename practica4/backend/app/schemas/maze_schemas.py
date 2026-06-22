"""
Schemas Pydantic para request/response de laberintos.

Define los modelos de entrada y salida que FastAPI usa para validar
y serializar los datos entre el cliente y la API.
"""

from __future__ import annotations

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

"""
Router de laberintos.

Expone el endpoint POST /api/mazes/random para generar
laberintos aleatorios bajo demanda.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ...domain.maze_generator import MazeGenerator
from ...schemas.maze_schemas import MazeRandomRequest, MazeResponse, PositionSchema

router = APIRouter()
_generator = MazeGenerator()


@router.post(
    "/random",
    response_model=MazeResponse,
    summary="Generar un laberinto aleatorio",
    description=(
        "Genera un laberinto perfecto utilizando el algoritmo *recursive backtracker*. "
        "El laberinto garantiza que siempre existe al menos un camino entre el inicio y la meta. "
        "No se persiste ningún dato en el servidor — el laberinto vive únicamente en la respuesta."
    ),
    status_code=status.HTTP_200_OK,
)
def generate_random_maze(request: MazeRandomRequest) -> MazeResponse:
    """
    Genera y devuelve un laberinto aleatorio con las dimensiones indicadas.

    - **cols**: número de celdas transitables en el eje horizontal (5–30).
    - **rows**: número de celdas transitables en el eje vertical (5–30).

    El grid devuelto tiene dimensiones reales **(2·rows + 1) × (2·cols + 1)**,
    donde las celdas transitables están en posiciones impares y los muros
    en posiciones pares.
    """
    try:
        maze = _generator.generate(cols=request.cols, rows=request.rows)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return MazeResponse(
        grid=maze.grid,
        start=PositionSchema(row=maze.start.row, col=maze.start.col),
        goal=PositionSchema(row=maze.goal.row, col=maze.goal.col),
        rows=maze.rows,
        cols=maze.cols,
    )

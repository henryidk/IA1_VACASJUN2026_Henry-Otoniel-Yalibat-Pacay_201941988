"""
Router de laberintos.

Expone:
    GET  /api/mazes         — lista los laberintos predefinidos (mínimo 5).
    GET  /api/mazes/{id}    — obtiene un laberinto predefinido completo.
    POST /api/mazes/random  — genera un laberinto aleatorio bajo demanda.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ...domain.maze_generator import MazeGenerator
from ...domain.maze_repository import MazeRepository
from ...schemas.maze_schemas import (
    MazeRandomRequest,
    MazeResponse,
    MazeSummary,
    PositionSchema,
    PredefinedMazeResponse,
)

router = APIRouter()
_generator = MazeGenerator()
_repository = MazeRepository()


@router.get(
    "",
    response_model=list[MazeSummary],
    summary="Listar laberintos predefinidos",
    description=(
        "Devuelve los metadatos de los laberintos predefinidos disponibles "
        "(id, nombre, dificultad y tamaño), sin la cuadrícula completa."
    ),
)
def listar_laberintos() -> list[MazeSummary]:
    return [
        MazeSummary(
            id=predefinido.id,
            nombre=predefinido.nombre,
            dificultad=predefinido.dificultad,
            rows=predefinido.maze.rows,
            cols=predefinido.maze.cols,
        )
        for predefinido in _repository.list_all()
    ]


@router.get(
    "/{maze_id}",
    response_model=PredefinedMazeResponse,
    summary="Obtener un laberinto predefinido",
    description="Devuelve la cuadrícula completa de un laberinto predefinido por su id.",
)
def obtener_laberinto(maze_id: str) -> PredefinedMazeResponse:
    predefinido = _repository.get(maze_id)
    if predefinido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un laberinto predefinido con id '{maze_id}'.",
        )

    maze = predefinido.maze
    return PredefinedMazeResponse(
        id=predefinido.id,
        nombre=predefinido.nombre,
        dificultad=predefinido.dificultad,
        rows=maze.rows,
        cols=maze.cols,
        grid=maze.grid,
        start=PositionSchema(row=maze.start.row, col=maze.start.col),
        goal=PositionSchema(row=maze.goal.row, col=maze.goal.col),
    )


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

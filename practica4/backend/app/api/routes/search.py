"""
Router de búsqueda de rutas.

Expone los endpoints para ejecutar BFS o DFS sobre un laberinto
recibido directamente en el cuerpo de la petición.

Endpoints:
    POST /api/search          — ejecuta un algoritmo seleccionado.
    POST /api/search/compare  — ejecuta BFS y DFS y devuelve ambos resultados.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ...domain.maze import Maze, Position
from ...schemas.maze_schemas import (
    CompareResponse,
    PositionSchema,
    SearchRequest,
    SearchResponse,
)
from ...services.maze_service import BusquedaResult, MazeService

router = APIRouter()
_service = MazeService()


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _build_maze(grid: list[list[int]], start: PositionSchema, goal: PositionSchema) -> Maze:
    """
    Construye un objeto ``Maze`` desde los datos recibidos en la petición.

    Raises:
        HTTPException(400): Si la cuadrícula o las posiciones son inválidas.
    """
    try:
        return Maze(
            grid=grid,
            start=Position(row=start.row, col=start.col),
            goal=Position(row=goal.row, col=goal.col),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


def _to_response(result: BusquedaResult) -> SearchResponse:
    """Convierte un ``BusquedaResult`` del servicio al schema de respuesta."""
    return SearchResponse(
        algoritmo=result.algoritmo,
        encontrado=result.encontrado,
        ruta=(
            [PositionSchema(row=p.row, col=p.col) for p in result.ruta]
            if result.ruta is not None
            else None
        ),
        explorados=[PositionSchema(row=p.row, col=p.col) for p in result.explorados],
        nodos_explorados=result.nodos_explorados,
        tiempo_ms=result.tiempo_ms,
        mensaje=result.mensaje,
    )


# ---------------------------------------------------------------------------
# POST /api/search
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=SearchResponse,
    summary="Ejecutar un algoritmo de búsqueda",
    description=(
        "Recibe la cuadrícula completa del laberinto, las posiciones de inicio y meta, "
        "y el nombre del algoritmo (`'BFS'` o `'DFS'`). Devuelve la ruta encontrada "
        "(si existe), la secuencia de nodos explorados para animación, "
        "el total de nodos visitados y el tiempo de ejecución."
    ),
    status_code=status.HTTP_200_OK,
)
def buscar(request: SearchRequest) -> SearchResponse:
    """
    Ejecuta BFS o DFS sobre el laberinto proporcionado.

    - **grid**: cuadrícula 2-D (0 = celda abierta, 1 = muro).
    - **start**: posición de inicio ``{row, col}``.
    - **goal**: posición objetivo ``{row, col}``.
    - **algoritmo**: ``'BFS'`` o ``'DFS'``.
    """
    maze = _build_maze(request.grid, request.start, request.goal)

    try:
        result = _service.buscar(maze, request.algoritmo)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _to_response(result)

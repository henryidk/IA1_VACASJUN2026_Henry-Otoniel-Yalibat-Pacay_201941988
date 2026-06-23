"""
App factory de RoboMaze.

Crea la instancia de FastAPI, registra los routers de la API
y sirve el frontend como archivos estáticos desde el mismo proceso,
eliminando la necesidad de un segundo servidor.

Uso:
    cd backend/
    source venv/bin/activate
    uvicorn app.main:app --reload

Luego abrir http://localhost:8000 en el navegador.
La documentación interactiva de la API estará en http://localhost:8000/docs
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import API_DESCRIPTION, API_TITLE, API_VERSION
from .api.routes import mazes, search

# ---------------------------------------------------------------------------
# Rutas de archivos
# ---------------------------------------------------------------------------

# main.py está en backend/app/ → subir dos niveles llega a practica4/
_PRACTICA_ROOT = Path(__file__).parent.parent.parent
_FRONTEND_DIR  = _PRACTICA_ROOT / "frontend"

# ---------------------------------------------------------------------------
# Aplicación
# ---------------------------------------------------------------------------

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — permite que el frontend en cualquier origen llame a la API
# (útil durante desarrollo; en producción se restringiría al dominio real)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers de la API
# ---------------------------------------------------------------------------

app.include_router(
    mazes.router,
    prefix="/api/mazes",
    tags=["Laberintos"],
)
app.include_router(
    search.router,
    prefix="/api/search",
    tags=["B\u00fasqueda"],
)

# ---------------------------------------------------------------------------
# Frontend estático
# ---------------------------------------------------------------------------
# Se monta DESPUÉS de los routers para que las rutas /api/* tengan prioridad.

if _FRONTEND_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(_FRONTEND_DIR), html=True),
        name="frontend",
    )

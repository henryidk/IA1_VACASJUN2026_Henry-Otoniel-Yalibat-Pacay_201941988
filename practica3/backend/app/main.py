import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, bitacora, facturas, proveedores

logger = logging.getLogger("smartinvoice")

app = FastAPI(title="SmartInvoice API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(proveedores.router)
app.include_router(facturas.router)
app.include_router(bitacora.router)


@app.exception_handler(Exception)
async def manejador_errores_no_controlados(request: Request, exc: Exception):
    logger.exception("Error no controlado en %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})


@app.get("/health")
def health_check():
    return {"status": "ok"}

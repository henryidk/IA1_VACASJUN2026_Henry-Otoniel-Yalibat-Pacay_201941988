import io
from datetime import date

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.reporte import FormatoReporte
from app.models.usuario import Usuario
from app.services.factura import listar_facturas
from app.services.reportes import generar_reporte_excel, generar_reporte_pdf, registrar_reporte

router = APIRouter(
    prefix="/api/reportes",
    tags=["reportes"],
    dependencies=[Depends(get_current_user)],
)


def _filtros_dict(estado, proveedor_id, fecha_desde, fecha_hasta) -> dict:
    return {
        "estado": estado,
        "proveedor_id": proveedor_id,
        "fecha_desde": fecha_desde.isoformat() if fecha_desde else None,
        "fecha_hasta": fecha_hasta.isoformat() if fecha_hasta else None,
    }


@router.get("/pdf")
def reporte_pdf(
    estado: str | None = None,
    proveedor_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    facturas = listar_facturas(
        db, estado=estado, proveedor_id=proveedor_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta
    )
    contenido = generar_reporte_pdf(facturas)
    registrar_reporte(
        db, usuario_actual.id, FormatoReporte.PDF, _filtros_dict(estado, proveedor_id, fecha_desde, fecha_hasta)
    )
    return StreamingResponse(
        io.BytesIO(contenido),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_facturas.pdf"},
    )


@router.get("/excel")
def reporte_excel(
    estado: str | None = None,
    proveedor_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    facturas = listar_facturas(
        db, estado=estado, proveedor_id=proveedor_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta
    )
    contenido = generar_reporte_excel(facturas)
    registrar_reporte(
        db, usuario_actual.id, FormatoReporte.EXCEL, _filtros_dict(estado, proveedor_id, fecha_desde, fecha_hasta)
    )
    return StreamingResponse(
        io.BytesIO(contenido),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_facturas.xlsx"},
    )

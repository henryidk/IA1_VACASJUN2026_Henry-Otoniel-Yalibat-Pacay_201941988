from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.bitacora import BitacoraOut
from app.services.bitacora import listar_bitacora

router = APIRouter(
    prefix="/api/bitacora",
    tags=["bitacora"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[BitacoraOut])
def listar(
    usuario_id: int | None = None,
    estado: str | None = None,
    factura_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    db: Session = Depends(get_db),
):
    return listar_bitacora(
        db,
        usuario_id=usuario_id,
        estado=estado,
        factura_id=factura_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )

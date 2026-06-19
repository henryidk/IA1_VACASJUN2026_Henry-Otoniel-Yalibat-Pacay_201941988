from sqlalchemy.orm import Session

from app.models.bitacora import Bitacora


def registrar_evento(
    db: Session,
    *,
    factura_id: int | None,
    usuario_id: int | None,
    tipo_evento: str,
    estado: str,
    documento: str | None = None,
    resultado: str | None = None,
) -> Bitacora:
    evento = Bitacora(
        factura_id=factura_id,
        usuario_id=usuario_id,
        tipo_evento=tipo_evento,
        documento=documento,
        estado=estado,
        resultado=resultado,
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

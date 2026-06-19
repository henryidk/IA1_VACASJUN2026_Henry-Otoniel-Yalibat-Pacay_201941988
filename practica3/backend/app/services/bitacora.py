from datetime import date

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


def listar_bitacora(
    db: Session,
    usuario_id: int | None = None,
    estado: str | None = None,
    factura_id: int | None = None,
    tipo_evento: str | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
) -> list[Bitacora]:
    query = db.query(Bitacora)
    if usuario_id:
        query = query.filter(Bitacora.usuario_id == usuario_id)
    if estado:
        query = query.filter(Bitacora.estado == estado)
    if factura_id:
        query = query.filter(Bitacora.factura_id == factura_id)
    if tipo_evento:
        query = query.filter(Bitacora.tipo_evento == tipo_evento)
    if fecha_desde:
        query = query.filter(Bitacora.fecha_hora >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Bitacora.fecha_hora <= fecha_hasta)
    return query.order_by(Bitacora.fecha_hora.desc()).all()

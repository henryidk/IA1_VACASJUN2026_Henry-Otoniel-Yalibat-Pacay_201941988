from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.factura import Factura

EXTENSIONES_PERMITIDAS = {".pdf", ".jpg", ".jpeg", ".png"}


def extension_valida(nombre_archivo: str) -> bool:
    return Path(nombre_archivo).suffix.lower() in EXTENSIONES_PERMITIDAS


def listar_facturas(
    db: Session,
    estado: str | None = None,
    proveedor_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
) -> list[Factura]:
    query = db.query(Factura)
    if estado:
        query = query.filter(Factura.estado == estado)
    if proveedor_id:
        query = query.filter(Factura.proveedor_id == proveedor_id)
    if fecha_desde:
        query = query.filter(Factura.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Factura.fecha <= fecha_hasta)
    return query.order_by(Factura.creado_en.desc()).all()


def crear_factura(db: Session, nombre_archivo: str, usuario_id: int) -> Factura:
    factura = Factura(nombre_archivo=nombre_archivo, usuario_id=usuario_id)
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


def obtener_factura(db: Session, factura_id: int) -> Factura | None:
    return db.query(Factura).filter(Factura.id == factura_id).first()


def actualizar_campos_factura(db: Session, factura: Factura, cambios: dict) -> Factura:
    for campo, valor in cambios.items():
        setattr(factura, campo, valor)
    db.commit()
    db.refresh(factura)
    return factura

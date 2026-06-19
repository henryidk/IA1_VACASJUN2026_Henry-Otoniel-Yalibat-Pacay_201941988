from pathlib import Path

from sqlalchemy.orm import Session

from app.models.factura import Factura

EXTENSIONES_PERMITIDAS = {".pdf", ".jpg", ".jpeg", ".png"}


def extension_valida(nombre_archivo: str) -> bool:
    return Path(nombre_archivo).suffix.lower() in EXTENSIONES_PERMITIDAS


def crear_factura(db: Session, nombre_archivo: str, usuario_id: int) -> Factura:
    factura = Factura(nombre_archivo=nombre_archivo, usuario_id=usuario_id)
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


def obtener_factura(db: Session, factura_id: int) -> Factura | None:
    return db.query(Factura).filter(Factura.id == factura_id).first()

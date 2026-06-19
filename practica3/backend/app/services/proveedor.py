from sqlalchemy.orm import Session

from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate


def listar_proveedores(db: Session) -> list[Proveedor]:
    return db.query(Proveedor).order_by(Proveedor.nombre).all()


def obtener_proveedor(db: Session, proveedor_id: int) -> Proveedor | None:
    return db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()


def obtener_por_nit(db: Session, nit: str) -> Proveedor | None:
    return db.query(Proveedor).filter(Proveedor.nit == nit).first()


def crear_proveedor(db: Session, datos: ProveedorCreate) -> Proveedor:
    proveedor = Proveedor(**datos.model_dump())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


def actualizar_proveedor(db: Session, proveedor: Proveedor, datos: ProveedorUpdate) -> Proveedor:
    for campo, valor in datos.model_dump().items():
        setattr(proveedor, campo, valor)
    db.commit()
    db.refresh(proveedor)
    return proveedor


def eliminar_proveedor(db: Session, proveedor: Proveedor) -> None:
    db.delete(proveedor)
    db.commit()

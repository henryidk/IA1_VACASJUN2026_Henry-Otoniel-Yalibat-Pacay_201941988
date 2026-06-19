from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.proveedor import ProveedorCreate, ProveedorOut, ProveedorUpdate
from app.services.proveedor import (
    actualizar_proveedor,
    crear_proveedor,
    eliminar_proveedor,
    listar_proveedores,
    obtener_por_nit,
    obtener_proveedor,
)

router = APIRouter(
    prefix="/api/proveedores",
    tags=["proveedores"],
    dependencies=[Depends(get_current_user)],
)


def _obtener_o_404(db: Session, proveedor_id: int):
    proveedor = obtener_proveedor(db, proveedor_id)
    if proveedor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")
    return proveedor


@router.get("", response_model=list[ProveedorOut])
def listar(db: Session = Depends(get_db)):
    return listar_proveedores(db)


@router.get("/{proveedor_id}", response_model=ProveedorOut)
def obtener(proveedor_id: int, db: Session = Depends(get_db)):
    return _obtener_o_404(db, proveedor_id)


@router.post("", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED)
def crear(datos: ProveedorCreate, db: Session = Depends(get_db)):
    if obtener_por_nit(db, datos.nit) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un proveedor con ese NIT")
    return crear_proveedor(db, datos)


@router.put("/{proveedor_id}", response_model=ProveedorOut)
def actualizar(proveedor_id: int, datos: ProveedorUpdate, db: Session = Depends(get_db)):
    proveedor = _obtener_o_404(db, proveedor_id)
    existente = obtener_por_nit(db, datos.nit)
    if existente is not None and existente.id != proveedor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya existe un proveedor con ese NIT")
    return actualizar_proveedor(db, proveedor, datos)


@router.delete("/{proveedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = _obtener_o_404(db, proveedor_id)
    eliminar_proveedor(db, proveedor)

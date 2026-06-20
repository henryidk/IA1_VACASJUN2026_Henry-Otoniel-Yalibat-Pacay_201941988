from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.bitacora import TipoEvento
from app.models.factura import EstadoFactura
from app.models.usuario import Usuario
from app.schemas.factura import FacturaDetalle, FacturaOut, FacturaUpdate
from app.services.bitacora import registrar_evento
from app.services.factura import (
    actualizar_campos_factura,
    crear_factura,
    extension_valida,
    listar_facturas,
    obtener_factura,
)
from app.services.procesamiento import procesar_factura
from app.services.proveedor import obtener_proveedor
from app.services.rpa import registrar_factura_en_formulario
from app.services.validacion import revalidar_factura

router = APIRouter(
    prefix="/api/facturas",
    tags=["facturas"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=FacturaOut, status_code=status.HTTP_201_CREATED)
async def cargar_factura(
    archivo: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    if not archivo.filename or not extension_valida(archivo.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no soportado. Use PDF, JPG, JPEG o PNG",
        )

    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo está vacío")

    factura = crear_factura(db, archivo.filename, usuario_actual.id)
    registrar_evento(
        db,
        factura_id=factura.id,
        usuario_id=usuario_actual.id,
        tipo_evento=TipoEvento.CARGA,
        estado=EstadoFactura.PENDIENTE,
        documento=factura.nombre_archivo,
        resultado="Factura cargada correctamente, pendiente de procesamiento",
    )

    background_tasks.add_task(procesar_factura, factura.id, contenido, factura.nombre_archivo, usuario_actual.id)
    return factura


@router.get("", response_model=list[FacturaOut])
def listar(
    estado: str | None = None,
    proveedor_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    db: Session = Depends(get_db),
):
    return listar_facturas(db, estado=estado, proveedor_id=proveedor_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)


@router.get("/{factura_id}", response_model=FacturaDetalle)
def obtener(factura_id: int, db: Session = Depends(get_db)):
    factura = obtener_factura(db, factura_id)
    if factura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return factura


@router.put("/{factura_id}", response_model=FacturaDetalle)
def actualizar(
    factura_id: int,
    datos: FacturaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    factura = obtener_factura(db, factura_id)
    if factura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")

    cambios = datos.model_dump(exclude_unset=True)
    if cambios.get("proveedor_id") is not None and obtener_proveedor(db, cambios["proveedor_id"]) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El proveedor indicado no existe")

    if cambios:
        actualizar_campos_factura(db, factura, cambios)

    errores = revalidar_factura(factura)
    db.commit()

    registrar_evento(
        db,
        factura_id=factura.id,
        usuario_id=usuario_actual.id,
        tipo_evento=TipoEvento.VALIDACION,
        estado=factura.estado,
        documento=factura.nombre_archivo,
        resultado="Validación exitosa tras corrección manual" if not errores else "; ".join(errores),
    )
    return factura


@router.post("/{factura_id}/rpa")
def disparar_rpa(
    factura_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    factura = obtener_factura(db, factura_id)
    if factura is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")

    try:
        resultado = registrar_factura_en_formulario(factura)
    except Exception as exc:
        registrar_evento(
            db,
            factura_id=factura.id,
            usuario_id=usuario_actual.id,
            tipo_evento=TipoEvento.RPA,
            estado="error",
            documento=factura.nombre_archivo,
            resultado=f"Error ejecutando RPA: {exc}",
        )
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="No se pudo completar el registro automático (RPA)") from exc

    registrar_evento(
        db,
        factura_id=factura.id,
        usuario_id=usuario_actual.id,
        tipo_evento=TipoEvento.RPA,
        estado="exitoso",
        documento=factura.nombre_archivo,
        resultado=resultado,
    )
    return {"detail": resultado}

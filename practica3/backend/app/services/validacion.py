from decimal import Decimal

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.models.factura import EstadoFactura, Factura
from app.models.proveedor import Proveedor
from app.schemas.proveedor import NIT_PATTERN, ProveedorCreate
from app.services.proveedor import crear_proveedor, obtener_por_nit

TOLERANCIA_MONTOS = Decimal("0.05")


def _crear_proveedor_automatico(db: Session, nit: str, nombre: str | None) -> Proveedor | None:
    if not nombre:
        return None
    try:
        datos = ProveedorCreate(nombre=nombre, nit=nit)
    except ValidationError:
        return None
    return crear_proveedor(db, datos)


def _evaluar_campos_basicos(factura: Factura) -> list[dict]:
    errores = []

    if factura.numero_factura is None:
        errores.append({"campo": "numero_factura", "mensaje": "No se pudo extraer el número de factura"})

    if factura.fecha is None:
        errores.append({"campo": "fecha", "mensaje": "No se pudo extraer una fecha válida"})

    if factura.subtotal is None or factura.impuestos is None or factura.total is None:
        errores.append({"campo": "montos", "mensaje": "Faltan montos (subtotal, impuestos o total)"})
    else:
        calculado = factura.subtotal + factura.impuestos
        if abs(calculado - factura.total) > TOLERANCIA_MONTOS:
            errores.append(
                {
                    "campo": "montos",
                    "mensaje": f"Subtotal + impuestos ({calculado}) no coincide con el total ({factura.total})",
                }
            )

    return errores


def validar_factura(
    db: Session,
    factura: Factura,
    nit_extraido: str | None,
    proveedor_nombre_extraido: str | None,
) -> list[dict]:
    """Validación tras el OCR: además de los campos básicos, intenta vincular el
    proveedor a partir del NIT extraído del texto (todavía no hay proveedor_id)."""
    errores = _evaluar_campos_basicos(factura)
    nit_valido = nit_extraido is not None and NIT_PATTERN.match(nit_extraido)

    if not nit_valido:
        errores.append({"campo": "proveedor_id", "mensaje": "El NIT extraído no tiene un formato válido"})

    if nit_valido:
        proveedor = obtener_por_nit(db, nit_extraido)
        if proveedor is None:
            proveedor = _crear_proveedor_automatico(db, nit_extraido, proveedor_nombre_extraido)
        if proveedor is not None:
            factura.proveedor_id = proveedor.id
        else:
            errores.append(
                {
                    "campo": "proveedor_id",
                    "mensaje": (
                        f"No existe un proveedor registrado con NIT {nit_extraido} y no se pudo crear "
                        "automáticamente (el OCR no logró leer un nombre de proveedor válido)"
                    ),
                }
            )

    factura.estado = EstadoFactura.RECHAZADO if errores else EstadoFactura.PROCESADO
    return errores


def revalidar_factura(factura: Factura) -> list[dict]:
    """Re-validación tras una corrección manual: los campos (incluido proveedor_id)
    ya fueron ajustados directamente por el usuario, solo se vuelven a comprobar."""
    errores = evaluar_errores_actuales(factura)
    factura.estado = EstadoFactura.RECHAZADO if errores else EstadoFactura.PROCESADO
    return errores


def evaluar_errores_actuales(factura: Factura) -> list[dict]:
    """Solo lectura: evalúa el estado actual de la factura sin mutar ni persistir
    nada. Se usa para mostrar en la UI qué corregir, en cualquier momento."""
    errores = _evaluar_campos_basicos(factura)

    if factura.proveedor_id is None:
        errores.append({"campo": "proveedor_id", "mensaje": "La factura no tiene un proveedor vinculado"})

    return errores

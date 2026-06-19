from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.factura import EstadoFactura, Factura
from app.schemas.proveedor import NIT_PATTERN
from app.services.proveedor import obtener_por_nit

TOLERANCIA_MONTOS = Decimal("0.05")


def _validar_campos_basicos(factura: Factura) -> list[str]:
    errores = []

    if factura.numero_factura is None:
        errores.append("No se pudo extraer el número de factura")

    if factura.fecha is None:
        errores.append("No se pudo extraer una fecha válida")

    if factura.subtotal is None or factura.impuestos is None or factura.total is None:
        errores.append("Faltan montos (subtotal, impuestos o total)")
    else:
        calculado = factura.subtotal + factura.impuestos
        if abs(calculado - factura.total) > TOLERANCIA_MONTOS:
            errores.append(f"Subtotal + impuestos ({calculado}) no coincide con el total ({factura.total})")

    return errores


def validar_factura(
    db: Session,
    factura: Factura,
    nit_extraido: str | None,
    proveedor_nombre_extraido: str | None,
) -> list[str]:
    """Validación tras el OCR: además de los campos básicos, intenta vincular el
    proveedor a partir del NIT extraído del texto (todavía no hay proveedor_id)."""
    errores = _validar_campos_basicos(factura)

    if nit_extraido is None or not NIT_PATTERN.match(nit_extraido):
        errores.append("El NIT extraído no tiene un formato válido")

    if nit_extraido:
        proveedor = obtener_por_nit(db, nit_extraido)
        if proveedor is not None:
            factura.proveedor_id = proveedor.id
        else:
            errores.append(
                f"No existe un proveedor registrado con NIT {nit_extraido}"
                + (f" ({proveedor_nombre_extraido})" if proveedor_nombre_extraido else "")
            )

    factura.estado = EstadoFactura.RECHAZADO if errores else EstadoFactura.PROCESADO
    return errores


def revalidar_factura(factura: Factura) -> list[str]:
    """Re-validación tras una corrección manual: los campos (incluido proveedor_id)
    ya fueron ajustados directamente por el usuario, solo se vuelven a comprobar."""
    errores = _validar_campos_basicos(factura)

    if factura.proveedor_id is None:
        errores.append("La factura no tiene un proveedor vinculado")

    factura.estado = EstadoFactura.RECHAZADO if errores else EstadoFactura.PROCESADO
    return errores

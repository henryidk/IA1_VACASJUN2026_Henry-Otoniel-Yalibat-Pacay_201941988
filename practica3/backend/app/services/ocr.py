import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

import numpy as np
import pytesseract

PATRON_NUMERO_FACTURA = re.compile(
    r"factura\s*(?:no\.?|n[uú]m(?:ero)?\.?)?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-]{2,19})",
    re.IGNORECASE,
)
PATRON_FECHA = re.compile(
    r"\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b|\b(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})\b"
)
PATRON_NIT = re.compile(r"nit\s*[:\-]?\s*(\d{1,10}-?[\dKk])", re.IGNORECASE)
PATRON_PROVEEDOR = re.compile(r"proveedor\s*[:\-]?\s*(.+)", re.IGNORECASE)
PATRON_SUBTOTAL = re.compile(r"sub\s*-?\s*total\s*[:\-]?\s*Q?\.?\s*([\d.,]+)", re.IGNORECASE)
PATRON_IMPUESTOS = re.compile(r"(?:impuestos?|iva)\s*[:\-]?\s*Q?\.?\s*([\d.,]+)", re.IGNORECASE)
PATRON_TOTAL = re.compile(r"\btotal\s*[:\-]?\s*Q?\.?\s*([\d.,]+)", re.IGNORECASE)


def extraer_texto(imagen: np.ndarray, idioma: str = "spa") -> str:
    return pytesseract.image_to_string(imagen, lang=idioma)


def _parsear_monto(texto: str) -> Decimal | None:
    limpio = texto.replace(",", "").strip().rstrip(".")
    try:
        return Decimal(limpio)
    except InvalidOperation:
        return None


def _parsear_fecha(texto: str) -> date | None:
    coincidencia = PATRON_FECHA.search(texto)
    if not coincidencia:
        return None
    grupos = coincidencia.groups()
    if grupos[0]:
        dia, mes, anio = grupos[0], grupos[1], grupos[2]
        anio = anio if len(anio) == 4 else f"20{anio}"
        try:
            return datetime.strptime(f"{dia}/{mes}/{anio}", "%d/%m/%Y").date()
        except ValueError:
            return None
    anio, mes, dia = grupos[3], grupos[4], grupos[5]
    try:
        return datetime.strptime(f"{anio}-{mes}-{dia}", "%Y-%m-%d").date()
    except ValueError:
        return None


def extraer_campos(texto: str) -> dict:
    coincidencia_numero = PATRON_NUMERO_FACTURA.search(texto)
    coincidencia_nit = PATRON_NIT.search(texto)
    coincidencia_proveedor = PATRON_PROVEEDOR.search(texto)
    coincidencia_subtotal = PATRON_SUBTOTAL.search(texto)
    coincidencia_impuestos = PATRON_IMPUESTOS.search(texto)
    coincidencia_total = PATRON_TOTAL.search(texto)

    return {
        "numero_factura": coincidencia_numero.group(1).strip() if coincidencia_numero else None,
        "fecha": _parsear_fecha(texto),
        "proveedor_nombre": (
            coincidencia_proveedor.group(1).strip().splitlines()[0][:150] if coincidencia_proveedor else None
        ),
        "nit": coincidencia_nit.group(1).strip().upper() if coincidencia_nit else None,
        "subtotal": _parsear_monto(coincidencia_subtotal.group(1)) if coincidencia_subtotal else None,
        "impuestos": _parsear_monto(coincidencia_impuestos.group(1)) if coincidencia_impuestos else None,
        "total": _parsear_monto(coincidencia_total.group(1)) if coincidencia_total else None,
    }

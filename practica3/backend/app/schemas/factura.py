from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class FacturaOut(BaseModel):
    id: int
    nombre_archivo: str
    numero_factura: str | None
    fecha: date | None
    subtotal: Decimal | None
    impuestos: Decimal | None
    total: Decimal | None
    estado: str
    proveedor_id: int | None
    usuario_id: int | None
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)


class ErrorValidacion(BaseModel):
    campo: str
    mensaje: str


class FacturaDetalle(FacturaOut):
    texto_ocr: str | None
    errores_validacion: list[ErrorValidacion] = []


class FacturaUpdate(BaseModel):
    numero_factura: str | None = None
    fecha: date | None = None
    proveedor_id: int | None = None
    subtotal: Decimal | None = None
    impuestos: Decimal | None = None
    total: Decimal | None = None

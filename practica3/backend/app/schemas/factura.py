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

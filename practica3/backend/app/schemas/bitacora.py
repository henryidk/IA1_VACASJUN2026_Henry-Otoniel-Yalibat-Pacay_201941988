from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BitacoraOut(BaseModel):
    id: int
    factura_id: int | None
    usuario_id: int | None
    tipo_evento: str
    documento: str | None
    estado: str
    resultado: str | None
    fecha_hora: datetime

    model_config = ConfigDict(from_attributes=True)

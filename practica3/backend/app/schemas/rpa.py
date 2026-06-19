from pydantic import BaseModel


class RegistroSimuladoRequest(BaseModel):
    numero_factura: str
    fecha: str
    proveedor: str
    nit: str
    subtotal: str
    impuestos: str
    total: str

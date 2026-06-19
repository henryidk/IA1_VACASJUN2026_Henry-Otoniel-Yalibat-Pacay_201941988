import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

NIT_PATTERN = re.compile(r"^\d{1,8}-?[\dKk]$")


class ProveedorBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    nit: str = Field(min_length=2, max_length=30)
    direccion: str | None = Field(default=None, max_length=255)
    telefono: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, max_length=150)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("El nombre del proveedor es obligatorio")
        return valor

    @field_validator("nit")
    @classmethod
    def validar_nit(cls, valor: str) -> str:
        valor = valor.strip().upper()
        if not NIT_PATTERN.match(valor):
            raise ValueError(
                "El NIT debe contener solo números, con un dígito o letra "
                "verificadora opcional separado por guion (ej. 12345678-9)"
            )
        return valor

    @field_validator("direccion", "telefono", "email")
    @classmethod
    def limpiar_opcional(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        valor = valor.strip()
        return valor or None


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(ProveedorBase):
    pass


class ProveedorOut(ProveedorBase):
    id: int
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)

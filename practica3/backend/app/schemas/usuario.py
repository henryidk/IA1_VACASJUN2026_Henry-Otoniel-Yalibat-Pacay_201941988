from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=6, max_length=128)


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

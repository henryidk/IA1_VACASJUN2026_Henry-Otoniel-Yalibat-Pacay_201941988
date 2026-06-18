from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoEvento:
    CARGA = "carga"
    OCR = "ocr"
    VALIDACION = "validacion"
    RPA = "rpa"
    REPORTE = "reporte"
    EMAIL = "email"


class Bitacora(Base):
    __tablename__ = "bitacora"

    id: Mapped[int] = mapped_column(primary_key=True)
    factura_id: Mapped[int | None] = mapped_column(ForeignKey("facturas.id"), nullable=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    tipo_evento: Mapped[str] = mapped_column(String(20), nullable=False)
    documento: Mapped[str | None] = mapped_column(String(255), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    resultado: Mapped[str | None] = mapped_column(Text, nullable=True)

    fecha_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    factura = relationship("Factura", back_populates="bitacoras")
    usuario = relationship("Usuario", back_populates="bitacoras")

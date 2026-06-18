from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EstadoFactura:
    PENDIENTE = "pendiente"
    PROCESADO = "procesado"
    RECHAZADO = "rechazado"
    ERROR = "error"


class Factura(Base):
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    numero_factura: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    subtotal: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    impuestos: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    total: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    texto_ocr: Mapped[str | None] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default=EstadoFactura.PENDIENTE, nullable=False)

    proveedor_id: Mapped[int | None] = mapped_column(ForeignKey("proveedores.id"), nullable=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    proveedor = relationship("Proveedor", back_populates="facturas")
    usuario = relationship("Usuario", back_populates="facturas")
    bitacoras = relationship("Bitacora", back_populates="factura")

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FormatoReporte:
    PDF = "pdf"
    EXCEL = "excel"


class Reporte(Base):
    __tablename__ = "reportes"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    formato: Mapped[str] = mapped_column(String(10), nullable=False)
    filtros: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_generacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="reportes")

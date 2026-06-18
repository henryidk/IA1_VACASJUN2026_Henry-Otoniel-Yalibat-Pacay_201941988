from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    facturas = relationship("Factura", back_populates="usuario")
    bitacoras = relationship("Bitacora", back_populates="usuario")
    reportes = relationship("Reporte", back_populates="usuario")

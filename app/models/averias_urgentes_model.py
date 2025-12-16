from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AveriaUrgente(Base):
    __tablename__ = "averias_urgentes"

    id_averia: Mapped[int] = mapped_column(primary_key=True, index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[str] = mapped_column(String(30),nullable=False,default="pendiente")
    prioridad: Mapped[str] = mapped_column(String(20),nullable=False,default="media")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),nullable=False)
    fecha_cierre: Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True)
    motivo_no_realizada: Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    id_maquina: Mapped[int] = mapped_column(ForeignKey("maquinas.id_maquina"),nullable=False)
    id_usuario_asignado: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"),nullable=False)
    id_usuario_creador: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"),nullable=False)

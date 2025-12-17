from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Date, DateTime, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TareaPreventivo(Base):
    __tablename__ = "tareas_catalogo_preventivo"

    id_tarea_asignada: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_gama: Mapped[int] = mapped_column(ForeignKey("gamas_preventivo.id_gama", ondelete="CASCADE"),nullable=False)
    id_maquina: Mapped[int] = mapped_column(ForeignKey("maquinas.id_maquina", ondelete="CASCADE"),nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),nullable=False)
    id_tarea_catalogo_gamas: Mapped[Optional[int]] = mapped_column(ForeignKey("tareas_catalogo_gamas.id_tarea_catalogo_gamas", ondelete="SET NULL"))
    estado: Mapped[str] = mapped_column(String(20),nullable=False,default="pendiente")
    fecha_asignada: Mapped[date] = mapped_column(Date,nullable=False,default=date.today)
    fecha_completado: Mapped[Optional[datetime]] = mapped_column(DateTime,nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    duracion_horas: Mapped[Optional[float]] = mapped_column(Numeric(4, 2))

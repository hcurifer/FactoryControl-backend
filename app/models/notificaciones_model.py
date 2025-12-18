# app/models/notificaciones_model.py

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id_notificacion: Mapped[int] = mapped_column(primary_key=True,index=True)
    id_averia: Mapped[Optional[int]] = mapped_column(ForeignKey("averias_urgentes.id_averia", ondelete="SET NULL"),nullable=True)
    id_tarea: Mapped[Optional[int]] = mapped_column(ForeignKey("tareas_catalogo_preventivo.id_tarea_asignada", ondelete="SET NULL"),nullable=True)
    id_maquina: Mapped[int] = mapped_column(ForeignKey("maquinas.id_maquina", ondelete="CASCADE"),nullable=False)
    id_usuario_origen: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),nullable=True)
    id_usuario_destino: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),nullable=True)
    tipo: Mapped[str] = mapped_column(String(100),nullable=False)
    contenido_resumen: Mapped[str] = mapped_column(Text,nullable=False)
    asunto: Mapped[Optional[str]] = mapped_column(String(150),nullable=True)
    fecha_envio: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),nullable=False)

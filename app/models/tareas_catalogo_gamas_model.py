from typing import Optional
from sqlalchemy import String, Text, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TareaCatalogoGama(Base):
    __tablename__ = "tareas_catalogo_gamas"

    id_tarea_catalogo_gamas: Mapped[int] = mapped_column(primary_key=True,index=True)
    id_gama: Mapped[int] = mapped_column(ForeignKey("gamas_preventivo.id_gama", ondelete="CASCADE"),nullable=False)
    nombre_tarea: Mapped[str] = mapped_column(String(150),nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    duracion_horas: Mapped[float] = mapped_column(Numeric(4, 2),nullable=False)
    orden: Mapped[int] = mapped_column(Integer,nullable=False)

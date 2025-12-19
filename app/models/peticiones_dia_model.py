# app/models/peticiones_dia_model.py

from datetime import date
from typing import Optional

from sqlalchemy import String, Date, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PeticionDia(Base):
    __tablename__ = "peticiones_dia"

    id_peticion: Mapped[int] = mapped_column(primary_key=True,index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),nullable=False,index=True)
    tipo_peticion: Mapped[str] = mapped_column(String(50),nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    estado: Mapped[str] = mapped_column(String(20),nullable=False,default="pendiente")
    fecha_resolucion: Mapped[Optional[date]] = mapped_column(Date,nullable=True)

# app/models/maquinas_model.py

from datetime import date
from typing import Optional
from sqlalchemy import String, Boolean, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Maquina(Base):
    __tablename__ = "maquinas"

    id_maquina: Mapped[int] = mapped_column(primary_key=True,index=True)
    nombre: Mapped[str] = mapped_column(String(100),nullable=False)
    codigo_maquina: Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(100),nullable=False)
    estado: Mapped[str] = mapped_column(String(30),nullable=False,default="disponible") # Valores esperados: disponible | parada | pendiente_preventivo
    alarma_activa: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    imagen: Mapped[Optional[str]] = mapped_column(String(255),nullable=True)
    fecha_alta: Mapped[date] = mapped_column(Date,default=date.today,nullable=False)
    fecha_baja: Mapped[Optional[date]] = mapped_column(Date,nullable=True) # Sin decidir si baja logica o Delete fisico

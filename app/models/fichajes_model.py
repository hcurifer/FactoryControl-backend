# app/models/fichajes_model.py

from datetime import date, time
from typing import Optional

from sqlalchemy import Date, Time, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Fichaje(Base):
    __tablename__ = "fichajes"

    id_fichaje: Mapped[int] = mapped_column(primary_key=True,index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),nullable=False,index=True)
    fecha: Mapped[date] = mapped_column(Date,nullable=False,default=date.today)
    hora_entrada: Mapped[Optional[time]] = mapped_column(Time,nullable=True)
    hora_salida: Mapped[Optional[time]] = mapped_column(Time,nullable=True)
    comentario: Mapped[Optional[str]] = mapped_column(Text,nullable=True)

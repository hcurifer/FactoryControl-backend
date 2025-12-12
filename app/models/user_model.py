from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from typing import Optional
from app.db.base import Base

class User(Base):
    __tablename__ = "usuarios"
    
    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    numero_empresa: Mapped[str] = mapped_column(String, unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellidos: Mapped[str] = mapped_column(String, nullable=False)
    correo: Mapped[str] = mapped_column(String, unique=True, index=True)
    contrasena_hash: Mapped[str] = mapped_column(String, nullable=False)
    rol: Mapped[str] = mapped_column(String, nullable=False)  # tecnico / mando
    estado_disponible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    imagen: Mapped[str | None] = mapped_column(String, nullable=True)
    fecha_alta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_baja: Mapped[Optional[date]] = mapped_column(Date, nullable=True)



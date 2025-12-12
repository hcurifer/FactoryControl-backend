from sqlalchemy import Column, Integer, String, Boolean, Date
from app.db.base import Base

class User(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    numero_empresa = Column(String, unique=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True)
    contrasena_hash = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # tecnico / mando
    estado_disponible = Column(Boolean, default=True)
    imagen = Column(String, nullable=True)
    fecha_alta = Column(Date, nullable=True)
    fecha_baja = Column(Date, nullable=True)

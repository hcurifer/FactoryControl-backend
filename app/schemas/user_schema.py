from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# Schema base 
class UserBase(BaseModel):
    numero_empresa: str
    nombre: str
    apellidos: str
    correo: EmailStr
    rol: str
    estado_disponible: bool = True
    imagen: Optional[str] = None


# CREAR usuarios (entrada)
class UserCreateSchema(UserBase):
    contrasena: str  # password texto plano antes de hashear


# MOSTRAR usuarios (salida)
class UserReadSchema(UserBase):
    id_usuario: int
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None

    class Config:
        orm_mode = True #FastAPI devuelve objetos a SQLAlchemy como JSON

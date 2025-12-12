from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import date
from typing import Optional
from enum import Enum

# Restriciones de datos
class RolEnum(str, Enum):
    tecnico = "tecnico"
    mando = "mando"

class UserEstadoUpdateSchema(BaseModel):
    estado_disponible: bool

# Schema base 
class UserBase(BaseModel):
    numero_empresa: str
    nombre: str
    apellidos: str
    correo: EmailStr    # validacion con EmailStr
    rol: RolEnum            # Valicacion arriba con funcion RolEnum() sustituye a str anterior
    estado_disponible: bool = True
    imagen: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)     # Cambio orm_mode = True por ser la nueva manera de Pydantic V2 y quejarse Pylance


# CREAR usuarios (entrada)
class UserCreateSchema(UserBase):
    contrasena: str  # password texto plano antes de hashear
    fecha_alta: Optional[date] =  Field(default_factory=date.today)
    fecha_baja: Optional[date] = None





# MOSTRAR usuarios (salida)
class UserReadSchema(UserBase):
    id_usuario: int
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None

    #class Config:
     #   orm_mode = True #FastAPI devuelve objetos a SQLAlchemy como JSON
# Cambio orm_mode = True por ser la nueva manera de Pydantic V2 y quejarse Pylance
    model_config = ConfigDict(from_attributes=True)
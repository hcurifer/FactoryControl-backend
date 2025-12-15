from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from enum import Enum


# Restriciones de datos

class EstadoMaquinaEnum(str, Enum):
    disponible = "disponible"
    parada = "parada"
    pendiente_preventivo = "pendiente_preventivo"



# Schema base 

class MaquinaBase(BaseModel):
    nombre: str
    codigo_maquina: str
    ubicacion: str
    estado: EstadoMaquinaEnum
    alarma_activa: bool
    descripcion: Optional[str] = None
    imagen: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# UPDATE 

class MaquinaUpdateSchema(BaseModel):
    estado: Optional[EstadoMaquinaEnum] = None
    alarma_activa: Optional[bool] = None
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MaquinaEstadoUpdateSchema(BaseModel):
    estado: EstadoMaquinaEnum
    model_config = ConfigDict(from_attributes=True)


class MaquinaAlarmaUpdateSchema(BaseModel):
    alarma_activa: bool
    model_config = ConfigDict(from_attributes=True)

# CREAR maquinas (entrada)

class MaquinaCreateSchema(MaquinaBase):
    fecha_alta: Optional[date] =  Field(default_factory=date.today)
    fecha_baja: Optional[date] = None



# MOSTRAR maquinas (salida)

class MaquinaReadSchema(MaquinaBase):
    id_maquina: int
    fecha_alta: Optional[date] = None
    fecha_baja: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


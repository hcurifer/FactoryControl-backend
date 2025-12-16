from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Restriciones de datos

class EstadoAveriaUrgenteEnum(str, Enum):
    pendiente = "pendiente"
    completada = "completada"
    no_realizada = "no_realizada"


class PrioridadAveriaUrgenteEnum(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

# Schema base 

class AveriaUrgenteBaseSchema(BaseModel):
    descripcion: str = Field(min_length=5, max_length=4000)
    prioridad: PrioridadAveriaUrgenteEnum = PrioridadAveriaUrgenteEnum.media
    estado: EstadoAveriaUrgenteEnum = EstadoAveriaUrgenteEnum.pendiente

    id_maquina: int
    id_usuario_asignado: int
    id_usuario_creador: int

    model_config = ConfigDict(from_attributes=True)

# CREAR maquAveriasUrgentesinas (entrada)

class AveriaUrgenteCreateSchema(AveriaUrgenteBaseSchema):
    pass

# UPDATE 

class AveriaUrgenteUpdateSchema(BaseModel):
    descripcion: Optional[str] = Field(default=None, min_length=5, max_length=4000)
    prioridad: Optional[PrioridadAveriaUrgenteEnum] = None
    id_usuario_asignado: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AveriaUrgenteEstadoUpdateSchema(BaseModel):
    estado: EstadoAveriaUrgenteEnum
    motivo_no_realizada: Optional[str] = Field(default=None, max_length=4000)

    model_config = ConfigDict(from_attributes=True)

# MOSTRAR AveriasUrgentes (salida)

class AveriaUrgenteReadSchema(AveriaUrgenteBaseSchema):
    id_averia: int
    fecha_creacion: datetime
    fecha_cierre: Optional[datetime] = None
    motivo_no_realizada: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

from datetime import date, datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class EstadoTareaPreventivoEnum(str, Enum):
    pendiente = "pendiente"
    completada = "completada"


# BASE
class TareaPreventivoBaseSchema(BaseModel):
    id_gama: int
    id_maquina: int
    id_usuario: int
    id_tarea_catalogo_gamas: Optional[int] = None
    duracion_horas: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


# CREATE
class TareaPreventivoCreateSchema(TareaPreventivoBaseSchema):
    fecha_asignada: Optional[date] = Field(default_factory=date.today)
    observaciones: Optional[str] = None

# GENERADOR
 
class GenerarTareasPreventivoSchema(BaseModel):
    id_gama: int
    id_maquina: int
    id_usuario: int
    fecha_asignada: date

    model_config = ConfigDict(from_attributes=True)

# UPDATE GENERAL
class TareaPreventivoUpdateSchema(BaseModel):
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# UPDATE ESTADO
class TareaPreventivoEstadoUpdateSchema(BaseModel):
    estado: EstadoTareaPreventivoEnum

    model_config = ConfigDict(from_attributes=True)


# READ
class TareaPreventivoReadSchema(TareaPreventivoBaseSchema):
    id_tarea_asignada: int
    estado: EstadoTareaPreventivoEnum
    fecha_asignada: date
    fecha_completado: Optional[datetime] = None
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

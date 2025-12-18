# app/schemas/peticiones_dia_schema.py

from datetime import date
from typing import Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict


# ENUMS

class TipoPeticionDiaEnum(str, Enum):
    licencia = "licencia"
    disfrute = "disfrute"
    antiguedad = "antiguedad"


class EstadoPeticionDiaEnum(str, Enum):
    pendiente = "pendiente"
    aprobada = "aprobada"
    rechazada = "rechazada"


# BASE

class PeticionDiaBaseSchema(BaseModel):
    id_usuario: int
    tipo_peticion: TipoPeticionDiaEnum
    comentario: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# CREATE

class PeticionDiaCreateSchema(PeticionDiaBaseSchema):
    pass


# UPDATE (gestión por mando)

class PeticionDiaUpdateSchema(BaseModel):
    estado: EstadoPeticionDiaEnum
    fecha_resolucion: date

    model_config = ConfigDict(from_attributes=True)


# READ

class PeticionDiaReadSchema(PeticionDiaBaseSchema):
    id_peticion: int
    estado: EstadoPeticionDiaEnum
    fecha_resolucion: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

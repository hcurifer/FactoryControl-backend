# app/schemas/fichajes_schema.py

from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# BASE

class FichajeBaseSchema(BaseModel):
    id_usuario: int
    comentario: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# CREATE (FICHAR ENTRADA)

class FichajeCreateSchema(FichajeBaseSchema):
    fecha: Optional[date] = Field(default_factory=date.today)
    hora_entrada: Optional[time] = None


# UPDATE (FICHAR SALIDA)

class FichajeSalidaSchema(BaseModel):
    hora_salida: time
    comentario: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# READ

class FichajeReadSchema(BaseModel):
    id_fichaje: int
    id_usuario: int
    fecha: date
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None
    comentario: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

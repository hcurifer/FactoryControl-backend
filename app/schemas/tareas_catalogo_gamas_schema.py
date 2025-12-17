from typing import Optional
from pydantic import BaseModel, ConfigDict


# BASE
class TareaCatalogoGamaBaseSchema(BaseModel):
    id_gama: int
    nombre_tarea: str
    descripcion: Optional[str] = None
    duracion_horas: float
    orden: int

    model_config = ConfigDict(from_attributes=True)


# CREATE
class TareaCatalogoGamaCreateSchema(TareaCatalogoGamaBaseSchema):
    pass


# UPDATE
class TareaCatalogoGamaUpdateSchema(BaseModel):
    nombre_tarea: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_horas: Optional[float] = None
    orden: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# READ
class TareaCatalogoGamaReadSchema(TareaCatalogoGamaBaseSchema):
    id_tarea_catalogo_gamas: int

    model_config = ConfigDict(from_attributes=True)

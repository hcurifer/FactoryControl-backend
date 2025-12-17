from typing import Optional
from pydantic import BaseModel, ConfigDict


# BASE
class GamaPreventivoBaseSchema(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# CREATE
class GamaPreventivoCreateSchema(GamaPreventivoBaseSchema):
    activa: bool = True


# UPDATE GENERAL
class GamaPreventivoUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# UPDATE ESTADO (activar / desactivar)
class GamaPreventivoEstadoUpdateSchema(BaseModel):
    activa: bool

    model_config = ConfigDict(from_attributes=True)


# READ
class GamaPreventivoReadSchema(GamaPreventivoBaseSchema):
    id_gama: int
    activa: bool

    model_config = ConfigDict(from_attributes=True)

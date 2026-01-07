# app/schemas/notificaciones_schema.py

from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# RESTICIONES ENUMS

class TipoNotificacionEnum(str, Enum):
    averia_no_realizada = "averia_no_realizada"
    alarma_preventivo = "alarma_preventivo"
    informativa = "informativa"
    sistema = "sistema"


# BASE

class NotificacionBaseSchema(BaseModel):
    tipo: TipoNotificacionEnum
    contenido_resumen: str
    asunto: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# CREAR (ENTRADA POST)

class NotificacionCreateSchema(NotificacionBaseSchema):
    id_averia: Optional[int] = None
    id_tarea: Optional[int] = None
    id_maquina: int
    id_usuario_origen: int
    id_usuario_destino: Optional[int] = None


# MOSTRAR (SALIDA API)

class NotificacionReadSchema(NotificacionBaseSchema):
    id_notificacion: int
    id_averia: Optional[int] = None
    id_tarea: Optional[int] = None
    id_maquina: int
    id_usuario_origen: Optional[int] = None
    id_usuario_destino: Optional[int] = None
    fecha_envio: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.tareas_preventivo_model import TareaPreventivo
from app.models.maquinas_model import Maquina
from app.models.user_model import User
from app.models.gamas_preventivo_model import GamaPreventivo

from app.schemas.tareas_preventivo_schema import (
    TareaPreventivoCreateSchema,
    TareaPreventivoUpdateSchema,
    TareaPreventivoEstadoUpdateSchema,
    EstadoTareaPreventivoEnum
)


# CREATE
def create_tarea_preventivo(db: Session, data: TareaPreventivoCreateSchema) -> TareaPreventivo:

    maquina = db.query(Maquina).filter(Maquina.id_maquina == data.id_maquina).first()
    if not maquina or maquina.fecha_baja is not None:
        raise HTTPException(status_code=400, detail="Máquina no válida")

    usuario = db.query(User).filter(User.id_usuario == data.id_usuario).first()
    if not usuario or usuario.fecha_baja is not None:
        raise HTTPException(status_code=400, detail="Usuario no válido")

    gama = db.query(GamaPreventivo).filter(GamaPreventivo.id_gama == data.id_gama).first()
    if not gama or not gama.activa:
        raise HTTPException(status_code=400, detail="Gama no activa o inexistente")

    tarea = TareaPreventivo(
        id_gama=data.id_gama,
        id_maquina=data.id_maquina,
        id_usuario=data.id_usuario,
        id_tarea_catalogo_gamas=data.id_tarea_catalogo_gamas,
        estado=EstadoTareaPreventivoEnum.pendiente.value,
        fecha_asignada=data.fecha_asignada,
        duracion_horas=data.duracion_horas,
        observaciones=data.observaciones
    )

    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


# GET
def get_all_tareas_preventivo(db: Session):
    return db.query(TareaPreventivo).all()


def get_tareas_por_usuario(db: Session, id_usuario: int):
    return db.query(TareaPreventivo).filter(TareaPreventivo.id_usuario == id_usuario).all()


def get_tareas_por_maquina(db: Session, id_maquina: int):
    return db.query(TareaPreventivo).filter(TareaPreventivo.id_maquina == id_maquina).all()


# UPDATE
def update_tarea_preventivo(
    db: Session,
    tarea_id: int,
    data: TareaPreventivoUpdateSchema
):
    tarea = db.query(TareaPreventivo).filter(TareaPreventivo.id_tarea_asignada == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if data.observaciones is not None:
        tarea.observaciones = data.observaciones

    db.commit()
    db.refresh(tarea)
    return tarea


def update_estado_tarea_preventivo(
    db: Session,
    tarea_id: int,
    data: TareaPreventivoEstadoUpdateSchema
):
    tarea = db.query(TareaPreventivo).filter(TareaPreventivo.id_tarea_asignada == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea.estado == EstadoTareaPreventivoEnum.completada.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La tarea ya está completada"
        )

    if data.estado == EstadoTareaPreventivoEnum.completada:
        tarea.estado = data.estado.value
        tarea.fecha_completado = datetime.now(timezone.utc)

    db.commit()
    db.refresh(tarea)
    return tarea

# app/services/notificaciones_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.notificaciones_model import Notificacion
from app.schemas.notificaciones_schema import (
    NotificacionCreateSchema,
    TipoNotificacionEnum,
)

from app.services.maquinas_service import get_maquina_by_id
from app.services.user_service import get_user_by_id
from app.services.averias_urgentes_service import get_averia_by_id


# CREATE

def create_notificacion(db: Session,data: NotificacionCreateSchema) -> Notificacion:
    """
    Crea una notificación y valida las FK asociadas.
    No envía correos, solo persiste el evento.
    """

    # Validar máquina (obligatoria)
    maquina = get_maquina_by_id(db, data.id_maquina)
    if not maquina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Máquina no encontrada"
        )

    # Validar avería si viene informada
    if data.id_averia is not None:
        averia = get_averia_by_id(db, data.id_averia)
        if not averia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avería no encontrada"
            )

    # Validar usuario origen si viene
    if data.id_usuario_origen is not None:
        usuario_origen = get_user_by_id(db, data.id_usuario_origen)
        if not usuario_origen:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario origen no encontrado"
            )

    # Validar usuario destino si viene
    if data.id_usuario_destino is not None:
        usuario_destino = get_user_by_id(db, data.id_usuario_destino)
        if not usuario_destino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario destino no encontrado"
            )

    # Crear notificación
    notificacion = Notificacion(
        id_averia=data.id_averia,
        id_tarea=data.id_tarea,
        id_maquina=data.id_maquina,
        id_usuario_origen=data.id_usuario_origen,
        id_usuario_destino=data.id_usuario_destino,
        tipo=data.tipo.value,
        contenido_resumen=data.contenido_resumen,
        asunto=data.asunto,
    )

    db.add(notificacion)
    db.commit()
    db.refresh(notificacion)

    return notificacion


# GET

def get_notificacion_by_id(db: Session,notificacion_id: int) -> Notificacion | None:
    return (
        db.query(Notificacion)
        .filter(Notificacion.id_notificacion == notificacion_id)
        .first()
    )


def get_all_notificaciones(db: Session) -> list[Notificacion]:
    return db.query(Notificacion).all()


def get_notificaciones_por_usuario_destino(db: Session,id_usuario: int) -> list[Notificacion]:
    return (
        db.query(Notificacion)
        .filter(Notificacion.id_usuario_destino == id_usuario)
        .order_by(Notificacion.fecha_envio.desc())
        .all()
    )


def get_notificaciones_por_maquina(db: Session,id_maquina: int) -> list[Notificacion]:
    return (
        db.query(Notificacion)
        .filter(Notificacion.id_maquina == id_maquina)
        .order_by(Notificacion.fecha_envio.desc())
        .all()
    )


def get_notificaciones_por_tipo(db: Session,tipo: TipoNotificacionEnum) -> list[Notificacion]:
    return (
        db.query(Notificacion)
        .filter(Notificacion.tipo == tipo.value)
        .order_by(Notificacion.fecha_envio.desc())
        .all()
    )

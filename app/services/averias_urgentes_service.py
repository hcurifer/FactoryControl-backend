from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.averias_urgentes_model import AveriaUrgente
from app.models.maquinas_model import Maquina
from app.models.user_model import User  
from app.schemas.averias_urgentes_schema import (
    AveriaUrgenteCreateSchema,
    AveriaUrgenteUpdateSchema,
    AveriaUrgenteEstadoUpdateSchema,
    EstadoAveriaUrgenteEnum,
)

from app.schemas.maquinas_schema import (
    MaquinaAlarmaUpdateSchema,
    MaquinaEstadoUpdateSchema,
    EstadoMaquinaEnum,
)

from app.services.maquinas_service import (
    get_maquina_by_id,
    update_maquina_alarma,
    update_maquina_estado,
)

from app.services.user_service import get_user_by_id  

# CREATE

def create_averia_urgente(
    db: Session,
    data: AveriaUrgenteCreateSchema
) -> AveriaUrgente:

    # Validar máquina
    maquina = get_maquina_by_id(db, data.id_maquina)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    if maquina.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La máquina está dada de baja"
        )

    # Validar usuarios
    usuario_asignado = get_user_by_id(db, data.id_usuario_asignado)
    if not usuario_asignado:
        raise HTTPException(status_code=404, detail="Usuario asignado no encontrado")

    usuario_creador = get_user_by_id(db, data.id_usuario_creador)
    if not usuario_creador:
        raise HTTPException(status_code=404, detail="Usuario creador no encontrado")

    # Crear avería
    new_averia = AveriaUrgente(
        descripcion=data.descripcion,
        prioridad=data.prioridad.value,
        estado=EstadoAveriaUrgenteEnum.pendiente.value,
        fecha_creacion=datetime.now(timezone.utc),
        fecha_cierre=None,
        motivo_no_realizada=None,
        id_maquina=data.id_maquina,
        id_usuario_asignado=data.id_usuario_asignado,
        id_usuario_creador=data.id_usuario_creador,
    )

    db.add(new_averia)
    db.commit()
    db.refresh(new_averia)

    # Regla de negocio: activar alarma de la máquina
    update_maquina_alarma(
        db,
        data.id_maquina,
        MaquinaAlarmaUpdateSchema(alarma_activa=True)
    )

    return new_averia

# GET

def get_averia_by_id(db: Session, averia_id: int) -> AveriaUrgente | None:
    return (
        db.query(AveriaUrgente)
        .filter(AveriaUrgente.id_averia == averia_id)
        .first()
    )


def get_all_averias(db: Session) -> list[AveriaUrgente]:
    return db.query(AveriaUrgente).all()


def get_averias_por_estado(
    db: Session,
    estado: EstadoAveriaUrgenteEnum
) -> list[AveriaUrgente]:
    return (
        db.query(AveriaUrgente)
        .filter(AveriaUrgente.estado == estado.value)
        .all()
    )


def get_averias_por_maquina(db: Session, id_maquina: int) -> list[AveriaUrgente]:
    return (
        db.query(AveriaUrgente)
        .filter(AveriaUrgente.id_maquina == id_maquina)
        .all()
    )


def get_averias_por_usuario_asignado(
    db: Session,
    id_usuario: int
) -> list[AveriaUrgente]:
    return (
        db.query(AveriaUrgente)
        .filter(AveriaUrgente.id_usuario_asignado == id_usuario)
        .all()
    )


 # UPDATES 
 
def update_averia_urgente(
    db: Session,
    averia_id: int,
    data: AveriaUrgenteUpdateSchema
) -> AveriaUrgente:

    averia = get_averia_by_id(db, averia_id)
    if not averia:
        raise HTTPException(status_code=404, detail="Avería no encontrada")

    if data.descripcion is not None:
        averia.descripcion = data.descripcion

    if data.prioridad is not None:
        averia.prioridad = data.prioridad.value

    if data.id_usuario_asignado is not None:
        usuario = get_user_by_id(db, data.id_usuario_asignado)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario asignado no encontrado")
        averia.id_usuario_asignado = data.id_usuario_asignado

    db.commit()
    db.refresh(averia)
    return averia

def update_estado_averia_urgente(
    db: Session,
    averia_id: int,
    data: AveriaUrgenteEstadoUpdateSchema
) -> AveriaUrgente:

    averia = get_averia_by_id(db, averia_id)
    if not averia:
        raise HTTPException(status_code=404, detail="Avería no encontrada")

    # NO REALIZADA
    if data.estado == EstadoAveriaUrgenteEnum.no_realizada:
        if not data.motivo_no_realizada or len(data.motivo_no_realizada.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe indicarse un motivo para marcar la avería como no realizada"
            )

        averia.estado = EstadoAveriaUrgenteEnum.no_realizada.value
        averia.motivo_no_realizada = data.motivo_no_realizada.strip()
        averia.fecha_cierre = datetime.now(timezone.utc)

        # La alarma permanece activa

    # COMPLETADA
    elif data.estado == EstadoAveriaUrgenteEnum.completada:
        averia.estado = EstadoAveriaUrgenteEnum.completada.value
        averia.motivo_no_realizada = None
        averia.fecha_cierre = datetime.now(timezone.utc)

        # Regla: quitar alarma y poner máquina disponible
        update_maquina_alarma(
            db,
            averia.id_maquina,
            MaquinaAlarmaUpdateSchema(alarma_activa=False)
        )

        update_maquina_estado(
            db,
            averia.id_maquina,
            MaquinaEstadoUpdateSchema(estado=EstadoMaquinaEnum.disponible)
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cambio de estado no permitido"
        )

    db.commit()
    db.refresh(averia)
    return averia

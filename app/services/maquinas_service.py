from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.maquinas_model import Maquina
from app.schemas.maquinas_schema import (
    MaquinaCreateSchema,
    MaquinaUpdateSchema,
    MaquinaEstadoUpdateSchema,
    MaquinaAlarmaUpdateSchema,
    EstadoMaquinaEnum,
)


# CREATE

def create_maquina(db: Session, data: MaquinaCreateSchema) -> Maquina:
    # Comprobar si ya existe una maquina con ese codigo al tener que ser unico
    existing = db.query(Maquina).filter(Maquina.codigo_maquina == data.codigo_maquina).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una máquina con ese código.",
        )

    new_maquina = Maquina(
        nombre=data.nombre,
        codigo_maquina=data.codigo_maquina,
        ubicacion=data.ubicacion,
        estado=data.estado.value,
        alarma_activa=data.alarma_activa,
        descripcion=data.descripcion,
        imagen=data.imagen,
        fecha_alta=date.today(),
        fecha_baja=None,
    )

    db.add(new_maquina)
    try:
        db.commit()
        db.refresh(new_maquina)
        return new_maquina
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha podido crear la máquina por un conflicto de datos (duplicados).",
        )


# GET

def get_maquina_by_id(db: Session, maquina_id: int) -> Maquina | None:
    return db.query(Maquina).filter(Maquina.id_maquina == maquina_id).first()


def get_all_maquinas(db: Session) -> list[Maquina]:
    return db.query(Maquina).all()


def get_maquinas_activas(db: Session) -> list[Maquina]:
    return db.query(Maquina).filter(Maquina.fecha_baja.is_(None)).all()


def get_maquinas_inactivas(db: Session) -> list[Maquina]:
    return db.query(Maquina).filter(Maquina.fecha_baja.is_not(None)).all()


def get_maquinas_con_alarma(db: Session) -> list[Maquina]:
    return (
        db.query(Maquina)
        .filter(Maquina.alarma_activa.is_(True), Maquina.fecha_baja.is_(None))
        .all()
    )


def get_maquinas_por_estado(db: Session,estado: EstadoMaquinaEnum) -> list[Maquina]:
    return (
        db.query(Maquina)
        .filter(
            Maquina.estado == estado.value,
            Maquina.fecha_baja.is_(None)
        )
        .all()
    )

def get_maquinas_en_produccion(db: Session) -> list[Maquina]:
    return get_maquinas_por_estado(db, EstadoMaquinaEnum.disponible)


def get_maquinas_paradas(db: Session) -> list[Maquina]:
    return get_maquinas_por_estado(db, EstadoMaquinaEnum.parada)


def get_maquinas_pendiente_preventivo(db: Session) -> list[Maquina]:
    return get_maquinas_por_estado(db, EstadoMaquinaEnum.pendiente_preventivo)


# UPDATE (general)

def update_maquina(db: Session, maquina_id: int, data: MaquinaUpdateSchema) -> Maquina:
    maquina = get_maquina_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    if maquina.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Máquina dada de baja"
        )

    # Actualización por partes de campos
    if data.ubicacion is not None:
        maquina.ubicacion = data.ubicacion
    if data.descripcion is not None:
        maquina.descripcion = data.descripcion
    if data.imagen is not None:
        maquina.imagen = data.imagen
    if data.estado is not None:
        maquina.estado = data.estado.value
    if data.alarma_activa is not None:
        maquina.alarma_activa = data.alarma_activa

    db.commit()
    db.refresh(maquina)
    return maquina


# UPDATE ESTADO

def update_maquina_estado(db: Session, maquina_id: int, data: MaquinaEstadoUpdateSchema) -> Maquina:
    maquina = get_maquina_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    if maquina.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Máquina dada de baja"
        )

    maquina.estado = data.estado.value
    db.commit()
    db.refresh(maquina)
    return maquina


# UPDATE ALARMA

def update_maquina_alarma(db: Session, maquina_id: int, data: MaquinaAlarmaUpdateSchema) -> Maquina:
    maquina = get_maquina_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    if maquina.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Máquina dada de baja"
        )

    maquina.alarma_activa = data.alarma_activa
    db.commit()
    db.refresh(maquina)
    return maquina


# DELETE LÓGICO y FISICO de BBDD

def delete_maquina_logico(db: Session, maquina_id: int) -> Maquina:
    maquina = get_maquina_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    if maquina.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La máquina ya está dada de baja"
        )

    maquina.fecha_baja = date.today()
    # Dar de baja dejamos coloco la máquina sin alarma y en parada
    maquina.alarma_activa = False
    maquina.estado = "parada"

    db.commit()
    db.refresh(maquina)
    return maquina


def delete_maquina_fisico(db: Session, maquina_id: int) -> None:
    maquina = get_maquina_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")

    db.delete(maquina)
    db.commit()

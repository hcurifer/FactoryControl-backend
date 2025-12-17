from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.tareas_catalogo_gamas_model import TareaCatalogoGama
from app.models.gamas_preventivo_model import GamaPreventivo
from app.schemas.tareas_catalogo_gamas_schema import (
    TareaCatalogoGamaCreateSchema,
    TareaCatalogoGamaUpdateSchema,
)


# CREATE
def create_tarea_catalogo_gama(db: Session,data: TareaCatalogoGamaCreateSchema) -> TareaCatalogoGama:

    # Validar gama
    gama = db.query(GamaPreventivo).filter(GamaPreventivo.id_gama == data.id_gama).first()
    if not gama:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La gama asociada no existe"
        )

    # Evitar duplicar orden dentro de una gama
    orden_existente = (
        db.query(TareaCatalogoGama)
        .filter(
            TareaCatalogoGama.id_gama == data.id_gama,
            TareaCatalogoGama.orden == data.orden
        )
        .first()
    )
    if orden_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una tarea con ese orden en la gama"
        )

    tarea = TareaCatalogoGama(
        id_gama=data.id_gama,
        nombre_tarea=data.nombre_tarea,
        descripcion=data.descripcion,
        duracion_horas=data.duracion_horas,
        orden=data.orden
    )

    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


# GET
def get_all_tareas_catalogo_gamas(db: Session):
    return db.query(TareaCatalogoGama).all()


def get_tareas_catalogo_por_gama(db: Session, id_gama: int):
    return (
        db.query(TareaCatalogoGama)
        .filter(TareaCatalogoGama.id_gama == id_gama)
        .order_by(TareaCatalogoGama.orden)
        .all()
    )


def get_tarea_catalogo_gama_by_id(db: Session, tarea_id: int):
    return (
        db.query(TareaCatalogoGama)
        .filter(TareaCatalogoGama.id_tarea_catalogo_gamas == tarea_id)
        .first()
    )


# UPDATE
def update_tarea_catalogo_gama(db: Session,tarea_id: int,data: TareaCatalogoGamaUpdateSchema):
    tarea = get_tarea_catalogo_gama_by_id(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea de catálogo no encontrada")

    if data.nombre_tarea is not None:
        tarea.nombre_tarea = data.nombre_tarea
    if data.descripcion is not None:
        tarea.descripcion = data.descripcion
    if data.duracion_horas is not None:
        tarea.duracion_horas = data.duracion_horas
    if data.orden is not None:
        tarea.orden = data.orden

    db.commit()
    db.refresh(tarea)
    return tarea


# DELETE (físico, solo sobre catálogo)
def delete_tarea_catalogo_gama(db: Session, tarea_id: int):
    tarea = get_tarea_catalogo_gama_by_id(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea de catálogo no encontrada")

    db.delete(tarea)
    db.commit()

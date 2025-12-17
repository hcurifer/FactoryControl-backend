from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.gamas_preventivo_model import GamaPreventivo
from app.schemas.gamas_preventivo_schema import (
    GamaPreventivoCreateSchema,
    GamaPreventivoUpdateSchema,
    GamaPreventivoEstadoUpdateSchema,
)


# CREATE
def create_gama_preventivo(db: Session, data: GamaPreventivoCreateSchema) -> GamaPreventivo:
    existing = (
        db.query(GamaPreventivo)
        .filter(GamaPreventivo.nombre == data.nombre)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una gama con ese nombre"
        )

    gama = GamaPreventivo(
        nombre=data.nombre,
        descripcion=data.descripcion,
        activa=data.activa
    )

    db.add(gama)
    db.commit()
    db.refresh(gama)
    return gama


# GET
def get_all_gamas(db: Session):
    return db.query(GamaPreventivo).all()


def get_gama_by_id(db: Session, gama_id: int):
    return db.query(GamaPreventivo).filter(GamaPreventivo.id_gama == gama_id).first()


def get_gamas_activas(db: Session):
    return db.query(GamaPreventivo).filter(GamaPreventivo.activa.is_(True)).all()


def get_gamas_inactivas(db: Session):
    return db.query(GamaPreventivo).filter(GamaPreventivo.activa.is_(False)).all()


# UPDATE GENERAL
def update_gama_preventivo(db: Session,gama_id: int,data: GamaPreventivoUpdateSchema):
    gama = get_gama_by_id(db, gama_id)
    if not gama:
        raise HTTPException(status_code=404, detail="Gama no encontrada")

    if data.nombre is not None:
        gama.nombre = data.nombre
    if data.descripcion is not None:
        gama.descripcion = data.descripcion

    db.commit()
    db.refresh(gama)
    return gama


# UPDATE ESTADO
def update_estado_gama_preventivo(db: Session,gama_id: int,data: GamaPreventivoEstadoUpdateSchema):
    gama = get_gama_by_id(db, gama_id)
    if not gama:
        raise HTTPException(status_code=404, detail="Gama no encontrada")

    gama.activa = data.activa
    db.commit()
    db.refresh(gama)
    return gama

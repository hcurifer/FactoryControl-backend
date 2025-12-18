# app/services/peticiones_dia_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.peticiones_dia_model import PeticionDia
from app.models.user_model import User

from app.schemas.peticiones_dia_schema import (
    PeticionDiaCreateSchema,
    PeticionDiaUpdateSchema,
    EstadoPeticionDiaEnum,
)


# CREATE

def create_peticion_dia(db: Session,data: PeticionDiaCreateSchema) -> PeticionDia:

    usuario = (
        db.query(User)
        .filter(User.id_usuario == data.id_usuario)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if usuario.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario está dado de baja"
        )

    peticion = PeticionDia(
        id_usuario=data.id_usuario,
        tipo_peticion=data.tipo_peticion.value,
        comentario=data.comentario.strip() if data.comentario else None,
        estado=EstadoPeticionDiaEnum.pendiente.value,
        fecha_resolucion=None
    )

    db.add(peticion)
    db.commit()
    db.refresh(peticion)

    return peticion


# GET

def get_all_peticiones_dia(db: Session):
    return (
        db.query(PeticionDia)
        .order_by(PeticionDia.id_peticion.desc())
        .all()
    )


def get_peticiones_dia_por_usuario(db: Session,id_usuario: int):
    return (
        db.query(PeticionDia)
        .filter(PeticionDia.id_usuario == id_usuario)
        .order_by(PeticionDia.id_peticion.desc())
        .all()
    )


def get_peticion_dia_by_id(db: Session,id_peticion: int):
    return (
        db.query(PeticionDia)
        .filter(PeticionDia.id_peticion == id_peticion)
        .first()
    )


# UPDATE (resolución por mando)

def update_peticion_dia(db: Session,id_peticion: int,data: PeticionDiaUpdateSchema) -> PeticionDia:

    peticion = get_peticion_dia_by_id(db, id_peticion)

    if not peticion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petición no encontrada"
        )

    if peticion.estado != EstadoPeticionDiaEnum.pendiente.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La petición ya ha sido resuelta"
        )

    peticion.estado = data.estado.value
    peticion.fecha_resolucion = data.fecha_resolucion

    db.commit()
    db.refresh(peticion)

    return peticion

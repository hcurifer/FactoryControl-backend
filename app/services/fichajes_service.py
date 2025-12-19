# app/services/fichajes_service.py

from datetime import date, datetime, time
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.fichajes_model import Fichaje
from app.models.user_model import User

from app.schemas.fichajes_schema import (
    FichajeCreateSchema,
    FichajeSalidaSchema
)


# FICHAR ENTRADA

def fichar_entrada(db: Session, data: FichajeCreateSchema) -> Fichaje:
    usuario = db.query(User).filter(User.id_usuario == data.id_usuario).first()

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

    hoy = data.fecha or date.today()

    # Comprobar si ya existe un fichaje abierto hoy
    fichaje_abierto = (
        db.query(Fichaje)
        .filter(
            Fichaje.id_usuario == data.id_usuario,
            Fichaje.fecha == hoy,
            Fichaje.hora_salida.is_(None)
        )
        .first()
    )

    if fichaje_abierto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un fichaje abierto para este usuario hoy"
        )

    fichaje = Fichaje(
        id_usuario=data.id_usuario,
        fecha=hoy,
        hora_entrada=data.hora_entrada or datetime.now().time(),
        hora_salida=None,
        comentario=data.comentario
    )

    usuario.estado_disponible = True

    db.add(fichaje)
    db.commit()
    db.refresh(fichaje)

    return fichaje


# FICHAR SALIDA

def fichar_salida(db: Session,id_usuario: int,data: FichajeSalidaSchema) -> Fichaje:

    fichaje = (
        db.query(Fichaje)
        .filter(
            Fichaje.id_usuario == id_usuario,
            Fichaje.hora_salida.is_(None)
        )
        .order_by(Fichaje.fecha.desc())
        .first()
    )

    if not fichaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe un fichaje abierto para este usuario"
        )

    fichaje.hora_salida = data.hora_salida
    fichaje.comentario = data.comentario

    usuario = db.query(User).filter(User.id_usuario == id_usuario).first()
    if usuario:
        usuario.estado_disponible = False

    db.commit()
    db.refresh(fichaje)

    return fichaje


# GETTERS

def get_all_fichajes(db: Session):
    return (
        db.query(Fichaje)
        .order_by(Fichaje.fecha.desc())
        .all()
    )

def get_fichajes_por_usuario(db: Session, id_usuario: int):
    return (
        db.query(Fichaje)
        .filter(Fichaje.id_usuario == id_usuario)
        .order_by(Fichaje.fecha.desc())
        .all()
    )

def get_fichaje_abierto(db: Session, id_usuario: int):
    return (
        db.query(Fichaje)
        .filter(
            Fichaje.id_usuario == id_usuario,
            Fichaje.hora_salida.is_(None)
        )
        .first()
    )

from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreateSchema, UserEstadoUpdateSchema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import date


def create_user(db: Session, user: UserCreateSchema, hashed_password: str):
    existing_user = (
        db.query(User)
        .filter(
            (User.numero_empresa == user.numero_empresa)
            | (User.correo == user.correo)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese número de empresa o correo.",
        )
    new_user = User(
        numero_empresa=user.numero_empresa,
        nombre=user.nombre,
        apellidos=user.apellidos,
        correo=user.correo,
        contrasena_hash=hashed_password,
        rol=user.rol,
        estado_disponible=user.estado_disponible,
        imagen=user.imagen,
        fecha_alta=date.today(),
        fecha_baja=None
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha podido crear el usuario por un conflicto de datos (duplicados).",
        )

# GET

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id_usuario == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()

def get_usuarios_disponibles(db: Session):
    return (
        db.query(User)
        .filter(
            User.estado_disponible == True,
            User.fecha_baja.is_(None),
        )
        .all()
    )


def get_usuarios_no_disponibles(db: Session):
    return (
        db.query(User)
        .filter(
            (User.estado_disponible == False)
            | (User.fecha_baja.is_not(None))
        )
        .all()
    )
    
def get_usuarios_activos(db: Session):
    return (
        db.query(User)
        .filter(User.fecha_baja.is_(None))
        .all()
    )

def get_usuarios_inactivos(db: Session):
    return (
        db.query(User)
        .filter(User.fecha_baja.is_not(None))
        .all()
    )
    
    
# UPDATE

#Actualizar Estado Usuarios 
def update_user_disponibilidad(
    db: Session,
    user_id: int,
    estado_data: UserEstadoUpdateSchema
):
    # Buscar usuario
    usuario = db.query(User).filter(User.id_usuario == user_id).first()

    # Si no existe → 404
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    if usuario.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario dado de baja"
        )

    # Actualizar solo el estado
    usuario.estado_disponible = estado_data.estado_disponible

    # Guardar cambios
    db.commit()
    db.refresh(usuario)

    # Devolver usuario actualizado
    return usuario

 # DELETE logico, mantengo historial y relaciones FK, controlo con fecha de baja
 
def delete_user_logico(db: Session, user_id: int):
    # Buscar usuario
    usuario = db.query(User).filter(User.id_usuario == user_id).first()

    # Si no existe error 404
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Si esta de baja, notificamos
    if usuario.fecha_baja is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya está dado de baja"
        )

    # Baja logica
    usuario.estado_disponible = False
    usuario.fecha_baja = date.today()

    db.commit()
    db.refresh(usuario)

    return usuario

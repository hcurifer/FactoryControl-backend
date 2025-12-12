from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreateSchema
from datetime import date


def create_user(db: Session, user: UserCreateSchema, hashed_password: str):
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
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id_usuario == user_id).first()


def get_all_users(db: Session):
    return db.query(User).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user_schema import UserReadSchema, UserCreateSchema
from app.services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Dependencia para obtener una sesión de BD por request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[UserReadSchema])
def listar_usuarios(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/{user_id}", response_model=UserReadSchema)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = get_user_by_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/", response_model=UserReadSchema)
def crear_usuario(user: UserCreateSchema, db: Session = Depends(get_db)):
    # un hash provisional antes de implementar bcrypt
    hashed_password = "hashed_" + user.contrasena

    return create_user(db, user, hashed_password)

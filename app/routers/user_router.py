from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.user_schema import UserReadSchema, UserCreateSchema, UserEstadoUpdateSchema
from app.services.user_service import (
     create_user, 
     get_user_by_id, 
     get_all_users, 
     update_user_disponibilidad, 
     get_usuarios_disponibles, 
     get_usuarios_no_disponibles,
     get_usuarios_activos,
     get_usuarios_inactivos,
     delete_user_logico
)
               

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Dependencia para obtener una sesión de BD por request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET

@router.get("/", response_model=list[UserReadSchema])
def listar_usuarios(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get(
    "/activos",
    response_model=list[UserReadSchema],
    summary="Listar usuarios activos en la empresa"
)
def listar_usuarios_activos(db: Session = Depends(get_db)):
    return get_usuarios_activos(db)

@router.get(
    "/inactivos",
    response_model=list[UserReadSchema],
    summary="Listar usuarios dados de baja en la empresa"
)
def listar_usuarios_inactivos(db: Session = Depends(get_db)):
    return get_usuarios_inactivos(db)

@router.get(
    "/disponibles",
    response_model=list[UserReadSchema]
)
def listar_disponibles(db: Session = Depends(get_db)):
    return get_usuarios_disponibles(db)

@router.get(
    "/no-disponibles",
    response_model=list[UserReadSchema]
)
def listar_no_disponibles(db: Session = Depends(get_db)):
    return get_usuarios_no_disponibles(db)

@router.get("/{user_id}", response_model=UserReadSchema)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = get_user_by_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario



# UPDATE

@router.patch(
    "/{user_id}/disponibilidad",
    response_model=UserReadSchema
)
def cambiar_disponibilidad(
    user_id: int,
    estado: UserEstadoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_user_disponibilidad(db, user_id, estado)




# POST

@router.post("/", response_model=UserReadSchema)
def crear_usuario(user: UserCreateSchema, db: Session = Depends(get_db)):
    
    return create_user(db, user)


# DELETE logico

@router.delete(
    "/{user_id}",
    response_model=UserReadSchema,
)
def eliminar_usuario(
    user_id: int,
    db: Session = Depends(get_db),
):
    return delete_user_logico(db, user_id)

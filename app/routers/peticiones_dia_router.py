# app/routers/peticiones_dia_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.peticiones_dia_schema import (
    PeticionDiaCreateSchema,
    PeticionDiaReadSchema,
    PeticionDiaUpdateSchema,
)

from app.services.peticiones_dia_service import (
    create_peticion_dia,
    get_all_peticiones_dia,
    get_peticiones_dia_por_usuario,
    get_peticion_dia_by_id,
    update_peticion_dia,
)

router = APIRouter(prefix="/peticiones-dia",tags=["Peticiones de día"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE

@router.post("/",response_model=PeticionDiaReadSchema,status_code=status.HTTP_201_CREATED,summary="Crear una petición de día libre")
def crear_peticion(
    data: PeticionDiaCreateSchema,
    db: Session = Depends(get_db)
):
    return create_peticion_dia(db, data)


# GET

@router.get("/",response_model=list[PeticionDiaReadSchema],summary="Listar todas las peticiones de día")
def listar_peticiones(db: Session = Depends(get_db)):
    return get_all_peticiones_dia(db)


@router.get("/usuario/{id_usuario}",response_model=list[PeticionDiaReadSchema],summary="Listar peticiones de día por usuario")
def listar_peticiones_por_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    return get_peticiones_dia_por_usuario(db, id_usuario)


@router.get("/{id_peticion}",response_model=PeticionDiaReadSchema,summary="Obtener una petición de día por ID")
def obtener_peticion(
    id_peticion: int,
    db: Session = Depends(get_db)
):
    peticion = get_peticion_dia_by_id(db, id_peticion)
    if not peticion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Petición no encontrada"
        )
    return peticion


# UPDATE (resolución por mando)

@router.patch("/{id_peticion}",response_model=PeticionDiaReadSchema,summary="Resolver una petición de día (aprobada o rechazada)")
def resolver_peticion(
    id_peticion: int,
    data: PeticionDiaUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_peticion_dia(db, id_peticion, data)

# app/routers/fichajes_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.fichajes_schema import (
    FichajeCreateSchema,
    FichajeSalidaSchema,
    FichajeReadSchema
)

from app.services.fichajes_service import (
    fichar_entrada,
    fichar_salida,
    get_all_fichajes,
    get_fichajes_por_usuario,
    get_fichaje_abierto
)

router = APIRouter(prefix="/fichajes",tags=["Fichajes"])

# DB 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FICHAR ENTRADA

@router.post("/entrada",response_model=FichajeReadSchema,status_code=status.HTTP_201_CREATED,summary="Fichar entrada de un usuario")
def fichar_entrada_endpoint(
    data: FichajeCreateSchema,
    db: Session = Depends(get_db)
):
    return fichar_entrada(db, data)


# FICHAR SALIDA

@router.patch("/salida/{id_usuario}",response_model=FichajeReadSchema,summary="Fichar salida de un usuario")
def fichar_salida_endpoint(
    id_usuario: int,
    data: FichajeSalidaSchema,
    db: Session = Depends(get_db)
):
    return fichar_salida(db, id_usuario, data)


# GET HISTÓRICO

@router.get("/",response_model=list[FichajeReadSchema],summary="Listar todos los fichajes")
def listar_fichajes(db: Session = Depends(get_db)):
    return get_all_fichajes(db)


@router.get("/usuario/{id_usuario}",response_model=list[FichajeReadSchema],summary="Listar fichajes por usuario")
def listar_fichajes_por_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    return get_fichajes_por_usuario(db, id_usuario)


@router.get("/abierto/{id_usuario}",response_model=FichajeReadSchema,summary="Obtener fichaje abierto de un usuario")
def obtener_fichaje_abierto(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    fichaje = get_fichaje_abierto(db, id_usuario)
    if not fichaje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene un fichaje abierto"
        )
    return fichaje

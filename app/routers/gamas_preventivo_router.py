from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.gamas_preventivo_schema import (
    GamaPreventivoCreateSchema,
    GamaPreventivoReadSchema,
    GamaPreventivoUpdateSchema,
    GamaPreventivoEstadoUpdateSchema,
)
from app.services.gamas_preventivo_service import (
    create_gama_preventivo,
    get_all_gamas,
    get_gama_by_id,
    get_gamas_activas,
    get_gamas_inactivas,
    update_gama_preventivo,
    update_estado_gama_preventivo,
)

router = APIRouter(prefix="/gamas-preventivo",tags=["Gamas Preventivo"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/",response_model=GamaPreventivoReadSchema,status_code=status.HTTP_201_CREATED,summary="Crear una nueva gama de mantenimiento preventivo")
def crear_gama(
    data: GamaPreventivoCreateSchema,
    db: Session = Depends(get_db)
):
    return create_gama_preventivo(db, data)


# GET
@router.get("/",response_model=list[GamaPreventivoReadSchema],summary="Listar todas las gamas de preventivo")
def listar_gamas(db: Session = Depends(get_db)):
    return get_all_gamas(db)


@router.get("/activas",response_model=list[GamaPreventivoReadSchema],summary="Listar gamas de preventivo activas")
def listar_gamas_activas(db: Session = Depends(get_db)):
    return get_gamas_activas(db)


@router.get("/inactivas",response_model=list[GamaPreventivoReadSchema],summary="Listar gamas de preventivo inactivas")
def listar_gamas_inactivas(db: Session = Depends(get_db)):
    return get_gamas_inactivas(db)


@router.get("/{gama_id}",response_model=GamaPreventivoReadSchema,summary="Obtener una gama de preventivo por ID")
def obtener_gama(
    gama_id: int,
    db: Session = Depends(get_db)
):
    gama = get_gama_by_id(db, gama_id)
    if not gama:
        raise HTTPException(status_code=404, detail="Gama no encontrada")
    return gama


# UPDATE
@router.patch("/{gama_id}",response_model=GamaPreventivoReadSchema,summary="Actualizar datos generales de una gama de preventivo")
def actualizar_gama(
    gama_id: int,
    data: GamaPreventivoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_gama_preventivo(db, gama_id, data)


@router.patch("/{gama_id}/estado",response_model=GamaPreventivoReadSchema,summary="Activar o desactivar una gama de preventivo")
def cambiar_estado_gama(
    gama_id: int,
    data: GamaPreventivoEstadoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_estado_gama_preventivo(db, gama_id, data)

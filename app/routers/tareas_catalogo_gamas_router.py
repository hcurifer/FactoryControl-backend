from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.tareas_catalogo_gamas_schema import (
    TareaCatalogoGamaCreateSchema,
    TareaCatalogoGamaReadSchema,
    TareaCatalogoGamaUpdateSchema,
)
from app.services.tareas_catalogo_gamas_service import (
    create_tarea_catalogo_gama,
    get_all_tareas_catalogo_gamas,
    get_tareas_catalogo_por_gama,
    get_tarea_catalogo_gama_by_id,
    update_tarea_catalogo_gama,
    delete_tarea_catalogo_gama,
)

router = APIRouter(prefix="/tareas-catalogo-gamas",tags=["Tareas Catálogo Gamas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post("/",response_model=TareaCatalogoGamaReadSchema,status_code=status.HTTP_201_CREATED,summary="Crear una tarea en el catálogo de una gama de preventivo")
def crear_tarea_catalogo(
    data: TareaCatalogoGamaCreateSchema,
    db: Session = Depends(get_db)
):
    return create_tarea_catalogo_gama(db, data)


# GET
@router.get("/",response_model=list[TareaCatalogoGamaReadSchema],summary="Listar todas las tareas del catálogo de gamas")
def listar_tareas_catalogo(db: Session = Depends(get_db)):
    return get_all_tareas_catalogo_gamas(db)


@router.get("/gama/{id_gama}",response_model=list[TareaCatalogoGamaReadSchema],summary="Listar tareas del catálogo asociadas a una gama")
def listar_por_gama(
    id_gama: int,
    db: Session = Depends(get_db)
):
    return get_tareas_catalogo_por_gama(db, id_gama)


@router.get("/{tarea_id}",response_model=TareaCatalogoGamaReadSchema,summary="Obtener una tarea del catálogo por ID")
def obtener_tarea_catalogo(
    tarea_id: int,
    db: Session = Depends(get_db)
):
    tarea = get_tarea_catalogo_gama_by_id(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea de catálogo no encontrada")
    return tarea


# UPDATE
@router.patch("/{tarea_id}",response_model=TareaCatalogoGamaReadSchema,summary="Actualizar una tarea del catálogo de gamas")
def actualizar_tarea_catalogo(
    tarea_id: int,
    data: TareaCatalogoGamaUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_tarea_catalogo_gama(db, tarea_id, data)


# DELETE
@router.delete("/{tarea_id}",status_code=status.HTTP_204_NO_CONTENT,summary="Eliminar una tarea del catálogo de gamas")
def eliminar_tarea_catalogo(
    tarea_id: int,
    db: Session = Depends(get_db)
):
    delete_tarea_catalogo_gama(db, tarea_id)
    return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.maquinas_schema import (
    MaquinaCreateSchema,
    MaquinaReadSchema,
    MaquinaUpdateSchema,
    MaquinaEstadoUpdateSchema,
    MaquinaAlarmaUpdateSchema,
    EstadoMaquinaEnum,
)
from app.services.maquinas_service import (
    create_maquina,
    get_maquina_by_id,
    get_all_maquinas,
    get_maquinas_activas,
    get_maquinas_inactivas,
    get_maquinas_con_alarma,
    get_maquinas_en_produccion,
    get_maquinas_paradas,
    get_maquinas_pendiente_preventivo,
    update_maquina,
    update_maquina_estado,
    update_maquina_alarma,
    delete_maquina_logico,
    delete_maquina_fisico,
)

router = APIRouter(prefix="/maquinas", tags=["Máquinas"])


# DB dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE

@router.post(
    "/",
    response_model=MaquinaReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva máquina"
)
def crear_maquina(
    data: MaquinaCreateSchema,
    db: Session = Depends(get_db)
):
    return create_maquina(db, data)


# GET

@router.get(
    "/",
    response_model=list[MaquinaReadSchema],
    summary="Listar todas las máquinas"
)
def listar_maquinas(db: Session = Depends(get_db)):
    return get_all_maquinas(db)


@router.get(
    "/activas",
    response_model=list[MaquinaReadSchema],
    summary="Listar máquinas activas"
)
def listar_maquinas_activas(db: Session = Depends(get_db)):
    return get_maquinas_activas(db)


@router.get(
    "/inactivas",
    response_model=list[MaquinaReadSchema],
    summary="Listar máquinas dadas de baja"
)
def listar_maquinas_inactivas(db: Session = Depends(get_db)):
    return get_maquinas_inactivas(db)


@router.get(
    "/con-alarma",
    response_model=list[MaquinaReadSchema],
    summary="Listar máquinas con alarma activa"
)
def listar_maquinas_con_alarma(db: Session = Depends(get_db)):
    return get_maquinas_con_alarma(db)


@router.get(
    "/produccion",
    response_model=list[MaquinaReadSchema],
    summary="Máquinas en producción"
)
def listar_maquinas_produccion(db: Session = Depends(get_db)):
    return get_maquinas_en_produccion(db)


@router.get(
    "/paradas",
    response_model=list[MaquinaReadSchema],
    summary="Máquinas paradas"
)
def listar_maquinas_paradas(db: Session = Depends(get_db)):
    return get_maquinas_paradas(db)


@router.get(
    "/pendiente-preventivo",
    response_model=list[MaquinaReadSchema],
    summary="Máquinas pendientes de preventivo"
)
def listar_maquinas_pendiente_preventivo(db: Session = Depends(get_db)):
    return get_maquinas_pendiente_preventivo(db)


@router.get(
    "/{maquina_id}",
    response_model=MaquinaReadSchema,
    summary="Obtener máquina por ID"
)
def obtener_maquina(
    maquina_id: int,
    db: Session = Depends(get_db)
):
    maquina = get_maquina_by_id(db, maquina_id)
    if not maquina:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return maquina


# UPDATE

@router.patch(
    "/{maquina_id}",
    response_model=MaquinaReadSchema,
    summary="Actualizar datos generales de una máquina"
)
def actualizar_maquina(
    maquina_id: int,
    data: MaquinaUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_maquina(db, maquina_id, data)


@router.patch(
    "/{maquina_id}/estado",
    response_model=MaquinaReadSchema,
    summary="Cambiar estado de la máquina"
)
def actualizar_estado_maquina(
    maquina_id: int,
    data: MaquinaEstadoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_maquina_estado(db, maquina_id, data)


@router.patch(
    "/{maquina_id}/alarma",
    response_model=MaquinaReadSchema,
    summary="Activar o desactivar alarma de la máquina"
)
def actualizar_alarma_maquina(
    maquina_id: int,
    data: MaquinaAlarmaUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_maquina_alarma(db, maquina_id, data)


# DELETE

@router.delete(
    "/{maquina_id}",
    response_model=MaquinaReadSchema,
    summary="Dar de baja lógica una máquina"
)
def eliminar_maquina_logico(
    maquina_id: int,
    db: Session = Depends(get_db)
):
    return delete_maquina_logico(db, maquina_id)


@router.delete(
    "/{maquina_id}/fisico",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar máquina definitivamente"
)
def eliminar_maquina_fisico(
    maquina_id: int,
    db: Session = Depends(get_db)
):
    delete_maquina_fisico(db, maquina_id)
    return None

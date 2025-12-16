from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.averias_urgentes_schema import (
    AveriaUrgenteCreateSchema,
    AveriaUrgenteReadSchema,
    AveriaUrgenteUpdateSchema,
    AveriaUrgenteEstadoUpdateSchema,
    EstadoAveriaUrgenteEnum,
)
from app.services.averias_urgentes_service import (
    create_averia_urgente,
    get_averia_by_id,
    get_all_averias,
    get_averias_por_estado,
    get_averias_por_maquina,
    get_averias_por_usuario_asignado,
    update_averia_urgente,
    update_estado_averia_urgente,
)

router = APIRouter(
    prefix="/averias-urgentes",
    tags=["Averías urgentes"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE POST

@router.post(
    "/",
    response_model=AveriaUrgenteReadSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una avería urgente"
)
def crear_averia_urgente(
    data: AveriaUrgenteCreateSchema,
    db: Session = Depends(get_db)
):
    return create_averia_urgente(db, data)

# GET

@router.get(
    "/",
    response_model=list[AveriaUrgenteReadSchema],
    summary="Listar todas las averías urgentes"
)
def listar_averias(db: Session = Depends(get_db)):
    return get_all_averias(db)

@router.get(
    "/{averia_id}",
    response_model=AveriaUrgenteReadSchema,
    summary="Obtener avería urgente por ID"
)
def obtener_averia(
    averia_id: int,
    db: Session = Depends(get_db)
):
    averia = get_averia_by_id(db, averia_id)
    if not averia:
        raise HTTPException(status_code=404, detail="Avería no encontrada")
    return averia

@router.get(
    "/estado/{estado}",
    response_model=list[AveriaUrgenteReadSchema],
    summary="Listar averías urgentes por estado"
)
def listar_por_estado(
    estado: EstadoAveriaUrgenteEnum,
    db: Session = Depends(get_db)
):
    return get_averias_por_estado(db, estado)

@router.get(
    "/maquina/{id_maquina}",
    response_model=list[AveriaUrgenteReadSchema],
    summary="Listar averías urgentes por máquina"
)
def listar_por_maquina(
    id_maquina: int,
    db: Session = Depends(get_db)
):
    return get_averias_por_maquina(db, id_maquina)

@router.get(
    "/usuario-asignado/{id_usuario}",
    response_model=list[AveriaUrgenteReadSchema],
    summary="Listar averías urgentes por técnico asignado"
)
def listar_por_usuario_asignado(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    return get_averias_por_usuario_asignado(db, id_usuario)

# UPDATE 

@router.patch(
    "/{averia_id}",
    response_model=AveriaUrgenteReadSchema,
    summary="Actualizar datos generales de una avería urgente"
)
def actualizar_averia(
    averia_id: int,
    data: AveriaUrgenteUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_averia_urgente(db, averia_id, data)

@router.patch(
    "/{averia_id}/estado",
    response_model=AveriaUrgenteReadSchema,
    summary="Cambiar estado de una avería urgente"
)
def actualizar_estado_averia(
    averia_id: int,
    data: AveriaUrgenteEstadoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_estado_averia_urgente(db, averia_id, data)

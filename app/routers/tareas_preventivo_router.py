from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.tareas_preventivo_schema import (
    TareaPreventivoCreateSchema,
    TareaPreventivoReadSchema,
    TareaPreventivoUpdateSchema,
    TareaPreventivoEstadoUpdateSchema,
    GenerarTareasPreventivoSchema
)
from app.services.tareas_preventivo_service import (
    create_tarea_preventivo,
    get_all_tareas_preventivo,
    get_tareas_por_usuario,
    get_tareas_por_maquina,
    update_tarea_preventivo,
    update_estado_tarea_preventivo,
    generar_tareas_desde_gama
)

router = APIRouter(prefix="/tareas-preventivo",tags=["Tareas Preventivo"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TareaPreventivoReadSchema, status_code=status.HTTP_201_CREATED, summary="Crear una tarea de mantenimiento preventivo asignada a un técnico")
def crear_tarea(data: TareaPreventivoCreateSchema, db: Session = Depends(get_db)):
    return create_tarea_preventivo(db, data)


@router.get("/", response_model=list[TareaPreventivoReadSchema], summary="Listar todas las tareas de preventivo")
def listar_tareas(db: Session = Depends(get_db)):
    return get_all_tareas_preventivo(db)


@router.get("/usuario/{id_usuario}", response_model=list[TareaPreventivoReadSchema], summary="Listar tareas de preventivo asignadas a un técnico")
def listar_por_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return get_tareas_por_usuario(db, id_usuario)


@router.get("/maquina/{id_maquina}", response_model=list[TareaPreventivoReadSchema], summary="Listar tareas de preventivo asociadas a una máquina")
def listar_por_maquina(id_maquina: int, db: Session = Depends(get_db)):
    return get_tareas_por_maquina(db, id_maquina)


@router.patch("/{tarea_id}", response_model=TareaPreventivoReadSchema, summary="Actualizar observaciones de una tarea de preventivo")
def actualizar_tarea(
    tarea_id: int,
    data: TareaPreventivoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_tarea_preventivo(db, tarea_id, data)


@router.patch("/{tarea_id}/estado", response_model=TareaPreventivoReadSchema, summary="Cambiar el estado de una tarea de preventivo")
def cambiar_estado(
    tarea_id: int,
    data: TareaPreventivoEstadoUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_estado_tarea_preventivo(db, tarea_id, data)


# GENERADOR

@router.post("/generar",response_model=list[TareaPreventivoReadSchema],summary="Generar tareas preventivas a partir de una gama")
def generar_tareas(
    data: GenerarTareasPreventivoSchema,
    db: Session = Depends(get_db)
):
    return generar_tareas_desde_gama(db, data)
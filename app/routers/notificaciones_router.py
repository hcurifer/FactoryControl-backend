# app/routers/notificaciones_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.schemas.notificaciones_schema import (
    NotificacionCreateSchema,
    NotificacionReadSchema,
    TipoNotificacionEnum,
)

from app.services.notificaciones_service import (
    create_notificacion,
    get_notificacion_by_id,
    get_all_notificaciones,
    get_notificaciones_por_usuario_destino,
    get_notificaciones_por_maquina,
    get_notificaciones_por_tipo,
)

router = APIRouter(prefix="/notificaciones",tags=["Notificaciones"])

# DB 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE

@router.post("/",response_model=NotificacionReadSchema,status_code=status.HTTP_201_CREATED,summary="Crear una notificación del sistema")
def crear_notificacion(
    data: NotificacionCreateSchema,
    db: Session = Depends(get_db)
):
    return create_notificacion(db, data)

# GET

@router.get("/",response_model=list[NotificacionReadSchema],summary="Listar todas las notificaciones")
def listar_notificaciones(
    db: Session = Depends(get_db)
):
    return get_all_notificaciones(db)

@router.get("/{id_notificacion}",response_model=NotificacionReadSchema,summary="Obtener una notificación por ID")
def obtener_notificacion(
    id_notificacion: int,
    db: Session = Depends(get_db)
):
    notificacion = get_notificacion_by_id(db, id_notificacion)
    if not notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    return notificacion

@router.get("/usuario-destino/{id_usuario}",response_model=list[NotificacionReadSchema],summary="Listar notificaciones por usuario destino")
def listar_por_usuario_destino(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    return get_notificaciones_por_usuario_destino(db, id_usuario)

@router.get("/maquina/{id_maquina}",response_model=list[NotificacionReadSchema],summary="Listar notificaciones asociadas a una máquina")
def listar_por_maquina(
    id_maquina: int,
    db: Session = Depends(get_db)
):
    return get_notificaciones_por_maquina(db, id_maquina)

@router.get("/tipo/{tipo}",response_model=list[NotificacionReadSchema],summary="Listar notificaciones por tipo")
def listar_por_tipo(
    tipo: TipoNotificacionEnum,
    db: Session = Depends(get_db)
):
    return get_notificaciones_por_tipo(db, tipo)

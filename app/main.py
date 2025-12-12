# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routers import health_router

from app.db.session import engine
from app.db.base import Base

from app.routers import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta al iniciar la aplicación
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente.")

    # FastAPI continúa funcionando
    yield

    # Se ejecuta al cerrar la aplicación (opcional)
    print("Aplicación apagándose...")

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="Backend de FactoryControl - Gestión de mantenimiento industrial",
        lifespan=lifespan,
    )

    # CORS 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health_router.router)       
    app.include_router(user_router.router)  
   
   
    return app

# instancia final de la APP
app = create_application()


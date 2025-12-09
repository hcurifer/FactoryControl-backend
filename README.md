# FactoryControl-backend
Backend en FastAPI para la aplicación FactoryControl. Incluye API REST, JWT, PostgreSQL y lógica de negocio 

# FactoryControl – Backend (FastAPI + PostgreSQL)

Repositorio del backend de FactoryControl. Proporciona una API REST para gestionar:
usuarios, máquinas, averías, gamas de preventivo, notificaciones y carga de trabajo.

## Tecnologías
- FastAPI
- Python 3.12
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT + OAuth2
- Uvicorn

## Instalación

python -m venv env  
source env/bin/activate  (Windows: env\Scripts\activate)  
pip install -r requirements.txt  
uvicorn main:app --reload

## Estructura
app/
 ├── routers/
 ├── models/
 ├── schemas/
 ├── services/
 ├── core/
 └── database/

## 🗄 Base de datos
Incluye backup SQL y diagrama ER en `factorycontrol-docs`.

## 🔗 Frontend
https://github.com/hcurifer/FactoryControl-frontend

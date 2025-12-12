from sqlalchemy.orm import declarative_base

#modelos  (esto no ha funcionado crea un bucle circular al importarlo en user.py)
#from app.models.user import User  

#NO PONER MAS MODELOS, PRIMERA PRUEBA MAL, REALIZAR LA LLAMADA EN EL MODELO



Base = declarative_base()

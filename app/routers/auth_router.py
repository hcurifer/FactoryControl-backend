from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.db.session import get_db
from app.models.user_model import User
from app.core.security import verify_password, create_access_token
from app.core.auth import get_current_user
from app.schemas.user_schema import UserReadSchema


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get(
    "/me",
    response_model=UserReadSchema,
    )
        
def read_me(current_user = Depends(get_current_user)):
    return current_user

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    )

def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
    ):

    # Autenticación de usuario.
    # Recibe número de empresa y contraseña y devuelve un token JWT.

    # LÓGICA 
    
    user = (
        db.query(User)
        .filter(User.numero_empresa == credentials.numero_empresa)
        .first()
    )

    # Usuario no existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
        
    # Usuario dado de baja
    if user.fecha_baja is not None:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no autorizado",
        )
         
    # Validar contraseña
    if not verify_password(credentials.password, user.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    # JWT TOKEN    
    access_token = create_access_token(
        data={
            "sub": user.numero_empresa,
            "rol": user.rol,
            "id_usuario": user.id_usuario,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id_usuario": user.id_usuario,
            "nombre": user.nombre,
            "apellidos": user.apellidos,
            "rol": user.rol,
        },
    }
    

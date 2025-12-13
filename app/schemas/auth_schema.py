from pydantic import BaseModel, Field


class LoginRequest(BaseModel):

    # Datos necesarios para iniciar sesión.

    numero_empresa: str = Field(
        ...,
        json_schema_extra={"example": "12345"}
    )
    password: str = Field(
        ...,
        json_schema_extra={"example": "********"}
    )

class UserLoginResponse(BaseModel):

    # Información básica del usuario autenticado.

    id_usuario: int
    nombre: str
    apellidos: str
    rol: str


class LoginResponse(BaseModel):

    # Respuesta devuelta tras un login correcto.

    access_token: str
    token_type: str = "bearer"
    user: UserLoginResponse

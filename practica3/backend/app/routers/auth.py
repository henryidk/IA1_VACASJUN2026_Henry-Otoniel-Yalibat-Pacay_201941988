from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token
from app.models.usuario import Usuario
from app.schemas.usuario import Token, UsuarioCreate, UsuarioOut
from app.services.usuario import autenticar_usuario, crear_usuario, obtener_por_email

router = APIRouter(prefix="/api/auth", tags=["autenticación"])


@router.post("/register", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(datos: UsuarioCreate, db: Session = Depends(get_db)):
    if obtener_por_email(db, datos.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")
    return crear_usuario(db, datos)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=usuario.email)
    return Token(access_token=access_token)


@router.get("/me", response_model=UsuarioOut)
def perfil_actual(usuario_actual: Usuario = Depends(get_current_user)):
    return usuario_actual

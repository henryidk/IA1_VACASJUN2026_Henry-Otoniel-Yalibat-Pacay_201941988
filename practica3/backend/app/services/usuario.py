from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


def obtener_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        password_hash=hash_password(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def autenticar_usuario(db: Session, email: str, password: str) -> Usuario | None:
    usuario = obtener_por_email(db, email)
    if usuario is None or not verify_password(password, usuario.password_hash):
        return None
    return usuario

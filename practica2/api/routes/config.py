from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Config
from dependencies import get_admin_session

router = APIRouter(prefix="/config", tags=["config"])


class ChatIdUpdate(BaseModel):
    chat_id: str


@router.get("/chat_id")
def obtener_chat_id(db: Session = Depends(get_db)):
    config = db.query(Config).filter(Config.clave == "telegram_chat_id").first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return {"chat_id": config.valor}


@router.put("/chat_id")
def actualizar_chat_id(data: ChatIdUpdate, db: Session = Depends(get_db), admin=Depends(get_admin_session)):
    if not admin:
        raise HTTPException(status_code=401, detail="No autenticado")
    config = db.query(Config).filter(Config.clave == "telegram_chat_id").first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    config.valor = data.chat_id
    db.commit()
    return {"mensaje": "Chat ID actualizado", "chat_id": config.valor}

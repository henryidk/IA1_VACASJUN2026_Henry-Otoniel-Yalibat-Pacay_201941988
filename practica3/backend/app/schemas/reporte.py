from pydantic import BaseModel


class EnviarReporteRequest(BaseModel):
    destinatario: str | None = None

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JogadorBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    posicao: Optional[str] = None
    habilidade: Optional[float] = 5.0

class JogadorCreate(JogadorBase):
    pass

class JogadorUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    posicao: Optional[str] = None
    habilidade: Optional[float] = None
    ativo: Optional[bool] = None

class JogadorResponse(JogadorBase):
    id: int
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True

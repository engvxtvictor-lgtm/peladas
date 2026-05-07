from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.partida import Partida, Presenca
from app.models.jogador import Jogador
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/partidas", tags=["partidas"])

class PartidaCreate(BaseModel):
    data: datetime
    local: Optional[str] = None
    valor_por_jogador: Optional[int] = 0

class PartidaResponse(BaseModel):
    id: int
    data: datetime
    local: Optional[str]
    valor_por_jogador: int
    status: str
    criado_em: datetime

    class Config:
        from_attributes = True

class PresencaCreate(BaseModel):
    jogador_id: int

@router.get("/", response_model=List[PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return db.query(Partida).all()

@router.post("/", response_model=PartidaResponse)
def criar_partida(partida: PartidaCreate, db: Session = Depends(get_db)):
    db_partida = Partida(**partida.model_dump())
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida

@router.get("/{partida_id}", response_model=PartidaResponse)
def buscar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida

@router.post("/{partida_id}/confirmar")
def confirmar_presenca(partida_id: int, dados: PresencaCreate, db: Session = Depends(get_db)):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    jogador = db.query(Jogador).filter(Jogador.id == dados.jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    presenca = db.query(Presenca).filter(
        Presenca.partida_id == partida_id,
        Presenca.jogador_id == dados.jogador_id
    ).first()
    if presenca:
        presenca.confirmado = True
    else:
        presenca = Presenca(partida_id=partida_id, jogador_id=dados.jogador_id, confirmado=True)
        db.add(presenca)
    db.commit()
    return {"message": "Presença confirmada!"}

@router.get("/{partida_id}/presencas")
def listar_presencas(partida_id: int, db: Session = Depends(get_db)):
    presencas = db.query(Presenca).filter(Presenca.partida_id == partida_id).all()
    return [{"jogador_id": p.jogador_id, "confirmado": p.confirmado, "pago": p.pago} for p in presencas]
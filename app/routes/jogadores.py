from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.jogador import Jogador
from app.schemas.jogador import JogadorCreate, JogadorUpdate, JogadorResponse
from typing import List

router = APIRouter(prefix="/jogadores", tags=["jogadores"])

@router.get("/", response_model=List[JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    return db.query(Jogador).filter(Jogador.ativo == True).all()

@router.post("/", response_model=JogadorResponse)
def cadastrar_jogador(jogador: JogadorCreate, db: Session = Depends(get_db)):
    db_jogador = Jogador(**jogador.model_dump())
    db.add(db_jogador)
    db.commit()
    db.refresh(db_jogador)
    return db_jogador

@router.get("/{jogador_id}", response_model=JogadorResponse)
def buscar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador

@router.patch("/{jogador_id}", response_model=JogadorResponse)
def atualizar_jogador(jogador_id: int, dados: JogadorUpdate, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(jogador, campo, valor)
    db.commit()
    db.refresh(jogador)
    return jogador

@router.delete("/{jogador_id}")
def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    jogador.ativo = False
    db.commit()
    return {"message": "Jogador desativado com sucesso"}
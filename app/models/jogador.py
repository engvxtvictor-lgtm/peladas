from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    posicao = Column(String, nullable=True)
    habilidade = Column(Float, default=5.0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
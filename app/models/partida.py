from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Partida(Base):
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, nullable=False)
    local = Column(String, nullable=True)
    valor_por_jogador = Column(Float, default=0)
    status = Column(String, default="aberta")  # aberta, confirmada, encerrada
    criado_em = Column(DateTime, server_default=func.now())

    presencas = relationship("Presenca", back_populates="partida")


class Presenca(Base):
    __tablename__ = "presencas"

    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=False)
    jogador_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    confirmado = Column(Boolean, default=False)
    pago = Column(Boolean, default=False)

    partida = relationship("Partida", back_populates="presencas")
    jogador = relationship("Jogador")
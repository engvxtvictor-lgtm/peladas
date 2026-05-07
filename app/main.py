from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models.jogador import Jogador
from app.models.partida import Partida, Presenca
from datetime import datetime
import app.models
from app.routes import jogadores, partidas

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Sistema de Peladas')

templates = Jinja2Templates(directory='app/templates')

app.include_router(jogadores.router)
app.include_router(partidas.router)

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, 'index.html')

@app.get('/jogadores', response_class=HTMLResponse)
def pagina_jogadores(request: Request, db: Session = Depends(get_db)):
    lista = db.query(Jogador).filter(Jogador.ativo == True).all()
    return templates.TemplateResponse(request, 'jogadores.html', {'jogadores': lista})

@app.post('/jogadores/cadastrar', response_class=HTMLResponse)
def cadastrar_jogador_html(request: Request, db: Session = Depends(get_db),
    nome: str = Form(...), telefone: str = Form(None),
    posicao: str = Form(None), habilidade: float = Form(5.0)):
    jogador = Jogador(nome=nome, telefone=telefone, posicao=posicao, habilidade=habilidade)
    db.add(jogador)
    db.commit()
    db.refresh(jogador)
    return RedirectResponse(url='/jogadores', status_code=303)

@app.get('/partidas', response_class=HTMLResponse)
def pagina_partidas(request: Request, db: Session = Depends(get_db)):
    lista = db.query(Partida).order_by(Partida.data.desc()).all()
    return templates.TemplateResponse(request, 'partidas.html', {'partidas': lista})

@app.post('/partidas/criar')
def criar_partida_html(request: Request, db: Session = Depends(get_db),
    data: str = Form(...), local: str = Form(None),
    valor_por_jogador: float = Form(0), max_jogadores: int = Form(10)):
    partida = Partida(data=datetime.fromisoformat(data), local=local, valor_por_jogador=valor_por_jogador, max_jogadores=max_jogadores)
    db.add(partida)
    db.commit()
    return RedirectResponse(url='/partidas', status_code=303)

@app.get('/partidas/{partida_id}', response_class=HTMLResponse)
def detalhe_partida(partida_id: int, request: Request, db: Session = Depends(get_db)):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        return RedirectResponse(url='/partidas')
    confirmados = db.query(Presenca).filter(
        Presenca.partida_id == partida_id,
        Presenca.confirmado == True
    ).all()
    ids_confirmados = [p.jogador_id for p in confirmados]
    jogadores_lista = db.query(Jogador).filter(
        Jogador.ativo == True,
        Jogador.id.notin_(ids_confirmados)
    ).all()
    return templates.TemplateResponse(request, 'partida_detalhe.html', {
        'partida': partida,
        'confirmados': confirmados,
        'jogadores': jogadores_lista,
        'times': None
    })

@app.post('/partidas/{partida_id}/confirmar')
def confirmar_presenca_html(partida_id: int, db: Session = Depends(get_db),
    jogador_id: int = Form(...)):
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    confirmados = db.query(Presenca).filter(
        Presenca.partida_id == partida_id,
        Presenca.confirmado == True
    ).count()
    if confirmados >= partida.max_jogadores:
        return RedirectResponse(url=f'/partidas/{partida_id}?erro=lotado', status_code=303)
    presenca = db.query(Presenca).filter(
        Presenca.partida_id == partida_id,
        Presenca.jogador_id == jogador_id
    ).first()
    if presenca:
        presenca.confirmado = True
    else:
        presenca = Presenca(partida_id=partida_id, jogador_id=jogador_id, confirmado=True)
        db.add(presenca)
    db.commit()
    return RedirectResponse(url=f'/partidas/{partida_id}', status_code=303)

@app.post('/partidas/{partida_id}/sortear', response_class=HTMLResponse)
def sortear_times_html(partida_id: int, request: Request, db: Session = Depends(get_db)):
    from app.services.sorteio import sortear_times
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    confirmados = db.query(Presenca).filter(
        Presenca.partida_id == partida_id,
        Presenca.confirmado == True
    ).all()
    jogadores_confirmados = [p.jogador for p in confirmados]
    times = sortear_times(jogadores_confirmados)
    times_enumerados = list(enumerate(times, start=1))
    jogadores_lista = db.query(Jogador).filter(Jogador.ativo == True).all()
    return templates.TemplateResponse(request, 'partida_detalhe.html', {
        'partida': partida,
        'confirmados': confirmados,
        'jogadores': jogadores_lista,
        'times': times_enumerados
    })

@app.post('/partidas/{partida_id}/pagamento/{jogador_id}')
def marcar_pagamento(partida_id: int, jogador_id: int, db: Session = Depends(get_db)):
    presenca = db.query(Presenca).filter(
        Presenca.partida_id == partida_id,
        Presenca.jogador_id == jogador_id
    ).first()
    if presenca:
        presenca.pago = not presenca.pago
        db.commit()
    return RedirectResponse(url=f'/partidas/{partida_id}', status_code=303)
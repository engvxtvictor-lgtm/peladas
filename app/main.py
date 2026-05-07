from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models.jogador import Jogador
from app.models.partida import Partida
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
    valor_por_jogador: float = Form(0)):
    partida = Partida(data=datetime.fromisoformat(data), local=local, valor_por_jogador=valor_por_jogador)
    db.add(partida)
    db.commit()
    return RedirectResponse(url='/partidas', status_code=303)
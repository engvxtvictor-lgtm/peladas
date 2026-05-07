from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Sistema de Peladas')

templates = Jinja2Templates(directory='app/templates')

@app.get('/')
def index():
    return {'status': 'ok', 'message': 'Sistema de Peladas rodando!'}
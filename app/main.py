from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, crud, schemas
from datetime import date
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from app.endpoints import router


#from app.endpoints import router as endpoints_router
#from app.endpoints import clientes_router, mesas_router, pedidos_router

# Iniciar el server:  uvicorn app.main:app --reload

# detener el server: CTRL+C

# Crear todas las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de Jinja2Templates para usar la carpeta 'templates'
templates = Jinja2Templates(directory="app/templates")

# Montar la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#app.include_router(endpoints_router)
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test")
def test_endpoint():
    return {"message": "Server is working"}

#============================ I C O N ======================================== 
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/assets/favicon.ico")

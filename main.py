from fastapi import FastAPI
from app.models import model
from app.database.connection import engine
from contextlib import asynccontextmanager
from app.routes import users, pets, diaries, medical, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: cria tabelas
    model.Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: limpeza
    engine.dispose()


app = FastAPI(
    title="Petto API",
    description="API para gerenciamento de pets, com funcionalidades de cadastro, atualização e consulta de informações sobre os pets e seus donos.",
    version="1.0.0",
    lifespan=lifespan,
)

# todas as rotas
app.include_router(users.router)
app.include_router(pets.router)
app.include_router(diaries.router)
app.include_router(medical.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API Petto!"}
from fastapi import FastAPI  # Ferramenta para criar API
from app.api.v1.auth import router as auth_router  # Rotas de autenticação
from app.api.v1.users import router as users_router  # Rotas de usuários

app = FastAPI(title="Library API", version="1.0.0", description="API for managing users in an online library")  # Cria API

app.include_router(auth_router, prefix="/api/v1")  # Adiciona rotas de autenticação
app.include_router(users_router, prefix="/api/v1")  # Adiciona rotas de usuários

@app.get("/", summary="Welcome message", description="Returns a welcome message for the Library API.")
async def root():  # Rota inicial
    return {"message": "Welcome to the Library API"}
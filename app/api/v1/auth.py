from fastapi import APIRouter, HTTPException  # Ferramentas para rotas e erros
from app.core.database import get_supabase  # Conexão com Supabase
from ...models.user import UserCreate  # Modelo para criar usuário
from supabase import Client  # Tipo Client

router = APIRouter(prefix="/auth", tags=["Authentication"])  # Grupo de rotas /auth

@router.post("/signup", status_code=201, summary="Register a new user", description="Creates a new user with email, password, name, and role. Saves credentials in Supabase Auth and profile in the profiles table.")
async def signup(user: UserCreate):  # Recebe dados do usuário
    supabase: Client = get_supabase()  # Conecta ao Supabase
    try:  # Tenta cadastrar
        # Cadastra no Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        if not auth_response.user:  # Se falhar
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        # Salva perfil na tabela profiles
        profile_data = {
            "id": auth_response.user.id,  # ID do usuário
            "full_name": user.full_name,  # Nome
            "role": user.role  # Função
        }
        supabase.table("profiles").insert(profile_data).execute()
        
        return {"message": "User created successfully"}  # Sucesso
    except Exception as e:  # Se der erro
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", summary="Log in a user", description="Authenticates a user with email and password, returning a JWT token for accessing protected routes.")
async def login(email: str, password: str):  # Recebe email e senha
    supabase: Client = get_supabase()  # Conecta ao Supabase
    try:  # Tenta fazer login
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if not response.session:  # Se falhar
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return {
            "access_token": response.session.access_token,  # Token
            "token_type": "bearer"  # Tipo do token
        }
    except Exception:  # Se der erro
        raise HTTPException(status_code=401, detail="Invalid email or password")
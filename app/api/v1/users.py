from fastapi import APIRouter, HTTPException, Depends  # Ferramentas para rotas, erros e dependências
from app.core.database import get_supabase  # Conexão com Supabase
from app.models.user import User, UserUpdate  # Modelos de usuário
from supabase import Client  # Tipo Client
from fastapi.security import OAuth2PasswordBearer  # Para verificar tokens

router = APIRouter()  # Grupo de rotas /users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  # Onde pegar o token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    supabase: Client = get_supabase()
    try:
        user = supabase.auth.get_user(token)
        print("🧪 DEBUG user:", user)
        if not user or not getattr(user.user, "id", None):
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user.id
    except Exception as e:
        print("❌ Erro ao obter usuário:", e)
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/", response_model=list[User], summary="List all users", description="Returns a list of all user profiles. Requires authentication.")
async def list_users(current_user: str = Depends(get_current_user)):  # Só para logados

    supabase: Client = get_supabase()  # Conecta ao Supabase
    response = supabase.table("profiles").select("*").execute()  # Pega todos os perfis
    return response.data  # Devolve lista

@router.get("/{user_id}", response_model=User, summary="Get user by ID", description="Returns details of a user by their ID. Requires authentication.")
async def get_user(user_id: str, current_user: str = Depends(get_current_user)):  # Só para logados
    supabase: Client = get_supabase()  # Conecta ao Supabase
    response = supabase.table("profiles").select("*").eq("id", user_id).execute()  # Busca usuário
    if not response.data:  # Se não encontrar
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]  # Devolve usuário

@router.put("/{user_id}", response_model=User, summary="Update user profile", description="Updates a user's name or role. Only the user themselves can update their profile. Requires authentication.")
async def update_user(user_id: str, user_update: UserUpdate, current_user: str = Depends(get_current_user)):
    supabase: Client = get_supabase()  # Conecta ao Supabase
    if current_user != user_id:  # Só o próprio usuário pode atualizar
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}  # Campos não vazios
    if not update_data:  # Se nada for enviado
        raise HTTPException(status_code=400, detail="No data to update")
    response = supabase.table("profiles").update(update_data).eq("id", user_id).execute()  # Atualiza
    if not response.data:  # Se falhar
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]  # Devolve usuário atualizado
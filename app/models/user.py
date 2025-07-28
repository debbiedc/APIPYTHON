from pydantic import BaseModel, EmailStr  # Ferramentas para validar dados
from datetime import datetime  # Para datas
from typing import Optional  # Para campos opcionais

class UserBase(BaseModel):  # Campos comuns
    full_name: Optional[str] = None  # Nome completo (pode ser vazio)
    role: str = "member"  # Função (padrão é "member")

class UserCreate(BaseModel):  # Para cadastrar usuário
    email: EmailStr  # Email válido
    password: str  # Senha
    full_name: Optional[str] = None  # Nome (opcional)
    role: str = "member"  # Função (padrão é "member")

class UserUpdate(BaseModel):  # Para atualizar usuário
    full_name: Optional[str] = None  # Nome (opcional)
    role: Optional[str] = None  # Função (opcional)

class User(UserBase):  # Modelo completo
    id: str  # ID do usuário
    email: EmailStr  # Email
    updated_at: Optional[datetime] = None  # Data de atualização

    class Config:  # Configuração
        from_attributes = True  # Permite usar dados do banco
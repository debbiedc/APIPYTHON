from pydantic_settings import BaseSettings  # Ferramenta para ler o .env

class Settings(BaseSettings):  # Classe para guardar as chaves
    supabase_url: str  # URL do Supabase
    supabase_key: str  # Chave do Supabase

    class Config:  # Configurações
        env_file = ".env"  # Arquivo com as chaves
        env_file_encoding = "utf-8"  # Formato do texto

settings = Settings()  # Carrega as chaves
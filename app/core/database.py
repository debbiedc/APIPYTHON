from supabase import create_client, Client  # Ferramentas para conectar ao Supabase
from app.core.config import settings  # Importa as chaves

def get_supabase() -> Client:  # Função que cria a conexão
    return create_client(settings.supabase_url, settings.supabase_key)  # Conecta com URL e chave
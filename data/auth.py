# auth.py
import json
import os
from datetime import datetime

# --- CONSTANTES ---
USUARIOS_FILE = "data/usuarios.json"
MAX_USERS = 50 # Limite de 50 usuários + 1 admin

# --- FUNÇÕES DE ACESSO AO ARQUIVO (você substituirá isso pela conexão com o banco de dados) ---

def carregar_usuarios():
    """Carrega usuários. Garante que o admin sempre exista."""
    if not os.path.exists(USUARIOS_FILE):
        # Se o arquivo não existe, cria com o admin
        admin_user = {
            "admin": {
                "senha": "admin",
                "criado_em": datetime.now().isoformat()
            }
        }
        with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
            json.dump(admin_user, f, indent=4)
        return admin_user
    
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
        
        # Garante que o admin exista e não seja sobrescrito
        if "admin" not in usuarios:
            usuarios["admin"] = {
                "senha": "admin",
                "criado_em": datetime.now().isoformat()
            }
            salvar_usuarios(usuarios)
            
        return usuarios
    except (json.JSONDecodeError, FileNotFoundError):
        return {} # Retorna vazio em caso de erro

def salvar_usuarios(usuarios):
    """Salva os usuários no arquivo."""
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

# --- LÓGICA DE LOGIN E CADASTRO ---

def verificar_login(username, password):
    """Verifica as credenciais do usuário."""
    usuarios = carregar_usuarios()
    user_data = usuarios.get(username)
    if user_data and user_data["senha"] == password:
        return True
    return False

def registrar_novo_usuario(username, password):
    """Registra um novo usuário com sistema de limite e rotação."""
    if not username or not password:
        return "Erro: Nome de usuário e senha não podem estar vazios."
    
    if username == "admin":
        return "Erro: Nome de usuário 'admin' é reservado."

    usuarios = carregar_usuarios()

    if username in usuarios:
        return "Erro: Nome de usuário já existe."

    # Lógica de Rotação (FIFO)
    # A contagem total de usuários não-admin
    non_admin_users = {u: d for u, d in usuarios.items() if u != "admin"}

    if len(non_admin_users) >= MAX_USERS:
        # Encontra o usuário mais antigo (que não seja o admin)
        # O mais antigo é o que tem o timestamp de 'criado_em' menor
        usuario_mais_antigo = min(
            non_admin_users.items(), 
            key=lambda item: item[1]["criado_em"]
        )[0] # Pega a chave (nome do usuário)
        
        # Remove o usuário mais antigo
        del usuarios[usuario_mais_antigo]
        print(f"Limite atingido. Usuário mais antigo '{usuario_mais_antigo}' foi removido.")

    # Adiciona o novo usuário
    usuarios[username] = {
        "senha": password,
        "criado_em": datetime.now().isoformat()
    }
    
    salvar_usuarios(usuarios)
    return "Sucesso: Usuário cadastrado com sucesso!"

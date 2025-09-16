# auth.py (versão com todas as funções de gerenciamento)
import streamlit as st
from datetime import datetime
import pandas as pd
from sqlalchemy.sql import text

# --- CONSTANTES ---
MAX_USERS = 50

# --- FUNÇÕES DE ACESSO AO BANCO DE DADOS ---

def get_db_connection():
    """Retorna uma conexão com o banco de dados do Supabase."""
    return st.connection("supabase_db", type="sql")

# --- FUNÇÕES DE GERENCIAMENTO DE USUÁRIOS (PARA ADMIN) ---

def delete_user(username):
    """Deleta um usuário do banco de dados."""
    try:
        conn = get_db_connection()
        with conn.session as s:
            s.execute(text("DELETE FROM usuarios WHERE username = :username;"), params={"username": username})
            s.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar usuário {username}: {e}")
        return False

def update_user_password(username, new_password):
    """Atualiza a senha de um usuário no banco de dados."""
    if not new_password:
        return False
    try:
        conn = get_db_connection()
        with conn.session as s:
            s.execute(
                text("UPDATE usuarios SET senha = :new_password WHERE username = :username;"),
                params={"new_password": new_password, "username": username}
            )
            s.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar senha para {username}: {e}")
        return False

def update_username(old_username, new_username):
    """Atualiza o nome de um usuário."""
    if not new_username:
        return False, "O novo nome de usuário não pode estar vazio."
    if new_username.lower() == 'admin':
        return False, "Não é possível renomear um usuário para 'admin'."
    
    conn = get_db_connection()
    try:
        # Verifica se o novo nome de usuário já existe
        df_existente = conn.query("SELECT * FROM usuarios WHERE username = :username;", params={"username": new_username}, ttl=0)
        if not df_existente.empty:
            return False, f"O nome de usuário '{new_username}' já está em uso."
        
        # Se não existe, atualiza
        with conn.session as s:
            s.execute(
                text("UPDATE usuarios SET username = :new_username WHERE username = :old_username;"),
                params={"new_username": new_username, "old_username": old_username}
            )
            s.commit()
        return True, f"Usuário '{old_username}' renomeado para '{new_username}'."
    except Exception as e:
        return False, f"Erro ao renomear usuário: {e}"

# --- LÓGICA DE LOGIN E CADASTRO ---

def verificar_login(username, password):
    """Verifica as credenciais do usuário."""
    try:
        conn = get_db_connection()
        df = conn.query("SELECT senha FROM usuarios WHERE username = :username;", params={"username": username}, ttl=0)
        if df.empty: return False
        return df.iloc[0]['senha'] == password
    except Exception as e:
        st.error(f"Erro ao verificar login: {e}")
        return False

def registrar_novo_usuario(username, password):
    """Registra um novo usuário."""
    if not username or not password:
        return "Erro: Nome de usuário e senha não podem estar vazios."
    if username.lower() == "admin":
        return "Erro: Nome de usuário 'admin' é reservado."

    conn = get_db_connection()
    try:
        df_existente = conn.query("SELECT * FROM usuarios WHERE username = :username;", params={"username": username}, ttl=0)
        if not df_existente.empty:
            return "Erro: Nome de usuário já existe."

        df_todos_nao_admin = conn.query("SELECT username, criado_em FROM usuarios WHERE username != 'admin' ORDER BY criado_em ASC;", ttl=0)
        
        with conn.session as s:
            if len(df_todos_nao_admin) >= MAX_USERS:
                usuario_para_remover = df_todos_nao_admin.iloc[0]['username']
                st.toast(f"Limite atingido. Removendo usuário mais antigo: '{usuario_para_remover}'...")
                s.execute(text("DELETE FROM usuarios WHERE username = :username;"), params={"username": usuario_para_remover})

            s.execute(
                text("INSERT INTO usuarios (username, senha, criado_em) VALUES (:username, :senha, :criado_em);"),
                params={"username": username, "senha": password, "criado_em": datetime.now()}
            )
            s.commit()
        return "Sucesso: Usuário cadastrado com sucesso!"
    except Exception as e:
        error_message = str(e)
        return f"Erro inesperado no banco de dados: {error_message}"

# auth.py (versão com correção final para escrita de dados)
import streamlit as st
from datetime import datetime
import pandas as pd
from sqlalchemy.sql import text # Import necessário

# --- CONSTANTES ---
MAX_USERS = 50

# --- FUNÇÕES DE ACESSO AO BANCO DE DADOS ---

def get_db_connection():
    """Retorna uma conexão com o banco de dados do Supabase."""
    return st.connection("supabase_db", type="sql")

# --- LÓGICA DE LOGIN E CADASTRO ---

def verificar_login(username, password):
    """Verifica as credenciais do usuário (operação de LEITURA)."""
    try:
        conn = get_db_connection()
        # .query() é o correto para SELECT
        df = conn.query("SELECT senha FROM usuarios WHERE username = :username;", params={"username": username}, ttl=0)
        
        if df.empty:
            return False
            
        senha_no_banco = df.iloc[0]['senha']
        return senha_no_banco == password
    except Exception as e:
        st.error(f"Erro ao verificar login: {e}")
        return False

def registrar_novo_usuario(username, password):
    """Registra um novo usuário (operações de ESCRITA)."""
    if not username or not password:
        return "Erro: Nome de usuário e senha não podem estar vazios."
    
    if username.lower() == "admin":
        return "Erro: Nome de usuário 'admin' é reservado."

    conn = get_db_connection()
    
    try:
        # LEITURA: Verificando se o usuário existe
        df_existente = conn.query("SELECT * FROM usuarios WHERE username = :username;", params={"username": username}, ttl=0)
        if not df_existente.empty:
            return "Erro: Nome de usuário já existe."

        # LEITURA: Buscando usuários para a lógica de rotação
        df_todos_nao_admin = conn.query("SELECT username, criado_em FROM usuarios WHERE username != 'admin' ORDER BY criado_em ASC;", ttl=0)
        
        # ESCRITA: Abrindo uma sessão para as operações de escrita
        with conn.session as s:
            if len(df_todos_nao_admin) >= MAX_USERS:
                usuario_para_remover = df_todos_nao_admin.iloc[0]['username']
                st.toast(f"Limite atingido. Removendo usuário mais antigo: '{usuario_para_remover}'...")
                # CORREÇÃO AQUI: Usando s.execute() para DELETE
                s.execute(text("DELETE FROM usuarios WHERE username = :username;"), params={"username": usuario_para_remover})

            # CORREÇÃO AQUI: Usando s.execute() para INSERT
            s.execute(
                text("INSERT INTO usuarios (username, senha, criado_em) VALUES (:username, :senha, :criado_em);"),
                params={
                    "username": username,
                    "senha": password,
                    "criado_em": datetime.now()
                }
            )
            s.commit() # Confirma as alterações no banco de dados
        
        return "Sucesso: Usuário cadastrado com sucesso!"

    except Exception as e:
        error_message = str(e)
        print(f"ERRO DE BANCO DE DADOS: {error_message}")
        return f"Erro inesperado no banco de dados: {error_message}"

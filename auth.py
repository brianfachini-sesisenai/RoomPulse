# auth.py (versão final para banco de dados)
import streamlit as st
from datetime import datetime
import pandas as pd

# --- CONSTANTES ---
MAX_USERS = 50

# --- FUNÇÕES DE ACESSO AO BANCO DE DADOS ---

def get_db_connection():
    """Retorna uma conexão com o banco de dados do Supabase."""
    return st.connection("supabase_db", type="sql")

# --- LÓGICA DE LOGIN E CADASTRO ---

def verificar_login(username, password):
    """Verifica as credenciais do usuário consultando o banco de dados."""
    try:
        conn = get_db_connection()
        # Busca apenas o usuário específico em vez de carregar a tabela inteira
        df = conn.query("SELECT senha FROM usuarios WHERE username = %s;", params=(username,), ttl=0)
        
        if df.empty:
            return False # Usuário não encontrado
            
        senha_no_banco = df.iloc[0]['senha']
        return senha_no_banco == password
    except Exception as e:
        st.error(f"Erro ao verificar login: {e}")
        return False

def registrar_novo_usuario(username, password):
    """Registra um novo usuário no banco de dados com tratamento de erros."""
    if not username or not password:
        return "Erro: Nome de usuário e senha não podem estar vazios."
    
    if username.lower() == "admin":
        return "Erro: Nome de usuário 'admin' é reservado."

    conn = get_db_connection()
    
    try:
        # 1. VERIFICA SE O USUÁRIO JÁ EXISTE
        df_existente = conn.query("SELECT * FROM usuarios WHERE username = %s;", params=(username,), ttl=0)
        if not df_existente.empty:
            return "Erro: Nome de usuário já existe."

        # 2. APLICA A LÓGICA DE ROTAÇÃO (SE NECESSÁRIO)
        df_todos_nao_admin = conn.query("SELECT username, criado_em FROM usuarios WHERE username != 'admin' ORDER BY criado_em ASC;", ttl=0)
        
        if len(df_todos_nao_admin) >= MAX_USERS:
            usuario_para_remover = df_todos_nao_admin.iloc[0]['username']
            st.toast(f"Limite atingido. Removendo usuário mais antigo: '{usuario_para_remover}'...")
            conn.execute("DELETE FROM usuarios WHERE username = %s;", params=(usuario_para_remover,))

        # 3. INSERE O NOVO USUÁRIO
        conn.execute(
            "INSERT INTO usuarios (username, senha, criado_em) VALUES (%s, %s, %s);",
            params=(username, password, datetime.now())
        )
        
        return "Sucesso: Usuário cadastrado com sucesso!"

    except Exception as e:
        error_message = str(e)
        print(f"ERRO DE BANCO DE DADOS: {error_message}") # Imprime no terminal
        
        if "permission denied" in error_message:
            return "Erro: Falha de permissão ao tentar escrever no banco de dados. Verifique as políticas da tabela no Supabase."
        else:
            return f"Erro inesperado no banco de dados: {error_message}"

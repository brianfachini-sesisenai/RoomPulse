# auth.py (versão com redefinição de senha por e-mail)
import streamlit as st
from datetime import datetime
import pandas as pd
from sqlalchemy.sql import text
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

# --- CONSTANTES ---
MAX_USERS = 50

# --- FUNÇÕES DE ACESSO AO BANCO DE DADOS ---
def get_db_connection():
    return st.connection("supabase_db", type="sql")

# --- FUNÇÕES DE GERENCIAMENTO DE E-MAIL E SENHA ---

def send_password_reset_email(recipient_email, temp_password):
    """Envia um e-mail com a senha temporária."""
    try:
        sender_email = st.secrets["email_credentials"]["sender_email"]
        password = st.secrets["email_credentials"]["sender_password"]
    except KeyError:
        st.error("Credenciais de e-mail não configuradas nos segredos (secrets.toml).")
        return False

    message = MIMEMultipart("alternative")
    message["Subject"] = "Redefinição de Senha - Room App"
    message["From"] = sender_email
    message["To"] = recipient_email

    html = f"""
    <html><body>
        <p>Olá,<br>
        Você solicitou a redefinição de sua senha no Room App.<br>
        Sua nova senha temporária é: <strong>{temp_password}</strong><br>
        Faça login com esta senha e altere-a o mais rápido possível.
        </p>
    </body></html>
    """
    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

def handle_password_reset(email):
    """Gera senha temporária, atualiza no DB e envia por e-mail."""
    if not email:
        return "Por favor, insira um e-mail."
    
    conn = get_db_connection()
    df_user = conn.query("SELECT username FROM usuarios WHERE email = :email;", params={"email": email}, ttl=0)
    
    if df_user.empty:
        return "Nenhum usuário encontrado com este e-mail."

    # Gera uma senha temporária de 8 caracteres
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Atualiza a senha no banco de dados
    username = df_user.iloc[0]['username']
    password_updated = update_user_password(username, temp_password)

    if not password_updated:
        return "Falha ao atualizar a senha no banco de dados."

    # Envia o e-mail
    email_sent = send_password_reset_email(email, temp_password)
    if email_sent:
        return "Sucesso! Uma senha temporária foi enviada para o seu e-mail."
    else:
        return "Falha ao enviar o e-mail de redefinição. Tente novamente mais tarde."

# --- FUNÇÕES DE GERENCIAMENTO DE USUÁRIOS (PARA ADMIN) ---
# ... (as funções delete_user, update_user_password, update_username continuam aqui, sem alterações) ...
def delete_user(username):
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
    if not new_password: return False
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
    if not new_username: return False, "O novo nome de usuário não pode estar vazio."
    if new_username.lower() == 'admin': return False, "Não é possível renomear um usuário para 'admin'."
    conn = get_db_connection()
    try:
        df_existente = conn.query("SELECT * FROM usuarios WHERE username = :username;", params={"username": new_username}, ttl=0)
        if not df_existente.empty: return False, f"O nome de usuário '{new_username}' já está em uso."
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
    # ... (sem alterações) ...
    try:
        conn = get_db_connection()
        df = conn.query("SELECT senha FROM usuarios WHERE username = :username;", params={"username": username}, ttl=0)
        if df.empty: return False
        return df.iloc[0]['senha'] == password
    except Exception as e:
        st.error(f"Erro ao verificar login: {e}")
        return False

def registrar_novo_usuario(username, password, email):
    """Registra um novo usuário, agora com e-mail."""
    if not username or not password or not email:
        return "Erro: Todos os campos (usuário, senha e e-mail) são obrigatórios."
    if username.lower() == "admin": return "Erro: Nome de usuário 'admin' é reservado."

    conn = get_db_connection()
    try:
        df_existente = conn.query("SELECT * FROM usuarios WHERE username = :username OR email = :email;", params={"username": username, "email": email}, ttl=0)
        if not df_existente.empty:
            return "Erro: Nome de usuário ou e-mail já existem."

        df_todos_nao_admin = conn.query("SELECT username FROM usuarios WHERE username != 'admin';", ttl=0)
        
        with conn.session as s:
            if len(df_todos_nao_admin) >= MAX_USERS:
                # ... (lógica de rotação continua a mesma) ...
                usuario_para_remover = conn.query("SELECT username FROM usuarios WHERE username != 'admin' ORDER BY criado_em ASC LIMIT 1;", ttl=0).iloc[0]['username']
                st.toast(f"Limite atingido. Removendo usuário mais antigo: '{usuario_para_remover}'...")
                s.execute(text("DELETE FROM usuarios WHERE username = :username;"), params={"username": usuario_para_remover})

            s.execute(
                text("INSERT INTO usuarios (username, senha, email, criado_em) VALUES (:username, :senha, :email, :criado_em);"),
                params={"username": username, "senha": password, "email": email, "criado_em": datetime.now()}
            )
            s.commit()
        return "Sucesso: Usuário cadastrado com sucesso!"
    except Exception as e:
        return f"Erro inesperado no banco de dados: {e}"

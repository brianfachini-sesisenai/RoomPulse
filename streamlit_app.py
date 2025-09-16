# streamlit_app.py V2.0
import streamlit as st
import json
import os

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Room App",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed" # Esconde a sidebar na tela de login
)

# --- CAMINHO DO ARQUIVO DE USUÁRIOS ---
USUARIOS_FILE = "data/usuarios.json"

# --- FUNÇÕES DE UTILIDADE ---

def carregar_usuarios():
    """Carrega os usuários do arquivo JSON de forma segura."""
    if not os.path.exists(USUARIOS_FILE):
        os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True)
        with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Se o arquivo estiver corrompido ou não for encontrado, cria um novo
        with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}

def salvar_usuarios(usuarios):
    """Salva o dicionário de usuários no arquivo JSON."""
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "view" not in st.session_state:
    st.session_state.view = "login" # 'login' ou 'cadastro'

# --- FUNÇÕES DE TELA (VIEWS) ---

def tela_login():
    """Renderiza a tela de login."""
    st.header("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Usuário", key="login_usuario")
        password = st.text_input("Senha", type="password", key="login_senha")
        submitted = st.form_submit_button("Entrar", type="primary")

        if submitted:
            if not username or not password:
                st.error("Preencha todos os campos!")
            else:
                usuarios = carregar_usuarios()
                if username in usuarios and usuarios[username] == password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.password = password
                    st.rerun() # Recarrega a página para mostrar a interface principal
                else:
                    st.error("Usuário ou senha incorretos.")
    
    if st.button("Ainda não tem conta? Cadastre-se aqui"):
        st.session_state.view = "cadastro"
        st.rerun()

def tela_cadastro():
    """Renderiza a tela de cadastro."""
    st.header("📝 Cadastro de Usuário")
    with st.form("cadastro_form"):
        novo_usuario = st.text_input("Escolha um nome de usuário", key="cadastro_usuario")
        nova_senha = st.text_input("Escolha uma senha", type="password", key="cadastro_senha")
        submitted = st.form_submit_button("Cadastrar", type="primary")

        if submitted:
            if not novo_usuario or not nova_senha:
                st.error("Preencha todos os campos!")
            else:
                usuarios = carregar_usuarios()
                if novo_usuario in usuarios:
                    st.error("Nome de usuário já existe! Tente outro.")
                else:
                    usuarios[novo_usuario] = nova_senha
                    salvar_usuarios(usuarios)
                    st.success("Cadastro realizado com sucesso! Faça o login.")
                    st.session_state.view = "login"
                    st.rerun() # Recarrega para a tela de login

    if st.button("🔙 Voltar ao Login"):
        st.session_state.view = "login"
        st.rerun()


# --- CONTROLE PRINCIPAL ---

# Se o usuário NÃO estiver autenticado, mostra login ou cadastro
if not st.session_state.authenticated:
    st.title("🏨 Bem-vindo ao Room App")
    if st.session_state.view == "login":
        tela_login()
    else:
        tela_cadastro()
else:
    # Se o usuário ESTIVER autenticado, mostra o título e uma mensagem.
    # O Streamlit cuidará de mostrar a navegação para as páginas na pasta `pages`.
    st.set_page_config(initial_sidebar_state="auto") # Restaura a sidebar
    st.title(f"🏨 Room App")
    st.sidebar.success(f"Logado como: {st.session_state.username}")
    st.write("### Selecione uma opção na barra lateral para começar.")

    # Botão de Logout na sidebar
    if st.sidebar.button("Sair da Conta"):
        # Limpa todos os dados da sessão
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

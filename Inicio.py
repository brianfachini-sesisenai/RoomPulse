# Inicio.py (versão com painel de admin)
import streamlit as st
import auth 

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Room App",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- FUNÇÕES DE TELA (VIEWS) ---

def tela_login():
    """Renderiza a tela de login."""
    st.header("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", type="primary")

        if submitted:
            if auth.verificar_login(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
    
    if st.button("Ainda não tem conta? Cadastre-se aqui"):
        st.session_state.view = "cadastro"
        st.rerun()

def tela_cadastro():
    """Renderiza a tela de cadastro."""
    st.header("📝 Cadastro de Usuário")
    with st.form("cadastro_form"):
        novo_usuario = st.text_input("Escolha um nome de usuário")
        nova_senha = st.text_input("Escolha uma senha", type="password")
        submitted = st.form_submit_button("Cadastrar", type="primary")

        if submitted:
            resultado = auth.registrar_novo_usuario(novo_usuario, nova_senha)
            if resultado.startswith("Sucesso"):
                st.success(resultado + " Agora você pode fazer o login.")
                st.session_state.view = "login"
                st.rerun()
            else:
                st.error(resultado)

    if st.button("🔙 Voltar ao Login"):
        st.session_state.view = "login"
        st.rerun()

# --- CONTROLE PRINCIPAL ---

if not st.session_state.authenticated:
    st.title("🏨 Bem-vindo ao Room App")
    if st.session_state.view == "login":
        tela_login()
    else:
        tela_cadastro()
else:
    # --- INTERFACE PRINCIPAL APÓS LOGIN ---
    st.title(f"🏨 Room App")
    st.sidebar.success(f"Logado como: {st.session_state.username}")

    # --- NOVA SEÇÃO DO PAINEL ADMIN ---
    # Este bloco só aparece se o usuário logado for 'admin'
    if st.session_state.get("username") == "admin":
        st.sidebar.divider()
        st.sidebar.header("Painel do Admin")

        # Botão para ativar a visualização de usuários
        if st.sidebar.button("Ver Todos os Usuários"):
            st.session_state.admin_view = "view_users"
        
        # Botão para voltar à visualização normal
        if st.sidebar.button("Ocultar Lista de Usuários"):
            # Deleta a variável de estado para voltar ao normal
            if "admin_view" in st.session_state:
                del st.session_state.admin_view
            st.rerun()

    # --- CONTEÚDO DA PÁGINA PRINCIPAL ---
    # Verifica se a visualização de admin está ativa
    if st.session_state.get("admin_view") == "view_users":
        st.subheader("👨‍💼 Lista de Todos os Usuários")
        try:
            conn = auth.get_db_connection()
            # Busca todos os usuários, exceto o próprio admin, ordenados por data de criação
            todos_usuarios = conn.query("SELECT username, criado_em FROM usuarios WHERE username != 'admin' ORDER BY criado_em DESC;", ttl=0)
            st.dataframe(todos_usuarios, use_container_width=True)
        except Exception as e:
            st.error(f"Não foi possível carregar os usuários: {e}")
    else:
        # Mensagem padrão para todos os usuários (incluindo o admin quando não está vendo a lista)
        st.write("### Selecione uma opção na barra lateral para começar.")

    # Botão de Logout na sidebar (sempre visível para quem está logado)
    st.sidebar.divider()
    if st.sidebar.button("Sair da Conta"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

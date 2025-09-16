# Inicio.py v2.0
import streamlit as st
import auth # ✅ Importa o nosso novo arquivo de autenticação. Perfeito!

# --- CONFIGURAÇÕES DA PÁGINA ---
# Você ainda precisa disso no seu arquivo principal.
st.set_page_config(
    page_title="Room App",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed" # Esconde a sidebar na tela de login
)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
# ✅ Você manteve isso corretamente.
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "view" not in st.session_state:
    st.session_state.view = "login" # 'login' ou 'cadastro'

# --- FUNÇÕES DE TELA (VIEWS) ATUALIZADAS ---
# ✅ Suas novas funções estão perfeitas! A lógica antiga foi removida
#    e agora elas chamam as funções do auth.py.

def tela_login():
    """Renderiza a tela de login usando a nova lógica."""
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
    """Renderiza a tela de cadastro usando a nova lógica."""
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
# 🎯 ESSA PARTE FINAL É CRUCIAL e precisa ser adicionada de volta.
# É ela que decide se mostra o login/cadastro ou o app principal.

if not st.session_state.authenticated:
    st.title("🏨 Bem-vindo ao Room App")
    if st.session_state.view == "login":
        tela_login()
    else:
        tela_cadastro()
else:
    # Se o usuário ESTIVER autenticado, mostra o título e a mensagem.
    st.set_page_config(initial_sidebar_state="auto") # Restaura a sidebar
    st.title(f"🏨 Room App")
    st.sidebar.success(f"Logado como: {st.session_state.username}")
    st.write("### Selecione uma opção na barra lateral para começar.")

    # Botão de Logout na sidebar
    if st.sidebar.button("Sair da Conta"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

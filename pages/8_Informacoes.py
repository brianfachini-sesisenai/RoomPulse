# pages/8_Informacoes.py
import streamlit as st

st.set_page_config(page_title="Minhas Informações", page_icon="ℹ️", layout="wide")

def render_info():
    st.header("ℹ️ Minhas Informações")

    # Busca os dados da sessão, com valores padrão para segurança
    nome_usuario = st.session_state.get('username', 'Não definido')
    senha_usuario = st.session_state.get('password', 'Não definida')

    st.text_input(
        "**Nome de Usuário:**", 
        value=nome_usuario, 
        disabled=True
    )
    
    st.text_input(
        "**Senha:**", 
        value=senha_usuario, 
        type="password", 
        disabled=True
    )

    st.info("Para alterar seus dados, por favor, contate a recepção.")

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_info()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_info"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

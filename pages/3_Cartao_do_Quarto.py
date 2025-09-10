# pages/3_Cartao_do_Quarto.py
import streamlit as st
import time

st.set_page_config(page_title="Cartão do Quarto", page_icon="💳", layout="wide")

@st.dialog("Aproxime para Abrir")
def show_unlock_dialog():
    st.write("Aproxime o dispositivo da fechadura da porta!")
    st.image("assets/Cartao_Aproximacao.png", use_container_width=True)
    
    # Simula um processo de verificação
    progress_bar = st.progress(0, text="Comunicando com a porta...")
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1, text=f"Comunicando com a porta... {i+1}%")
    
    progress_bar.empty()
    st.success("Porta Destrancada!")
    time.sleep(2) # Espera 2 segundos antes de fechar o dialog
    st.rerun()

def render_cartao_quarto():
    st.header("🔑 Cartão Digital do Quarto")
    st.write("Use seu dispositivo para destravar a porta do seu quarto.")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("assets/Cartao_Aproximacao.png", caption="Cartão Digital")
        if st.button("Destrancar Porta", use_container_width=True, type="primary"):
            show_unlock_dialog()

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_cartao_quarto()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_cartao"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

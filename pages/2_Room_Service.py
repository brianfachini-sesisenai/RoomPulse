# pages/2_Room_Service.py
import streamlit as st

st.set_page_config(page_title="Room Service", page_icon="🧼", layout="wide")

def render_servico_de_quarto():
    st.header("🧼 Solicitar Limpeza de Quarto")
    
    with st.form("limpeza_form"):
        autorizado = st.radio(
            "Você autoriza a entrada da equipe de limpeza no seu quarto?", 
            ("Sim", "Não"), 
            index=1 # Padrão para "Não"
        )
        presente = st.radio(
            "Você está no quarto agora?", 
            ("Sim", "Não"), 
            index=1 # Padrão para "Não"
        )
        
        submitted = st.form_submit_button("Enviar Solicitação")
        
        if submitted:
            if autorizado == "Não":
                st.warning("Sua solicitação não foi enviada, pois a entrada não foi autorizada.")
            elif presente == "Sim":
                st.warning("A equipe de limpeza não pode entrar enquanto você estiver no quarto. Por favor, solicite novamente quando sair.")
            else: # Autorizado == "Sim" e Presente == "Não"
                st.success("Solicitação registrada! A equipe de limpeza foi notificada e irá assim que possível.")

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_servico_de_quarto()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_room_service"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

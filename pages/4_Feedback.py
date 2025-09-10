# pages/4_Feedback.py
import streamlit as st

st.set_page_config(page_title="Feedback", page_icon="🗣️", layout="wide")

def render_feedback():
    st.header("🗣️ Deixe seu Feedback")
    st.write("Sua opinião é muito importante para nós!")

    # Inicializa a lista de feedbacks na sessão se ainda não existir
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []

    with st.form("feedback_form"):
        # Pega o nome do usuário logado
        nome_usuario = st.session_state.get('username', 'Anônimo')
        
        estrelas = st.slider(
            "Avalie sua experiência (de 1 a 5 estrelas):", 
            min_value=1, max_value=5, value=5, 
            key="slider_feedback"
        )
        
        comentario = st.text_area(
            "Comentário:", 
            placeholder="Descreva sua experiência, sugestões ou críticas.",
            key="text_feedback"
        )
        
        submitted = st.form_submit_button("Enviar Feedback")

        if submitted:
            if not comentario.strip():
                st.error("Por favor, escreva um comentário antes de enviar.")
            else:
                # Adiciona o novo feedback à lista na sessão
                st.session_state.feedbacks.append({
                    "nome": nome_usuario, 
                    "estrelas": estrelas, 
                    "comentario": comentario
                })
                st.success("Feedback enviado com sucesso! Obrigado.")
    
    st.divider()

    # Mostra todos os feedbacks já enviados
    if st.session_state.feedbacks:
        st.subheader("📌 Feedbacks Anteriores")
        # Itera sobre a lista de feedbacks em ordem reversa (mais novo primeiro)
        for fb in reversed(st.session_state.feedbacks):
            with st.container(border=True):
                st.write(f"**👤 {fb['nome']}**")
                st.write(f"{'⭐' * fb['estrelas']}")
                st.write(f"_{fb['comentario']}_")

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_feedback()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_feedback"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

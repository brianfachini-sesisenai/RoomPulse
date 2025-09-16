# pages/1_Cardapio.py
import streamlit as st
import json
import os

st.set_page_config(page_title="Cardápio", page_icon="🍽️", layout="wide")

def carregar_menu():
    """Carrega os dados do menu a partir de um arquivo JSON."""
    caminho_menu = "data/menu.json"
    if os.path.exists(caminho_menu):
        try:
            with open(caminho_menu, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error("Erro ao ler o arquivo do cardápio. O formato é inválido.")
            return {}
    else:
        st.warning("Arquivo 'data/menu.json' não encontrado.")
        return {}

def render_cardapio():
    st.header("🍽️ Refeições da Semana")
    menu_data = carregar_menu()

    if not menu_data:
        st.info("Nenhum cardápio disponível para esta semana.")
        return

    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
    # Garante a ordem correta dos dias e que todos sejam exibidos
    cols = st.columns(len(dias_semana))
    
    for i, dia in enumerate(dias_semana):
        with cols[i]:
            st.subheader(dia)
            refeicoes = menu_data.get(dia, ["-"]) # Pega a lista de refeições ou uma lista com '-'
            
            # Usando markdown para criar listas
            for item in refeicoes:
                st.markdown(f"- {item}")

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_cardapio()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_cardapio"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

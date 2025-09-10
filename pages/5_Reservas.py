# pages/5_Reservas.py
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Reservas Extras", page_icon="📅", layout="wide")

# Inicializa o preço total se não existir
if "preco_total" not in st.session_state:
    st.session_state.preco_total = 0.0

def render_reservas():
    st.header("📅 Reservar Noites Extras")
    
    PRECO_BASE_NOITE = 200.0
    TAXA_ALTA_OCUPACAO = 100.0

    # Define as datas mínimas e máximas para seleção
    data_minima = datetime.today()
    data_maxima = data_minima + timedelta(days=365) # Limite de 1 ano para reserva

    periodo = st.date_input(
        "Selecione o período da reserva:", 
        value=(data_minima, data_minima + timedelta(days=1)),
        min_value=data_minima,
        max_value=data_maxima
    )
    
    ocupado = st.checkbox("Simular alta ocupação do hotel (preço maior)")

    if periodo and len(periodo) == 2:
        data_entrada, data_saida = periodo
        noites = (data_saida - data_entrada).days
        
        if noites < 1:
            st.error("A data de saída deve ser pelo menos um dia depois da data de entrada.")
            return

        preco_por_noite = PRECO_BASE_NOITE + TAXA_ALTA_OCUPACAO if ocupado else PRECO_BASE_NOITE
        preco_calculado = preco_por_noite * noites

        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Noites", f"{noites}")
        col2.metric("Preço por Noite", f"R$ {preco_por_noite:.2f}")
        col3.metric("Preço Total da Reserva", f"R$ {preco_calculado:.2f}")

        if st.button("Confirmar e Adicionar ao Carrinho", type="primary"):
            # Adiciona o valor calculado ao total da sessão
            st.session_state.preco_total += preco_calculado
            st.success(f"Reserva de {noites} noites adicionada! O valor de R$ {preco_calculado:.2f} foi somado à sua conta.")
            st.info(f"Seu saldo devedor atual é de R$ {st.session_state.preco_total:.2f}. Vá para a página de Pagamento para quitar.")

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_reservas()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_reservas"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

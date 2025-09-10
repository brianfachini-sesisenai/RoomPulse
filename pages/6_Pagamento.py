# pages/6_Pagamento.py
import streamlit as st
import time

st.set_page_config(page_title="Pagamento", page_icon="💳", layout="wide")

# Inicializa o preço total se não existir
if "preco_total" not in st.session_state:
    st.session_state.preco_total = 0.0

@st.dialog("Verificando Pagamento PIX")
def verificar_pagamento_pix():
    st.write("Aguarde, estamos confirmando seu pagamento...")
    st.image("assets/Pix.gif", width=150)
    
    progress_text = "Verificando transação..."
    bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.03)
        bar.progress(percent_complete + 1, text=progress_text)
        
    bar.empty()
    st.success("Pagamento via PIX confirmado com sucesso!")
    time.sleep(2)
    st.session_state.preco_total = 0.0 # Zera o saldo
    st.rerun()

def render_pagamento():
    st.header("💳 Pagamento da Hospedagem")
    
    saldo_devedor = st.session_state.get("preco_total", 0.0)
    st.metric("SALDO DEVEDOR ATUAL", f"R$ {saldo_devedor:.2f}")
    
    if saldo_devedor == 0:
        st.success("🎉 Você não possui pendências financeiras. Obrigado!")
        st.balloons()
        return

    st.divider()

    metodo = st.selectbox(
        "Escolha o método de pagamento",
        ("PIX", "Cartão de Crédito", "Cartão de Débito", "Boleto")
    )

    if metodo == "PIX":
        col1, col2 = st.columns([1,1])
        with col1:
            st.image("assets/qrcode_pix.png", caption="Escaneie para pagar", width=250)
        with col2:
            st.text_input("Ou use a chave PIX:", "hotel@roomapp.com", disabled=True)
            if st.button("Já fiz o pagamento PIX", type="primary"):
                verificar_pagamento_pix()

    elif metodo in ["Cartão de Crédito", "Cartão de Débito"]:
        with st.form("cartao_form"):
            st.text_input("Nome no cartão")
            st.text_input("Número do cartão")
            col1, col2 = st.columns(2)
            col1.text_input("Validade (MM/AA)")
            col2.text_input("CVV", type="password")
            if st.form_submit_button("Pagar com Cartão", type="primary"):
                st.success("Pagamento com cartão simulado com sucesso!")
                st.session_state.preco_total = 0.0
                time.sleep(2)
                st.rerun()

    elif metodo == "Boleto":
        st.text_input("CPF para emissão do boleto")
        if st.button("Gerar Boleto", type="primary"):
            st.success("Boleto gerado com sucesso! (Simulação)")
            st.info("O pagamento pode levar até 3 dias úteis para ser confirmado.")
            st.session_state.preco_total = 0.0
            time.sleep(2)
            st.rerun()


# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_pagamento()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_pagamento"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

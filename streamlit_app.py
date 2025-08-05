import streamlit as st
import json
from datetime import datetime

# -------- CONFIGURAÇÕES BÁSICAS --------
st.set_page_config(page_title="RoomPulse", page_icon="🛎️", layout="wide")

# -------- ESTADO DE AUTENTICAÇÃO --------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -------- FUNÇÃO DE LOGIN SIMPLES --------
def login():
    st.header("🔐 Login Obrigatório")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username and password:
            st.session_state.authenticated = True
            st.success(f"Bem-vindo, {username}!")
        else:
            st.error("Usuário e senha são obrigatórios.")

# -------- FUNÇÃO DE CARDÁPIO --------
def cardapio():
    st.header("🍽️ Refeições da Semana")
    try:
        with open("data/menu.json", "r", encoding="utf-8") as f:
            menu_data = json.load(f)
    except:
        menu_data = {"Segunda": "Arroz, feijão, bife", "Terça": "Macarrão, frango", "Quarta": "Feijoada"}
    for dia, refeicao in menu_data.items():
        st.write(f"**{dia}:** {refeicao}")

# -------- FUNÇÃO DE LIMPEZA --------
def solicitar_limpeza():
    st.header("🧼 Solicitar Limpeza de Quarto")
    autorizado = st.radio("Você autoriza a entrada da equipe de limpeza?", ["Sim", "Não"])
    presente = st.radio("Você está no quarto agora?", ["Sim", "Não"])
    if st.button("Enviar Solicitação"):
        if presente == "Sim":
            st.warning("A equipe de limpeza não poderá entrar enquanto você estiver no quarto.")
        elif autorizado == "Sim":
            st.success("Solicitação registrada! A equipe de limpeza foi notificada.")
        else:
            st.info("Limpeza não autorizada no momento.")

# -------- FUNÇÃO DE FEEDBACK --------
def feedback():
    st.header("🗣️ Enviar Feedback")
    estrelas = st.slider("Avalie sua experiência", 1, 5)
    comentario = st.text_area("Comentário")
    if st.button("Enviar Feedback"):
        st.success("Feedback enviado com sucesso!")
        st.write("⭐" * estrelas)
        st.write(f"Comentário: {comentario}")

# -------- FUNÇÃO DE RESERVAS EXTRAS --------
def reservas_extras():
    st.header("📅 Reservar Noites Extras")
    noites = st.number_input("Quantas noites deseja adicionar?", min_value=1, max_value=10, step=1)
    ocupado = st.checkbox("O hotel está lotado?")
    preco_base = 200
    preco_total = (preco_base + 100 if ocupado else preco_base) * noites
    st.write(f"Preço por noite: R${preco_base + 100 if ocupado else preco_base}")
    st.write(f"Preço total: R${preco_total}")
    if st.button("Confirmar Reserva"):
        st.success("Reserva adicionada com sucesso!")

# -------- FUNÇÃO DE PAGAMENTO --------
def pagamento():
    st.header("💳 Pagamento da Hospedagem")
    preco_hospedagem = st.number_input("Valor da Hospedagem (R$)", min_value=0.0, format="%.2f")
    nome = st.text_input("Nome no cartão")
    numero = st.text_input("Número do cartão")
    validade = st.text_input("Validade (MM/AA)")
    cvv = st.text_input("CVV")
    if st.button("Pagar"):
        if nome and numero and validade and cvv and preco_hospedagem > 0:
            st.success("Pagamento simulado com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente.")

# -------- FUNÇÃO DE FAQ --------
def faq():
    st.header("❓ Dúvidas Frequentes")
    st.write("**Posso mudar o cardápio?** Sim, entre em contato com a recepção.")
    st.write("**Como autorizar a limpeza?** Pelo menu 'Solicitar Limpeza'.")
    st.write("**Posso estender a estadia?** Sim, pela opção 'Reservas Extras'.")

# -------- INTERFACE PRINCIPAL --------
if not st.session_state.authenticated:
    login()
else:
    st.sidebar.title("Menu")
    opcao = st.sidebar.radio("Ir para:", ["Cardápio", "Solicitar Limpeza", "Feedback", "Reservas Extras", "Pagamento", "FAQ"])

    if opcao == "Cardápio":
        cardapio()
    elif opcao == "Solicitar Limpeza":
        solicitar_limpeza()
    elif opcao == "Feedback":
        feedback()
    elif opcao == "Reservas Extras":
        reservas_extras()
    elif opcao == "Pagamento":
        pagamento()
    elif opcao == "FAQ":
        faq()

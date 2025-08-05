import streamlit as st
import json
from datetime import datetime, timedelta

# -------- CONFIGURAÇÕES BÁSICAS --------
st.set_page_config(page_title="RoomPulse", page_icon="🛎️", layout="wide")

# -------- ESTADO DE AUTENTICAÇÃO E PREÇO --------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "preco_total" not in st.session_state:
    st.session_state.preco_total = 0.0

if "aba_ativa" not in st.session_state:
    st.session_state.aba_ativa = "Cardápio"

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

    periodo = st.date_input("Selecione o período da reserva:", value=(datetime.today(), datetime.today() + timedelta(days=1)))
    if len(periodo) == 2:
        data_entrada, data_saida = periodo
        noites = (data_saida - data_entrada).days
        if noites < 1:
            st.error("A data de saída deve ser posterior à data de entrada.")
            return
        st.text_input("Data de Entrada", value=str(data_entrada), disabled=True)
        st.text_input("Data de Saída", value=str(data_saida), disabled=True)

        ocupado = st.checkbox("O hotel está lotado?")
        preco_base = 200
        preco_por_noite = preco_base + 100 if ocupado else preco_base
        st.session_state.preco_total = preco_por_noite * noites
        st.write(f"Preço por noite: R${preco_por_noite}")
        st.write(f"Preço total: R${st.session_state.preco_total}")
        if st.button("Confirmar Reserva"):
            st.success("Reserva adicionada com sucesso!")

# -------- FUNÇÃO DE PAGAMENTO --------
def pagamento():
    st.header("💳 Pagamento da Hospedagem")
    st.write(f"Valor da Hospedagem: R${st.session_state.preco_total:.2f}")
    
    # Seleção do método de pagamento
    metodo_pagamento = st.selectbox("Escolha o método de pagamento", ["Cartão de Crédito", "Débito", "Pix", "Boleto", "Outros"])
    
    # Exibe campos específicos conforme o método de pagamento
    if metodo_pagamento == "Cartão de Crédito":
        nome = st.text_input("Nome no cartão")
        numero = st.text_input("Número do cartão")
        validade = st.text_input("Validade (MM/AA)")
        cvv = st.text_input("CVV")
    elif metodo_pagamento == "Débito":
        nome = st.text_input("Nome no cartão")
        numero = st.text_input("Número do cartão")
        validade = st.text_input("Validade (MM/AA)")
        cvv = st.text_input("CVV")
    elif metodo_pagamento == "Pix":
        chave_pix = st.text_input("Chave Pix (Email, CPF, etc.)")
    elif metodo_pagamento == "Boleto":
        cpf = st.text_input("CPF para emissão do boleto")
        st.write("O boleto será gerado após a confirmação.")
    else:
        st.text_input("Método de pagamento adicional")
    
    if st.button("Pagar"):
        if metodo_pagamento == "Pix" and chave_pix:
            st.success("Pagamento via Pix simulado com sucesso!")
        elif metodo_pagamento == "Boleto" and cpf:
            st.success("Boleto gerado com sucesso!")
        elif metodo_pagamento in ["Cartão de Crédito", "Débito"] and nome and numero and validade and cvv and st.session_state.preco_total > 0:
            st.success("Pagamento simulado com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente e confirme a reserva antes de pagar.")

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
    abas = {
        "Cardápio": cardapio,
        "Solicitar Limpeza": solicitar_limpeza,
        "Feedback": feedback,
        "Reservas Extras": reservas_extras,
        "Pagamento": pagamento,
        "FAQ": faq
    }

    for nome_aba in abas.keys():
        if st.sidebar.button(
            f"{'👉 ' if st.session_state.aba_ativa == nome_aba else ''}{nome_aba}",
            key=nome_aba
        ):
            st.session_state.aba_ativa = nome_aba

    abas[st.session_state.aba_ativa]()

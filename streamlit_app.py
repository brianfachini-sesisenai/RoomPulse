import streamlit as st
from datetime import date

# -------- LOGIN SIMPLES --------
def login():
    st.title("🔐 Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario == "admin" and senha == "1234":
            st.session_state["logado"] = True
        else:
            st.error("Usuário ou senha incorretos")

# -------- MENU LATERAL --------
def menu_lateral():
    st.sidebar.title("RoomPulse 🏨")
    abas = {
        "📅 Reservar Noites Extras": "reservas",
        "💳 Pagamento": "pagamento",
        "📝 Feedback": "feedback"
    }
    for nome, chave in abas.items():
        if st.sidebar.button(nome, use_container_width=True):
            st.session_state["aba"] = chave

# -------- FUNÇÃO DE RESERVAS EXTRAS --------
def reservas_extras():
    st.header("📅 Reservar Noites Extras")
    data_range = st.date_input("Selecione o período da reserva:", value=(date.today(), date.today()))
    if isinstance(data_range, tuple) and len(data_range) == 2:
        data_entrada, data_saida = data_range
        st.text_input("Data de Entrada", value=str(data_entrada), disabled=True)
        st.text_input("Data de Saída", value=str(data_saida), disabled=True)

        noites = (data_saida - data_entrada).days
        if noites > 0:
            ocupado = st.checkbox("O hotel está lotado?")
            preco_base = 200
            preco_total = (preco_base + 100 if ocupado else preco_base) * noites
            st.write(f"Preço por noite: R${preco_base + 100 if ocupado else preco_base}")
            st.write(f"Preço total: R${preco_total}")
            if st.button("Confirmar Reserva"):
                st.session_state["preco_total"] = preco_total
                st.success("Reserva adicionada com sucesso!")
        else:
            st.warning("A data de saída deve ser posterior à data de entrada.")

# -------- FUNÇÃO DE PAGAMENTO --------
def pagamento():
    st.header("💳 Pagamento da Hospedagem")
    if "preco_total" not in st.session_state:
        st.warning("Faça a reserva primeiro para gerar o valor da hospedagem.")
        return

    st.text_input("Valor da Hospedagem", value=f"R${st.session_state['preco_total']:.2f}", disabled=True)
    nome = st.text_input("Nome no cartão")
    numero = st.text_input("Número do cartão")
    validade = st.text_input("Validade (MM/AA)")
    cvv = st.text_input("CVV")
    if st.button("Pagar"):
        if nome and numero and validade and cvv:
            st.success("Pagamento simulado com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente.")

# -------- FUNÇÃO DE FEEDBACK --------
def feedback():
    st.header("📝 Feedback")
    comentario = st.text_area("Deixe seu comentário ou sugestão:")
    if st.button("Enviar Feedback"):
        if comentario:
            st.success("Obrigado pelo seu feedback!")
        else:
            st.error("Por favor, escreva algo antes de enviar.")

# -------- APP PRINCIPAL --------
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "aba" not in st.session_state:
    st.session_state["aba"] = "reservas"

if not st.session_state["logado"]:
    login()
else:
    menu_lateral()
    st.title("RoomPulse - Gerenciamento de Quartos")
    aba_atual = st.session_state["aba"]

    if aba_atual == "reservas":
        reservas_extras()
    elif aba_atual == "pagamento":
        pagamento()
    elif aba_atual == "feedback":
        feedback()

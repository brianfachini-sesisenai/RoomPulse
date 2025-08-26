import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, Tuple

# -------- CONFIGURAÇÕES BÁSICAS --------
st.set_page_config(page_title="RoomPulse", page_icon="🛎️", layout="wide")

# -------- ESTADO GLOBAL --------
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("preco_total", 0.0)
st.session_state.setdefault("aba_ativa", "Cardápio")
st.session_state.setdefault("username", "")
st.session_state.setdefault("password", "")


# -------- FUNÇÃO DE LOGIN --------
def login() -> None:
    """Exibe tela de login simples"""
    st.header("🔐 Login Obrigatório")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username.strip() and password.strip():
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.password = password
            st.success(f"Bem-vindo, {username}!")
        else:
            st.error("Usuário e senha são obrigatórios.")


# -------- FUNÇÃO DE CARDÁPIO --------
def cardapio() -> None:
    st.header("🍽️ Refeições da Semana")
    try:
        with open("data/menu.json", "r", encoding="utf-8") as f:
            menu_data: Dict[str, str] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        menu_data = {
            "Segunda": "Arroz, feijão, bife",
            "Terça": "Macarrão, frango",
            "Quarta": "Feijoada"
        }

    for dia, refeicao in menu_data.items():
        st.write(f"**{dia}:** {refeicao}")


# -------- FUNÇÃO DE LIMPEZA --------
def solicitar_limpeza() -> None:
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
def feedback() -> None:
    st.header("🗣️ Enviar Feedback")
    estrelas = st.slider("Avalie sua experiência", 1, 5)
    comentario = st.text_area("Comentário")

    if st.button("Enviar Feedback"):
        st.success("Feedback enviado com sucesso!")
        st.write("⭐" * estrelas)
        if comentario:
            st.write(f"Comentário: {comentario}")


# -------- FUNÇÃO DE RESERVAS EXTRAS --------
def reservas_extras() -> None:
    st.header("📅 Reservar Noites Extras")
    periodo: Tuple[datetime, datetime] = st.date_input(
        "Selecione o período da reserva:",
        value=(datetime.today(), datetime.today() + timedelta(days=1))
    )

    if len(periodo) == 2:
        data_entrada, data_saida = periodo
        noites = (data_saida - data_entrada).days

        if noites < 1:
            st.error("A data de saída deve ser posterior à data de entrada.")
            return

        col1, col2 = st.columns(2)
        col1.text_input("Data de Entrada", value=str(data_entrada), disabled=True)
        col2.text_input("Data de Saída", value=str(data_saida), disabled=True)

        ocupado = st.checkbox("O hotel está lotado?")
        preco_base = 200
        preco_por_noite = preco_base + 100 if ocupado else preco_base
        st.session_state.preco_total = preco_por_noite * noites

        st.write(f"💲 Preço por noite: **R${preco_por_noite}**")
        st.write(f"💲 Preço total: **R${st.session_state.preco_total}**")

        if st.button("Confirmar Reserva"):
            st.success("Reserva adicionada com sucesso!")


# -------- FUNÇÃO DE PAGAMENTO --------
def pagamento() -> None:
    st.header("💳 Pagamento da Hospedagem")
    st.write(f"Valor da Hospedagem: **R${st.session_state.preco_total:.2f}**")

    metodo_pagamento = st.selectbox(
        "Escolha o método de pagamento",
        ["Cartão de Crédito", "Débito", "Pix", "Boleto", "Outros"]
    )

    campos_ok = False

    if metodo_pagamento in ["Cartão de Crédito", "Débito"]:
        nome = st.text_input("Nome no cartão")
        numero = st.text_input("Número do cartão")
        validade = st.text_input("Validade (MM/AA)")
        cvv = st.text_input("CVV")
        campos_ok = all([nome, numero, validade, cvv])

    elif metodo_pagamento == "Pix":
        chave_pix = st.text_input("Chave Pix (Email, CPF, etc.)")
        campos_ok = bool(chave_pix)

    elif metodo_pagamento == "Boleto":
        cpf = st.text_input("CPF para emissão do boleto")
        st.info("O boleto será gerado após a confirmação.")
        campos_ok = bool(cpf)

    else:
        outro = st.text_input("Método de pagamento adicional")
        campos_ok = bool(outro)

    if st.button("Pagar"):
        if st.session_state.preco_total <= 0:
            st.error("Confirme a reserva antes de efetuar o pagamento.")
        elif campos_ok:
            st.success(f"Pagamento via **{metodo_pagamento}** realizado com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente.")


# -------- FUNÇÃO DE FAQ --------
def faq() -> None:
    st.header("❓ Dúvidas Frequentes")
    st.write("**Posso mudar o cardápio?** → Sim, entre em contato com a recepção.")
    st.write("**Como autorizar a limpeza?** → Pelo menu 'Solicitar Limpeza'.")
    st.write("**Posso estender a estadia?** → Sim, pela opção 'Reservas Extras'.")


# -------- FUNÇÃO DE CONFIGURAÇÕES --------
def configuracoes() -> None:
    st.header("⚙️ Configurações da Conta")
    st.write(f"**Usuário:** {st.session_state.username}")
    st.write(f"**Senha:** {'*' * len(st.session_state.password)}")  # esconde a senha

    if st.button("Sair da Conta"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.password = ""
        st.session_state.aba_ativa = "Cardápio"
        st.success("Você saiu da conta com sucesso!")


# -------- INTERFACE PRINCIPAL --------
def main() -> None:
    if not st.session_state.authenticated:
        login()
        return

    st.sidebar.title("Menu")
    abas: Dict[str, callable] = {
        "Cardápio": cardapio,
        "Solicitar Limpeza": solicitar_limpeza,
        "Feedback": feedback,
        "Reservas Extras": reservas_extras,
        "Pagamento": pagamento,
        "FAQ": faq,
        "⚙️ Configurações": configuracoes
    }

    for nome_aba in abas:
        if st.sidebar.button(
            f"{'👉 ' if st.session_state.aba_ativa == nome_aba else ''}{nome_aba}",
            key=nome_aba
        ):
            st.session_state.aba_ativa = nome_aba

    st.markdown("---")
    abas[st.session_state.aba_ativa]()


if __name__ == "__main__":
    main()

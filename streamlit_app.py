import streamlit as st
import json
from datetime import datetime

# -------- CONFIGURAÇÕES BÁSICAS --------
st.set_page_config(page_title="RoomPulse", page_icon="🛎️", layout="centered")

# -------- FUNÇÕES AUXILIARES --------
def load_menu():
    try:
        with open("data/menu.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"Segunda": "Arroz, feijão, bife", "Terça": "Macarrão, frango", "Quarta": "Feijoada"}

# -------- TÍTULO --------
st.title("🛎️ RoomPulse")
st.subheader("Seu hotel, no ritmo certo.")

# -------- SIDEBAR - MENU --------
menu = st.sidebar.selectbox("Menu", ["Login", "Cardápio", "Solicitar Limpeza", "Feedback", "Reservas Extras", "Pagamento", "FAQ", "Relatório Semanal"])

# -------- LOGIN SIMPLES (SEM BACKEND) --------
if menu == "Login":
    st.header("🔐 Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        st.success(f"Bem-vindo, {username}!")
        st.info("Funcionalidade de login apenas para fins de demonstração.")
        
# -------- CARDÁPIO --------
elif menu == "Cardápio":
    st.header("🍽️ Refeições da Semana")
    menu_data = load_menu()
    for dia, refeicao in menu_data.items():
        st.write(f"**{dia}:** {refeicao}")

# -------- LIMPEZA --------
elif menu == "Solicitar Limpeza":
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

# -------- FEEDBACK --------
elif menu == "Feedback":
    st.header("🗣️ Enviar Feedback")
    estrelas = st.slider("Avalie sua experiência", 1, 5)
    comentario = st.text_area("Comentário")
    if st.button("Enviar"):
        st.success("Feedback enviado com sucesso!")
        st.write("⭐" * estrelas)
        st.write(f"Comentário: {comentario}")

# -------- RESERVAS EXTRAS --------
elif menu == "Reservas Extras":
    st.header("📅 Reservar Noites Extras")
    noites = st.number_input("Quantas noites deseja adicionar?", min_value=1, max_value=10, step=1)
    ocupado = st.checkbox("O hotel está lotado?")
    preco = 200
    if ocupado:
        preco += 100
    total = preco * noites
    st.write(f"Preço total: R${total}")
    if st.button("Confirmar Reserva"):
        st.success("Reserva adicionada com sucesso!")

# -------- PAGAMENTO --------
elif menu == "Pagamento":
    st.header("💳 Pagamento da Hospedagem")
    st.info("Integração futura com Pix, PagSeguro ou Stripe.")
    st.text_input("Valor (R$)", value="200.00")
    st.text_input("Nome no cartão")
    st.text_input("Número do cartão")
    st.text_input("Validade (MM/AA)")
    st.text_input("CVV")
    if st.button("Pagar"):
        st.success("Pagamento simulado com sucesso!")

# -------- FAQ --------
elif menu == "FAQ":
    st.header("❓ Dúvidas Frequentes")
    st.write("**Posso mudar o cardápio?** Sim, entre em contato com a recepção.")
    st.write("**Como autorizar a limpeza?** Pelo menu 'Solicitar Limpeza'.")
    st.write("**Posso estender a estadia?** Sim, pela opção 'Reservas Extras'.")

# -------- RELATÓRIO SEMANAL --------
elif menu == "Relatório Semanal":
    st.header("📅 Relatórios das Reuniões Scrum")
    
    relatorios = {
        "01/07/2025": "Distribuição de funções e definição do nome RoomPulse.",
        "08/07/2025": "Continuação do backlog e início do Sprint Planning.",
        "15/07/2025": "Guia Scrum pronto, início do Sprint 1.",
        "29/07/2025": "Daily Scrum realizada. Desenvolvimento em andamento."
    }
    
    for data, texto in relatorios.items():
        st.markdown(f"**{data}** - {texto}")

    st.markdown("---")
    nova_data = st.date_input("Adicionar novo relatório")
    novo_texto = st.text_area("Descrição da reunião")
    if st.button("Salvar Relatório"):
        st.success(f"Relatório de {nova_data.strftime('%d/%m/%Y')} salvo (simulado).")

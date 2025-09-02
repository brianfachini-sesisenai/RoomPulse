import streamlit as st
import json
from datetime import datetime, timedelta
import time
import base64
import os

# -------- CONFIGURAÇÕES BÁSICAS --------
st.set_page_config(page_title="Room App", page_icon="🏨", layout="wide")

# -------- ARQUIVO DE USUÁRIOS --------
USUARIOS_FILE = "usuarios.json"

# Cria o arquivo se não existir
if not os.path.exists(USUARIOS_FILE):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# -------- ESTADO DE SESSÃO --------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "preco_total" not in st.session_state:
    st.session_state.preco_total = 0.0

if "aba_ativa" not in st.session_state:
    st.session_state.aba_ativa = "Cardápio"

if "tela" not in st.session_state:
    st.session_state.tela = "login"

# -------- FUNÇÃO DE LOGIN --------
def login():
    st.header("🔐 Login")
    username = st.text_input("Usuário", key="login_usuario")
    password = st.text_input("Senha", type="password", key="login_senha")
    
    if st.button("Entrar", key="botao_login"):
        if username and password:
            with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
            if username in usuarios and usuarios[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.password = password
                st.success(f"Bem-vindo, {username}!")
            else:
                st.error("Usuário ou senha incorretos.")
        else:
            st.error("Preencha todos os campos!")

    # Botão estilizado como link (não precisa de rerun)
    if st.button("Ainda não tem conta? Cadastre-se aqui", key="link_cadastro"):
        st.session_state.tela = "cadastro"

# -------- FUNÇÃO DE CADASTRO --------
def cadastro():
    st.header("📝 Cadastro de Usuário")
    novo_usuario = st.text_input("Escolha um nome de usuário", key="cadastro_usuario")
    nova_senha = st.text_input("Escolha uma senha", type="password", key="cadastro_senha")
    
    if st.button("Cadastrar", key="botao_cadastrar"):
        if not novo_usuario or not nova_senha:
            st.error("Preencha todos os campos!")
            return
        
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
        
        if novo_usuario in usuarios:
            st.error("Usuário já existe! Tente outro.")
        else:
            usuarios[novo_usuario] = nova_senha
            with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, ensure_ascii=False, indent=4)
            st.success("Cadastro realizado com sucesso!")
            st.session_state.tela = "login"
            st.experimental_rerun()

# -------- FUNÇÃO DE CARDÁPIO --------
def cardapio():
    st.header("🍽️ Refeições da Semana")
    try:
        with open("data/menu.json", "r", encoding="utf-8") as f:
            menu_data = json.load(f)
    except:
        menu_data = {}

    # Pega os dias e divide em blocos (ex: 3 colunas por linha)
    dias = list(menu_data.items())
    num_colunas = 7  # <- você pode mudar para 2, 4 etc.

    for i in range(0, len(dias), num_colunas):
        cols = st.columns(num_colunas)
        for idx, (col, (dia, refeicoes)) in enumerate(zip(cols, dias[i:i+num_colunas])):
            with col:
                border_style = "border-right: 2px solid #ccc; padding-right: 10px;" if idx < num_colunas-1 else ""
                lista_html = "".join(f"<li>{item}</li>" for item in refeicoes)
                bloco_html = (
                    f'<div style="{border_style}">'
                    f'    <h4>{dia}</h4>'
                    f'    <ul>'
                    f'        {lista_html}'
                    f'    </ul>'
                    f'</div>'
                )
                st.markdown(bloco_html, unsafe_allow_html=True)
# -------- FUNÇÃO DE LIMPEZA --------
def servico_de_quarto():
    st.header("🧼 Solicitar Limpeza de Quarto")
    autorizado = st.radio("Você autoriza a entrada da equipe de limpeza?", ["Sim", "Não"])
    presente = st.radio("Você está no quarto agora?", ["Sim", "Não"])
    if st.button("Enviar Solicitação"):
        if autorizado == "Não":
            st.warning("Limpeza não autorizada no momento.")
        elif presente == "Sim":
            st.warning("A equipe de limpeza não poderá entrar enquanto você estiver no quarto.")
        elif autorizado == "Sim":
            st.success("Solicitação registrada! A equipe de limpeza foi notificada.")
        else:
            st.info("Limpeza não autorizada no momento.")

# -------- FUNÇÃO DE FEEDBACK --------
def feedback():
    st.header("🗣️ Enviar Feedback")

    # inicializa lista de feedbacks se ainda não existir
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []

    estrelas = st.slider("Avalie sua experiência", 1, 5, key="slider_feedback")
    comentario = st.text_area("Comentário", key="text_feedback")
    nome = st.session_state.get('username', 'Não definido')

    if st.button("Enviar Feedback"):
        if comentario.strip() == "":
            st.error("Você precisa escrever algo!")
        else:
            st.session_state.feedbacks.append({"nome": nome, "estrelas": estrelas, "comentario": comentario})
            st.success("Feedback enviado com sucesso!")

    # mostra todos os feedbacks já enviados
    if st.session_state.feedbacks:
        st.subheader("📌 Feedbacks enviados")
        for fb in st.session_state.feedbacks:
            st.write(f"**👤 {fb['nome']} |**", "⭐" * fb["estrelas"])
            st.write(f"Comentário: {fb['comentario']}")
            st.divider()
# -------- FUNÇÃO DE RESERVAS EXTRAS --------
def reservas():
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
        st.subheader("📷 QR Code para pagamento")
        col1, col2, col3 = st.columns([4, 3, 4])  # A coluna central é 3x maior
        
        with col2:
            st.image("qrcode_pix.png", caption="Escaneie o QR Code para pagar via Pix", use_container_width=True, width=250)
        
    elif metodo_pagamento == "Boleto":
        cpf = st.text_input("CPF para emissão do boleto")
        st.write("O boleto será gerado após a confirmação.")
        
    else:
        st.text_input("Método de pagamento adicional")
    
    if st.button("Verificar Pagamento"):
        if metodo_pagamento == "Pix" and chave_pix and st.session_state.preco_total > 0:
            
            # cria placeholder para o GIF + overlay
            gif_placeholder = st.empty()
            
            gif_placeholder.markdown(
                """
                <div style="
                    position: fixed; 
                    top: 0; left: 0; 
                    width: 100%; height: 100%; 
                    background-color: rgba(0,0,0,0.6);  /* fundo escuro com transparência */
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    z-index: 9999;
                ">
                    <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmVid3EwZzJyN2o4NW5hOWhjYzlsbTYybmM1ZWYwam1seHJnb2N3ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/18u3OnFPamgVOAcoUr/giphy.gif" width="200">
                </div>
                """,
                unsafe_allow_html=True
            )
    
            # simula tempo de processamento sem travar completamente
            for i in range(30):  # 30 x 0.1s = 3 segundos
                time.sleep(0.1)
            
            # remove o GIF e overlay
            gif_placeholder.empty()
                
            st.success("Pagamento via Pix simulado com sucesso!")
            
        elif metodo_pagamento == "Boleto" and cpf:
            st.success("Boleto gerado com sucesso!")
            
        elif metodo_pagamento in ["Cartão de Crédito", "Débito"] and nome and numero and validade and cvv and st.session_state.preco_total > 0:
            st.success("Pagamento simulado com sucesso!")

        elif st.session_state.preco_total == 0:
            st.error(f"Sem contas para pagar, seu saldo é de RS: {st.session_state.preco_total:.2f}")
            
        else:
            st.error("Preencha todos os campos corretamente e confirme a reserva antes de pagar.")

# -------- FUNÇÃO DE FAQ --------
def faq():
    st.header("❓ Dúvidas Frequentes")
    st.write("**Posso mudar o cardápio?** Sim, entre em contato com a recepção.")
    st.write("**Como autorizar a limpeza?** Pelo menu 'Solicitar Limpeza'.")
    st.write("**Posso estender a estadia?** Sim, pela opção 'Reservas Extras'.")

# -------- FUNÇÃO DE INFO --------
def info():
    st.header("ℹ️ Informações do Usuário")
    nome = st.session_state.get('username', 'Não definido')
    st.text_input("**Nome:**", value=nome, disabled=True)

    senha = st.session_state.get("password", "Não definida")
    st.text_input("**Senha:**", value=senha, type="password", disabled=True)
    
    st.write("**Gênero:** (Não informado)")

# -------- INTERFACE PRINCIPAL --------
if st.session_state.get("logout", False):
    # Limpa dados da sessão
    for key in ["authenticated", "username", "password", "preco_total", "aba_ativa", "logout"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()  # Recarrega página após limpar

# -------- INTERFACE PRINCIPAL USANDO SIDEBAR --------
if not st.session_state.get("authenticated", False):
    login()
else:
    st.title("🏨 Room App")

    menu_opcoes = ["Cardápio", "Room Service", "Feedback", "Reservas", "Pagamento", "FAQ", "Informações"]
    escolha = st.sidebar.selectbox("📌 Menu", menu_opcoes)

    # Executa a página escolhida
    if escolha == "Cardápio":
        cardapio()
    elif escolha == "Room Service":
        servico_de_quarto()
    elif escolha == "Feedback":
        feedback()
    elif escolha == "Reservas":
        reservas()
    elif escolha == "Pagamento":
        pagamento()
    elif escolha == "FAQ":
        faq()
    elif escolha == "Informações":
        info()

    # Logout seguro
    st.sidebar.divider()
    if st.sidebar.button("Sair da Conta"):
        st.session_state.clear()
        st.stop()












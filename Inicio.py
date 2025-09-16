# Inicio.py (versão com correção do set_page_config)
import streamlit as st
import auth 
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA ---
# ESTA É A ÚNICA CHAMADA PERMITIDA E ESTÁ NO LUGAR CORRETO
st.set_page_config(page_title="Room App", icon="🏨", layout="wide", initial_sidebar_state="collapsed")

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "view" not in st.session_state: st.session_state.view = "login"

# --- FUNÇÕES DE TELA (VIEWS) ---

def tela_login():
    st.header("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", type="primary")
        if submitted:
            if auth.verificar_login(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ainda não tem conta? Cadastre-se"):
            st.session_state.view = "cadastro"
            st.rerun()
    with col2:
        if st.button("Esqueci minha senha"):
            st.session_state.view = "esqueci_senha"
            st.rerun()

def tela_cadastro():
    st.header("📝 Cadastro de Usuário")
    with st.form("cadastro_form"):
        novo_usuario = st.text_input("Escolha um nome de usuário")
        novo_email = st.text_input("Seu e-mail")
        nova_senha = st.text_input("Escolha uma senha", type="password")
        submitted = st.form_submit_button("Cadastrar", type="primary")
        if submitted:
            resultado = auth.registrar_novo_usuario(novo_usuario, nova_senha, novo_email)
            if resultado.startswith("Sucesso"):
                st.success(resultado + " Agora você pode fazer o login.")
                st.session_state.view = "login"
                st.rerun()
            else:
                st.error(resultado)
    if st.button("🔙 Voltar ao Login"):
        st.session_state.view = "login"
        st.rerun()

def tela_esqueci_senha():
    st.header("🔑 Redefinir Senha")
    with st.form("reset_form"):
        email = st.text_input("Digite o e-mail associado à sua conta")
        submitted = st.form_submit_button("Enviar E-mail de Redefinição")
        if submitted:
            with st.spinner("Processando..."):
                resultado = auth.handle_password_reset(email)
            if resultado.startswith("Sucesso"):
                st.success(resultado)
            else:
                st.error(resultado)
    if st.button("🔙 Voltar ao Login"):
        st.session_state.view = "login"
        st.rerun()

# --- CONTROLE PRINCIPAL ---

if not st.session_state.authenticated:
    st.title("🏨 Bem-vindo ao Room App")
    if st.session_state.view == "login":
        tela_login()
    elif st.session_state.view == "cadastro":
        tela_cadastro()
    elif st.session_state.view == "esqueci_senha":
        tela_esqueci_senha()
else:
    # --- INTERFACE PRINCIPAL APÓS LOGIN ---
    # A LINHA st.set_page_config(...) FOI REMOVIDA DAQUI
    st.title(f"🏨 Room App")
    st.sidebar.success(f"Logado como: {st.session_state.username}")

    if st.session_state.get("username") == "admin":
        st.sidebar.divider()
        st.sidebar.header("Painel do Admin")
        admin_options = ["Página Inicial", "Gerenciar Usuários"]
        admin_choice = st.sidebar.radio("Navegação Admin", admin_options, key="admin_nav")
    else:
        admin_choice = "Página Inicial"

    if admin_choice == "Gerenciar Usuários":
        st.subheader("👨‍💼 Gerenciamento de Usuários")
        with st.expander("➕ Criar Novo Usuário"):
            with st.form("create_user_form"):
                new_username = st.text_input("Nome do novo usuário")
                new_email = st.text_input("E-mail do novo usuário")
                new_password = st.text_input("Senha do novo usuário", type="password")
                submitted = st.form_submit_button("Criar Usuário")
                if submitted:
                    resultado = auth.registrar_novo_usuario(new_username, new_password, new_email)
                    if resultado.startswith("Sucesso"):
                        st.success(resultado)
                        st.rerun()
                    else:
                        st.error(resultado)
        st.divider()
        st.write("**Modificar ou Excluir Usuários Existentes**")
        try:
            conn = auth.get_db_connection()
            todos_usuarios = conn.query("SELECT username, email, criado_em FROM usuarios WHERE username != 'admin' ORDER BY criado_em DESC;", ttl=0)
            if "usuarios_para_editar" not in st.session_state or st.button("🔄 Recarregar Lista"):
                st.session_state.usuarios_para_editar = todos_usuarios.copy()
            if todos_usuarios.empty:
                st.warning("Nenhum usuário cadastrado.")
            else:
                usuarios_df = pd.DataFrame(st.session_state.usuarios_para_editar)
                usuarios_df["nova_senha"] = ""
                usuarios_df["deletar"] = False
                edited_df = st.data_editor(
                    usuarios_df,
                    column_config={
                        "username": st.column_config.TextColumn("Usuário"),
                        "email": st.column_config.TextColumn("E-mail (não pode ser alterado)", disabled=True),
                        "criado_em": st.column_config.DatetimeColumn("Data de Criação", disabled=True),
                        "nova_senha": st.column_config.TextColumn("Definir Nova Senha"),
                        "deletar": st.column_config.CheckboxColumn("Deletar?")
                    },
                    hide_index=True, use_container_width=True, key="data_editor"
                )
                if st.button("Salvar Alterações", type="primary"):
                    for i, original_row in todos_usuarios.iterrows():
                        edited_row = edited_df.iloc[i]
                        original_username = original_row["username"]
                        if edited_row["deletar"]:
                            auth.delete_user(original_username)
                            st.success(f"Usuário '{original_username}' agendado para exclusão.")
                            continue
                        if original_username != edited_row["username"]:
                            success, message = auth.update_username(original_username, edited_row["username"])
                            if success:
                                st.success(message)
                                original_username = edited_row["username"] 
                            else:
                                st.error(message)
                        if edited_row["nova_senha"]:
                            auth.update_user_password(original_username, edited_row["nova_senha"])
                            st.success(f"Senha do usuário '{original_username}' agendada para atualização.")
                    st.info("As alterações foram processadas. Recarregando a lista...")
                    st.rerun()
        except Exception as e:
            st.error(f"Não foi possível carregar os usuários: {e}")
    else:
        st.write("### Selecione uma opção na barra lateral para começar.")

    st.sidebar.divider()
    if st.sidebar.button("Sair da Conta"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Inicio.py (versão com painel de admin interativo)
import streamlit as st
import auth 
import pandas as pd

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Room App",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- FUNÇÕES DE TELA (VIEWS) ---

def tela_login():
    """Renderiza a tela de login."""
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
    
    if st.button("Ainda não tem conta? Cadastre-se aqui"):
        st.session_state.view = "cadastro"
        st.rerun()

def tela_cadastro():
    """Renderiza a tela de cadastro."""
    st.header("📝 Cadastro de Usuário")
    with st.form("cadastro_form"):
        novo_usuario = st.text_input("Escolha um nome de usuário")
        nova_senha = st.text_input("Escolha uma senha", type="password")
        submitted = st.form_submit_button("Cadastrar", type="primary")

        if submitted:
            resultado = auth.registrar_novo_usuario(novo_usuario, nova_senha)
            if resultado.startswith("Sucesso"):
                st.success(resultado + " Agora você pode fazer o login.")
                st.session_state.view = "login"
                st.rerun()
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
    else:
        tela_cadastro()
else:
    # --- INTERFACE PRINCIPAL APÓS LOGIN ---
    st.title(f"🏨 Room App")
    st.sidebar.success(f"Logado como: {st.session_state.username}")

    # --- NOVA SEÇÃO DO PAINEL ADMIN ---
    if st.session_state.get("username") == "admin":
        st.sidebar.divider()
        st.sidebar.header("Painel do Admin")
        
        admin_options = ["Página Inicial", "Gerenciar Usuários"]
        admin_choice = st.sidebar.radio("Navegação Admin", admin_options)
    else:
        admin_choice = "Página Inicial"


    # --- CONTEÚDO DA PÁGINA PRINCIPAL ---
    if admin_choice == "Gerenciar Usuários":
        st.subheader("👨‍💼 Gerenciamento de Usuários")
        
        try:
            conn = auth.get_db_connection()
            todos_usuarios = conn.query("SELECT username, criado_em FROM usuarios WHERE username != 'admin' ORDER BY criado_em DESC;", ttl=0)
            
            if todos_usuarios.empty:
                st.warning("Nenhum usuário cadastrado (além do admin).")
            else:
                # Cria uma cópia para edição
                usuarios_editaveis = todos_usuarios.copy()
                
                # Adiciona colunas para as ações do admin
                usuarios_editaveis["nova_senha"] = ""
                usuarios_editaveis["deletar"] = False

                # Usa o st.data_editor para criar uma tabela interativa
                edited_df = st.data_editor(
                    usuarios_editaveis,
                    column_config={
                        "username": st.column_config.TextColumn("Usuário (não pode ser alterado)", disabled=True),
                        "criado_em": st.column_config.DatetimeColumn("Data de Criação", disabled=True),
                        "nova_senha": st.column_config.TextColumn("Nova Senha (deixe em branco se não for alterar)"),
                        "deletar": st.column_config.CheckboxColumn("Deletar Usuário?")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                if st.button("Salvar Alterações", type="primary"):
                    for index, row in edited_df.iterrows():
                        username_to_update = row["username"]
                        
                        # Ação de deletar (tem prioridade)
                        if row["deletar"]:
                            if auth.delete_user(username_to_update):
                                st.success(f"Usuário '{username_to_update}' deletado com sucesso!")
                        
                        # Ação de modificar senha
                        elif row["nova_senha"]:
                            if auth.update_user_password(username_to_update, row["nova_senha"]):
                                st.success(f"Senha do usuário '{username_to_update}' atualizada com sucesso!")
                    
                    st.rerun() # Recarrega a página para mostrar os dados atualizados

        except Exception as e:
            st.error(f"Não foi possível carregar os usuários: {e}")
            
    else: # admin_choice == "Página Inicial"
        st.write("### Selecione uma opção na barra lateral para começar.")

    # Botão de Logout na sidebar
    st.sidebar.divider()
    if st.sidebar.button("Sair da Conta"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# pages/7_FAQ.py
import streamlit as st

st.set_page_config(page_title="Dúvidas Frequentes", page_icon="❓", layout="wide")

def render_faq():
    st.header("❓ Dúvidas Frequentes (FAQ)")

    with st.expander("**Posso personalizar o cardápio da semana?**"):
        st.write("""
        Sim, é possível solicitar alterações. Para isso, por favor, entre em contato 
        diretamente com a recepção do hotel pelo ramal ou pessoalmente para verificar 
        as opções e possíveis custos adicionais.
        """)

    with st.expander("**Como funciona a solicitação de limpeza do quarto?**"):
        st.write("""
        Você pode solicitar a limpeza a qualquer momento através da aba 'Room Service'. 
        Basta autorizar a entrada da equipe e garantir que você não esteja no quarto 
        no momento da limpeza. A equipe será notificada automaticamente.
        """)

    with st.expander("**É possível estender minha estadia pelo aplicativo?**"):
        st.write("""
        Sim! Utilize a opção 'Reservas' no menu. Lá você poderá selecionar as noites 
        extras que deseja adicionar à sua estadia. O valor será calculado e somado 
        à sua conta, que pode ser paga na aba 'Pagamento'.
        """)

    with st.expander("**Perdi minha senha. Como posso recuperá-la?**"):
        st.write("""
        Atualmente, a recuperação de senha não está disponível pelo aplicativo. 
        Por favor, dirija-se à recepção para obter assistência e redefinir sua senha 
        com segurança.
        """)

# --- Verificação de Autenticação ---
if not st.session_state.get("authenticated", False):
    st.error("Acesso negado. Por favor, faça o login primeiro.")
    st.stop()

# --- Renderiza a página ---
render_faq()

# Botão de Logout na sidebar de cada página
if st.sidebar.button("Sair da Conta", key="logout_faq"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

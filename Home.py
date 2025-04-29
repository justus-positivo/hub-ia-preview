import streamlit as st
import streamlit_authenticator as stauth
import yaml
import utils.util as util

from yaml import SafeLoader

st.set_page_config(
    page_icon="🤖", 
    layout="wide",
    page_title="HUB.IA"
)

# Carrega configurações de autenticação
with open('./.streamlit/config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Layout com 2 colunas
col1, col2 = st.columns([1, 5])

with col1:
    # Adiciona imagem de boas-vindas
    st.image("./images/edu.webp", use_container_width=True, width=100)

with col2:
    # Adiciona título
    st.subheader("HUB.IA Labs 🧪")

# Configuração de autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Formulário de autenticação
authenticator.login(fields={'Form name': 'Acesso', 'Username': 'Email', 'Password': 'Senha', 'Login': 'Login'})

# Verifica status de autenticação
if st.session_state.get("authentication_status"):
    st.write('Usuário autenticado - acessar menu lateral')

    # Menu lateral para usuários autenticados
    st.sidebar.title(st.session_state.name)
    st.sidebar.title("Menu")
    st.sidebar.page_link("./pages/POC Preview 01.py", label="POC - Prévia")
    st.sidebar.page_link("./pages/POC Class Plan.py", label="POC - Planejamento")
    st.sidebar.button("Logout", on_click=authenticator.logout)

elif st.session_state.get("authentication_status") is False:
    st.error('Usuário/Senha incorretos')
else:
    st.warning('Entre com suas credenciais para acessar')
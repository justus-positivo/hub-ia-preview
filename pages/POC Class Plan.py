import streamlit as st
from groq import Groq
import utils.util as util
import time  # Importa o módulo para medir o tempo

st.set_page_config(
    page_icon="🥷", 
    layout="wide",
    page_title="Minha Aula - Planejamento de Aula POC"
)

# Inicializa página
util.init_page()

# Adiciona título
st.subheader("Planejamento de Aula com IA")

# Inicializa o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Layout com duas colunas
col1, col2 = st.columns([1, 2])

with col1:
    # Controles para entrada de dados
    st.markdown("### Configurações da Aula")

    # Combo box para níveis de ensino fundamental
    nivel_ensino = st.selectbox(
        "Nível de Ensino:",
        options=[f"Fundamental {i}" for i in range(1, 10)],
        help="Selecione o nível de ensino fundamental (1º ao 9º ano)."
    )

    # Combo box para disciplinas do ensino básico
    disciplina = st.selectbox(
        "Disciplina:",
        options=["Matemática", "Português", "Ciências", "História", "Geografia", "Arte", "Educação Física", "Inglês"],
        help="Selecione a disciplina para a aula."
    )

    # Combo box para duração da aula
    duracao = st.selectbox(
        "Duração da Aula (minutos):",
        options=[10, 34, 90, 240],
        help="Selecione a duração da aula em minutos."
    )

    # Campo de texto grande para descrever o tema da aula
    tema_aula = st.text_area(
        "Tema da Aula:",
        placeholder="Descreva o tema da aula aqui...",
        help="Digite uma breve descrição do tema da aula."
    )

    # Botão para gerar o plano da aula
    if st.button("Gerar Plano da Aula"):
        if not tema_aula.strip():
            st.warning("Por favor, preencha o tema da aula antes de gerar o plano.")
        else:
            try:
                st.info("Gerando plano de aula...")
                start_time = time.time()  # Marca o início do processo

                # Chamada ao modelo GenIA do Groq
                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # Modelo GenIA do Groq (llama-3.3-70b-versatile)
                    messages=[
                        {"role": "user", "content": f"Crie um plano de aula para o nível {nivel_ensino}, disciplina {disciplina}, duração de {duracao} minutos, com o tema: {tema_aula} deve ter 500 tokens, usar markdown"}
                    ],
                    max_tokens=500,
                    stream=False
                )

                # Marca o fim do processo
                end_time = time.time()
                elapsed_time = end_time - start_time  # Calcula o tempo total

                # Acessa os atributos do objeto retornado
                previa_aula = chat_completion.choices[0].message.content
                st.success(f"Plano gerado com sucesso em {elapsed_time:.2f} segundos!")
            except Exception as e:
                previa_aula = f"Erro ao gerar plano: {e}"
                st.error(previa_aula)
    else:
        previa_aula = "O plano será exibido aqui após a geração."

with col2:
    # Exibe o resultado formatado em Markdown
    st.markdown("### Plano da Aula")
    st.markdown(
        previa_aula,
        unsafe_allow_html=False  # Permite apenas Markdown seguro
    )
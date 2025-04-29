import streamlit as st
import json
from groq import Groq
import utils.util as util
import time  # Importa o módulo para medir o tempo

st.set_page_config(
    page_icon="🥷", 
    layout="wide",
    page_title="Minha Aula - Prévia de Aula POC"
)

# Inicializa página
util.init_page()

# Adiciona título
st.subheader("Prévia de Aula com IA")

# Inicializa o cliente Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Carrega o arquivo bncc.json
with open('./resources/bncc.json', 'r') as file:
    bncc_data = json.load(file)

# Carrega o arquivo bloom.json
with open('./resources/bloom.json', 'r') as file:
    bloom_data = json.load(file)

# Função para estruturar as habilidades da BNCC
def get_bncc_options(data):
    options = []
    for category in data:
        for item in category["itens"]:
            options.append({
                "label": f"{item['code']} - {item['range']}\n{item['description']}",
                "description": item["description"]
            })
    return options

bncc_options = get_bncc_options(bncc_data)

# Função para estruturar as abordagens pedagógicas da Taxonomia de Bloom
def get_bloom_options(data):
    options = []
    for item in data:
        options.append({
            "label": f"{item['nivel']}",
            "descricao": item["descricao"],
            "exemplos": item["exemplos_de_atividades"]
        })
    return options

bloom_options = get_bloom_options(bloom_data)

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

    # Seleção de até 2 abordagens pedagógicas (Taxonomia de Bloom)
    abordagens_selecionadas = st.multiselect(
        "Selecione até 2 Abordagens Pedagógicas:",
        options=[option["label"] for option in bloom_options],
        help="Selecione até 2 abordagens pedagógicas para a aula.",
        max_selections=2
    )

    # Obtém as descrições e exemplos das abordagens selecionadas
    abordagens_descricao = [
        f"{option['label']} - {option['descricao']}" for option in bloom_options if option["label"] in abordagens_selecionadas
    ]
    abordagens_exemplos = [
        f"Exemplos: {', '.join(option['exemplos'])}" for option in bloom_options if option["label"] in abordagens_selecionadas
    ]

    # Seleção de até 3 habilidades da BNCC
    habilidades_selecionadas = st.multiselect(
        "Selecione até 3 habilidades da BNCC:",
        options=[option["label"] for option in bncc_options],
        help="Selecione até 3 habilidades da BNCC para a aula.",
        max_selections=3
    )

    # Obtém as descrições das habilidades selecionadas
    habilidades_descricao = [
        option["description"] for option in bncc_options if option["label"] in habilidades_selecionadas
    ]

    # Inicializa a variável `prompt` no estado da sessão, se ainda não existir
    if "prompt" not in st.session_state:
        st.session_state["prompt"] = ""

    # Botão para gerar a prévia da aula
    if st.button("Gerar Prévia da Aula"):
        if not tema_aula.strip():
            st.warning("Por favor, preencha o tema da aula antes de gerar a prévia.")
        else:
            try:
                st.info("Gerando Prévia de aula...")
                start_time = time.time()  # Marca o início do processo

                # Novo prompt detalhado
                st.session_state["prompt"] = f"""
                Gere uma prévia detalhada e clara de um plano de aula com base nos seguintes parâmetros:

                1. **Disciplina**: {disciplina}
                2. **Ano Escolar**: {nivel_ensino}
                3. **Duração**: {duracao} minutos
                4. **Tema da Aula**: {tema_aula}
                5. **Abordagens Didáticas**: {'; '.join(abordagens_descricao) if abordagens_descricao else "Não especificado"}
                6. **Exemplos de Atividades**: {'; '.join(abordagens_exemplos) if abordagens_exemplos else "Não especificado"}
                7. **Habilidades a serem Desenvolvidas**: {', '.join(habilidades_descricao) if habilidades_descricao else "Não especificado"}
                8. **Conhecimentos Prévios Recomendados**: Reconhecimento de números, contagem simples, atenção e foco

                Certifique-se de que a resposta seja clara e objetiva, usando uma estrutura semelhante aos exemplos fornecidos, deve trazer uma informação mas objetiva de como o professor está configurando a aula para depois gerar, inclua informações:
                - Descrição geral do plano de aula (disciplina, ano escolar, duração e tema).
                - Abordagem didática utilizada
                - Exemplos de atividades
                - Habilidades a serem desenvolvidas (se aplicável)
                - Conhecimentos prévios recomendados (se aplicável), SEMPRE incluir em uma sessão separada no final

                Desired Output Pattern:
                - structure: paragraphs without bullet points
                - format: markdown with bold and italic emphasis without bullets and headings, use paragraphs like descritive text
                - format exclude: no code blocks, no bullet points, never use headings
                - language: pt-BR
                - size: 300 tokens
                - focus: on the main topic of the lesson with subject and grade
                - example_response: Será gerado um plano de aula de matemática para o 1º ano do Ensino Fundamental, com duração de 45 minutos. O tema da aula será Primeira aula de números. A aula utilizará uma abordagem tradicional com ênfase na aplicação, conforme a Taxonomia de Bloom. Serão desenvolvidas as habilidades de reconhecimento de números e contagem simples. Conhecimentos recomendados incluem reconhecimento de números, contagem simples, atenção e foco
                """

                # Chamada ao modelo GenIA do Groq
                chat_completion = client.chat.completions.create(
                    model="llama3-8b-8192",  # Modelo GenIA do Groq
                    messages=[
                        {"role": "user", "content": st.session_state["prompt"]}
                    ],
                    max_tokens=350,
                    stream=False
                )

                # Marca o fim do processo
                end_time = time.time()
                elapsed_time = end_time - start_time  # Calcula o tempo total

                # Acessa os atributos do objeto retornado
                previa_aula = chat_completion.choices[0].message.content
                st.success(f"Prévia gerada com sucesso em {elapsed_time:.2f} segundos!")
            except Exception as e:
                previa_aula = f"Erro ao gerar prévia: {e}"
                st.error(previa_aula)
    else:
        previa_aula = "A prévia será exibida aqui após a geração."

    # Botão discreto para visualizar o prompt gerado
    if st.button("Visualizar Prompt Gerado"):
        if st.session_state["prompt"]:
            st.text_area(
                "Prompt Gerado:",
                value=st.session_state["prompt"],
                height=300,
                help="Este é o prompt gerado para consulta.",
                disabled=True
            )
        else:
            st.warning("O prompt ainda não foi gerado. Clique em 'Gerar Prévia da Aula' primeiro.")

with col2:
    # Exibe o resultado formatado em Markdown
    st.markdown("### Prévia da Aula")
    st.markdown(
        previa_aula,
        unsafe_allow_html=False  # Permite apenas Markdown seguro
    )
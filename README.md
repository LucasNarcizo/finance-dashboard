# finance-dashboard
(Estarei separando o desenvolvimento em fases para ser melhor para explicar quais complicações eu passei para poder explicar deu um jeito melhor para quem estiver lendo entender)

Fase 1: Comecei fazendo a base do Python com a API AwesomeAPI(Para ver cotação do dolar e futuramente outras moedas em uma aba especifica)

Primeiro erro: Durante o desenvolvimento eu fiz o arquivo de HTML e CSS, e por conta do streamlit ele estava reconhecendo o HTML como um codigo de exposição no caso ele acho que eu estava importando um codigo para mostra pra quem abrisse a pagina, coisa que não era pra esta acontecendo acabei fazendo de outro modo para importar e conectar junto ao Streamlit que acabei usando as seguinte linha de codigos

Antes:
def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as file_to_read:
        st.markdown(file_to_read.read(), unsafe_allow_html=True)

Depois:(onde coloquei um import para conseguir isolar o HTML do Streamlit)
import streamlit.components.v1 as components

def load_html(file_name):
    with open(file_name, "r", encoding="utf-8") as file_to_read:
        html_code = file_to_read.read()
        components.html(html_code, height=150)


Termino da fase 1 do projeto, fiz a base do Dashboard onde eu conseguir arrumar os arquivos separando pastas tive diversos problemas de importação mas fui arrumando 1 por 1, mudei nome de algumas variaveis pra ficar legivel pra mim e para quem estiver lendo,
a partir de amanha pretendo começar mexer na parte visual do projeto no html e no css e colocar um novo grafico de gastos.

Fase 2:


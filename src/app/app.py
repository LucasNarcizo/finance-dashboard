import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px
from pathlib import Path
from dotenv import load_dotenv
from src.database.database import get_supabase_client, buscar_transacoes, salvar_transacoes
from src.utils.utils import ui_css, get_usd_rate


rota_path = Path(__file__).resolve().parent.parent.parent
if str(rota_path) not in sys.path:
    sys.path.append(str(rota_path))


ui_css_path = rota_path / "src" / "web" / "style.css"

load_dotenv()
st.set_page_config(page_title="Finanças Pro", layout="wide")

ui_css(str("src/web/style.css"))

cor_entrada = "#00ff88"
st.sidebar.header("🎨 Customização")
cor_entrada_usario = st.sidebar.color_picker("Cor para Entradas", "#00ff88")
cor_saida_usario = st.sidebar.color_picker("Cor para Gastos", "#FF4B4B")

st.markdown("""
    <div class="banner-container">
        <h1 class="banner-title">📊 Finanças Pro</h1>
        <p classe="banner-subtitle">Gestão Simplificada em Python</p>
    </div>
    """, unsafe_allow_html=True)


supabase = get_supabase_client()
if not supabase:
    st.error("Erro: Variáveis de ambiente não encontradas. Verifique o arquivo .env")
    st.stop()


st.sidebar.header("Nova Transação")
desc = st.sidebar.text_input("Descrição (Ex: Salário, Aluguel)")
valor = st.sidebar.number_input("Valor (R$)", min_value=0.0, step=0.01)
tipo = st.sidebar.selectbox("Tipo", ["Entrada", "Saída"])

if st.sidebar.button("Salvar Transação"):
    if desc and valor > 0:
        try:
            salvar_transacoes(supabase, desc, valor, tipo)
            st.sidebar.success("Dados salvos com sucesso!")
            st.rerun() 
        except Exception as e:
            st.sidebar.error(f"Erro ao salvar: {e}")
    else:
        st.sidebar.error("Preencha todos os campos!")


st.subheader("Resumo de Saldo")

try:
    response = buscar_transacoes(supabase)
    df = pd.DataFrame(response.data)

    if not df.empty:
        # Cálculos de Saldo
        total_entradas = df[df['type'] == 'Entrada']['amount'].sum()
        total_saidas = df[df['type'] == 'Saída']['amount'].sum()
        saldo = total_entradas - total_saidas
        cotacao = get_usd_rate()
        saldo_usd = saldo / cotacao
        
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Entradas", f"R$ {total_entradas:,.2f}")
        c2.metric("Total Saídas", f"R$ -{total_saidas:,.2f}", delta_color="inverse")
        c3.metric("Saldo Atual", f"R$ {saldo:,.2f}")
        
        st.markdown(f""" 
        <div class=cotacao-card> 
            Cotação do Dólar<b> R${cotacao:.2f}</b> | 
            Saldo em USD: <b>{saldo_usd:,.2f}</b>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        
        st.markdown(f"""

        """, unsafe_allow_html=True)

        dispesas, = st.columns(1)
        with dispesas:
            st.markdown('<div class="card-grafico">', unsafe_allow_html=True)
            st.write("#### Entradas e Saídas")

            df_pizza = df.groupby('type')['amount'].sum().reset_index()
            fig = px.pie(
                df_pizza, 
                values='amount', 
                names='type',
                hole=0.4,
                color='type',
                color_discrete_map={
                    'Entrada': cor_entrada_usario,
                    'Saída': cor_saida_usario
                }
            )          

            # 3. Ajustar o visual do gráfico para combinar com seu fundo verde escuro
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                ),
                paper_bgcolor='rgba(0,0,0,0)', # Fundo transparente
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                margin=dict(t=0, b=0, l=0, r=0)
            )

            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
    else:
        st.info("Nenhuma transação cadastrada ainda no Supabase.")

except Exception as erro:
    st.error(f"Erro ao carregar dados do banco: {erro}")
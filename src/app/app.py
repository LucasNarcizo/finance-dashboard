import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from src.database.database import get_supabase_client, save_transaction, fetch_transactions
from src.utils.utils import get_usd_rate, load_custom_css, load_custom_html

# 1. CARREGAMENTO DE CONFIGURAÇÕES E ESTILO
load_dotenv()
st.set_page_config(page_title="Finanças Pro", layout="wide")

# Aplica o CSS e o HTML que você separou nos arquivos externos
load_custom_css("src/web/style.css")
load_custom_html("src/web/index.html")

# 2. CONEXÃO COM O BANCO DE DADOS
supabase = get_supabase_client()

if not supabase:
    st.error("Erro: Variáveis de ambiente não encontradas. Verifique o arquivo .env")
    st.stop()

# --- SIDEBAR: ENTRADA DE DADOS ---
st.sidebar.header("Nova Transação")
desc = st.sidebar.text_input("Descrição (Ex: Salário, Aluguel)")
valor = st.sidebar.number_input("Valor (R$)", min_value=0.0, step=0.01)
tipo = st.sidebar.selectbox("Tipo", ["Entrada", "Saída"])

if st.sidebar.button("Salvar Transação"):
    if desc and valor > 0:
        try:
            save_transaction(supabase, desc, valor, tipo)
            st.sidebar.success("Dados salvos com sucesso!")
            st.rerun() 
        except Exception as e:
            st.sidebar.error(f"Erro ao salvar: {e}")
    else:
        st.sidebar.error("Preencha todos os campos!")

# --- CORPO PRINCIPAL: RESUMO E GRÁFICOS ---
st.subheader("Resumo de Saldo")

try:
    response = fetch_transactions(supabase)
    df = pd.DataFrame(response.data)

    if not df.empty:
        # Cálculos de Saldo
        total_entradas = df[df['type'] == 'Entrada']['amount'].sum()
        total_saidas = df[df['type'] == 'Saída']['amount'].sum()
        saldo = total_entradas - total_saidas
        
        # Cards de Métricas (O estilo vem do style.css)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Entradas", f"R$ {total_entradas:,.2f}")
        c2.metric("Total Saídas", f"R$ -{total_saidas:,.2f}", delta_color="inverse")
        c3.metric("Saldo Atual", f"R$ {saldo:,.2f}")

        # Cotação do Dólar (Vem do utils.py)
        cotacao = get_usd_rate()
        st.info(f"💵 Cotação do Dólar: R$ {cotacao:.2f} | Saldo em USD: ${saldo/cotacao:,.2f}")

        st.divider()

        # Gráficos de Visualização
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            st.write("**Distribuição por Tipo**")
            st.bar_chart(df.groupby('type')['amount'].sum())

        with col_graf2:
            st.write("**Histórico de Gastos**")
            st.bar_chart(df.set_index('description')['amount'])
            
    else:
        st.info("Nenhuma transação cadastrada ainda no Supabase.")

except Exception as e:
    st.error(f"Erro ao carregar dados do banco: {e}")
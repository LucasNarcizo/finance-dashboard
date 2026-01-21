import streamlit as st
import pandas as pd
import requests
from supabase import create_client

# --- CONFIGURAÇÕES DO SUPABASE ---
# Pegue esses dados no painel do Supabase (Project Settings > API)
SUPABASE_URL = "https://lpbdxmpnnaaikurrlrqe.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxwYmR4bXBubmFhaWt1cnJscnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMDg4ODcsImV4cCI6MjA4NDU4NDg4N30.rsy9pvUTWn4NYO5TR5aLCaIyTBThAp0QhBfSP_uyLiI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNÇÃO PARA API DE CÂMBIO ---
def get_usd_rate():
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = requests.get(url).json()
        return float(response["USDBRL"]["bid"])
    except:
        return 5.0  # Valor padrão caso a API falhe

# --- INTERFACE ---
st.set_page_config(page_title="Finanças Portfolio", layout="wide")
st.title("📊 Meu Dashboard Financeiro")

# Sidebar para inserir dados
st.sidebar.header("Nova Transação")
desc = st.sidebar.text_input("Descrição (Ex: Salário, Aluguel)")
valor = st.sidebar.number_input("Valor (R$)", min_value=0.0, step=0.01)
tipo = st.sidebar.selectbox("Tipo", ["Entrada", "Saída"])

if st.sidebar.button("Salvar Transação"):
    if desc and valor > 0:
        data = {"description": desc, "amount": valor, "type": tipo}
        supabase.table("transactions").insert(data).execute()
        st.sidebar.success("Dados salvos no Supabase!")
        st.rerun() # Atualiza a tela
    else:
        st.sidebar.error("Preencha todos os campos!")

# --- EXIBIÇÃO DOS DADOS ---
st.subheader("Resumo de Saldo")

try:
    # Busca dados do banco
    response = supabase.table("transactions").select("*").execute()
    df = pd.DataFrame(response.data)

    if not df.empty:
        # Lógica de cálculos
        total_entradas = df[df['type'] == 'Entrada']['amount'].sum()
        total_saidas = df[df['type'] == 'Saída']['amount'].sum()
        saldo = total_entradas - total_saidas
        
        # Cards Visuais
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Entradas", f"R$ {total_entradas:,.2f}")
        c2.metric("Total Saídas", f"R$ -{total_saidas:,.2f}", delta_color="inverse")
        c3.metric("Saldo Atual", f"R$ {saldo:,.2f}")

        # API de Câmbio em ação
        cotacao = get_usd_rate()
        st.info(f"💵 Cotação atual do Dólar: R$ {cotacao:.2f} | Seu saldo em USD: ${saldo/cotacao:,.2f}")

        # Gráfico Simples
        st.bar_chart(df.set_index('description')['amount'])
    else:
        st.info("Nenhuma transação cadastrada ainda.")

except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}")
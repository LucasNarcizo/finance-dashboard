import streamlit as st
import pandas as pd
from src.database.database import get_supabase_client, buscar_transacoes, salvar_transacoes
from src.utils.utils import ui_css, get_usd_rate
from src.components.charts import renderizar_grafico_escada, renderizar_grafico_pizza

st.set_page_config(page_title="Finanças Pro", layout="wide")


ui_css("src/web/style.css")
 
with st.expander("⚙️ Painel de Controle e Lançamentos", expanded=True):
    st.markdown("""
    <div class="banner-container">
        <h1 class="banner-title">📊 Finanças Pro</h1>
        <p class="banner-subtitle">Gestão Simplificada em Python</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5, c6 = st.columns([0.5, 0.5, 2, 1, 1, 1])
    
    with c1:
        cor_entrada_usuario = st.color_picker("Entradas", "#00ff88", key="cp_ent")
    with c2:
        cor_saida_usuario = st.color_picker("Gastos", "#FF4B4B", key="cp_sai")
    with c3:
        desc = st.text_input("Descrição", placeholder="Ex: Aluguel", key="in_desc")
    with c4:
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, key="in_val")
    with c5:
        tipo = st.selectbox("Tipo", ["Entrada", "Saída"], key="sel_tipo")
    with c6:
        st.write(" ") 
        if st.button("Salvar", use_container_width=True, key="btn_save"):
            pass



# Conexão com o banco 
supabase = get_supabase_client()



try:
    response = buscar_transacoes(supabase)
    # Note: se buscar_transacoes já retorna os dados
    df = pd.DataFrame(response) if isinstance(response, list) else pd.DataFrame(response.data)

    if not df.empty:
        # Cálculos (Poderiam ir para utils.py depois para limpar ainda mais)
        total_entradas = df[df['type'] == 'Entrada']['amount'].sum()
        total_saidas = df[df['type'] == 'Saída']['amount'].sum()
        saldo = total_entradas - total_saidas
        cotacao = get_usd_rate()
        saldo_usd = saldo / cotacao
        
        # Métricas
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Entradas", f"R$ {total_entradas:,.2f}")
        c2.metric("Total Saídas", f"R$ -{total_saidas:,.2f}", delta_color="inverse")
        c3.metric("Saldo Atual", f"R$ {saldo:,.2f}")
        
        st.markdown(f""" 
            <div class='cotacao-card'> 
                Cotação do Dólar <b>R$ {cotacao:.2f}</b> | 
                Saldo em USD: <b>$ {saldo_usd:,.2f}</b>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Chamada dos Gráficos
        renderizar_grafico_escada(df)
        col1, col2 = st.columns(2)
        with col1:
            renderizar_grafico_pizza(df, cor_entrada_usuario, cor_saida_usuario)
                
    else:
        st.info("Nenhuma transação cadastrada ainda no Supabase.")

except Exception as erro:
    st.error(f"Erro ao carregar dados: {erro}")
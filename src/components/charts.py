import streamlit as st
import plotly.express as px

def renderizar_grafico_escada(df):
    st.markdown('<div class="grafico-escada">', unsafe_allow_html=True)
    st.markdown("#### Entradas e Saídas")
    
    # Exemplo de gráfico Plotly
    fig = px.bar(df, x='type', y='amount', color='type')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

def renderizar_grafico_pizza(df, cor_entrada_usuario, cor_saida_usuario):
    
    
    with st.container():
        # O Markdown agora serve apenas para o título
        st.markdown("<h4 style='text-align: center; color: white;'>Proporção de Gastos</h4>", unsafe_allow_html=True)
        
        df_pizza = df.groupby('type')['amount'].sum().reset_index()
        
        fig = px.pie(
            df_pizza, 
            values='amount', 
            names='type',
            hole=0.5,
            color='type',
            color_discrete_map={'Entrada': cor_entrada_usuario, 'Saída': cor_saida_usuario}
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            height=400,
            showlegend=True,
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
        )
    

        st.plotly_chart(fig, width='stretch')
    
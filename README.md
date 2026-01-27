### Dashboard Financeiro

Este repositório documenta a construção de um Dashboard Financeiro em Python. Mais do que uma ferramenta final, este projeto é um laboratório de estudos em Engenharia de Software, focado em superar desafios de arquitetura, UX customizada e persistência de dados.

## 🛠️ O que está sendo construído?
O objetivo é criar uma plataforma onde o usuário possa gerenciar transações financeiras com uma interface de alta fidelidade, fugindo dos padrões básicos de bibliotecas prontas.

## ✅ Já implementado (Sprint Atual):
Refatoração de UI: Migração da Sidebar para um menu superior expansível (st.expander) para melhor aproveitamento de tela.

Componentização de Gráficos: Criação de funções modulares para gráficos de pizza/donut utilizando Plotly.

Estilização com CSS Scoping: Uso de seletores CSS avançados (:has) para isolar o estilo dos containers sem afetar o background global.

Persistência de Dados: Conexão funcional com Supabase para Create e Read de transações.

## 🔄 Em progresso (Bugs & Ajustes):
Sincronização de Cores: Ajuste fino entre os seletores de cor do usuário e a aplicação imediata nos gráficos via color_discrete_map.

Otimização de Layout: Ajuste de paddings e margens nos containers para evitar sobreposição de elementos.

## 🚀 Próximos Passos (Backlog):
[ ] Implementação de Gráfico de Barras para histórico mensal.

[ ] Criação de Cards de métricas (Saldo, Entradas e Saídas) com lógica de cálculo direto no DataFrame.

[ ] Filtros avançados por data e categoria.

[ ] Exportação de relatórios em CSV/PDF.
